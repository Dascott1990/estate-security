# from flask import Flask, request, jsonify, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from datetime import datetime, timedelta
# from dotenv import load_dotenv
# import random
# import string
# import os
# import logging
# import smtplib
# from email.mime.text import MIMEText
#
# # Load environment variables
# load_dotenv()
#
# EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
# EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
#
# # App Configuration
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitors.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
#
# # Logging Setup
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # Database Models
# class Visitor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     phone = db.Column(db.String(15), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     host_name = db.Column(db.String(100), nullable=False)
#     purpose = db.Column(db.String(200), nullable=False)
#     hashed_pin = db.Column(db.String(128), nullable=False)
#     expiration_time = db.Column(db.DateTime, nullable=False)
#     is_used = db.Column(db.Boolean, default=False)
#
# # Utility Functions
# def generate_pin():
#     """Generates a random 6-digit PIN."""
#     return ''.join(random.choices(string.digits, k=6))
#
# def send_email_notification(email, pin):
#     """Sends an email notification with the visitor's PIN."""
#     try:
#         subject = "Your Visitor Access PIN"
#         body = f"""
#         Dear Visitor,
#
#         Your PIN for accessing the estate is: {pin}.
#
#         Please keep this PIN confidential and use it within the allowed time frame.
#
#         Best regards,
#         Estate Security Team
#         """
#         msg = MIMEText(body)
#         msg['Subject'] = subject
#         msg['From'] = EMAIL_ADDRESS
#         msg['To'] = email
#
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#             server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#             server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
#
#         logger.info(f"Email sent to {email} with PIN {pin}")
#     except Exception as e:
#         logger.error(f"Failed to send email: {e}")
#
# # Routes
# @app.route('/')
# def index():
#     """Render the visitor registration form."""
#     return render_template('index.html')
#
# @app.route('/register', methods=['POST'])
# def register_visitor():
#     """Register a visitor and send a PIN via email."""
#     data = request.json
#
#     name = data.get('name')
#     phone = data.get('phone')
#     email = data.get('email')
#     host_name = data.get('host_name')
#     purpose = data.get('purpose')
#
#     if not all([name, phone, email, host_name, purpose]):
#         return jsonify({"error": "All fields are required."}), 400
#
#     # Generate a unique PIN and expiration time
#     plain_pin = generate_pin()
#     hashed_pin = bcrypt.generate_password_hash(plain_pin).decode('utf-8')
#     expiration_time = datetime.now() + timedelta(hours=6)
#
#     visitor = Visitor(name=name, phone=phone, email=email, host_name=host_name,
#                       purpose=purpose, hashed_pin=hashed_pin, expiration_time=expiration_time)
#
#     try:
#         db.session.add(visitor)
#         db.session.commit()
#         send_email_notification(email, plain_pin)
#         return jsonify({"message": "Visitor registered successfully.", "pin": plain_pin}), 201
#     except Exception as e:
#         db.session.rollback()
#         logger.error("Error during registration: %s", str(e))
#         return jsonify({"error": "An error occurred while registering the visitor."}), 500
#
# @app.route('/validate', methods=['POST'])
# def validate_pin():
#     """Validate a visitor's PIN."""
#     data = request.json
#     pin = data.get('pin')
#
#     if not pin:
#         return jsonify({"error": "PIN is required."}), 400
#
#     visitor = Visitor.query.filter_by(is_used=False).first()
#
#     if not visitor or not bcrypt.check_password_hash(visitor.hashed_pin, pin):
#         return jsonify({"error": "Invalid PIN."}), 404
#
#     if datetime.now() > visitor.expiration_time:
#         return jsonify({"error": "PIN has expired."}), 400
#
#     visitor.is_used = True
#     db.session.commit()
#
#     return jsonify({"message": "Access granted."}), 200
#
# if __name__ == '__main__':
#     app.run(debug=True)
