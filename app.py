import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
import os

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
        'image': 'https://www.thegoodfoodguide.co.uk/images/restaurant/210312_1864612_Interior%201[xya:1360x680].jpg',
        'maps_link': 'https://www.adelinayard.com/'
    },
    {
        'name': 'Pasture',
        'service': '6.8/7.5',
        'food': '6/7',
        'atmosphere': '4.5/4',
        'price': '7/6',
        'image': 'https://cdn.sanity.io/images/90b5g4ze/production/b6b00f5153dad28ae121aba2e3c2c74412ce40be-2000x1009.jpg?w=1300&h=656&auto=format',
        'maps_link': 'https://pasturerestaurant.com/locations/pasture-bristol/'
    },
    {
        'name': 'Marceline',
        'service': '8/9',
        'food': '8/9',
        'atmosphere': '8/7',
        'price': '8/8',
        'image': 'https://canarywharf.com/wp-content/uploads/2024/05/PS-1.jpg',
        'maps_link': 'http://www.marceline.london/'
    },
    {
        'name': 'Cheeky Scones',
        'service': '-/-',
        'food': '7/8',
        'atmosphere': '3/6',
        'price': '9/7',
        'image': 'https://images.squarespace-cdn.com/content/v1/63ef654b857ef246af30b0de/ce9a1da7-dcfb-41bb-87ba-64c0238e42cb/tempImageA76mKj.jpg',
        'maps_link': 'https://www.cheekyscone.com/'
    },
    {
        'name': 'Da Corradi',
        'service': '6/7',
        'food': '2/3',
        'atmosphere': '8/9',
        'price': '3/2',
        'image': 'https://dacorradi.com/wp-content/uploads/2024/04/285160934_314266920895185_6708643095931781791_n-1.jpg',
        'maps_link': 'http://www.dacorradi.com/'
    },
    {
        'name': 'Ivy in the Park',
        'service': '3/4',
        'food': '6.4/8',
        'atmosphere': '7.5/7.5',
        'price': '8/8',
        'image': 'https://lh3.googleusercontent.com/p/AF1QipPHY2EA14ryyS3XS_IyScuVJbDxM0wja-Pb1HJp=s680-w680-h510',
        'maps_link': 'https://ivycollection.com/restaurants/the-ivy-in-the-park/?utm_source=LocalGoogle&utm_medium=Organic'
    }
]

# Create DataFrame
df = pd.DataFrame(data)

# Calculate statistics
def parse_ratings(rating_str):
    his, her = rating_str.split('/')
    return float(his) if his != '-' else np.nan, float(her) if her != '-' else np.nan

df[['service_his', 'service_her']] = df['service'].apply(lambda x: pd.Series(parse_ratings(x)))
df[['food_his', 'food_her']] = df['food'].apply(lambda x: pd.Series(parse_ratings(x)))
df[['atmosphere_his', 'atmosphere_her']] = df['atmosphere'].apply(lambda x: pd.Series(parse_ratings(x)))
df[['price_his', 'price_her']] = df['price'].apply(lambda x: pd.Series(parse_ratings(x)))

# Average ratings per category
avg_service_his = df['service_his'].mean()
avg_service_her = df['service_her'].mean()
avg_food_his = df['food_his'].mean()
avg_food_her = df['food_her'].mean()
avg_atmosphere_his = df['atmosphere_his'].mean()
avg_atmosphere_her = df['atmosphere_her'].mean()
avg_price_his = df['price_his'].mean()
avg_price_her = df['price_her'].mean()

# Best overall restaurant
df['overall_his'] = df[['service_his', 'food_his', 'atmosphere_his', 'price_his']].mean(axis=1)
df['overall_her'] = df[['service_her', 'food_her', 'atmosphere_her', 'price_her']].mean(axis=1)
best_overall = df.loc[df[['overall_his', 'overall_her']].mean(axis=1).idxmax()]


# Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = 'Restaurant Ratings Dashboard'

# Timer component for the "Next Visit" tab
next_visit_date = datetime(2024, 10, 30, 23, 45)  # Set your next visit date here

# Graphs
avg_ratings_df = pd.DataFrame({
    'Category': ['Service', 'Food', 'Atmosphere', 'Price'],
    'His Average': [avg_service_his, avg_food_his, avg_atmosphere_his, avg_price_his],
    'Her Average': [avg_service_her, avg_food_her, avg_atmosphere_her, avg_price_her]
})

fig_avg_ratings = px.bar(avg_ratings_df, x='Category', y=['His Average', 'Her Average'],
                         barmode='group', title='Average Ratings per Category',
                         labels={'value': 'Average Rating', 'Category': 'Category'},
                         color_discrete_map={'His Average': '#0067A5', 'Her Average': '#FFD700'})

best_overall_ratings_df = df[['name', 'overall_his', 'overall_her']]
fig_best_overall = px.bar(best_overall_ratings_df, x='name', y=['overall_his', 'overall_her'],
                          barmode='group', title='Overall Ratings per Restaurant',
                          labels={'value': 'Overall Rating', 'name': 'Restaurant'},
                          color_discrete_map={'overall_his': '#0067A5', 'overall_her': '#FFD700'})

