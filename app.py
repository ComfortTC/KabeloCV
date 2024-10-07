from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('resume'))  # Serve the resume page by default

@app.route('/')
def resume():
    return render_template('index.html')  # Render the resume template

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='img/favicon.ico')), 204  # Update favicon route

# PostgreSQL configuration (Heroku environment variable)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u5p73bnjcii92r:p06607f621271672f439fcd354079a12193e81a8bb7bf5e597e621a062f2115b0@c8m0261h0c7idk.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d12cq1lo29hl5d'
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
