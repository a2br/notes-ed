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

Le script ne marche qu'avec les comptes `E` (Eleve). Les comptes famille ne sont pas supportés. Ouvrez le script depuis le terminal ou en cliquant sur l'icône dans le File Explorer.
```console
$ py ./main.py
```
![Démo](https://i.ibb.co/c34xvYT/notes-ed-demo-2.gif)

#### Remplir automatiquement le nom d'utilisateur
Il y a une option pour vous éviter de toujours ré-entrer votre nom d'utilisateur. Pour l'utiliser, créez un fichier appelé `username.txt` à la racine du projet. Entrez-y votre nom d'utilisateur. C'est tout ! Maintenant, il ne vous faudra qu'entrer votre mot de passe pour accéder à vos statistiques.

### Valeurs montrées
Le script, pour chaque matière (et la section générale), montrera :
- le code de la matière
- le coefficient de la matière
- la moyenne (arithmétique pondérée), la même qui figurera dans le bulletin
- la note médiane : vous avez autant de notes plus hautes et plus basses qu'elle
- le rang par rapport au reste de la classe : une valeur qui n'est pas affichée par EcoleDirecte. Si `#00`, le rang est inconnu ou incalculable

## Autres outils ED

### Python
[`archive-ed`](https://github.com/a2br/archive-ed/) permet de sauvegarder vos notes, même quand elles ne sont plus accessibles ! Le développement est mis sur pause pour le moment, les fonctionnalités sont limitées.

### JavaScript / TypeScript
[`ecoledirecte.js`](https://github.com/a2br/ecoledirecte.js) ([npm](https://npmjs.com/package/ecoledirecte.js)) est un module Node permettant d'interagir avec EcoleDirecte depuis Node.js. Il est basé sur [`ecoledirecte-api-types`](https://github.com/a2br/ecoledirecte-api-types) ([npm](https://npmjs.com/package/ecoledirecte-api-types)), qui regroupe les types de l'API EcoleDirecte. Son utilisation est recommandée si vous construisez un project avec TypeScript.
