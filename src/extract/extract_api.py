import requests
from sqlAlchemy import createengine


def extract():
    api_football = ['https://v3.football.api-sports.io//fixtures/rounds?league=39&season=2024',
    'https://v3.football.api-sports.io/fixtures?league=39&season=2024&round=Regular Season - 1',
    'https://v3.football.api-sports.io/teams?league=39&season=2024',
    'https://v3.football.api-sports.io/players?team=40&season=2024',
    ]

    api_football_data_org = ['https://api.football-data.org/v4/competitions/PL', #Enumere uma competição específica.
    'https://api.football-data.org//v4/competitions/PL/standings?season=2025',#Visualizar a classificação de uma competição específica.
    'https://api.football-data.org//v4/competitions/PL/matches?season=2025', #Liste todas as partidas de uma determinada competição.
    'https://api.football-data.org//v4/competitions/PL/teams?season=2025', #Liste todas as equipas para uma determinada competição.
    'https://api.football-data.org/v4/competitions/PL/scorers?season=2025' #Enumera os melhores pontuadores de uma determinada competição.
    'https://api.football-data.org/v4/teams/4' # Listar equipas - jogadores ex: equipa com id 4
    'https://api.football-data.org/v4/teams/4/matches/', # Mostrar todas as partidas de uma determinada equipa
    ] 


site1 = 'https://www.api-football.com/?utm_source=chatgpt.com'
site2 = 'https://www.football-data.org/?utm_source=chatgpt.com'

api_key_header1 = 'x-apisports-key'
api_key_value1  = '1ccafb22044efb5d6aa2c2a6701a6f84'

api_key_header2 = 'X-Auth-Token'
api_key_value2  = '5728f032d1cd4fa7a6b4023e65389267'