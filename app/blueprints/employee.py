from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit
from app import socketio, db
from app.models.message import Message
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit
from app import socketio, db
from app.models.message import Message
from app.models.task import Task
from app.models.user import User

employee = Blueprint('employee', __name__)

@employee.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(assigned_to=current_user.id).all()
    return render_template('employee/dashboard.html', tasks=tasks)

@employee.route('/tasks')
@login_required
def tasks():
    active_tasks = Task.query.filter_by(
        assigned_to=current_user.id,
        status='pending'
    ).all()
    completed_tasks = Task.query.filter_by(
        assigned_to=current_user.id,
        status='completed'
    ).all()
    return render_template('employee/tasks.html', 
                         active_tasks=active_tasks,
                         completed_tasks=completed_tasks)


@employee.route('/chat')
@login_required
def chat():
    admin = User.query.filter_by(role='admin').first()
    # Get existing messages between current user and admin
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == admin.id)) |
        ((Message.sender_id == admin.id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()
    
    return render_template('employee/chat.html', admin=admin, messages=messages)

@socketio.on('send_message')
def handle_message(data):
    message = Message(
        sender_id=current_user.id,
        receiver_id=data['receiver_id'],
        content=data['message']
    )
    db.session.add(message)
    db.session.commit()
    
    emit('receive_message', {
        'sender': current_user.username,
        'message': data['message'],
        'timestamp': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }, room=data['receiver_id'])

