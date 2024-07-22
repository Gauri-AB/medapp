# MedApp

MedApp is a Flask-based application for scheduling and managing healthcare appointments.

## Features

- **User Authentication:** Secure login and registration.
- **Appointment Booking:** Schedule and manage appointments.
- **Real-Time Notifications:** Get updates on appointment statuses.


## Technologies

- **Backend:** Flask, SQLAlchemy, Flask-Login, Flask-Security, Flask-SocketIO, Flask-RESTful
- **Frontend:** HTML5, CSS3, Bootstrap

## Installation

1. **Clone the Repository**

    ```bash
   git clone https://github.com/yourusername/medapp.git
   cd medappoint
2.**Set Up Environment**
     
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    
3.**Initialize Database**
    
    flask db upgrade

4.**Run the App**
    
    flask run



