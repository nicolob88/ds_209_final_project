from flask import Flask, render_template, request
from energy_charts import energyCharts

ec = energyCharts()
app = Flask(__name__)
import pandas as pd
@app.route("/")
def ping():
   return "<h2>I am still alive</h2>"

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

if __name__ == "__main__":
   app.run()

