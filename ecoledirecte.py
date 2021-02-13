from requests import request as req
from main import calm_exit
from rich import print

# Se connecte à EcoleDirecte
def login(username: str, password: str, token: str = None):
    payload = 'data={ "identifiant": "' + username + \
              '", "motdepasse": "' + password + '", "acceptationCharte": true }'
    try:
        response = req(
            "POST", "https://api.ecoledirecte.com/v3/login.awp", data=payload).json()
        token = response['token'] or token
        return response, token
    except Exception as exception:
        if type(exception).__name__ == "ConnectionError":
            print("[reverse bold red]La connexion a échoué[/]")
            print("[red]Vérifiez votre connexion Internet.[/]")
        else:
            print("[reverse bold red]Une erreur inconnue est survenue.[/]")
        calm_exit()


# Récupère les notes
def fetch_notes(account, token: str):
    payload = 'data={"token": "' + token + '"}'
    response = req("POST", "https://api.ecoledirecte.com/v3/eleves/" +
                   str(account['id']) + "/notes.awp?verbe=get&", data=payload).json()
    token = response['token'] or token
    return response, token
