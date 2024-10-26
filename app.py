import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output

# Updated data with images and Google Maps links
# Sample data with added images and Google Maps links
data = [
    {
        'name': 'Goram & Vincent, Bristol Avon Gorge',
        'service': '4/5',
        'food': '4/5',
        'atmosphere': '9/8',
        'price': '5/5',
        'image': 'https://www.visitwest.co.uk/imageresizer/?image=%2Fdmsimgs%2F1_1405792695.png&action=FullSize',
        'maps_link': 'https://www.google.com/maps/place/Goram+%26+Vincent,+Bristol+Avon+Gorge/@51.4534616,-2.6262911,19z/data=!4m11!1m3!2m2!1sRestaurants!6e5!3m6!1s0x48718dc9f8de7287:0x376cd24a04fc78e0!8m2!3d51.4534!4d-2.6253512!15sCgtSZXN0YXVyYW50c1oNIgtyZXN0YXVyYW50c5IBCnJlc3RhdXJhbnTgAQA!16s%2Fg%2F11j0tr3q9h?hl=en&entry=ttu&g_ep=EgoyMDI0MTAyMy4wIKXMDSoASAFQAw%3D%3D'
    },
    {
        'name': 'Adelina Yards',
        'service': '7/8.5',
        'food': '7/10',
        'atmosphere': '6/6',
        'price': '9/9.5',
        'image': 'https://media.timeout.com/images/105239240/image.jpg',
        'maps_link': 'https://goo.gl/maps/MRbq8eA6wztWLm8j8'
    },
    {
        'name': 'Pasture',
        'service': '6.8/7.5',
        'food': '6/7',
        'atmosphere': '4.5/4',
        'price': '7/6',
        'image': 'https://media.timeout.com/images/105239241/image.jpg',
        'maps_link': 'https://goo.gl/maps/BwZ2fFdh9xn72ZVE9'
    },
    {
        'name': 'Marceline',
        'service': '8/9',
        'food': '8/9',
        'atmosphere': '8/7',
        'price': '8/8',
        'image': 'https://media.timeout.com/images/105239242/image.jpg',
        'maps_link': 'https://goo.gl/maps/pK7GmopK8pZTB3P79'
    },
    {
        'name': 'Cheeky Scones',
        'service': '-/-',
        'food': '7/8',
        'atmosphere': '3/6',
        'price': '9/7',
        'image': 'https://media.timeout.com/images/105239243/image.jpg',
        'maps_link': 'https://goo.gl/maps/D6ZDHzFz7b6x2Tyv6'
    },
    {
        'name': 'Da Corradi',
        'service': '6/7',
        'food': '2/3',
        'atmosphere': '8/9',
        'price': '3/2',
        'image': 'https://media.timeout.com/images/105239244/image.jpg',
        'maps_link': 'https://goo.gl/maps/zvxdLQ5eT4F2'
    },
    {
        'name': 'Ivy in the Park',
        'service': '3/4',
        'food': '6.4/8',
        'atmosphere': '7.5/7.5',
        'price': '8/8',
        'image': 'https://media.timeout.com/images/105239245/image.jpg',
        'maps_link': 'https://goo.gl/maps/7PRRpdkXNGQ2'
    }
]

# Create DataFrame
df = pd.DataFrame(data)

# Calculate statistics
def parse_ratings(rating_str):
    his, mine = rating_str.split('/')
    return float(his) if his != '-' else np.nan, float(mine) if mine != '-' else np.nan

df[['service_his', 'service_mine']] = df['service'].apply(lambda x: pd.Series(parse_ratings(x)))
df[['food_his', 'food_mine']] = df['food'].apply(lambda x: pd.Series(parse_ratings(x)))
df[['atmosphere_his', 'atmosphere_mine']] = df['atmosphere'].apply(lambda x: pd.Series(parse_ratings(x)))
df[['price_his', 'price_mine']] = df['price'].apply(lambda x: pd.Series(parse_ratings(x)))

# Average ratings per category
avg_service_his = df['service_his'].mean()
avg_service_mine = df['service_mine'].mean()
avg_food_his = df['food_his'].mean()
avg_food_mine = df['food_mine'].mean()
avg_atmosphere_his = df['atmosphere_his'].mean()
avg_atmosphere_mine = df['atmosphere_mine'].mean()
avg_price_his = df['price_his'].mean()
avg_price_mine = df['price_mine'].mean()

# Best overall restaurant
df['overall_his'] = df[['service_his', 'food_his', 'atmosphere_his', 'price_his']].mean(axis=1)
df['overall_mine'] = df[['service_mine', 'food_mine', 'atmosphere_mine', 'price_mine']].mean(axis=1)
best_overall = df.loc[df[['overall_his', 'overall_mine']].mean(axis=1).idxmax()]

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Restaurant Ratings Dashboard'

