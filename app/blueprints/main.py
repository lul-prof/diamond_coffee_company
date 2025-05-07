from flask import Blueprint, render_template, request,flash,redirect,url_for
from app.models.product import Product
from app.models.blog import BlogPost
from datetime import datetime
from app import mail


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main/index.html')

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/products')
def products():
    products = Product.query.all()
    return render_template('main/products.html', products=products)

@main.route('/sustainability')
def sustainability():
    return render_template('main/sustainability.html')

@main.route('/blog')
def blog():
    posts = BlogPost.query.filter_by(status='published').order_by(BlogPost.published_at.desc()).all()
    return render_template('main/blog.html', posts=posts)

@main.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return render_template('main/blog_post.html', post=post)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        try:
            msg = Message(
                subject=f'Contact Form: {subject}',
                sender=email,
                recipients=['your-email@example.com'],  # Replace with your email
                body=f'''
                From: {name}
                Email: {email}
                
                Message:
                {message}
                '''
            )
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash('An error occurred while sending your message. Please try again.', 'error')
            
        return redirect(url_for('main.contact'))
        
    return render_template('main/contact.html')