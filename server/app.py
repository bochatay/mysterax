import uuid
import os
import jinja2
import json 

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse

from server.game_engine.loader import GameData
from server.game_engine.state import GameState
from server.game_engine.actions import process_click, delete_object, process_click_object, testEnigme
from server.game_engine.utils import select_version

from jinja2 import FileSystemLoader, Environment
from config import settings

# Dictionnaire pour stocker l'état du jeu par session
player_states = {}
player_game = {}

app = FastAPI()

print("Mode debug") if settings.debug else print("Mode normal")

templates = Jinja2Templates(directory="templates")

# Servir le frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Parcourir les répertoires de jeux et ajouter un app.mount pour chaque jeu
games_directory = "games"
for game in os.listdir(games_directory):
    game_path = os.path.join(games_directory, game)
    if os.path.isdir(game_path):
        # Monter les fichiers statiques spécifiques à chaque jeu
        static_directory = os.path.join(game_path, "media")
        if os.path.exists(static_directory):
            app.mount(f"/games/{game}/media", StaticFiles(directory=static_directory), name=f"{game}_static")


# Route principale pour démarrer le jeu avec un jeu sélectionné
@app.get("/games/{game_name}")
async def get_game(request: Request, game_name: str):
    game_data = GameData(f"games/{game_name}/json")  # Charger les données du jeu spécifique
    
    # Déterminer l'URL de base pour les médias du jeu
    media_url = f"/games/{game_name}/media"  # URL des médias spécifiques au jeu

    # Vérifier si le template spécifique existe dans "games/{game_name}/templates/index.html"
    game_templates_dir = os.path.join("games", game_name, "templates")
    game_template_path = os.path.join(game_templates_dir, "index.html")

    if os.path.exists(game_template_path):
        # Si le template spécifique au jeu existe, utiliser ce répertoire
        env = Environment(loader=FileSystemLoader(game_templates_dir))
        template = env.get_template("index.html")
    else:
        # Si le template spécifique n'existe pas, utiliser le template global
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("index.html")

    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in player_states:
        session_id = str(uuid.uuid4())  # Générer un ID de session unique
        player_states[session_id] = GameState(
            start_room=game_data.start_room,
            bools_data=game_data.bools.copy(),
            input_data=game_data.inputs.copy()
        )
    player_game[session_id] = game_data
    debug_mode = settings.debug
    html_content = template.render(
        request=request,
        css_debug="<link rel='stylesheet' href='/static/css/style_debug.css'>" if debug_mode else "",
        style_coordinates="" if debug_mode else "display:none;",
        media_url=media_url
    )

    # Retourner la réponse HTML avec le contenu rendu
    response = HTMLResponse(content=html_content)
    response.set_cookie("session_id", session_id)
    return response

@app.get("/api/state")
async def get_state(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in player_states:
        return JSONResponse({"error": "Session non trouvée"}, status_code=400)

    game_state = player_states[session_id]
    game_data = player_game.get(session_id)

    # Sélectionner la version de la salle et récupérer les phrases
    current_room_version, current_room_data = select_version(
        game_data.rooms[game_state.current_room_id],
        game_state.bools,
        game_state.inventory,
        game_state.inputs
    )
    if current_room_version is None or current_room_data is False:
        current_room_data = game_data.rooms[game_state.current_room_id][game_state.current_room_version]
    else:
        game_state.current_room_version = current_room_version

    message_id = current_room_data.get("message_id")
    phrases = []
    if message_id and message_id not in game_state.messages_vus:
        game_state.messages_vus.add(message_id)
        phrases = game_data.messages[message_id]["phrases"]

    return {
        "room": game_state.current_room_id,
        "room_version": game_state.current_room_version,
        "image": current_room_data["image"],
        "inventory": [{"id": obj_id, **game_data.objects[obj_id]} for obj_id in game_state.inventory],
        "bools": {
            bool_id: {**game_data.bools[bool_id], "status": status}
            for bool_id, status in game_state.bools.items()
        },
        "zones": current_room_data.get("zones", []),
        "phrases": phrases
    }

@app.post("/api/testEnigme")
async def test_enigme(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in player_states:
        return JSONResponse({"error": "Session non trouvée"}, status_code=400)

    data = await request.json()
    input_id = data.get("input_id")
    valeur = data.get("valeur")

    game_state = player_states[session_id]
    game_data = player_game.get(session_id)
    
    result = testEnigme(input_id, valeur, game_state, game_data)
    return JSONResponse(result)

@app.post("/api/click")
async def click_action(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in player_states:
        return JSONResponse({"error": "Session non trouvée"}, status_code=400)

    data = await request.json()
    zone_id = data.get("zone_id")

    game_state = player_states[session_id]
    game_data = player_game.get(session_id)

    result = process_click(zone_id, game_state, game_data)

    if result.get("event") == "game_reset":
        # Réinitialiser la session et renvoyer la page de jeu initiale
        player_states[session_id] = GameState(
            start_room=game_data.start_room,
            bools_data=game_data.bools.copy(),
            input_data=game_data.inputs.copy()
        )
        debug_mode = request.cookies.get("debug_mode", "false") == "true"
        css_debug = "<link rel='stylesheet' href='/static/css/style_debug.css'>" if debug_mode else ""
        style_coordinates = "" if debug_mode else "display:none;"
        return JSONResponse({"event": "game_reset", "redirect": True})
    return JSONResponse(result)

@app.post("/api/clickObject")
async def click_object(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in player_states:
        return JSONResponse({"error": "Session non trouvée"}, status_code=400)

    data = await request.json()
    object_id = data.get("object_id")
    media_id = data.get("media_id")
    media_version = data.get("media_version")

    game_state = player_states[session_id]
    game_data = player_game.get(session_id)

    result = process_click_object(object_id, media_id, media_version, game_state, game_data)
    return JSONResponse(result)

@app.post("/api/deposeObjet")
async def del_object(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in player_states:
        return JSONResponse({"error": "Session non trouvée"}, status_code=400)

    data = await request.json()
    object_id = data.get("object_id")

    game_state = player_states[session_id]
    game_data = player_game.get(session_id)

    result = delete_object(object_id, game_state, game_data)
    return JSONResponse(result)

@app.get("/")
async def get_home(request: Request):
# Parcourir le répertoire "games" et récupérer les noms des jeux
    games_directory = "games"
    games_data = []

    # Parcourir les répertoires de jeux dans le dossier 'games'
    for game in os.listdir(games_directory):
        game_path = os.path.join(games_directory, game)
        if os.path.isdir(game_path):
            game_json_path = os.path.join(game_path, "json", "game.json")
            
            # Vérifier si le fichier game.json existe pour ce jeu
            if os.path.exists(game_json_path):
                with open(game_json_path, 'r', encoding='utf-8') as f:
                    game_info = json.load(f)
                    game_name = game_info.get("name", "Nom du jeu introuvable")  # Extraire le nom du jeu
                    games_data.append({"game": game, "name": game_name})

    # Passer la liste des jeux avec leur nom au template
    return templates.TemplateResponse("jeux.html", {
        "request": request,
        "games": games_data  # Liste des jeux avec leurs noms
    })