from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from app.extensions import db
from app.models import Task , User
from app.forms import TaskForm
from app.utils import load_user 
from datetime import datetime # Import the refactored function



# Create the Blueprint
blueprint = Blueprint('tasks', __name__)

@blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Ensure g.user is available
    if not hasattr(g, 'user') or g.user is None:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('auth.login'))

    # Fetch tasks for the logged-in user
    tasks = Task.query.filter_by(user_id=g.user.id ).all()

    form = TaskForm()
    
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            deadline=form.deadline.data,
            user_id=g.user.id,
            Priority=form.Priority.data
            
        
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.dashboard'))

    return render_template('tasks.html', tasks=tasks, form=form)
@blueprint.route('/edit-task/<int:id>', methods=['POST'])
def edit_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    title = request.form.get('title')
    description = request.form.get('description')
    deadline = request.form.get('deadline')
    Priority = request.form.get('Priority')
    

    if not title or not description or not deadline or not Priority:
        return jsonify({'error': 'All fields are required'}), 400
    deadline = datetime.strptime(deadline, '%Y-%m-%d')
    # Update the task
    task.title = title
    task.description = description
    task.deadline = deadline
    task.Priority = Priority
    db.session.commit()

    return jsonify({'message': 'Task updated successfully'}), 200



@blueprint.route('/delete-task/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.dashboard'))

@blueprint.route('/get-task/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({
        'title': task.title,
        'description': task.description,
        'deadline': task.deadline.strftime('%Y-%m-%d'),  # Format correctly for date input
        'Priority': task.Priority
    })

@blueprint.route('/tasks/<int:task_id>/update-completion', methods=['POST'])
def update_task_completion(task_id):
    task = Task.query.get_or_404(task_id)
    completed = request.form.get('completed') == 'on'
    
    # Update the task's completion status
    task.completed = completed
    db.session.commit()

    # If the task is marked as completed, increment the user's rank
    if completed:
        user = User.query.get(g.user.id)
        
         
        if user:
            user.rank = (user.rank or 0) + 10
            db.session.commit()

    return redirect(url_for('tasks.dashboard'))
