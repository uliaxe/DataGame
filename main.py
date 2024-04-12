from dash import Dash, html, dcc, callback, Input, Output, State, dash_table
import pandas as pd
import dash

# Charger les données à partir du fichier CSV
df = pd.read_csv('vgsales.csv')

# Déclarer la variable game_title comme globale
game_title = ''

# Définir une fonction pour initialiser un nouveau jeu
def initialize_game():
    global game_title
    # Sélectionner un jeu aléatoire dans le dataset
    random_game = df.sample()

    # Titre du jeu à deviner
    game_title = random_game.iloc[0]['Name']

    # Indications initiales
    hints = [
        f"Le jeu a été publié en {random_game.iloc[0]['Year']}.",
        f"Le genre du jeu est {random_game.iloc[0]['Genre']}.",
        f"Le jeu a été développé pour la plateforme {random_game.iloc[0]['Platform']}.",
        f"Le jeu a été publié par {random_game.iloc[0]['Publisher']}.",
        f"Les ventes globales du jeu sont {random_game.iloc[0]['Global_Sales']} millions de copies."
    ]

    return hints

# Définir une fonction pour générer un nouvel indice
def generate_hint(attempts):
    global game_title
    if attempts == 1:
        return f"Indice 1: {hints[0]}"
    elif attempts > len(hints):
        return f"Désolé, vous avez utilisé tous vos essais. Le jeu était {game_title}."
    else:
        return f"Indice {attempts}: {hints[attempts - 1]}"

# Créer une application Dash
app = Dash(__name__)

# Stocker les indices fournis à l'utilisateur
provided_hints = []

# Initialiser le score
score = 0

# Initialiser le nombre d'essais
attempts = 1

# Mise en page de l'application
app.layout = html.Div(style={'textAlign': 'center'}, children=[
    html.Div(style={'margin': 'auto'}, children=[
        html.H1("Devinez le jeu vidéo !"),
        html.Div(id='hint-output'),
        dcc.Dropdown(
            id='user-input',
            options=[{'label': title, 'value': title} for title in df['Name']],
            placeholder="Sélectionnez ou tapez le nom du jeu...",
            style={'width': '50%', 'margin': 'auto'}
        ),
        html.Button('Soumettre', id='submit-button', n_clicks=0),
        html.Div(id='result-output', style={'display': 'none'}),
        html.Button('Recommencer', id='restart-button', n_clicks=0),
        html.Div(id='score-output', children=f"Score: {score}")
    ])
])

# Callback pour gérer le bouton de soumission et recommencer le jeu
@app.callback(
    [Output('hint-output', 'children'),
     Output('result-output', 'children'),
     Output('result-output', 'style'),
     Output('score-output', 'children')],
    [Input('submit-button', 'n_clicks'),
     Input('restart-button', 'n_clicks')],
    [State('user-input', 'value')]
)
def update_hint_and_result(submit_clicks, restart_clicks, user_input):
    global game_title, hints, provided_hints, score, attempts
    if dash.callback_context.triggered:
        trigger_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'restart-button':
            hints = initialize_game()
            provided_hints = []
            score = 0
            attempts = 1  # Réinitialiser le nombre d'essais à 1
            return "", "", {'display': 'none'}, f"Score: {score}"
        elif trigger_id == 'submit-button' and submit_clicks > 0:
            if isinstance(provided_hints, str) and "Félicitations" in provided_hints:
                hints = initialize_game()
                provided_hints = []
                score += 1
            if user_input.lower() == game_title.lower():
                return f"Félicitations ! Vous avez deviné le jeu correctement. Le jeu était bien {game_title}.", "", {'display': 'none'}, f"Score: {score}"
            else:
                hint = generate_hint(attempts)
                provided_hints.append(hint)
                hint_table = dash_table.DataTable(
                    columns=[{'name': 'Indices', 'id': 'index'}],
                    data=[{'index': hint} for hint in provided_hints],
                    style_cell={'textAlign': 'center'},
                    style_table={'margin': 'auto'}
                )
                attempts += 1  # Incrémenter le nombre d'essais
                return hint_table, "", {'display': 'block'}, f"Score: {score}"
    return "", "", {'display': 'none'}, f"Score: {score}"

# Exécuter l'application
if __name__ == '__main__':
    hints = initialize_game()
    app.run_server(debug=True, port=8080)
