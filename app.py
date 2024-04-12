from dash import Dash, html, dcc, callback, Output, Input, dash_table
import pandas as pd
import plotly.express as px
import os
from flask import send_file

df = pd.read_csv('vgsales.csv')

df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Year'])

year_options = [{'label': str(int(year)), 'value': int(year)} for year in sorted(df['Year'].unique())]
publisher_options = [{'label': str(publisher), 'value': str(publisher)} for publisher in sorted(df['Publisher'].dropna().unique())]
genre_options = [{'label': genre, 'value': genre} for genre in sorted(df['Genre'].dropna().unique())]
platform_options = [{'label': platform, 'value': platform} for platform in sorted(df['Platform'].dropna().unique())]

app = Dash(__name__)

num_games = len(df)

app.layout = html.Div([
    html.Div([
        html.H1('Game Database Analyser', style={'textAlign': 'center', 'color': '#F400A1', 'fontFamily': 'Roboto'}),
        html.A(html.Button('Télécharger le PDF', id='download-pdf', n_clicks=0), href='/download-pdf'),
    ]),
    html.Div([
        html.P(f'Nombre de jeux dans la base de données : {num_games}', style={'textAlign': 'center'}),
        html.P(f'les ventes globales sont les copies vendues', style={'textAlign': 'center'})
    ]),
    dcc.Input(id='search-name', type='text', placeholder='Rechercher par nom...'),
    dcc.Dropdown(id='filter-year', options=year_options, placeholder='Filtrer par année...'),
    dcc.Dropdown(id='filter-publisher', options=publisher_options, placeholder='Filtrer par éditeur...'),
    dcc.Dropdown(id='filter-genre', options=genre_options, placeholder='Filtrer par genre...'),
    dcc.Dropdown(id='filter-platform', options=platform_options, placeholder='Filtrer par plateforme...'),
    dash_table.DataTable(id='filtered-data', columns=[{"name": i, "id": i} for i in df.columns], page_size=10),
    dcc.Graph(id='sales-pie-chart'),
    dcc.Graph(id='publisher-sales-bar-chart'), 
    dcc.Graph(id='platform-sales-bar-chart'),
    dcc.Graph(id='year-sales-bar-chart'),
    dcc.Graph(id='genre-sales-pie-chart'),
    html.Footer('Copyright © 2024 Game Database Analyser. All rights reserved.', style={'textAlign': 'center'})
])



@app.callback(
    Output('filtered-data', 'data'),
    Input('search-name', 'value'),
    Input('filter-year', 'value'),
    Input('filter-publisher', 'value'),
    Input('filter-genre', 'value'),
    Input('filter-platform', 'value')
)
def update_data(search_name, filter_year, filter_publisher, filter_genre, filter_platform):
    filtered_df = df
    
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]
    
    if filter_year:
        filtered_df = filtered_df[filtered_df['Year'] == filter_year]
    
    if filter_publisher:
        filtered_df = filtered_df[filtered_df['Publisher'] == filter_publisher]
    
    if filter_genre:
        filtered_df = filtered_df[filtered_df['Genre'] == filter_genre]
    
    if filter_platform:
        filtered_df = filtered_df[filtered_df['Platform'] == filter_platform]
    
    return filtered_df.to_dict('records')

@app.callback(
    Output('sales-pie-chart', 'figure'),
    Input('search-name', 'value'),
    Input('filter-year', 'value'),
    Input('filter-publisher', 'value'),
    Input('filter-genre', 'value'),
    Input('filter-platform', 'value')
)
def update_pie_chart(search_name, filter_year, filter_publisher, filter_genre, filter_platform):
    filtered_df = df
    
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]
    if filter_year:
        filtered_df = filtered_df[filtered_df['Year'] == filter_year]
    if filter_publisher:
        filtered_df = filtered_df[filtered_df['Publisher'] == filter_publisher]
    if filter_genre:
        filtered_df = filtered_df[filtered_df['Genre'] == filter_genre]
    if filter_platform:
        filtered_df = filtered_df[filtered_df['Platform'] == filter_platform]
    
    area_sales = filtered_df[['NA_Sales','EU_Sales', 'JP_Sales', 'Other_Sales']]
    area_sales = area_sales.sum()
    
    fig = px.pie(values=area_sales.values, names=area_sales.index, title='Ventes par région')
    
    return fig

