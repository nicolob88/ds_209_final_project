from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder='static')
import pandas as pd

# Flask routes
@app.route('/')
def home():
    return render_template('index.html', css=url_for('static', filename='style.css'))

@app.route('/energyoverview')
def energyoverview():
    return render_template('energyoverview.html', css=url_for('static', filename='style.css'))

@app.route('/energyprojections')
def energyprojections():
    return render_template('energyprojections.html', css=url_for('static', filename='style.css'))

@app.route('/cleanenergy')
def cleanenergy():
    return render_template('cleanenergy.html', css=url_for('static', filename='style.css'))

@app.route('/datasources')
def datasources():
    return render_template('datasources.html', css=url_for('static', filename='style.css'))

@app.route('/contact')
def contact():
    return render_template('contact.html', css=url_for('static', filename='style.css'))

if __name__ == '__main__':
    app.run(debug=True)
