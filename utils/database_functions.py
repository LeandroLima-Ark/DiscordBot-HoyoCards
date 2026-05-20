from utils.database import supabase
from utils.HoyoAPI import insertCache

def create_user(user):
    data = {
        "user_id": str(user.id),
        "username": user.name,
        "favorites": []
    }

    supabase.table("users").insert(data).execute()

def user_exists(user_id):
    response = (
        supabase
        .table("users")
        .select("*")
        .eq("user_id", str(user_id))
        .execute()
    )
    return len(response.data) > 0

def ClaimCharacter(
    user_id,
    game,
    character_id,
    guild_id
):

    # ==========================================
    # verifica se já possui dono
    # ==========================================

    existing = supabase.table(
        "player_characters"
    ).select("*").eq(
        "game",
        game
    ).eq(
        "character_id",
        character_id
    ).eq(
        "guild_id",
        guild_id
    ).execute()

    # ==========================================
    # personagem já possui dono
    # ==========================================

    if existing.data:

        owner = existing.data[0]

        return {

            "success": False,

            "owner": owner["user_id"]
        }

    # ==========================================
    # salvar ownership
    # ==========================================

    supabase.table(
        "player_characters"
    ).insert({

        "user_id": str(user_id),

        "game": game,

        "character_id": character_id,

        "guild_id": guild_id

    }).execute()

    char = supabase.table("player_characters").select("*").eq("game", game).eq("character_id", character_id).eq("guild_id", guild_id).execute()
    insertCache(guild_id, char.data[0])

    # ==========================================
    # sucesso
    # ==========================================

    return {
        "success": True
    }

def SearchAllCharacters():
    response = supabase.table("hsr_characters").select("*").order("name", desc=False).execute()

    return response.data