@app.callback(
    Output('publisher-sales-bar-chart', 'figure'),
    Input('search-name', 'value'),
    Input('filter-year', 'value'),
    Input('filter-publisher', 'value'),
    Input('filter-genre', 'value'),
    Input('filter-platform', 'value')
)
def update_publisher_sales_bar_chart(search_name, filter_year, filter_publisher, filter_genre, filter_platform):
    filtered_df = df
    
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]
    if filter_year:
        filtered_df = filtered_df[filtered_df['Year'] == filter_year]
    if filter_publisher:
        filtered_df = filtered_df[filtered_df['Publisher'] == filter_publisher]
    if filter_genre:
        filtered_df = filtered_df[filtered_df['Genre'] == filter_genre]
    if filter_platform:
        filtered_df = filtered_df[filtered_df['Platform'] == filter_platform]
    
    publisher_sales = filtered_df.groupby('Publisher')['Global_Sales'].sum().reset_index()
    publisher_sales = publisher_sales.sort_values(by='Global_Sales', ascending=False).head(10)
    
    fig = px.bar(publisher_sales, x='Global_Sales', y='Publisher', title='Ventes globales par éditeur (Top 10)', orientation='h', color='Global_Sales', color_continuous_scale='Plotly3')

    
    return fig

@app.callback(
    Output('platform-sales-bar-chart', 'figure'),
    Input('search-name', 'value'),
    Input('filter-year', 'value'),
    Input('filter-publisher', 'value'),
    Input('filter-genre', 'value'),
    Input('filter-platform', 'value')
)
def update_platform_sales_bar_chart(search_name, filter_year, filter_publisher, filter_genre, filter_platform):
    filtered_df = df
    
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]
    if filter_year:
        filtered_df = filtered_df[filtered_df['Year'] == filter_year]
    if filter_publisher:
        filtered_df = filtered_df[filtered_df['Publisher'] == filter_publisher]
    if filter_genre:
        filtered_df = filtered_df[filtered_df['Genre'] == filter_genre]
    if filter_platform:
        filtered_df = filtered_df[filtered_df['Platform'] == filter_platform]
    
    platform_counts = filtered_df.groupby('Platform').size().reset_index(name='Count')
    platform_counts = platform_counts.sort_values(by='Count', ascending=False).head(10)
    
    fig = px.bar(platform_counts, x='Platform', y='Count', title='Nombre de jeux sortis par plateforme (Top 10)', color='Count', color_continuous_scale='Sunset')
    
    return fig


@app.callback(
    Output('year-sales-bar-chart', 'figure'),
    Input('search-name', 'value'),
    Input('filter-year', 'value'),
    Input('filter-publisher', 'value'),
    Input('filter-genre', 'value'),
    Input('filter-platform', 'value')
)
def update_year_sales_bar_chart(search_name, filter_year, filter_publisher, filter_genre, filter_platform):
    filtered_df = df
    
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]
    if filter_year:
        filtered_df = filtered_df[filtered_df['Year'] == filter_year]
    if filter_publisher:
        filtered_df = filtered_df[filtered_df['Publisher'] == filter_publisher]
    if filter_genre:
        filtered_df = filtered_df[filtered_df['Genre'] == filter_genre]
    if filter_platform:
        filtered_df = filtered_df[filtered_df['Platform'] == filter_platform]

    year_sales = filtered_df.groupby('Year')['Global_Sales'].sum().reset_index()
    year_sales = year_sales.sort_values(by='Year')

    fig = px.bar(year_sales, x='Year', y='Global_Sales', title='Ventes globales par année', color='Global_Sales', color_continuous_scale='Magenta')

    return fig

@app.callback(
    Output('genre-sales-pie-chart', 'figure'),
    Input('search-name', 'value'),
    Input('filter-year', 'value'),
    Input('filter-publisher', 'value'),
    Input('filter-genre', 'value'),
    Input('filter-platform', 'value')
)

def update_genre_sales_pie_chart(search_name, filter_year, filter_publisher, filter_genre, filter_platform):
    filtered_df = df
    
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]
    if filter_year:
        filtered_df = filtered_df[filtered_df['Year'] == filter_year]
    if filter_publisher:
        filtered_df = filtered_df[filtered_df['Publisher'] == filter_publisher]
    if filter_genre:
        filtered_df = filtered_df[filtered_df['Genre'] == filter_genre]
    if filter_platform:
        filtered_df = filtered_df[filtered_df['Platform'] == filter_platform]

    genre_sales = filtered_df.groupby('Genre')['Global_Sales'].sum().reset_index()
    genre_sales = genre_sales.sort_values(by='Global_Sales', ascending=False)

    fig = px.pie(genre_sales, values='Global_Sales', names='Genre', title='Ventes globales par genre')

    return fig


@app.server.route('/download-pdf')
def download_pdf():
    pdf_path='Data_analyse.pdf'
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    else:
        return 'Fichier non trouvé'
    

if __name__ == '__main__':
    app.run_server(debug=True)
