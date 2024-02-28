# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# The list of launch sites
launch_sites = list(spacex_df['Launch Site'].unique())

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                         options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]        ,
                                                         value='ALL',
                                                         placeholder="Select a Launch Site here",
                                                         searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                        Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df =spacex_df.groupby('Launch Site')['class'].sum().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
                            names='Launch Site', 
                            title='Total Succcess Launches By Site')
        return fig
    
    else:
        # return the outcomes piechart for a selected site
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Count occurrences using class column
        class_counts = site_df['class'].value_counts().reset_index()
        # Render and return a pie chart for success and failure count for the selected site
        fig = px.pie(class_counts, 
                     values = 'count',
                     names='class',
                     title=f'Total Success Launches for site {entered_site}')
        
        return fig
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Callback function to update scatter chart based on dropdown and slider inputs
@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'), 
                               [Input(component_id='site-dropdown', component_property='value'),
                                Input(component_id = 'payload-slider', component_property = 'value')])


def update_scatter_chart(entered_site, selected_payload_range):
    if entered_site == 'ALL':
        # Filter DataFrame based on payload range
        range_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                            (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]
        fig = px.scatter(range_df,
                         x='Payload Mass (kg)',
                         y='class', 
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        #site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        site_df = spacex_df[(spacex_df['Launch Site'] == entered_site)]
        site_range_df = site_df[(site_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                             (site_df['Payload Mass (kg)'] <= selected_payload_range[1])]
        
        fig = px.scatter(site_range_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for {entered_site} Site')
        return fig
      
        
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)