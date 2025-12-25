# Mysterax
## Moteur de jeu d’énigmes – Point & Click
*Python · FastAPI · JSON · HTML · JavaScript*

### Installation du moteur:
git clone mysterax
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### Installation de jeux:
cd games
git clone nom_du_jeu

### Lancement:
uvicorn server.app:app --reload

### Accès
localhost:8000







# Description

---

Ce projet est un moteur de jeu d’énigmes narratif de type point & click, développé en Python (FastAPI) pour le backend et HTML / JavaScript pour le frontend.

La particularité du moteur est que tout le jeu est défini de manière déclarative via des fichiers JSON :

pièces (rooms)

zones cliquables

objets

états logiques (booléens)

énigmes textuelles

médias (images, sons)

dialogues et narration

👉 Il est possible de créer un jeu complet sans modifier le code Python, uniquement en remplissant les fichiers JSON et en ajoutant des assets.

🧠 Philosophie du moteur

Une room n’est pas figée : elle peut avoir plusieurs versions conditionnelles

Le monde évolue selon :

des booléens persistants

l’inventaire

la résolution d’énigmes

Les interactions sont simples :

cliquer → envoyer l’action au serveur → recevoir un événement → mettre à jour l’affichage

Le moteur est pensé pour :

des jeux d’exploration

des escape games

des aventures narratives

des puzzles multi-étapes

🗂️ Architecture du projet
project/
├── server/
│ ├── app.py
│ ├── game_engine/
│   ├── actions.py
│   ├── conditions.py
│   ├── loader.py
│   ├── state.py
│   └── utils.py
├── games/
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
├── static/
│ ├── img/
│ │ ├── rooms/
│ │ ├── zones/
│ │ ├── objects/
│ │ ├── media/
│ │ ├── inputs/
│ │ └── persos/
│ ├── js/
│ │ └── game.js
│ └── css/
│   └── style.css
├── templates/
|   └── index.html
├── static/
│ ├── img/
│ │ ├── rooms/
│ │ ├── zones/
│ │ ├── objects/
│ │ ├── media/
│ │ ├── inputs/
│ │ └── persos/
│ ├── js/
│ │ └── game.js
│ └── css/
│ └── style.css
└── templates/
└── index.html












## 🎮 Présentation

Ce projet est un **moteur de jeu d’énigmes narratif de type point & click**, développé en **Python (FastAPI)** pour le backend et **HTML / JavaScript** pour le frontend.

🧩 La particularité du moteur est que **l’intégralité du jeu est décrite via des fichiers JSON** :
- pièces (rooms)
- zones cliquables
- objets
- états logiques
- énigmes
- dialogues
- médias (images / sons)

👉 Il est possible de créer un jeu complet **sans modifier le code Python**.

---

## 🧠 Philosophie du moteur

- Une room peut avoir **plusieurs versions conditionnelles**
- Le monde évolue selon :
  - des **booléens persistants**
  - l’**inventaire**
  - les **énigmes résolues**
- Le moteur est **déclaratif** :
  
> *On décrit le monde, le moteur applique les règles.*

Idéal pour :
- escape games
- aventures narratives
- jeux d’exploration
- projets pédagogiques

---

## 🗂️ Architecture du projet
project/
├── server/
│ ├── main.py
│ ├── game_engine/
│ │ ├── actions.py
│ │ ├── conditions.py
│ │ ├── loader.py
│ │ ├── state.py
│ │ └── utils.py
│ └── data/
│ ├── game.json
│ ├── rooms.json
│ ├── objects.json
│ ├── bools.json
│ ├── inputs.json
│ ├── media.json
│ └── messages.json
├── static/
│ ├── img/
│ │ ├── rooms/
│ │ ├── zones/
│ │ ├── objects/
│ │ ├── media/
│ │ ├── inputs/
│ │ └── persos/
│ ├── js/
│ │ └── game.js
│ └── css/
│ └── style.css
└── templates/
└── index.html


---

## ▶️ Lancer le jeu

1. Installer les dépendances Python
2. Lancer le serveur FastAPI
3. Ouvrir le navigateur à l’adresse indiquée (ex. `http://127.0.0.1:8000`)

---

## 🏠 Rooms (`rooms.json`)

Une **room** représente un lieu logique du jeu.

