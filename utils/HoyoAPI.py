import requests
from utils.database import supabase

def LoadDatabaseCache():

    global GENSHIN_CACHE
    global HSR_CACHE

    print("Carregando cache do Genshin...")

    genshin = supabase.table(
        "genshin_characters"
    ).select("*").execute()

    GENSHIN_CACHE = genshin.data

    print(
        f"{len(GENSHIN_CACHE)} personagens carregados."
    )

    print("Carregando cache do HSR...")

    hsr = supabase.table(
        "hsr_characters"
    ).select("*").execute()

    HSR_CACHE = hsr.data

    print(
        f"{len(HSR_CACHE)} personagens carregados."
    )

    print("Cache carregado.")

def GenshinDatabase():
    return GENSHIN_CACHE

def HonkaiDatabase():
    return HSR_CACHE

# 0 - Genshin Impact, 1 - Honkai: Star Rail
Games = [0, 1]

def GetRandomIndex(data):
    import random
    return random.choice(data)

def getCharacter():
    game = GetRandomIndex(Games)

    if game == 0:
        Game = "Genshin Impact"
        data = GenshinDatabase()
        Character = GetRandomIndex(data)

        ImageUrl = Character["card_url"]

        return {
            "id": Character["id"],
            "name": Character["name"],
            "image": ImageUrl,
            "game": Game
        }
    if game == 1:
        Game = "Honkai: Star Rail"
        data = HonkaiDatabase()
        Character = GetRandomIndex(data)

        ImageUrl = Character["portrait_url"]
        return {
            "id":  Character["id"],
            "name": Character["name"],
            "image": ImageUrl,
            "game": Game
        }

