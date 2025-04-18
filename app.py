from flask import Flask, render_template, request
import json
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()

app = Flask(__name__)

# Flask-Mail Configuration using environment variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'

mail = Mail(app)

def load_json(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)

szolgaltatasok = load_json('config/services.json')
team_members = load_json('config/team_members.json')

@app.route('/')
def index():
    return render_template('landing.html', szolgaltatasok=szolgaltatasok)

@app.route('/szolgaltatas/<string:route>')
def szolgaltatas(route):
    szolgaltatas = next((item for item in szolgaltatasok if item['route'] == route), None)
    if szolgaltatas is None:
        return "Szolgáltatás nem található!", 404
    return render_template('service.html', szolgaltatas=szolgaltatas)

@app.route('/about')
def about():
    return render_template('about.html', team_members=team_members)

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/products')
def products():
    return render_template("products.html")

@app.route("/send_msg", methods=['POST']) 
def send_msg():
    # Get form data from request
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Create the email content
    msg = Message(
        subject="New message from contact form",
        sender=app.config['MAIL_USERNAME'],
        recipients=["greengg.sports@gmail.com"],
    )
    
    # Construct the body with the form data
    msg.body = f"New message received from {name} ({email}):\n\n{message}"

    try:
        # Send the email
        mail.send(msg)
        return "Message sent successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