# Graphs
avg_ratings_df = pd.DataFrame({
    'Category': ['Service', 'Food', 'Atmosphere', 'Price'],
    'His Average': [avg_service_his, avg_food_his, avg_atmosphere_his, avg_price_his],
    'My Average': [avg_service_mine, avg_food_mine, avg_atmosphere_mine, avg_price_mine]
})

fig_avg_ratings = px.bar(avg_ratings_df, x='Category', y=['His Average', 'My Average'],
                         barmode='group', title='Average Ratings per Category',
                         labels={'value': 'Average Rating', 'Category': 'Category'},
                         color_discrete_map={'His Average': '#0067A5', 'My Average': '#FFD700'})

best_overall_ratings_df = df[['name', 'overall_his', 'overall_mine']]
fig_best_overall = px.bar(best_overall_ratings_df, x='name', y=['overall_his', 'overall_mine'],
                          barmode='group', title='Overall Ratings per Restaurant',
                          labels={'value': 'Overall Rating', 'name': 'Restaurant'},
                          color_discrete_map={'overall_his': '#0067A5', 'overall_mine': '#FFD700'})

# App layout
app.layout = html.Div([
    dbc.Container([
        html.H1('Our Restaurant Ratings', className='text-center my-4', style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.A([
                        html.Img(src=row['image'], className='img-fluid', style={'border-radius': '10px', 'margin-bottom': '10px', 'height': '200px', 'width': '100%', 'object-fit': 'cover'}),
                    ], href=row['maps_link'], target='_blank'),
                    html.H4(row['name'], className='my-2', style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}),
                    html.Div([
                        html.P('Service:', style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.Span('★' * int(row['service_his']) if not np.isnan(row['service_his']) else '', style={'color': '#FFD700', 'margin-right': '5px'}),
                        html.Span('★' * int(row['service_mine']) if not np.isnan(row['service_mine']) else '', style={'color': '#0067A5'})
                    ], style={'margin-bottom': '5px'}),
                    html.Div([
                        html.P('Food:', style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.Span('★' * int(row['food_his']) if not np.isnan(row['food_his']) else '', style={'color': '#FFD700', 'margin-right': '5px'}),
                        html.Span('★' * int(row['food_mine']) if not np.isnan(row['food_mine']) else '', style={'color': '#0067A5'})
                    ], style={'margin-bottom': '5px'}),
                    html.Div([
                        html.P('Atmosphere:', style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.Span('★' * int(row['atmosphere_his']) if not np.isnan(row['atmosphere_his']) else '', style={'color': '#FFD700', 'margin-right': '5px'}),
                        html.Span('★' * int(row['atmosphere_mine']) if not np.isnan(row['atmosphere_mine']) else '', style={'color': '#0067A5'})
                    ], style={'margin-bottom': '5px'}),
                    html.Div([
                        html.P('Price:', style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.Span('★' * int(row['price_his']) if not np.isnan(row['price_his']) else '', style={'color': '#FFD700', 'margin-right': '5px'}),
                        html.Span('★' * int(row['price_mine']) if not np.isnan(row['price_mine']) else '', style={'color': '#0067A5'})
                    ], style={'margin-bottom': '5px'}),
                ], className='restaurant-block text-center p-3', style={'background-color': '#f9f9f9', 'border-radius': '15px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-bottom': '20px'})
            ], md=4, xs=12)
            for _, row in df.iterrows()
        ]),
        dbc.Container([
            html.H3('Statistics', className='my-4', style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}),
            html.P(f'Best Overall Restaurant: {best_overall["name"]}', style={'font-weight': 'bold'}),
            html.P(f"His Favorite: {df.loc[df['overall_his'].idxmax()]['name']}", style={'font-weight': 'bold'}),
            html.P(f"My Favorite: {df.loc[df['overall_mine'].idxmax()]['name']}", style={'font-weight': 'bold'}),
            html.P(f'Average Service Rating - His: {avg_service_his:.1f}, Mine: {avg_service_mine:.1f}', style={'font-weight': 'bold'}),
            html.P(f'Average Food Rating - His: {avg_food_his:.1f}, Mine: {avg_food_mine:.1f}', style={'font-weight': 'bold'}),
            html.P(f'Average Atmosphere Rating - His: {avg_atmosphere_his:.1f}, Mine: {avg_atmosphere_mine:.1f}', style={'font-weight': 'bold'}),
            html.P(f'Average Price Rating - His: {avg_price_his:.1f}, Mine: {avg_price_mine:.1f}', style={'font-weight': 'bold'})
        ], className='statistics-block p-3', style={'background-color': '#ffffff', 'border-radius': '15px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-top': '30px'}),
        dbc.Container([
            dcc.Graph(figure=fig_avg_ratings),
            dcc.Graph(figure=fig_best_overall)
        ], className='graphs-block p-3', style={'background-color': '#ffffff', 'border-radius': '15px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-top': '30px'})
    ], fluid=True)
], style={'background-color': '#f0f0f5'})

# Run server
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