# App layout
ratings_layout = html.Div([
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
                        html.Span('★' * int(row['service_her']) if not np.isnan(row['service_her']) else '', style={'color': '#0067A5'})
                    ], style={'margin-bottom': '5px'}),
                    html.Div([
                        html.P('Food:', style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.Span('★' * int(row['food_his']) if not np.isnan(row['food_his']) else '', style={'color': '#FFD700', 'margin-right': '5px'}),
                        html.Span('★' * int(row['food_her']) if not np.isnan(row['food_her']) else '', style={'color': '#0067A5'})
                    ], style={'margin-bottom': '5px'}),
                    html.Div([
                        html.P('Atmosphere:', style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.Span('★' * int(row['atmosphere_his']) if not np.isnan(row['atmosphere_his']) else '', style={'color': '#FFD700', 'margin-right': '5px'}),
                        html.Span('★' * int(row['atmosphere_her']) if not np.isnan(row['atmosphere_her']) else '', style={'color': '#0067A5'})
                    ], style={'margin-bottom': '5px'}),
                    html.Div([
                        html.P('Price:', style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.Span('★' * int(row['price_his']) if not np.isnan(row['price_his']) else '', style={'color': '#FFD700', 'margin-right': '5px'}),
                        html.Span('★' * int(row['price_her']) if not np.isnan(row['price_her']) else '', style={'color': '#0067A5'})
                    ], style={'margin-bottom': '5px'}),
                ], className='restaurant-block text-center p-3', style={'background-color': '#f9f9f9', 'border-radius': '15px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-bottom': '20px'})
            ], md=4, xs=12)
            for _, row in df.iterrows()
        ]),
        dbc.Container([
            html.H3('Statistics', className='my-4', style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold'}),
            html.P(f'Best Overall Restaurant: {best_overall["name"]}', style={'font-weight': 'bold'}),
            html.P(f"His Favorite: {df.loc[df['overall_his'].idxmax()]['name']}", style={'font-weight': 'bold'}),
            html.P(f"Her Favorite: {df.loc[df['overall_her'].idxmax()]['name']}", style={'font-weight': 'bold'}),
            html.P(f'Average Service Rating - His: {avg_service_his:.1f}, Her: {avg_service_her:.1f}', style={'font-weight': 'bold'}),
            html.P(f'Average Food Rating - His: {avg_food_his:.1f}, Her: {avg_food_her:.1f}', style={'font-weight': 'bold'}),
            html.P(f'Average Atmosphere Rating - His: {avg_atmosphere_his:.1f}, Her: {avg_atmosphere_her:.1f}', style={'font-weight': 'bold'}),
            html.P(f'Average Price Rating - His: {avg_price_his:.1f}, Her: {avg_price_her:.1f}', style={'font-weight': 'bold'})
        ], className='statistics-block p-3', style={'background-color': '#ffffff', 'border-radius': '15px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-top': '30px'}),
        dbc.Container([
            dcc.Graph(figure=fig_avg_ratings),
            dcc.Graph(figure=fig_best_overall)
        ], className='graphs-block p-3', style={'background-color': '#ffffff', 'border-radius': '15px', 'box-shadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'margin-top': '30px'})
    ], fluid=True)
], style={'background-color': '#f0f0f5'})

# Layout for "Next Visit" page
next_visit_layout = html.Div([
    html.H1("🇮🇹 ❤️ Countdown to Next Visit ❤️ 🇮🇹", className='text-center my-4', style={'font-family': 'Arial, sans-serif', 'font-weight': 'bold', 'color': '#ff6347'}),
    html.Div(id='countdown', className='text-center', style={'font-size': '60px', 'font-weight': 'bold', 'margin-top': '20px', 'color': '#ff4500'}),
    html.H3("Bologna", className='text-center my-4', style={'font-family': 'Comic Sans MS, cursive', 'font-weight': 'bold', 'color': '#ff6347'}),
    html.Div(style={
        'background-image': 'url(https://www.tasteatlas.com/images/dishes/53133d5e91f847c39d0b63f27340b712/bologna.jpg)',
        'background-size': 'cover',
        'background-position': 'center',
        'position': 'absolute',
        'top': '0',
        'left': '0',
        'right': '0',
        'bottom': '0',
        'z-index': '-1',
        'opacity': '0.2'
    })
], style={'background-color': '#f0f0f5', 'height': '100vh', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center', 'position': 'relative'})

# Tabs for navigation
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='ratings', children=[
        dcc.Tab(label='Our Ratings Dashboard', value='ratings'),
        dcc.Tab(label='Next Visit', value='next_visit'),
    ]),
    html.Div(id='tabs-content')
])

# Callback to switch between tabs
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_tab_content(tab):
    if tab == 'ratings':
        return ratings_layout
    elif tab == 'next_visit':
        return next_visit_layout

# Callback to update the countdown timer
@app.callback(
    Output('countdown', 'children'),
    [Input('tabs', 'value')]
)
def update_countdown(tab):
    if tab == 'next_visit':
        time_remaining = next_visit_date - datetime.now()
        days, remainder = divmod(time_remaining.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(days)}d {int(hours)}h {int(minutes)}m"
    return ""


# Run server

if __name__ == '__main__':
    app.run_server(debug=True, port=int(os.environ.get("PORT", 8050)), host='0.0.0.0')
