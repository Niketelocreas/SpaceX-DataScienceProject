# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)


# Extract unique launch sites from the DataFrame
launch_sites = spacex_df['Launch Site'].unique()

# Create the options list for the dropdown
options = [{'label': site, 'value': site} for site in launch_sites]
options.insert(0, {'label': 'All Sites', 'value': 'ALL'})  # Add the 'All Sites' option at the beginning

# Add the dropdown to the app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Task 1: Add a dropdown list to enable Launch Site selection
    
    # Add additional components like graphs and tables below
])




# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=options,
                                    value='ALL',  # Default value placeholder="Select a Launch Site here",
                                    searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([
                                    dcc.RangeSlider(
                                        id='payload-slider',
                                        min=0,  # Minimum payload in kg
                                        max=10000,  # Maximum payload in kg
                                        step=1000,  # Step size
                                        value=[min_payload, max_payload],  # Default range
                                        marks={i: str(i) for i in range(0, 10001, 1000)}  # Marks at every 1000 kg
                                        ),
                                        html.Div(id='slider-output-container')  # Optional: Display the selected range
                                        ]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # Initialize filtered DataFrame
    filtered_df = spacex_df

    if entered_site == 'ALL':
        # Use all rows in the dataframe for the pie chart
        # Count success (class=1) and failure (class=0)
        success_counts = filtered_df['class'].value_counts()
        fig = px.pie(
            values=success_counts,
            names=success_counts.index,
            title='Total Successful Launches for All Sites'
        )
    else:
        # Filter DataFrame for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        # Count success (class=1) and failure (class=0) for the selected site
        success_counts = filtered_df['class'].value_counts()
        fig = px.pie(
            values=success_counts,
            names=success_counts.index,
            title=f'Success vs. Failed Launches for {entered_site}'
        )

    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter the DataFrame based on the selected site and payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                             (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if selected_site == 'ALL':
        # All sites selected: plot all data
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Launch Success',
            labels={'class': 'Launch Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
            hover_data=['Launch Site']  # Optional: Display launch site on hover
        )
    else:
        # Specific launch site selected: filter further
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Launch Success for {selected_site}',
            labels={'class': 'Launch Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
            hover_data=['Launch Site']  # Optional: Display launch site on hover
        )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
