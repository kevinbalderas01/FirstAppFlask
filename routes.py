from flask import render_template, redirect, url_for, flash, get_flashed_messages
from app import app, db
from datetime import datetime
import forms
from models import Task

@app.route('/')
def index():
    #return '<h1>Hello</h1> World'
    tasks = Task.query.all()
    return render_template('index_ej.html', tasks = tasks)  #TEMPLATE INJECTION JINJA !!!

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = forms.AddTaskForm()
    if form.validate_on_submit(): #After hit the submit botton and OK
        #print('Submited title', form.title.data)
        t = Task(title = form.title.data, date = datetime.utcnow())
        db.session.add(t)
        db.session.commit()
        flash('Task added to the DB') #Display a flash message
        #return render_template('about.html', form=form, title=form.title.data)
        return redirect(url_for('index'))
    return render_template('add.html', form = form)

@app.route('/edit/<int:task_id>', methods=['GET','POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    form = forms.AddTaskForm()
    if task:
        if form.validate_on_submit():
            task.title = form.title.data
            task.date = datetime.utcnow()
            db.session.commit()
            flash('Task have been updated')
            return redirect(url_for('index'))
        form.title.data = task.title
        return render_template('edit.html', form = form, task_id = task_id)
    else:
        flash('No Task found')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get(task_id)
    form = forms.DeleteTaskForm()
    if task:
        if form.validate_on_submit():
            db.session.delete(task)
            db.session.commit()
            flash('Task have been deleted')
            return redirect(url_for('index'))
        return render_template('delete.html', form = form, task_id = task_id, title=task.title)
    else:
        flash('No Task found for deleting')
    return redirect(url_for('index'))