```json
"entrance": {
  "main": {
    "image": "entrance.jpg",
    "zones": []
  }
}






















🕵️‍♂️ Moteur de jeu d’énigmes Point & Click (Python / JSON)
🎮 Présentation

Ce projet est un moteur de jeu d’énigmes narratif de type point & click, développé en Python (FastAPI) pour le backend et HTML / JavaScript pour le frontend.

La particularité du moteur est que tout le jeu est défini de manière déclarative via des fichiers JSON :

pièces (rooms)

zones cliquables

objets

états logiques (booléens)

énigmes textuelles

médias (images, sons)

dialogues et narration

👉 Il est possible de créer un jeu complet sans modifier le code Python, uniquement en remplissant les fichiers JSON et en ajoutant des assets.

🧠 Philosophie du moteur

Une room n’est pas figée : elle peut avoir plusieurs versions conditionnelles

Le monde évolue selon :

des booléens persistants

l’inventaire

la résolution d’énigmes

Les interactions sont simples :

cliquer → envoyer l’action au serveur → recevoir un événement → mettre à jour l’affichage

Le moteur est pensé pour :

des jeux d’exploration

des escape games

des aventures narratives

des puzzles multi-étapes

🗂️ Architecture du projet
project/
├── server/
│   ├── main.py
│   ├── game_engine/
│   │   ├── actions.py
│   │   ├── conditions.py
│   │   ├── loader.py
│   │   ├── state.py
│   │   └── utils.py
│   └── data/
│       ├── game.json
│       ├── rooms.json
│       ├── objects.json
│       ├── bools.json
│       ├── inputs.json
│       ├── media.json
│       └── messages.json
├── static/
│   ├── img/
│   │   ├── rooms/
│   │   ├── zones/
│   │   ├── objects/
│   │   ├── media/
│   │   ├── inputs/
│   │   └── persos/
│   ├── js/game.js
│   └── css/style.css
└── templates/
    └── index.html

▶️ Lancer le jeu

Installer les dépendances Python

Lancer le serveur FastAPI

Ouvrir le navigateur à l’adresse indiquée (ex : http://127.0.0.1:8000)

🏠 Les rooms (rooms.json)

Une room représente un lieu logique du jeu.

"entrance": {
  "main": {
    "image": "entrance.jpg",
    "zones": [...]
  }
}

🔀 Versions conditionnelles

Une room peut avoir plusieurs versions, sélectionnées dynamiquement selon l’état du jeu :

"sousol": {
  "main": {...},
  "allume": {
    "condition": {
      "requires_bools": { "petrol_lamp": true }
    }
  }
}


👉 Une version peut :

changer l’image ou non

changer uniquement les zones

afficher un message ou un dialogue

Une version est un état de la même salle, pas une nouvelle salle.

🖱️ Zones cliquables

Chaque room contient des zones définies par leurs coordonnées :

{
  "id": "go_kitchen",
  "type": "move",
  "coords": [120, 340, 80, 60]
}

Types de zones supportés
Type	Effet
move	changer de room
object	ramasser un objet
bool	activer / désactiver un état
media	afficher une image ou un son
input	afficher une énigme
reset	recommencer le jeu
🔘 États logiques (bools.json)

Les booléens sont des interrupteurs persistants du monde.

"petrol_lamp": {
  "status": false,
  "condition_true": {
    "requires_objets": ["matchbox"]
  }
}

condition_true / condition_false

condition_true → conditions pour passer le bool à true

condition_false → conditions pour repasser à false

Ils peuvent afficher un message d’échec si les conditions ne sont pas remplies.

🎒 Objets (objects.json)

Les objets sont stockés dans l’inventaire du joueur.

"flashlight": {
  "name": "Lampe torche",
  "image": "flashlight.png",
  "description": "Une vieille lampe.",
  "pickup_once": true
}


Fonctionnalités :

inventaire limité

dépôt d’objets

interactions avec médias et booléens

⌨️ Énigmes (inputs.json)

Les inputs permettent de créer des énigmes textuelles.

"computer_password": {
  "solutions": ["cervin", "matterhorn"],
  "image": "pc.gif",
  "success_room": "sousol"
}


Fonctionnalités :

plusieurs solutions possibles

indice optionnel

déclenchement de progression

🖼️ Médias interactifs (media.json)

Les médias peuvent être :

des images

des sons

des scènes interactives

"mouse": {
  "image": "mouse.jpg",
  "action": {
    "object": "bread",
    "bool": "acces_chambre_enfants"
  }
}


👉 Ils permettent :

dialogues avec PNJ

puzzles “donner un objet”

déclencheurs narratifs

💬 Messages & dialogues (messages.json)

Les messages sont des séquences de phrases, affichées une seule fois.

"debut_jeu": {
  "phrases": [
    {"message":"Bienvenue !","image":"narrateur.png"}
  ]
}


📌 L’image correspond à l’avatar du locuteur :

joueur

narrateur

PNJ (souris, alien, IA…)

🧑‍💻 Frontend (HTML / JS)

Le frontend :

affiche l’image de la room

dessine les zones cliquables

gère l’inventaire

affiche messages, médias et énigmes

Le fichier game.js :

communique avec l’API (/api/state, /api/click, etc.)

interprète les événements (move, item_found, show_media, etc.)

met à jour l’interface

👉 Le moteur n’impose pas ce frontend : n’importe quel client peut consommer l’API.

🎨 Ajouter des assets

static/img/rooms/ → images de fond

static/img/zones/ → zones visibles

static/img/objects/ → objets inventaire

static/img/media/ → images & sons

static/img/inputs/ → écrans d’énigmes

static/img/persos/ → avatars des dialogues

Un mode debug affiche les coordonnées de la souris pour placer les zones.

🧩 Créer son propre jeu (résumé)

Définir la room de départ (game.json)

Créer les rooms et leurs zones

Ajouter des objets

Définir les booléens

Ajouter des énigmes

Écrire les dialogues

Ajouter les images et sons

🎉 Le jeu est prêt, sans toucher au code Python.

✨ Conclusion

Ce moteur permet de créer des jeux d’énigmes riches, narratifs et évolutifs, en séparant totalement :

la logique du jeu

le contenu

la narration

Il est idéal pour :

prototypes

escape games

projets pédagogiques

aventures interactives






















mysterax/
├── server/
│   ├── main.py
│   └── (autres fichiers)
├── games/
│   ├── abandoned_lab/
│   └── another_game/
├── static/
├── templates/
│   ├── jeux.html  # Page principale qui liste les jeux
│   ├── index.html  # Template des jeux (1 seul pour tous les jeux)
└── (autres fichiers)