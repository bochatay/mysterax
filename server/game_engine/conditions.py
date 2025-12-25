def check_condition(game_state, condition):
    if not condition:
        return True

    required = condition.get("requires", [])
    for item in required:
        if item not in game_state.inventory:
            return False

    return True
