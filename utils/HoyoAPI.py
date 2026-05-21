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
    ClaimedCache = {}

    for char in data.data:
        guild_id = char["guild_id"]
        character_id = char["character_id"]

        if guild_id not in ClaimedCache:
            ClaimedCache[guild_id] = {}
        
        ClaimedCache[guild_id][character_id] = char

def verifyOwner(guild_id, char_id):
    return ClaimedCache.get(guild_id, {}).get(char_id)

def insertCache(guild_id, char_data):
    ClaimedCache.setdefault(guild_id, {})
    ClaimedCache[guild_id][char_data["character_id"]] = char_data

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
    if game == 1:
        Game = "Honkai: Star Rail"
        data = HonkaiDatabase()
        Character = GetRandomIndex(data)
    return Character, Game
    
def convert(data):
    Image = data[0]["portrait_url"] if data[1] == "Honkai: Star Rail" else data[0]["card_url"]
    Trace = data[0]["path"] if data[1] == "Honkai: Star Rail" else data[0]["weapon"]
    return {
        "id":  data[0]["id"],
        "name": data[0]["name"],
        "image": Image,
        "icon": data[0]["icon_url"],
        "rarity": data[0]["rarity"],
        "element": data[0]["element"],
        "trace": Trace,
        "game": data[1]
    }
    
def searchCharacter(name):
    response = (
        supabase.table("hsr_characters")
        .select("*")
        .ilike("name", f"%{name}%")
        .limit(1)
        .execute()
    )
    game = "Honkai: Star Rail"

    if not response.data:
        response = (
            supabase.table("genshin_characters")
            .select("*")
            .ilike("name", f"%{name}%")
            .limit(1)
            .execute()
        )
        game = "Genshin Impact"
        
    if not response.data:
        return None
    
    return response.data[0], game