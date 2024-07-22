from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_mail import Mail, Message
import os
from datetime import datetime
app = Flask(__name__)
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medapp.db'
app.config['MAIL_SERVER'] = 'smtp.yourmailserver.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_gmail'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(150), nullable=False)
    appointment_date = db.Column(db.String(150), nullable=False)
    doctor_name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class AppointmentForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired()])
    appointment_date = DateField('Appointment Date', format='%Y-%m-%d', validators=[DataRequired()])
    doctor_name = StringField('Doctor Name', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

with app.app_context():
    db.create_all()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Already logged in, redirect to index

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('appointments'))
        else:
            return "Invalid credetials"
    return render_template('login.html')



@app.route('/appointments')
@login_required
def appointments():
    return render_template('appointments.html')


@app.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        patient_name = form.patient_name.data
        appointment_date = form.appointment_date.data
        doctor_name = form.doctor_name.data

        # Create a new appointment object
        new_appointment = Appointment(
            patient_name=patient_name,
            appointment_date=appointment_date,
            doctor_name=doctor_name,
            user_id=current_user.id
        )

        try:
            # Save the appointment to the database
            db.session.add(new_appointment)
            db.session.commit()

            # Send confirmation email
            send_confirmation_email(current_user.email, patient_name, appointment_date, doctor_name)
            # Flash message and redirect to appointments page
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('appointments'))
        except Exception as e:
            # Handle database errors gracefully
        
            flash(f'An error occurred while booking your appointment: {str(e)}', 'danger')
            db.session.rollback()
            return redirect(url_for('book_appointment'))

    return render_template('book_appointment.html', form=form)




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Already logged in, redirect to index

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user or existing_email:
            return 'Username or email already exists'
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('appointments.html')  # Redirect to appointments page





@app.route('/get_appointments', methods=['GET'])
@login_required
def get_appointments():
    user_appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    appointment_list = [
        {
            "patientName": appt.patient_name,
            "appointmentDate": appt.appointment_date,
            "doctorName": appt.doctor_name
        }
        for appt in user_appointments
    ]
    return jsonify(appointment_list)

def send_confirmation_email(to, patient_name, appointment_date, doctor_name):
    msg = Message('Appointment Confirmation', sender='gmail', recipients=[to])
    msg.body = f"Dear {patient_name},\n\nYour appointment with Dr. {doctor_name} on {appointment_date} has been confirmed.\n\nBest regards,\nMedAppoint Team"
    mail.send(msg)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=8001)
