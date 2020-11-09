#
# Par Anatole DEBIERRE
#

# Le code n'est pas achevé.

import sys
from getpass import getpass

from requests import request as req
from rich import print
import inquirer


def choose(message: str, choices: list):
    questions = [
        inquirer.List('a', message, choices)
    ]
    answer = inquirer.prompt(questions)['a']
    return answer


def login(username: str, password: str, token: str = None):
    payload = 'data={ "identifiant": "'+username + \
        '", "motdepasse": "'+password+'" }'
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
        exit()


def select_account(accounts: list):
    # Définit les comptes de type E
    e_accounts = list(filter(lambda account: bool(
        account['typeCompte'] == "E"), accounts))
    # Met en page les futurs choix
    choices = list(
        map(lambda account: (str(account['id']) + " | " + account['prenom'] + " " + account['nom']),
            e_accounts))
    # Choix automatique
    choice = None
    if len(choices) > 1:
        choice = choose("Sélectionnez un compte disponible: ", choices=choices)
    elif len(choices) < 1:
        choice = None
    elif len(choices) == 1:
        choice = choices[0]
    if not choice:
        print("[reverse bold red]Aucun compte ne semble disponible[/]")
        if next(filter(lambda account: account['typeCompte'] == "1", accounts), None):
            print("[red]Le compte connecté semble être un compte Famille. " +
                  "Essayez de vous connecter avec un compte Elève ![/]")
        exit()

    account = next(filter(lambda account: (
        str(account['id']) == choice[0:4]), e_accounts))
    return account


def fetch_notes(account, token: str):
    payload = 'data={"token": "' + token + '"}'
    response = req("POST", "https://api.ecoledirecte.com/v3/eleves/" +
                   str(account['id']) + "/notes.awp?verbe=get&", data=payload).json()
    token = response['token'] or token
    return response, token


def handle_notes(data):
    matieres = []
    for periode in data['periodes']:
        for matiere in periode['ensembleMatieres']['disciplines']:
            if not matieres.index(matiere['codeMatiere']):
                matieres.append(matiere['codeMatiere'])
    return matieres


def main():
    username = input("Identifiant: ")
    password = getpass("Mot de passe: ")
    print("Connexion...")
    loginRes, token = login(username, password)
    if not token:
        print(loginRes['message'])
        exit()

    account = select_account(loginRes['data']['accounts'])
    print(f"[blue]Bonjour, [bold]{account['prenom']}[/].[/]")

    print("Collecte des notes...")
    notesRes, token = fetch_notes(account, token)
    if notesRes['code'] != 200:
        print(notesRes['message'])
        exit()
    print("Traitement des notes...")
    handle_notes(notesRes['data'])
    print("~END~")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
