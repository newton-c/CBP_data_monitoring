#!/usr/bin/python3

import pandas as pd 
import os
from datetime import datetime
import plotly.express as px


# Find which of the downloaded datasets is the most recent
if len(os.listdir('data/')) > 0:
    matches = [file for file in os.listdir('data/') if "cbp_data_" in file]
    dates = ([datetime.strptime(match.replace('cbp_data_', '')
                                   .replace('.csv', ''), "%Y-%m-%d")
                 .date() for match in matches])
    current_date = max(dates)
else:
    raise ValueError('Error:\nNo files in the "data/" directory')
    

# grab and clean the most recent dataset
filename = 'data/cbp_data_' + str(current_date) + '.csv'
cbp_data = pd.read_csv(filename)
cbp_data['FY'] = cbp_data['FY'].str.replace(' (FYTD)', '')
cbp_data['date'] = pd.to_datetime(cbp_data['FY'] + '-' + cbp_data['Month (abbv)'] + '-' + '01',
                                  format="%Y-%b-%d")

sw_data = cbp_data[cbp_data['Region'] == 'Southwest Border']

# there are some weird dates that haven't happened yet
sw_data = sw_data[sw_data['date'] < datetime.strptime(str(current_date), "%Y-%m-%d")]

# grab the fentanyl data
f_data = sw_data[sw_data['Drug Type']=='Fentanyl']
f_data = f_data.groupby('date', as_index=False)[['Sum Qty (lbs)']].sum()

# convert pounds to kilograms
f_data['kilos'] = f_data['Sum Qty (lbs)'] / 2.2

# define the data range
start_date = str(min(f_data['date']).date())[0:7]
end_date = str(max(f_data['date']).date())[0:7]


# make the plot
fig = px.line(f_data, x="date", y="kilos",
             labels={
                     "date": "",
                     "kilos": "Kilograms Seized"
                 },
             hover_data={
                         "date": False,
                         "kilos": ":.0f"
             })

fig.update_layout(
    title=dict(text=f"Kilograms of Fentayl Seized by CBP<br><sup>Southwest Border Region, from {start_date} to {end_date}</sup>",
               font=dict(size=24), automargin=False),
    font_family="Open Sans",
    font_color="#3B3B3B",
    title_font_family="Open Sans",
    hovermode="x unified",
    plot_bgcolor="#FAFAFA",
    paper_bgcolor="#FAFAFA"
)

fig.update_layout(height=420, width=640,
                 margin_t=120,
                 margin_b=35,
                 margin_l=40,
                 margin_r=35)



fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor='black')
fig.update_yaxes(showgrid=False, zeroline=True,
                 range=[0, f_data['kilos'].max()+100],
                 title=None)
#fig.show()
fig.write_html("figs/fentanyl.html")


# grab the methamphetamine data
m_data = sw_data[sw_data['Drug Type']=='Methamphetamine']
m_data = m_data.groupby('date', as_index=False)[['Sum Qty (lbs)']].sum()

# convert pounds to kilograms
m_data['kilos'] = m_data['Sum Qty (lbs)'] / 2.2

# define the data range
start_date = str(min(m_data['date']).date())[0:7]
end_date = str(max(m_data['date']).date())[0:7]


fig = px.line(m_data, x="date", y="kilos",
             labels={
                     "date": "",
                     "kilos": "Kilograms Seized"
                 },
             hover_data={
                         "date": False,
                         "kilos": ":.0f"
             })

fig.update_layout(
    title=dict(text=f"Kilograms of Methamphetamine Seized by CBP<br><sup>Southwest Border Region, from {start_date} to {end_date}</sup>",
               font=dict(size=24), automargin=False),
    font_family="Open Sans",
    font_color="#3B3B3B",
    title_font_family="Open Sans",
    hovermode="x unified",
    plot_bgcolor="#FAFAFA",
    paper_bgcolor="#FAFAFA"
)

fig.update_layout(height=420, width=640,
                 margin_t=120,
                 margin_b=35,
                 margin_l=40,
                 margin_r=35)



fig.update_xaxes(showgrid=False, showline=True, linewidth=2, linecolor='black')
fig.update_yaxes(showgrid=False, zeroline=True,
                 range=[0, m_data['kilos'].max()+1000],
                 title=None)
#fig.show()
fig.write_html("figs/meth.html")

import chart_studio.tools as tls

tls.get_embed('https://public-ic-resources.s3.us-east-2.amazonaws.com/cbp_meth.html')