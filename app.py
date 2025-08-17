from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    hr_name = db.Column(db.String(100))
    hr_contact = db.Column(db.String(20))
    recruiter_name = db.Column(db.String(100))
    work_mode = db.Column(db.String(50))
    l1_date = db.Column(db.Date)
    l2_date = db.Column(db.Date)
    final_round_date = db.Column(db.Date)
    offer_status = db.Column(db.String(50), default='Waiting for HR')
    follow_up_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    status_filter = request.args.get('status')
    query = Application.query
    
    if status_filter:
        query = query.filter_by(offer_status=status_filter)
    
    applications = query.order_by(Application.follow_up_date.asc()).all()
    return render_template('index.html', applications=applications, datetime=datetime)

@app.route('/add', methods=['GET', 'POST'])
def add_application():
    if request.method == 'POST':
        try:
            # Convert empty strings to None for date fields
            def parse_date(date_str):
                return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
            
            new_app = Application(
                company_name=request.form['company_name'],
                role=request.form['role'],
                hr_name=request.form['hr_name'],
                hr_contact=request.form['hr_contact'],
                recruiter_name=request.form['recruiter_name'],
                work_mode=request.form['work_mode'],
                l1_date=parse_date(request.form['l1_date']),
                l2_date=parse_date(request.form['l2_date']),
                final_round_date=parse_date(request.form['final_round_date']),
                offer_status=request.form['offer_status'],
                follow_up_date=parse_date(request.form['follow_up_date']),
                notes=request.form['notes']
            )
            
            db.session.add(new_app)
            db.session.commit()
            flash('Application added successfully!', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_application(id):
    application = Application.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            def parse_date(date_str):
                return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
            
            application.company_name = request.form['company_name']
            application.role = request.form['role']
            application.hr_name = request.form['hr_name']
            application.hr_contact = request.form['hr_contact']
            application.recruiter_name = request.form['recruiter_name']
            application.work_mode = request.form['work_mode']
            application.l1_date = parse_date(request.form['l1_date'])
            application.l2_date = parse_date(request.form['l2_date'])
            application.final_round_date = parse_date(request.form['final_round_date'])
            application.offer_status = request.form['offer_status']
            application.follow_up_date = parse_date(request.form['follow_up_date'])
            application.notes = request.form['notes']
            
            db.session.commit()
            flash('Application updated successfully!', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    # Prepare date strings for the form
    def format_date(date):
        return date.strftime('%Y-%m-%d') if date else ''
    
    date_fields = {
        'l1_date': format_date(application.l1_date),
        'l2_date': format_date(application.l2_date),
        'final_round_date': format_date(application.final_round_date),
        'follow_up_date': format_date(application.follow_up_date)
    }
    
    return render_template('edit.html', application=application, **date_fields)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_application(id):
    application = Application.query.get_or_404(id)
    try:
        db.session.delete(application)
        db.session.commit()
        flash('Application deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('index'))



if __name__ == '__main__':
    create_tables()
    app.run(debug=True)