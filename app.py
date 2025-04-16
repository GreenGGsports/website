from flask import Flask, render_template
import json

app = Flask(__name__)


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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

