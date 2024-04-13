from dash import Dash, html, dcc, callback, Input, Output, State, dash_table
import pandas as pd
import dash

df = pd.read_csv('vgsales.csv')

game_title = ''

def initialize_game():
    global game_title

    random_game = df.sample()

    game_title = random_game.iloc[0]['Name']

    hints = [
        f"Le jeu a été publié en {random_game.iloc[0]['Year']}.",
        f"Le genre du jeu est {random_game.iloc[0]['Genre']}.",
        f"Le jeu a été développé pour la plateforme {random_game.iloc[0]['Platform']}.",
        f"Le jeu a été publié par {random_game.iloc[0]['Publisher']}.",
        f"Les ventes globales du jeu sont {random_game.iloc[0]['Global_Sales']} millions de copies."
    ]

    return hints

def generate_hint(attempts):
    global game_title
    if attempts == 1:
        return f"Indice 1: {hints[0]}"
    elif attempts > len(hints):
        return f"Désolé, vous avez utilisé tous vos essais. Le jeu était {game_title}."
    else:
        return f"Indice {attempts}: {hints[attempts - 1]}"

app = Dash(__name__)

provided_hints = []

score = 0

attempts = 1

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
        html.Div(id='score-output', children=f"Score: {score}"),
        html.Div([
            html.Div("Note: Le jeu n'affine pas les résultats de la recherche. Veuillez taper le nom du jeu exact pour le deviner. Si vous voulez voud aider, lancer la base de données de jeux vidéo. Chaque indice donné correspond à un filtre de la base de données. Bonne chance !", style={'background-color': '#f8d7da', 'border': '1px solid #f5c6cb', 'color': '#721c24', 'padding': '10px', 'border-radius': '5px', 'margin-bottom': '10px'}),
            html.Div("PS : Pour voir la base de données de jeux vidéo, veuillez lancer le fichier app.py.", style={'background-color': '#d4edda', 'border': '1px solid #c3e6cb', 'color': '#155724', 'padding': '10px', 'border-radius': '5px'})
        ], style={'margin-top': '20px'})
    ])
])

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
            attempts = 1
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
                attempts += 1 
                return hint_table, "", {'display': 'block'}, f"Score: {score}"
    return "", "", {'display': 'none'}, f"Score: {score}"

if __name__ == '__main__':
    hints = initialize_game()
    app.run_server(debug=True, port=8080)
