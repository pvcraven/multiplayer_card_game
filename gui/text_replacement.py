def text_replacement(text, game_data):
    text = text.replace("#users-0-name#", game_data["users"][0]["name"])

    text = text.replace("#users-0-resources-0#", str(game_data["users"][0]["resources"][0]))
    text = text.replace("#users-0-resources-1#", str(game_data["users"][0]["resources"][1]))
    text = text.replace("#users-0-resources-2#", str(game_data["users"][0]["resources"][2]))
    text = text.replace("#users-0-resources-3#", str(game_data["users"][0]["resources"][3]))
    text = text.replace("#users-0-resources-4#", str(game_data["users"][0]["resources"][4]))
    text = text.replace("#users-0-resources-5#", str(game_data["users"][0]["resources"][5]))
    return text
