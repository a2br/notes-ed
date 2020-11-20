import locale
import os
import sys

from rich import print
from rich.console import Console
from rich.table import Table
import inquirer

import ecoledirecte as ed

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
console = Console()


def calm_exit():
    console.input(password=True)
    exit()


def get_credentials():
    # Récupère le nom d'utilisateur
    username = ""
    usernamePath = sys.argv[0] + "\\..\\username.txt"
    if os.path.isfile(usernamePath):
        with open(usernamePath) as file:
            username = file.readline()
    if not username:
        username = console.input("Identifiant: ")
    else:
        print(f"Connexion en tant que [bold]{username}[/]")
    # Récupère le mot de passe
    password = console.input("Mot de passe: ", password=True)
    # Retourne les valeurs
    return username, password


# Crée un menu de sélection
def choose(message: str, choices: list):
    questions = [
        inquirer.List('a', message, choices)
    ]
    answer = inquirer.prompt(questions)['a']
    return answer

# Sélectionne ou demande le compte à retourner
def select_account(accounts: list):
    # Filtre les comptes de type E
    e_accounts = list(filter(lambda account: bool(
        account['typeCompte'] == "E"), accounts))
    # Met en page les choix
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
        # Pas de compte supporté
        print("[reverse bold red]Aucun compte compatible trouvé[/]")
        print("[red]Essayez de vous connecter avec un compte Elève.[/]")
        calm_exit()

    account = next(filter(lambda account: (
        str(account['id']) == choice[0:4]), e_accounts))
    return account

# Affiche la moyenne pour chaque période (et chaque matière)
def handle_notes(data):
    periodes = data['periodes']
    notes = data['notes']

    for periode in periodes:
        matieres = periode['ensembleMatieres']['disciplines']
        notes_list = []  # Liste des notes (=> calcul de la médiane)
        notes_periode = 0  # Somme des notes de la période
        diviseur_periode = 0  # Somme des coefficients
        infos_matieres = {}

        for matiere in matieres:
            notes_list_matiere = []
            notes_matiere = 0
            diviseur_matiere = 0
            notesM = list(filter(lambda note: (note['codePeriode'] == periode['idPeriode']) and
                                              (note['codeMatiere'] == matiere['codeMatiere']), notes))
            for note in notesM:
                try:
                    notes_matiere += (locale.atof(note['valeur']) / locale.atof(note['noteSur'])) * \
                        locale.atof(note['coef'])
                    diviseur_matiere += locale.atof(note['coef'])
                    notes_list.append(locale.atof(
                        note['valeur']) / locale.atof(note['noteSur']))
                    notes_list_matiere.append(locale.atof(
                        note['valeur']) / locale.atof(note['noteSur']))
                except:
                    pass

            moyenne_matiere = None
            notes_list_matiere.sort()

            if diviseur_matiere:
                moyenne_matiere = (notes_matiere / diviseur_matiere)
                notes_periode += moyenne_matiere * float(matiere['coef'])
                diviseur_periode += float(matiere['coef'])
            infos_matieres[matiere['codeMatiere']] = {
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

            for codeMatiere in infos_matieres:
                matiere = infos_matieres[codeMatiere]
                if codeMatiere:
                    table.add_row(codeMatiere, str(matiere['coef']),
                                  str(round(
                                      matiere['moyenne'] * 20, 1) if matiere['moyenne'] else None).zfill(4),
                                  str(round(
                                      matiere['mediane'] * 20, 1) if matiere['mediane'] else None).zfill(4),
                                  f"#{str(matiere['rang']).zfill(2)}")
            moyenne_periode = notes_periode / diviseur_periode
            table.add_row("GENERAL", "0", str(round(moyenne_periode * 20, 1)),
                          str(round((notes_list[round((len(notes_list) - 1) / 2)]) * 20, 2)), "#00", style='red')
            console.print(table)


def main():
    username, password = get_credentials()
    print("Connexion...")
    loginRes, token = ed.login(username, password)
    if not token:
        print(loginRes['message'])
        calm_exit()

    account = select_account(loginRes['data']['accounts'])
    print(f"[blue]Bonjour, [bold]{account['prenom']}[/].[/]")

    print("Collecte des notes...")
    notesRes, token = ed.fetch_notes(account, token)
    if notesRes['code'] != 200:
        print(notesRes['message'])
        calm_exit()
    print("Traitement des notes...")
    handle_notes(notesRes['data'])
    print("[reverse green]Terminé.[/] Pressez [reverse]ENTER[/] pour quitter.")
    calm_exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
