from flask import Flask, render_template, url_for
from energy_charts import energyCharts

ec = energyCharts()
app = Flask(__name__, static_folder='static')
import pandas as pd

# Flask routes
@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html', css=url_for('static', filename='style.css'))

@app.route('/energyoverview.html')
def energyoverview():
    return render_template('energyoverview.html')

@app.route('/energyprojections.html')
def energyprojections():
    return render_template('energyprojections.html', css=url_for('static', filename='style.css'))

@app.route('/cleanenergy.html')
def cleanenergy():
    return render_template('cleanenergy.html', css=url_for('static', filename='style.css'))

@app.route('/datasources.html')
def datasources():
    return render_template('datasources.html', css=url_for('static', filename='style.css'))

@app.route('/contact.html')
def contact():
    return render_template('contact.html', css=url_for('static', filename='style.css'))

@app.route("/cost_expenditure")
def cost_expenditure():
    mychart = ec.createCostExpenditureChart()
    chart_json = mychart.to_json()
    return render_template('chart_template.html', chart_json=chart_json)

@app.route("/generation_consumption")
def generation_consumption():
    mychart = ec.createGenerationConsumptionChart()
    chart_json = mychart.to_json()
    return render_template('chart_template.html', chart_json=chart_json)

if __name__ == '__main__':
    app.run()





