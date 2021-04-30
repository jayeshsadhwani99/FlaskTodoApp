# imports
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Connect the Database to the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# Initialize the Database
db = SQLAlchemy(app)


# Create a model
class Todo(db.Model):
    # Columns in the table
    # ID for uniquely identifying entries
    id = db.Column(db.Integer, primary_key=True)
    # Actual content (cannot be empty)
    content = db.Column(db.String(200), nullable=False)
    # When the task was created
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Returns a string when a new element is created
    def __repr__(self):
        return '<Task %r>' % self.id


# Routes

# Initial Route
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']  # Get the content from the body
        # Create a new task (Object of Todo Class)
        new_task = Todo(content=task_content)

        try:
            # Add to Database
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding the task'
    else:
        # Get all the tasks from the Database
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


# Delete Route
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Task could not be deleted'


# Update route
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error in editing your task'

    else:
        return render_template('update.html', task=task)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)  # This shows the error in the webpage
