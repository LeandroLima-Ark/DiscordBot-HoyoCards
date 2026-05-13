import requests
from utils.database import supabase

async def LoadDatabaseCache():

    global GENSHIN_CACHE
    global HSR_CACHE

    print("Carregando cache do Genshin...")

    genshin = supabase.table(
        "genshin_characters"
    ).select("*").execute()

    GENSHIN_CACHE = genshin.data

    print("Carregando cache do HSR...")

    hsr = supabase.table(
        "hsr_characters"
    ).select("*").execute()

    HSR_CACHE = hsr.data

    print("Cache carregado.")

async def LoadClaimedCache():
    global ClaimedCache

    data = supabase.table("player_characters").select("*").execute()
    ClaimedCache = {
        char["character_id"]: char
        for char in data.data
    }

def verifyOwner(char_id):
    return ClaimedCache.get(char_id)

def insertCache(char_data):
    ClaimedCache[char_data["character_id"]] = char_data

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

