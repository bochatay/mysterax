# Mysterax
## Moteur de jeu d’énigmes – Point & Click
*Python · FastAPI · JSON · HTML · JavaScript*

[Cuisine du jeu Arc-en ciel en Valais utilisant le moteur Mysterax](static/im1.jpg)
## License

License MIT.
Voir le fichier LICENSE pour plus de détails

### Installation du moteur:
git clone https://github.com/bochatay/mysterax.git

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

### Installation de jeux:
cd games

Exemple: git clone https://github.com/bochatay/mysterax_maison_abandonnee.git


### Lancement:
uvicorn server.app:app --reload

### Accès
localhost:8000


## Présentation

---

Mysterax est un **moteur de jeu d’énigmes narratif de type point & click**, développé en **Python (FastAPI)** pour le backend et **HTML / JavaScript** pour le frontend.

La particularité du moteur est que **l’intégralité du jeu est décrite via des fichiers JSON** :
- pièces (rooms)
- zones cliquables
- objets
- états logiques
- énigmes
- dialogues
- médias (images / sons)

Il est possible de créer un jeu complet **sans modifier le code Python**.



Philosophie du moteur

Une "room" est une image fixe contenant des zones cliquables. Chaque room est déclinée en une ou plusieurs versions conditionnelles. La version de la room affichée dépend de différentes conditions: booleens, inventaire et énigmes résolues.

Les interactions sont simples :

cliquer → envoyer l’action au serveur → recevoir un événement → mettre à jour l’affichage

Le moteur est pensé pour :

des jeux d’exploration

des escape games

des aventures narratives

des puzzles multi-étapes

### Architecture du projet
```text
project/
├── server/
│ ├── app.py
│ ├── game_engine/
│   ├── actions.py
│   ├── loader.py
│   ├── state.py
│   └── utils.py
├── games/ <- Les jeux sont ajoutés dans ce répertoire
│   ├── nom_du_jeu_1
│   │ ├── json
│   │ | ├── game.json
│   │ | ├── bools.json
│   │ | ├── inputs.json
│   │ | ├── media.json
│   │ | ├── messages.json
│   │ | ├── objects.json
│   │ | ├── rooms.json
│   │ ├── media
│   │ | ├── inputs
│   │ | | ├── image_input1.jpg
│   │ | | ├── image_input2.png
│   │ | | ├── ...
│   │ | ├── media
│   │ | ├── objects
│   │ | ├── persos
│   │ | ├── rooms
│   │ | ├── zones
│   │ | ├── preview.jpg
├── static/ <- Si les dossiers static et template se trouvent dans le répertoire du jeu, ils ont la priorité.
│   ├── js/
│   │ └── game.js
│   └── css/
│     └── style.css   
├── templates/
    └── index.html
```

### Rooms (`rooms.json`)

Une **room** représente un lieu logique du jeu.

```json
"entrance": {
  "main": {
    "image": "entrance.jpg",
    "zones": []
  }
}
```

### Versions conditionnelles

Une room peut avoir plusieurs versions, sélectionnées dynamiquement selon l’état du jeu :
```json
"sous-sol": {
  "sans_eclairage": {...},
  "avec_eclairage": {
    "condition": {
      "requires_bools": { "petrol_lamp": true }
    }
  }
}
```

Une version peut :

changer l’image ou non

changer uniquement les zones

afficher un message ou un dialogue

Une version est un état de la même salle, pas une nouvelle salle.

### Zones cliquables

Chaque room contient des zones définies par leurs coordonnées :

```json
{
  "id": "go_kitchen",
  "type": "move",
  "coords": [120, 340, 80, 60]
}
```

Types de zones supportés
**move**	changer de room
**object**	ramasser un objet
**bool** activer / désactiver un état
**media**	afficher une image ou un son
**input**	afficher une énigme
**reset**	recommencer le jeu

### États logiques (bools.json)

Les booléens sont des interrupteurs persistants du monde.
```json
"petrol_lamp": {
  "status": false,
  "condition_true": {
    "requires_objets": ["matchbox"]
  }
}
```

condition_true / condition_false

condition_true → conditions pour passer le bool à true

condition_false → conditions pour repasser à false

Ils peuvent afficher un message d’échec si les conditions ne sont pas remplies.

### Objets (objects.json)

Les objets sont stockés dans l’inventaire du joueur.

```json
"flashlight": {
  "name": "Lampe torche",
  "image": "flashlight.png",
  "description": "Une vieille lampe.",
  "pickup_once": true
}
```

Fonctionnalités :

inventaire limité

dépôt d’objets

interactions avec médias et booléens

Énigmes (inputs.json)

Les inputs permettent de créer des énigmes textuelles.

```json
"computer_password": {
  "solutions": ["cervin", "matterhorn"],
  "image": "pc.gif",
  "success_room": "sousol"
}
```

Fonctionnalités :

plusieurs solutions possibles

indice optionnel


### Médias interactifs (media.json)

Les médias peuvent être :

des images

des sons

des scènes interactives

```json
"mouse": {
  "image": "mouse.jpg",
  "action": {
    "object": "bread",
    "bool": "acces_chambre_enfants"
  }
}
```

Ils permettent :

Agrandir un objet pour voir les détails (un tableau au mur par exemple)

Interagir en cliquant sur un objet de l'inventaire 


### Messages & dialogues (messages.json)

Les messages sont des séquences de phrases, affichées une seule fois.

```json
"debut_jeu": {
  "phrases": [
    {"message":"Bienvenue !","image":"narrateur.png"}
  ]
}
```

L’image correspond à l’avatar du locuteur :

joueur

narrateur

personnages du jeu

### Frontend (HTML / JS)

Le frontend :

affiche l’image de la room

dessine les zones cliquables

gère l’inventaire

affiche messages, médias et énigmes

Le fichier game.js :

communique avec l’API (/api/state, /api/click, etc.)

interprète les événements (move, item_found, show_media, etc.)

met à jour l’interface

Le moteur n’impose pas ce frontend : n’importe quel client peut consommer l’API.



### Créer son propre jeu (résumé)

Définir la room de départ et le nom du jeu dans game.json

Créer les rooms et leurs zones dans rooms.json

Ajouter des objets (objects.json)

Définir les booléens (bools.json)

Ajouter des énigmes (inputs.json)

Écrire les dialogues (messages.json)

Ajouter les images et sons
