from flask.cli import FlaskGroup
from app import create_app, db
from app.models.user import User

cli = FlaskGroup(create_app=create_app)

@cli.command("create-admin")
def create_admin():
    """Create an admin user"""
    print("Creating admin user...")
    
    email = input("Enter admin email: ")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        print("Error: User with this email already exists!")
        return
    
    admin = User(
        email=email,
        username=username,
        role='admin',
        company_name='Diamond Coffee Company',
        contact_person=username,
        country='Kenya'
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user {username} created successfully!")

@cli.command("create-employee")
def create_employee():
    """Create an employee user"""
    print("Creating employee user...")
    
    email = input("Enter employee email: ")
    username = input("Enter employee username: ")
    password = input("Enter employee password: ")
    
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        print("Error: User with this email already exists!")
        return
    
    employee = User(
        email=email,
        username=username,
        role='employee',
        company_name='Diamond Coffee Company',
        contact_person=username,
        country='Kenya'
    )
    employee.set_password(password)
    
    db.session.add(employee)
    db.session.commit()
    print(f"Employee user {username} created successfully!")

if __name__ == '__main__':
    cli()