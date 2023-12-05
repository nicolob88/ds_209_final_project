from flask import Flask, render_template, request
from energy_charts import energyCharts

ec = energyCharts()
app = Flask(__name__)
@app.route("/")
def w209():
   file="about9.jpg"
   return render_template("w209.html",file=file)

@app.route("/test/")
def test():
   return "<h1>This is another test</h1>"

@app.route("/cost_expediture")
def cost_expediture():
    mychart = ec.createCostExpeditureChart()
    chart_json = mychart.to_json()
    return render_template('chart_template.html', chart_json=chart_json)

@app.route("/generation_consumption")
def generation_consumption():
    mychart = ec.createGenerationConsumptionChart()
    chart_json = mychart.to_json()
    return render_template('chart_template.html', chart_json=chart_json)

if __name__ == "__main__":
   app.run(host="0.0.0.0", debug=True, port=8888)

