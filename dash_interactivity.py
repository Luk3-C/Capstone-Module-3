import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max = spacex_df['Payload Mass (kg)'].max()
min = spacex_df['Payload Mass (kg)'].min()


app = dash(__name__)
app.layout = html.Div([
dcc.Dropdown(id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 'ALL'},
                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                
                value='ALL',
                placeholder="Select a Launch Site here",
                searchable=True)

                html.Div(dcc.Graph(id='pie_chart'))

                dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                marks={0: '0',
                       100: '100'},
                value=[min, max])

                html.Div(dcc.Graph(id='payload_scatter_plot'))


]),

 # Function decorator to specify function input and output
@app.callback(Output(component_id='pie_chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value')])

def pie_chart(entered_site):
    filter_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title=f'Total Success Launches by Site {entered_site}')
        return fig
    else:
        filter_df = spacex_df[spacex_df['Launch Site']==entered_site]
        filter_df = filtered_df.groupby(['Launch Site', 'class']).size().reset_index()
        filter_df.rename(columns={0:'class count'}, inplace=True)
        fig2 = px.pie(
            filter_df
            , values='class count'
            , names= ' class'
            , title = 'Total Success Launches for Site ' + site_val
        )    
        return fig2

html.Div(dcc.Graph(id='success-pie-chart'))


# Function decorator to specify function input and output
@app.callback(Output(component_id='payload_scatter_plot', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property="value")])

def payload_scatter_plot(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig3 = px.scatter(spacex_df, x="Payload Mass (kg)", y="class",
        color = 'Booster Version Category', 
        labels={"Payload Mass": "Payload Mass", 
        "Class": "Launch Outcome" }, 
        title="Payload Mass vs. Launch Outcome")
        return fig3

    else:
        filter_df = spacex_df[spacex_df['Launch Site']==entered_site]
        filter_df = filtered_df.groupby(['Launch Site', 'class']).size().reset_index()
        filter_df.rename(columns={0:'class count'}, inplace=True)
        fig4 = px.scatter(spacex_df, x="Payload Mass (kg)", y="class",
        color = 'Booster Version Category', 
        labels={"Payload Mass": "Payload Mass", 
        "Class": "Launch Outcome" }, 
        title="Payload Mass vs. Launch Outcome")
        return fig4
        # return the outcomes piechart for a selected site

if __name__ == '__main__':
    app.run(debug=True)