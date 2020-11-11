from getpass import getpass
import locale

from requests import request as req
from rich import print
from rich.console import Console
from rich.table import Table
import inquirer

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
console = Console()

# Crée un menu de sélection
def choose(message: str, choices: list):
    questions = [
        inquirer.List('a', message, choices)
    ]
    answer = inquirer.prompt(questions)['a']
    return answer

# Se connecte
def login(username: str, password: str, token: str = None):
    payload = 'data={ "identifiant": "'+username + \
        '", "motdepasse": "'+password+'", "acceptationCharte": true }'
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

# Sélectionne ou demande le compte à retourner
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

# Récupère les notes
def fetch_notes(account, token: str):
    payload = 'data={"token": "' + token + '"}'
    response = req("POST", "https://api.ecoledirecte.com/v3/eleves/" +
                   str(account['id']) + "/notes.awp?verbe=get&", data=payload).json()
    token = response['token'] or token
    return response, token

# Affiche la moyenne pour chaque période (et chaque matière)
def handle_notes(data):
    periodes = data['periodes']
    notes = data['notes']

    for periode in periodes:
        matieres = periode['ensembleMatieres']['disciplines']
        notes_list = []
        notes_periode = 0
        diviseur_periode = 0
        moyenne_matieres = {}

        for matiere in matieres:
            notes_list_matiere = []
            notes_matiere = 0
            diviseur_matiere = 0
            # Chercher des notes de MATIERE dans PERIODE
            notesM = list(filter(lambda note: (note['codePeriode'] == periode['idPeriode']) and
                                              (note['codeMatiere'] == matiere['codeMatiere']), notes))
            for note in notesM:
                try:
                    notes_matiere += (locale.atof(note['valeur']) / locale.atof(note['noteSur'])) * \
                                     locale.atof(note['coef'])
                    diviseur_matiere += locale.atof(note['coef'])
                    notes_list.append(locale.atof(note['valeur']) / locale.atof(note['noteSur']))
                    notes_list_matiere.append(locale.atof(note['valeur']) / locale.atof(note['noteSur']))
                except:
                    pass

            moyenne_matiere = None
            notes_list_matiere.sort()

            if diviseur_matiere:
                moyenne_matiere = (notes_matiere / diviseur_matiere)
                notes_periode += moyenne_matiere * float(matiere['coef'])
                diviseur_periode += float(matiere['coef'])
            moyenne_matieres[matiere['codeMatiere']] = {
                'moyenne': moyenne_matiere if diviseur_matiere else None,
                'mediane': notes_list_matiere[round((len(notes_list_matiere) - 1) / 2)] if notes_list_matiere else None,
                'rang': matiere['rang'],
                'coef': matiere['coef']
            }

        notes_list.sort()

        if diviseur_periode:
            # Création du tableau
            table = Table(title=periode['periode'])
            table.add_column("Matière", style='cyan', justify='left')
            table.add_column("Coef", style='white', justify='center')
            table.add_column("Moyenne", style='magenta', justify='center')
            table.add_column("Médiane", style='hot_pink', justify='center')
            table.add_column("Rang", style='green', justify='right')

            for codeMatiere in moyenne_matieres:
                matiere = moyenne_matieres[codeMatiere]
                if codeMatiere:
                    table.add_row(codeMatiere, str(matiere['coef']),
                                  str(round(matiere['moyenne']*20, 1) if matiere['moyenne'] else None).zfill(4),
                                  str(round(matiere['mediane'] * 20, 1) if matiere['mediane'] else None).zfill(4),
                                  f"#{str(matiere['rang']).zfill(2)}")
            moyenne_periode = notes_periode / diviseur_periode
            # print(f"{periode['periode']} : {moyenne_periode * 20}/20")
            table.add_row("GENERAL", "0", str(round(moyenne_periode*20, 1)),
                          str(round((notes_list[round((len(notes_list) - 1) / 2)]) * 20, 2)), "#00", style='red')
            console.print(table)


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
    print("Terminé.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
