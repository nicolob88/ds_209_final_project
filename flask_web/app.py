import pandas as pd
from flask import Flask, render_template, url_for
import altair as alt

app = Flask(__name__)
df_gen = pd.read_csv('static/energy_gen.csv')


#### Flask routes
@app.route('/')
def home():
    return render_template('home.html', nrecords=f'{len(df_gen):,}')


@app.route('/gen')
def gen():
    return render_template('gen.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

#### Graph routes
@app.route('/charts/gen')
def gen_chart():
    df_tot1 = df_gen.groupby('dt')['generation'].sum().reset_index()
    chart = alt.Chart(df_tot1).mark_line().encode(
        x=alt.X('yearmonth(dt):N', title='Year'),
        y=alt.Y('generation:Q', title='Generation (mW)'),
        tooltip=alt.Tooltip('generation:Q', title='mW:', format='0,')
    ).properties(
        width=800,
        height=300,
        # title='Energy generation by source by month'
    ).interactive()
    return chart.to_json()


if __name__ == "__main__":
    app.run(debug=True)