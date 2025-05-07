from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.order import Order
from app.models.product import Product
from app import db

client = Blueprint('client', __name__)

@client.route('/dashboard')
@login_required
def dashboard():
    orders = Order.query.filter_by(client_id=current_user.id).all()
    return render_template('client/dashboard.html', orders=orders)

@client.route('/order/<int:product_id>', methods=['POST'])
@login_required
def place_order(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = float(request.form.get('quantity'))
    
    if quantity > product.available_quantity:
        return jsonify({'error': 'Insufficient quantity available'}), 400
        
    order = Order(
        client_id=current_user.id,
        product_id=product_id,
        quantity=quantity,
        price_per_kg=product.price_per_kg,
        total_amount=quantity * product.price_per_kg,
        shipping_address=request.form.get('shipping_address')
    )
    
    product.available_quantity -= quantity
    db.session.add(order)
    db.session.commit()
    
    return jsonify({'message': 'Order placed successfully'})
'''
@client.route('/orders')
@login_required
def view_orders():
    orders = Order.query.filter_by(client_id=current_user.id).all()
    return render_template('client/orders.html', orders=orders)
'''

@client.route('/orders')
@login_required
def view_orders():
    # Get filter parameters
    status = request.args.get('status')
    date = request.args.get('date')
    
    # Start with base query
    query = Order.query.filter_by(client_id=current_user.id)
    
    # Apply filters if they exist
    if status:
        query = query.filter(Order.status == status)
    if date:
        # Convert string date to datetime
        filter_date = datetime.strptime(date, '%Y-%m-%d')
        query = query.filter(
            db.func.date(Order.created_at) == filter_date.date()
        )
    
    # Get filtered orders
    orders = query.order_by(Order.created_at.desc()).all()
    return render_template('client/orders.html', orders=orders)