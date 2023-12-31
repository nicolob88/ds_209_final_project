import pandas as pd
import numpy as np
import altair as alt
import os

class energyCharts:
    def __init__(self):
        print(os.listdir())
        self.df_e = pd.read_csv("w209/energy_data.csv")
        self.df_e_us = self.df_e.query("state == 'US'") 
        self.df_e_st = self.df_e.query("state != 'US'") 

    def createCostExpenditureChart(self):
        df_cost_exp = self.df_e_st[['state', 'year', 'expenditures (M dollars)', 'price (dollars per MBtu)']]
        df_cost_exp = df_cost_exp.rename(columns={'expenditures (M dollars)' : 'Expenditures (M dollars)', 'price (dollars per MBtu)' : 'Price (dollars per MBtu)'})
        df_cost_exp = df_cost_exp.melt(id_vars=['state', 'year'], var_name='view_category', value_name='energy_value')
        energy_type = ['Expenditures (M dollars)', 'Price (dollars per MBtu)']

        brush = alt.selection_point(fields=['year'], value={'year': df_cost_exp['year'].min()}, nearest=True, on="mouseover", empty=True)
        selector = alt.selection_point(
        name='Select',
        fields=['view_category'],
        value={'view_category': energy_type},
        bind=alt.binding_select(options=energy_type)
        )

        text_config = {'angle': 0, 'color': 'grey', 'size': 25, 'dx': 400, 'dy': 0, 'text': 'US Energy Cost/Expenditure by State and Year'}
        textheader = alt.Chart().mark_text(**text_config).encode()

        us_level = alt.Chart(df_cost_exp).mark_bar(
        ).encode(
         x=alt.X('year:N', title='Year'),
         y=alt.Y('average_r:Q', title='Average'),
         color=alt.condition(brush, 'average_r:Q', alt.value("lightgrey")),
         tooltip=['year:N', 'average_r:Q'],
        ).add_params(
        selector, brush
        ).transform_filter(
        selector
        ).transform_aggregate(
        average='mean(energy_value)',
        groupby=['year']
        ).transform_calculate(
        average_r='round(datum.average * 100)/100'
        ).properties(
        width=800,
        height=100,
        title="US Energy Cost/Expenditure (2001-2021)"
        )

        state_level = alt.Chart(df_cost_exp).mark_bar(
        ).encode(
        color=alt.Color('energy_value:Q', scale=alt.Scale(scheme="blues")), 
        x=alt.X('state:N', title='State'), 
        y=alt.Y('energy_value:Q', title='Energy Cost/Expenditure'), 
        tooltip=['year:N', 'state:N', 'energy_value:Q']).add_params( 
        selector, brush
        ).transform_filter( 
        selector).transform_filter(
        brush).properties(
        title='States Energy Cost/Expenditure', width=800, height=300
        )
        mychart = alt.vconcat(textheader, us_level, state_level)
        return mychart

    def createEnergySourceCharts(self, df, brush, etype, color, axistitle, title=False):
        estr = etype.capitalize()
        etitle = f"{estr} Energy (BBTU)"
        gen = alt.Chart(df).mark_line(point=True).encode(
        x='year:N',
        y=alt.Y(f'{etype}_generation:Q', title=etitle),
        color=alt.value(color),
        tooltip=['year:N', f'{etype}_generation:Q'],
        shape=alt.value('square'),
        opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05))
        ).properties(
        width=250,
        height=150
        )
        if axistitle:
           con = alt.Chart(df).mark_line(point=True).encode(
           x=alt.X('year:N', title="Year"), 
           y=alt.Y(f'{etype}_consumption:Q', title=etitle),
           strokeDash=alt.value([8,4]),
           color=alt.value(color),
           tooltip=['year:N', f'{etype}_consumption:Q'],
           shape=alt.value('cross'),
           opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05))
           ).properties(
           width=250,
           height=150
           )
        else:
           con = alt.Chart(df).mark_line(point=True).encode(
           x=alt.X('year:N', axis=alt.Axis(labels=False), title=None),
           y=alt.Y(f'{etype}_consumption:Q', title=etitle),
           strokeDash=alt.value([8,4]),
           color=alt.value(color),
           tooltip=['year:N', f'{etype}_consumption:Q'],
           shape=alt.value('cross'),
           opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05))
           ).properties(
           width=250,
           height=150
           )

        combined = gen + con
        combined.encode(opacity=alt.condition(brush, alt.value(0.75), alt.value(0.05)))
        if title:
           combined = combined.properties(title="Source Breakdown")
        return combined

    def createGenerationConsumptionChart(self):
        df_us = self.df_e_us.drop(['expenditures (M dollars)', 'price (dollars per MBtu)'], axis=1)
        df_us['total_generation'] = df_us['gas_generation'] + df_us['coal_generation'] + df_us['oil_generation'] + df_us['nuclear_generation'] + df_us['renewable_generation']
        df_us['total_consumption'] = df_us['gas_consumption'] + df_us['coal_consumption'] + df_us['oil_consumption'] + df_us['nuclear_consumption'] + df_us['renewable_consumption']
        df_us['diff'] = df_us['total_generation'] - df_us['total_consumption']

        brush = alt.selection_interval(
        encodings=['x'], # limit selection to x-axis (year) values
        )

        overall = alt.Chart(df_us).mark_bar(
        point=True
        ).add_params(
        brush
        ).encode(
        x=alt.X('year:N', title='Year'),
        y=alt.Y('diff:Q', title='Net Energy (BBTU)'),
        tooltip=['year:N', 'diff:Q'],
        color=alt.condition('datum.diff < 0', alt.value('#ff9999'), alt.value('#1f77b4')),
        opacity=alt.condition(brush, alt.value(0.75), alt.value(0.25))
        ).properties(
        width=600,
        height=300,
        title='Net US BBTU by Year')

        # generation + consumption summaries
        consumption = alt.Chart(df_us).mark_area(point=True
        ).encode(
        alt.X('year:N', title='Year'),
        alt.Y('total_consumption:Q', title='Energy Generation/Consumption (BBTU)'),
        color=alt.value('#76B7B2'),
        opacity=alt.condition(brush, alt.value(0.45), alt.value(0.25)),
        strokeDash=alt.value([8,4]),
        shape=alt.value('cross'),
        tooltip=['year:N', 'total_consumption:Q'],
        ).properties(
        width=600,
        height=400,
        title='US Energy Generation/Consumption (2001-2021)'
        )

        generation = alt.Chart(df_us).mark_area(point=True).encode(
        alt.X('year:N', title='Year'),
        alt.Y('total_generation:Q', title='Energy Generation/Consumption (BBTU)'),
        color=alt.value('#59A14F'),
        opacity=alt.condition(brush, alt.value(0.45), alt.value(0.25)),
        shape=alt.value('square'),
        tooltip=['year:N', 'total_generation:Q'],
        ).properties(
        width=600,
        height=400
        )

        text_gen = alt.Chart(df_us).mark_text(
        fontSize=15,
        dx=50,
        dy=-10
        ).encode(
        x="min(year):N",
        y=alt.Y("total_generation:Q", aggregate={'argmin': 'year'}),
        color=alt.value('#696969'),
        text=alt.value("Generation"),
        )

        text_con = alt.Chart(df_us).mark_text(
        fontSize=15,
        dx=50,
        dy=-20
        ).encode(
        x="min(year):N",
        y=alt.Y("total_consumption:Q", aggregate={'argmin': 'year'}),
        color=alt.value('#696969'),
        text=alt.value("Consumption"),
        )

        years = generation + consumption + text_gen + text_con

        gas_combined = self.createEnergySourceCharts(df_us, brush, 'gas', '#F2A252', False)
        coal_combined = self.createEnergySourceCharts(df_us, brush, 'coal', '#6E91B6', False, True)
        oil_combined = self.createEnergySourceCharts(df_us, brush, 'oil', '#76B7B2', False)
        nuclear_combined = self.createEnergySourceCharts(df_us, brush, 'nuclear', '#E15759', False)
        renewable_combined = self.createEnergySourceCharts(df_us, brush, 'renewable', '#59A14F', True)

        text_config = {'angle': 0, 'color': 'grey', 'size': 25, 'dx': 400, 'dy': 0, 'text': 'Energy Generation/Consumption by Energy Sources'}
        textheader = alt.Chart().mark_text(**text_config).encode()

        combine_energy = alt.vconcat(coal_combined, gas_combined, nuclear_combined, oil_combined, renewable_combined).properties(spacing=5)
        overview = alt.vconcat(overall, years)
        mychart = alt.hconcat(overview, combine_energy).properties(spacing=5)
        mychart = alt.vconcat(textheader, mychart)

        return mychart

