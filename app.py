from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

@app.route('/favicon.ico')
def favicon():
    return 'assets/img/favicon.ico', 204 

# PostgreSQL configuration (Heroku environment variable)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://localhost/dbname'
db = SQLAlchemy(app)

# Define a Job model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Job('{self.title}', '{self.company}')"

# Create database tables
with app.app_context():
    db.create_all()

# Routes for CRUD operations
@app.route('/admin/jobs', methods=['GET'])
def list_jobs():
    jobs = Job.query.all()
    return render_template('admin.html', jobs=jobs)

@app.route('/admin/job/new', methods=['POST'])
def create_job():
    title = request.form['title']
    company = request.form['company']
    description = request.form['description']
    new_job = Job(title=title, company=company, description=description)
    db.session.add(new_job)
    db.session.commit()
    return redirect(url_for('list_jobs'))

@app.route('/admin/job/delete/<int:id>', methods=['POST'])
def delete_job(id):
    job = Job.query.get_or_404(id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('list_jobs'))

@app.route('/admin/job/update/<int:id>', methods=['POST'])
def update_job(id):
    job = Job.query.get_or_404(id)
    job.title = request.form['title']
    job.company = request.form['company']
    job.description = request.form['description']
    db.session.commit()
    return redirect(url_for('list_jobs'))

if __name__ == '__main__':
    app.run(debug=True)
