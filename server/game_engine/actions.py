from .conditions import check_condition
from .utils import select_version
MAX_INVENTORY_SIZE = 5


def delete_object(object_id, game_state, game_data):
    # Vérifie si l'object_id est dans l'inventaire
    if object_id in game_state.inventory:
        # Supprime l'object_id du set
        game_state.inventory.remove(object_id)
        object = game_data.objects[object_id]["name"]
        return {"event": "deleted_object", "message": {"message":f"Objet {object} déposé.","image":False}}
    else:
        # Si l'objet n'est pas trouvé dans l'inventaire
        return {"event": "error", "message": {"message":f"Object {object_id} not found in inventory.","image":False}}

def process_click_object(object_id, media_id, media_version, game_state, game_data):
    #Voyons si le media a une action existante.
    if (media_id) :
        media_version, media_data = select_version(game_data.media[media_id], game_state.bools, game_state.inventory, game_state.inputs)
        if ("action" in media_data) :
            if (media_data["action"]["object"] == object_id) :
                bool_id = media_data["action"]["bool"]
                bool_data = game_data.bools.get(bool_id)
                current_status = game_state.bools[bool_id]
                game_state.bools[bool_id] = media_data["action"]["status"]
                message = media_data["action"].get("message")
                if (not message):
                    message={"message":"Action réalisée", "image":"narrateur.png"}
                return {
                    "event": "move",
                    "text":message,
                }
                
    message = game_data.objects[object_id].get("message")
    if(message) :
        return {"event": "message", "message": message}
    return {"event": "no_event"}

def process_click(zone_id, game_state, game_data):
    
    print(zone_id+" clic")

    room = game_data.rooms[game_state.current_room_id][game_state.current_room_version]
    zones = room["zones"]
    zone = next((z for z in zones if z["id"] == zone_id), None)
    if not zone:
        return {"error": "invalid_zone"}

    # Vérifier conditions
    if not check_condition(game_state, zone.get("condition")):
        return {"event": "blocked", "zone": zone_id}

    ztype = zone["type"]

    # --- Déplacement ---
    if ztype == "move":
        target_room_id = zone["target_room"]
        target_room_all_data = game_data.rooms[target_room_id]
        requires_objects = zone.get("requires_objects")

        # Si des objets sont requis, on vérifie l'inventaire
        if requires_objects:
            missing_objects = set(requires_objects) - game_state.inventory

            if missing_objects:
                message = zone.get("access_denied_message")
                return {
                    "event": "missing_condition",
                    "message": message
                }

        # Sélectionne la bonne version de la salle en fonction de l'état des bools
        current_room_version, current_room_data = select_version(target_room_all_data, game_state.bools, game_state.inventory, game_state.inputs)

        if (not current_room_data) :
            return {
                    "event": "missing_condition",
                    "message": {"message":"Impossible d'entrer dans cette pièce!", "image":"narrateur.png"}
                } 
        # Met à jour la salle courante dans l'état du jeu
        game_state.current_room_id = target_room_id
        game_state.current_room_version = current_room_version
        
        # Retourne la version correspondante de la salle avec l'image et la description correctes
        return {
            "event": "move",
            "text":current_room_data.get("text")
        }

    # --- Prise d'objet ---
    if ztype == "object":
        obj_id = zone["object_id"]
        if obj_id in game_state.inventory:
            return {"event": "already_picked"}
        if len(game_state.inventory) >= MAX_INVENTORY_SIZE:
            return {"event": "inventory_full"}
        game_state.inventory.add(obj_id)
        return {"event": "item_found", "item": game_data.objects[obj_id]}

    
    # --- Gestion des bools ---
    if ztype == "bool":
        bool_id = zone["bool_id"]
        bool_data = game_data.bools.get(bool_id)

        if bool_id in game_state.bools:  # Vérifie si l'interrupteur est déjà dans game_state.bools
            current_status = game_state.bools[bool_id]  # L'état actuel de l'interrupteur

            if bool_data:  # Si l'interrupteur existe
                # --- Passage à False (éteindre la lampe) ---
                if current_status:  # Si l'état est 'true' (on essaie de l'éteindre)
                    conditions = bool_data["condition_false"]
                    missing_items = [obj for obj in conditions.get("requires_objets", []) if obj not in game_state.inventory]

                    if not missing_items:  # Si aucune condition n'est manquante
                        game_state.bools[bool_id] = False  # Désactive l'interrupteur
                        return {"event": "switch_off", "item": bool_data["name"], "status": False}
                    else:
                        if (conditions.get("message_fail")) :
                            message = conditions.get("message_fail")
                        else :
                            message = {"message":"Missing items to switch off: {', '.join(missing_items)}","image":"joueur.png"}
                        return {
                            "event": "missing_condition",
                            "message": message
                        }

                # --- Passage à True (allumer la lampe) ---
                else:  # Si l'état est 'false' (on essaie de l'allumer)
                    conditions = bool_data["condition_true"]
                    missing_items = [obj for obj in conditions.get("requires_objets", []) if obj not in game_state.inventory]

                    if not missing_items:  # Si aucune condition n'est manquante
                        game_state.bools[bool_id] = True  # Active l'interrupteur
                        return {"event": "switch_on", "item": bool_data["name"], "status": True}
                    else:
                        if (conditions.get("message_fail")) :
                            message = conditions.get("message_fail")
                        else :
                            message = {"message":"Missing items to switch on: {', '.join(missing_items)}","image":"narrateur.png"}
                        return {
                            "event": "missing_condition",
                            "message": message
                        }

        else:
            return {"event": "missing_bool", "message": "Bool not found in game state."}
    
    if ztype == "media":
        media_version, media = select_version(game_data.media[zone["media_id"]], game_state.bools, game_state.inventory, game_state.inputs)
        media["id"] = zone["media_id"]
        media["version"] = media_version
        return {"event": "show_media", "media": media}

    if ztype == "input":
        input = game_data.inputs[zone["input_id"]]
        input["id"] = zone["input_id"]
        return {"event": "show_input", "input": input}
    
    if ztype == "reset":
        # Réinitialiser l'état du joueur
        game_state.reset(
            start_room=game_data.start_room,
            bools_data=game_data.bools.copy(),
            input_data=game_data.inputs.copy()
        )
        return {"event": "game_reset"}
    
    # Aucune action reconnue
    return {"event": "no_action", "message": "No action performed."}

def testEnigme(input_id, valeur, game_state, game_data) :
    input = game_data.inputs[input_id]
    if (valeur in input["solutions"]) :
        game_state.inputs[input_id] = True
        target_room_all_data = game_data.rooms[input['success_room']]
        current_room_version, current_room_data = select_version(target_room_all_data, game_state.bools, game_state.inventory, game_state.inputs)
        game_state.current_room_id = input['success_room']
        game_state.current_room_version = current_room_version
        # Retourne la version correspondante de la salle avec l'image et la description correctes
        return {
            "event": "move",
            "text":current_room_data.get("text")
        }
    else :
        message = input.get("indice", {"message":"La réponse est fausse","image":"narrateur.png"})
        return {
            "event": "missing_condition",
            "message": message
        } 
