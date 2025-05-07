from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.product import Product
from app.models.user import User
from app.models.order import Order
from app.models.task import Task
from app import db
from functools import wraps
from app.models.blog import BlogPost
from app.models.message import Message
from flask import jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from slugify import slugify


admin = Blueprint('admin', __name__)


UPLOAD_FOLDER = os.path.join('app', 'static', 'img', 'products')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.role == 'admin':
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get all orders
    orders = Order.query.all()
    # Get all users (excluding admin)
    users = User.query.filter(User.role != 'admin').all()
    # Get all products
    products = Product.query.all()
    employees = User.query.filter_by(role='employee').all()
    
    return render_template('admin/dashboard.html', orders=orders, users=users, products=products,employees=employees )
'''
@admin.route('/products', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_products():
    if request.method == 'POST':
        product = Product(
            name=request.form.get('name'),
            grade=request.form.get('grade'),
            origin=request.form.get('origin'),
            altitude=request.form.get('altitude'),
            processing=request.form.get('processing'),
            moisture_level=float(request.form.get('moisture_level')),
            cupping_notes=request.form.get('cupping_notes'),
            available_quantity=float(request.form.get('available_quantity')),
            price_per_kg=float(request.form.get('price_per_kg'))
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('admin.manage_products'))
    products = Product.query.all()
    return render_template('admin/products.html', products=products)
    '''

@admin.route('/products', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_products():
    if request.method == 'POST':
        name = request.form.get('name')
        grade = request.form.get('grade')
        origin = request.form.get('origin')
        altitude = request.form.get('altitude')
        processing = request.form.get('processing')
        moisture_level = request.form.get('moisture_level')
        cupping_notes = request.form.get('cupping_notes')
        available_quantity = request.form.get('available_quantity')
        price_per_kg = request.form.get('price_per_kg')
        
        # Handle image upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Generate unique filename to avoid overwriting
                base, ext = os.path.splitext(filename)
                image_filename = f"{base}_{int(datetime.utcnow().timestamp())}{ext}"
                file.save(os.path.join(UPLOAD_FOLDER, image_filename))

        product = Product(
            name=name,
            grade=grade,
            origin=origin,
            altitude=altitude,
            processing=processing,
            moisture_level=float(moisture_level) if moisture_level else None,
            cupping_notes=cupping_notes,
            available_quantity=float(available_quantity),
            price_per_kg=float(price_per_kg),
            image=image_filename
        )
        
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.manage_products'))
    
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@admin.route('/users')
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/orders')
@login_required
@admin_required
def manage_orders():
    orders = Order.query.all()
    return render_template('admin/orders.html', orders=orders)


@admin.route('/orders/update-status/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    if status in ['pending', 'processing', 'shipped', 'delivered']:
        order.status = status
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully'})
    return jsonify({'error': 'Invalid status'}), 400


@admin.route('/users/edit', methods=['POST'])
@login_required
@admin_required
def edit_user():
    user_id = request.form.get('user_id')
    user = User.query.get_or_404(user_id)
    
    user.username = request.form.get('username')
    user.email = request.form.get('email')
    user.role = request.form.get('role')
    user.company_name = request.form.get('company_name')
    user.contact_person = request.form.get('contact_person')
    user.country = request.form.get('country')
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@admin.route('/users/activate/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = True
    db.session.commit()
    return jsonify({'message': 'User activated successfully'})

@admin.route('/users/deactivate/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def deactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    return jsonify({'message': 'User deactivated successfully'})

@admin.route('/blog')
@login_required
@admin_required
def manage_blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)

@admin.route('/blog/add', methods=['POST'])
@login_required
@admin_required
def add_blog_post():
    title = request.form.get('title')
    content = request.form.get('content')
    
    slug = slugify(title)
    # Handle image upload
    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_filename = f"{int(datetime.utcnow().timestamp())}_{filename}"
            file.save(os.path.join('app/static/img/blog', image_filename))
    
    post = BlogPost(
        title=title,
        slug=slug,
        content=content,
        image_url=image_filename,
        author_id=current_user.id,
        status='published',
        published_at=datetime.utcnow()
    )
    
    db.session.add(post)
    db.session.commit()
    
    flash('Blog post published successfully!', 'success')
    return redirect(url_for('admin.manage_blog'))

@admin.route('/blog/edit/<int:post_id>', methods=['POST'])
@login_required
@admin_required
def edit_blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    
    post.title = request.form.get('title')
    post.content = request.form.get('content')
    
    # Handle image upload
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            # Delete old image if it exists
            if post.image:
                old_image_path = os.path.join('app/static/img/blog', post.image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            filename = secure_filename(file.filename)
            image_filename = f"{int(datetime.utcnow().timestamp())}_{filename}"
            file.save(os.path.join('app/static/img/blog', image_filename))
            post.image = image_filename
    
    db.session.commit()
    flash('Blog post updated successfully!', 'success')
    return redirect(url_for('admin.manage_blog'))

@admin.route('/blog/delete/<int:post_id>', methods=['POST'])
@login_required
@admin_required
def delete_blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    
    # Delete associated image if it exists
    if post.image:
        image_path = os.path.join('app/static/img/blog', post.image)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({'message': 'Blog post deleted successfully'})

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
'''
@admin.route('/messages')
@login_required
@admin_required
def view_messages():
    messages = Message.query.filter_by(receiver_id=current_user.id).order_by(Message.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)
'''

@admin.route('/messages/<int:employee_id>')
@login_required
@admin_required
def view_messages(employee_id):
    employee = User.query.get_or_404(employee_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == employee_id)) |
        ((Message.sender_id == employee_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()
    
    return render_template('admin/messages.html', messages=messages, employee_id=employee_id)
