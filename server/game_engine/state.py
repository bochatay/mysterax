class GameState:
    def __init__(self, start_room, bools_data=None, input_data=None):
        self.current_room_id = start_room
        self.current_room_version = "main"
        self.inventory = set()
        self.inputs = {}
        self.bools = {}
        self.messages_vus = set()

        for bool_id, bool_data in bools_data.items():
            self.bools[bool_id] = bool_data["status"]
        
        for input_id, input_data in input_data.items():
            self.inputs[input_id] = input_data["status"]

    # Méthode pour réinitialiser l'état du jeu
    def reset(self, start_room, bools_data, input_data):
        # Réinitialiser la salle actuelle
        self.current_room_id = start_room
        self.current_room_version = "main"  # Retour à la version principale de la salle
        self.inventory = set()  # Réinitialiser l'inventaire
        self.inputs = {}  # Réinitialiser les inputs
        self.bools = {}  # Réinitialiser les bools
        self.messages_vus = set()  # Réinitialiser les messages vus

        # Recharger les bools et inputs avec les nouvelles données
        for bool_id, bool_data in bools_data.items():
            self.bools[bool_id] = bool_data["status"]
        
        for input_id, input_data in input_data.items():
            self.inputs[input_id] = input_data["status"]
            
    def has_item(self, item_id):
        return item_id in self.inventory

    def set_bool(self, bool_id, status):
        self.bools[bool_id] = status
