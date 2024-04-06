# Import des packages
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import pandas as pd

# Chargement du jeu de données
df = pd.read_csv('vgsales.csv')

# Convertir la colonne "Year" en type numérique
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Exclure les lignes avec des années manquantes
df = df.dropna(subset=['Year'])

# Options pour la liste déroulante des années
year_options = [{'label': str(int(year)), 'value': int(year)} for year in sorted(df['Year'].unique())]

# Options pour la liste déroulante des éditeurs
publisher_options = [{'label': str(publisher), 'value': str(publisher)} for publisher in sorted(df['Publisher'].dropna().unique())]

# Options pour la liste déroulante des genres
genre_options = [{'label': genre, 'value': genre} for genre in sorted(df['Genre'].dropna().unique())]

# Options pour la liste déroulante des plateformes
platform_options = [{'label': platform, 'value': platform} for platform in sorted(df['Platform'].dropna().unique())]

# Initialisation de l'application Dash
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('Analyse des ventes de jeux vidéo'),
    dcc.Input(id='search-name', type='text', placeholder='Rechercher par nom...'),
    dcc.Dropdown(id='filter-year', options=year_options, placeholder='Filtrer par année...'),
    dcc.Dropdown(id='filter-publisher', options=publisher_options, placeholder='Filtrer par éditeur...'),
    dcc.Dropdown(id='filter-genre', options=genre_options, placeholder='Filtrer par genre...'),
    dcc.Dropdown(id='filter-platform', options=platform_options, placeholder='Filtrer par plateforme...'),
    dash_table.DataTable(id='filtered-data', columns=[{"name": i, "id": i} for i in df.columns], page_size=10)
])

# Callback pour mettre à jour les données en fonction des filtres
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
    
    # Filtre par nom
    if search_name:
        filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]
    
    # Filtre par année
    if filter_year:
        filtered_df = filtered_df[filtered_df['Year'] == filter_year]
    
    # Filtre par éditeur
    if filter_publisher:
        filtered_df = filtered_df[filtered_df['Publisher'] == filter_publisher]
    
    # Filtre par genre
    if filter_genre:
        filtered_df = filtered_df[filtered_df['Genre'] == filter_genre]
    
    # Filtre par plateforme
    if filter_platform:
        filtered_df = filtered_df[filtered_df['Platform'] == filter_platform]
    
    return filtered_df.to_dict('records')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
