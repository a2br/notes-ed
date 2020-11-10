# notes-ed
Ce programme vous permettra de récupérer des informations sur vos notes et de calculer votre moyenne, avec une simple 
connexion à EcoleDirecte.

## Téléchargement

### Pré-requis
Vous devez avoir Python 3 installé ainsi que pip (installé en même temps que Python).
### Installation
La méthode habituelle.

```console
$ git clone https://github.com/a2br/notes-ed.git
$ cd ./notes-ed
```

Une fois le repo installé et une fois que vous êtes dedans, installez les modules requis.

```console
$ py -m pip install -r .\requirements.txt
```
### Mettre à jour
Pour mettre votre clone à jour,
```console
$ git pull
```

## Utilisation

Le script ne marche qu'avec les comptes `E` (Eleve). Les comptes familles ne sont pas supportés.
```console
$ py ./main.py
Identifiant: 
Mot de passe: 
```
![Démo](https://i.ibb.co/6rn35q2/notes-ed-demo.gif)

### Valeurs montrées
Le script, pour chaque matière (et la section générale), montrera :
- le code de la matière
- le coefficient de la matière
- la moyenne (arithmétique pondérée), la même qui figurera dans le bulletin
- la note médiane : vous avez autant de notes plus hautes et plus basses qu'elle
- le rang par rapport au reste de la classe : une valeur qui n'est pas affichée par EcoleDirecte. Si `#00`, le rang est inconnu ou incalculable
