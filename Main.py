import pygame
import sys
import math
import random
import json
import os
import time

player_accounts = {}

if os.path.exists("accounts.json"):

    with open("accounts.json", "r") as file:
        player_accounts = json.load(file)

try:

    with open("players.json", "r") as file:

        player_data = json.load(file)

except:

    player_data = {}

# Muted users (persisted in muted.json). Muted players can't chat.
muted_users = []

# Timestamps of chat announcements (rendered red in chat).
announcement_times = []

try:

    with open("muted.json", "r") as file:

        muted_users = json.load(file)

except:

    muted_users = []

pygame.init()
login_error_timer = 0
accounts = {
    "DevGuard": "g",
    "Test": "password"
}
#|------------------------|
#|           |            |
#|           |----------  |
#|---------               |
#|        |---------|  |--|
#|        |####-----|  |  |
#|--- ----|############|  |
#| PLAYER |--------  --|  |
#|--------|---------------|

# ---------------- SETTINGS ----------------
# ---------------- UPGRADE MENU ----------------
starter_walls = []
PLAYER_SPAWN_PROTECTION_TIME = 180   # 3 seconds at 60 FPS
player_spawn_cooldown = PLAYER_SPAWN_PROTECTION_TIME
inventory = []
inventory_scroll = 0
INVENTORY_ROW_SIZE = 5
INVENTORY_SLOT_SIZE = 60
INVENTORY_GAP = 10
INVENTORY_COLS = 5
INVENTORY_SLOT_SIZE = 40
INVENTORY_SLOT_GAP = 8
# ---------------- ENEMY ZONES ----------------

ZONE_RARITIES = {

    "common": [
        "Common"
    ],


    "epic": [
        "Rare",
        "Epic"
    ]

}
boss_hp = 0
boss_max_hp = 0
boss_name = ""
infino_gradient_offset = 0
boss_rarity = ""
spawn_message = ""
infino_gradient_offset = 0
infino_gradient_angle = 0
infino_gradient_target_angle = 0
infino_gradient_timer = 0
spawn_message_timer = 0
spawn_message_alpha = 255

error_message = ""
error_message_timer = 0
error_message_alpha = 255

upgrade_menu_open = False
WALL = 100
WORLD = 5000
# ---------------- WALLS ----------------

walls = []
new_rarity_gradient = 0
leaf_heal_timer = 0
hp_upgrade_cost = 2
rose_heal_timer = 0

hp_upgrade_amount = 25
password_text = ""
acc_name_text = ""

active_input = None

WIDTH = 1500
HEIGHT = 845
FPS = 60
MAP_SIZE = 15000
MINIMAP_SIZE = 200
MINIMAP_MARGIN = 20

MINIMAP_SIZE = 150

MINIMAP_X = WIDTH - MINIMAP_SIZE - 5
MINIMAP_Y = 5

minimap_x = WIDTH - MINIMAP_SIZE - 10
minimap_y = HEIGHT - MINIMAP_SIZE - 10

PLAYER_SPEED = 2.5
PLAYER_RADIUS = 25

# Enemy loot boxes: a small box tinted by the drop's rarity with the
# petal art drawn inside.  Despawns on its own after a while, and is
# collected when the flower touches it, adding the petal to the
# inventory.
PICKUP_SIZE = 34
PICKUP_LIFETIME = 300.0
PICKUP_SHRINK_TIME = 0.2
PICKUP_LIST = []
pickup_pulse_phase = 0.0

PLAYER_ACCEL = 0.14
PLAYER_FRICTION = 0.90
PLAYER_DEATH_DURATION = 90

GRASS_SIZE = 64
petal_respawn_text_timer = []
WORLD_WIDTH = 15000
WORLD_HEIGHT = 15000

# ---------------- FLOWER LEVEL ----------------

flower_level = 1

flower_xp = 0

flower_xp_needed = 100

upgrade_points = 0

# ---------------- RARITY HP MULTIPLIER ----------------

PETAL_HP_MULTIPLIER = {

    "Common": 1.0,

    "Unusual": 5.6,

    "Rare": 16.3,

    "Epic": 47.1,

    "Legendary": 84.2,

    "Mythic": 113.6,

    "Ultra": 451.7,

    "Super": 793.1,

    "Omega": 1262.1,

    "Unique": 4147.5,

    "Eternal": 9125.8,

    "Cosmo": 12623.5,

    "Jeddiful": 40000.0,

    "Tacnic": 64254.1,

    "Radium": 124355.4,

    "Ancient": 432566.2,

    "Omnient": 824345.1,

    "Celestial": 1000000.0,

    "Infino": 6139340.1
}

ENEMY_RARITIES = [
    "Common",
    "Unusual",
    "Rare",
    "Epic",
    "Legendary",
    "Mythic",
    "Ultra",
    "Super",
    "Omega",
    "Unique",
    "Eternal",
    "Cosmo",
    "Jeddiful",
    "Tacnic",
    "Radium",
    "Ancient",
    "Omnient",
    "Celestial"
]

HEAVY_KNOCKBACK_MULTIPLIER = {
    "Common": 1.0,
    "Unusual": 1.2,
    "Rare": 1.5,
    "Epic": 1.8,
    "Legendary": 2.2,
    "Mythic": 2.7,
    "Ultra": 3.3,
    "Super": 4.0,
    "Omega": 4.8,
    "Unique": 5.8,
    "Eternal": 7.0,
    "Cosmo": 8.5,
    "Jeddiful": 10.0,
    "Tacnic": 12.0,
    "Radium": 14.5,
    "Ancient": 17.5,
    "Omnient": 21.0,
    "Celestial": 24.0,
    "Infino": float(300)
}

MOB_WEIGHT = {
    "Ladybug": 1.0,
    "HoleLadybug": 2.0,
    "HoleBee": 1.6,
    "HoleSpider": 2.0,
    "HoleRock": 4.0,
    "HoleHornet": 2.0,
    "HoleBabyAnt": 3.0,
    "HoleSoldierAnt": 2.5,
    "HoleWorkerAnt": 2.8,
    "HoleQueenAnt": 1.5,
    "Bee": 0.8,
    "Spider": 1.1,
    "Rock": 1.0,
    "Hornet": 1.0,
    "BabyAnt": 0.7,
    "SoldierAnt": 1.2,
    "WorkerAnt": 1.0,
    "QueenAnt": 3.0,
    "AntEgg": 0.5
}

MOB_WEIGHT_MULTIPLIER = {
    "Common": 1.0,
    "Unusual": 1.1,
    "Rare": 1.25,
    "Epic": 1.45,
    "Legendary": 1.7,
    "Mythic": 2.0,
    "Ultra": 2.4,
    "Super": 2.9,
    "Omega": 3.5,
    "Unique": 4.2,
    "Eternal": 5.0,
    "Cosmo": 6.0,
    "Jeddiful": 7.2,
    "Tacnic": 8.6,
    "Radium": 10.3,
    "Ancient": 12.4,
    "Omnient": 15.0,
    "Celestial": 18.1
}

MOB_HP_MULTIPLIER = {
    "Common": 1.0,
    "Unusual": 9.6,
    "Rare": 16.3,
    "Epic": 47.1,
    "Legendary": 114.2,
    "Mythic": 935.0,
    "Ultra": 4000.0,
    "Super": 15000.0,
    "Omega": 123000.0,
    "Unique": 23100000.0,
    "Eternal": 1500000000.0,
    "Cosmo": 9200000000.0,
    "Jeddiful": 300000000000.0,
    "Tacnic": 10000000000000.1,
    "Radium": 200000000000000.0,
    "Ancient": 200000000000000.0,
    "Omnient": 390483200000000.0,
    "Celestial": 212400000000000.0
}

MOB_DAMAGE_MULTIPLIER = {
    "Common": 1.0,
    "Unusual": 2.5,
    "Rare": 5.0,
    "Epic": 12.0,
    "Legendary": 30.0,
    "Mythic": 80.0,
    "Ultra": 200.0,
    "Super": 500.0,
    "Omega": 1200.0,
    "Unique": 3000.0,
    "Eternal": 10000.0,
    "Cosmo": 25000.0,
    "Jeddiful": 75000.0,
    "Tacnic": 150000.0,
    "Radium": 300000.0,
    "Ancient": 1000000.0,
    "Omnient": 5000000.0,
    "Celestial": 15000000.0
}

LEAF_HEAL = {
    "Common": 2,
    "Unusual": 10,
    "Rare": 50,
    "Epic": 160,
    "Legendary": 450,
    "Mythic": 1800,
    "Ultra": 21000,
    "Super": 190000,
    "Omega": 3800000,
    "Unique": 10000000,
    "Eternal": 200000000,
    "Cosmo": 912000000,
    "Jeddiful": 2570000000,
    "Tacnic": 9180000000,
    "Radium": 29000000000,
    "Ancient": 91000000000,
    "Omnient": 131000000000,
    "Celestial": 730000000000,
    "Infino": 11000000000000
}

MOB_SIZE_MULTIPLIER = {
    "Common": 1.0,
    "Unusual": 1.2,
    "Rare": 1.4,
    "Epic": 1.6,
    "Legendary": 1.8,
    "Mythic": 2.0,
    "Ultra": 2.2,
    "Super": 2.4,
    "Omega": 2.6,
    "Unique": 2.8,
    "Eternal": 3.0,
    "Cosmo": 3.2,
    "Jeddiful": 3.4,
    "Tacnic": 3.6,
    "Radium": 3.8,
    "Ancient": 4.0,
    "Omnient": 4.2,
    "Celestial": 4.4
}

MOB_XP_MULTIPLIER = {
    "Common": 1.0,
    "Unusual": 3.0,
    "Rare": 8.0,
    "Epic": 20.0,
    "Legendary": 50.0,
    "Mythic": 120.0,
    "Ultra": 300.0,
    "Super": 700.0,
    "Omega": 1500.0,
    "Unique": 3500.0,
    "Eternal": 8000.0,
    "Cosmo": 20000.0,
    "Jeddiful": 50000.0,
    "Tacnic": 100000.0,
    "Radium": 250000.0,
    "Ancient": 600000.0,
    "Omnient": 1500000.0,
    "Celestial": 5000000.0
}

# ---------------- PETAL SLOTS ----------------

def get_petal_slots(level):
    if level >= 75:
        return 10
    if level >= 55:
        return 9
    if level >= 35:
        return 8
    if level >= 15:
        return 7
    if level >= 5:
        return 6
    return 5

PETAL_SLOTS = get_petal_slots(flower_level)

petal_slots = []
for _ in range(PETAL_SLOTS):
    petal_slots.append({
        "filled": False,
        "petal": "Basic",
        "rarity": "Common"
    })

# Swap petal slots (second set of PETAL_SLOTS slots)
swap_petal_slots = []
for _ in range(PETAL_SLOTS):
    swap_petal_slots.append({
        "filled": False,
        "petal": "Basic",
        "rarity": "Common"
    })

# ---------------- PETAL INVENTORY ----------------

PETAL_SLOT_COUNT = 10  # Maximum slots (will be overridden by PETAL_SLOTS at runtime)
PETAL_SLOT_SIZE = 55
PETAL_SLOT_GAP = 5

PETAL_BAR_Y = HEIGHT - 130
# ---------------- WORLD ----------------

WORLD_SIZE = 15000

# ---------------- WINDOW ----------------

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("https://Velora.io")

clock = pygame.time.Clock()
game_font = pygame.font.SysFont(None, 28)
login_font = pygame.font.Font(None, 32)
# ---------------- PLAYER ----------------

player_x = 0
player_y = 0

camera_x = 0
camera_y = 0

player_vel_x = 0
player_vel_y = 0

player_flash_timer = 0

player_rot_angle = 0
player_rot_vel = 0

player_dead = False
player_death_timer = 0
player_bounce_x = 0
player_bounce_y = 0
player_death_dir_x = 1
player_death_dir_y = 0
killer_name = None
killer_rarity = None

# Respawn button geometry: near the bottom edge of the screen, up a little.
RESPAWN_BUTTON_W = 240
RESPAWN_BUTTON_H = 70
respawn_button_rect = pygame.Rect(
    WIDTH // 2 - RESPAWN_BUTTON_W // 2,
    (HEIGHT - 60) - RESPAWN_BUTTON_H,
    RESPAWN_BUTTON_W,
    RESPAWN_BUTTON_H
)

# ---------------- PLAYER HP ----------------
PLAYER_MAX_HP = 50

player_hp = PLAYER_MAX_HP
# ---------------- PLAYER HP UPGRADE ----------------

PLAYER_HP_LEVEL = 0

PLAYER_HP_UPGRADE_AMOUNT = 25

hp_upgrade_cost = 1


petal_cooldowns = []

for i in range(PETAL_SLOTS):
    petal_cooldowns.append(0)

# Per-light cooldowns for Light petal (each light has its own cooldown)
light_cooldowns = []
for i in range(PETAL_SLOTS):
    light_cooldowns.append([])

# Per-light HP for Light petal
light_hp = []
for i in range(PETAL_SLOTS):
    light_hp.append([])

# Per-light alive state for Light petal
light_alive = []
for i in range(PETAL_SLOTS):
    light_alive.append([])

# ---------------- PETAL HP ----------------

PETAL_HP = {

    "Basic": 10,

    "Light": 1,

    "Stinger": 1,

    "Heavy": 300,

    "Rose": 1,

    "Wing": 100,

    "Cactus": 60,

    "Leaf": 55,

    "Pea": 2,

    "Missile": 8,

    "Bone": 80,

    "Web": 1,

    "Rock": 250,

    "Faster": 0.01,

    "Magnet": 0.01,

    "Bubble": 0.001,

    "Honey": 0.2,

    "Poison": 60,

    "Shark": 1,

    "Rice": 1,

    "Corn": 110,

    "Stick": 0.2,

    "Clover": 0.5,

    "Glass": 0.6,

    "Antenna": 3000,

    "Pollen": 0.01,

    "Soil": 30,

    "Ant Egg": 1,

    "Sand": 0.01,

    "Lentil": 0.1,

    "Pincer": 1,

    "Shell": 2,

    "Beetle Egg": 1,

    "Third Eye": 30,

    "Cice": 210,

    "Boubloom": 20,

    "Boulder": 50,

    "Moon": 300,

    "Grape": 0.2
}

PETAL_ROT_SPEED_MUL = {
    "Common": 0.5,
    "Unusual": 1,
    "Rare": 3/2,
    "Epic": 4/2,
    "Legendary": 5/2,
    "Mythic": 6/2,
    "Ultra": 7/2,
    "Super": 8/2,
    "Omega": 9/2,
    "Unique": 10/2,
    "Eternal": 11/2,
    "Cosmo": 12/2,
    "Jeddiful": 13/2,
    "Tacnic": 14/2,
    "Radium": 15/2,
    "Ancient": 16/2,
    "Omnient": 17/2,
    "Celestial": 18/2,
    "Infino": 19/2
}
PETAL_RADIUS = 12
petal_angle = 0
petal_self_spin_angle = 0


petal_hp = []
petal_alive = []
petal_max_hp = []
petal_flash_timers = []
petal_respawn_timer = []

petal_respawn_text_timer = []

# Per-slot deploy progress (0..1). When a petal respawns it starts
# at the flower's position and slides out to its orbit slot.
petal_deploy = []

def petal_orbit_distance(i, extra=0):
    # Orbit distance of a petal, scaled by its deploy progress so
    # freshly respawned petals slide out from the flower.
    return (petal_distance + extra) * petal_deploy[i]

def resize_petal_lists():
    # Reset petal_alive based on petal_slots filled status
    while len(petal_alive) < len(petal_slots):
        petal_alive.append(petal_slots[len(petal_alive)]["filled"])
    while len(petal_alive) > len(petal_slots):
        petal_alive.pop()
    # Ensure petal_alive matches petal_slots filled status
    for i in range(min(len(petal_alive), len(petal_slots))):
        petal_alive[i] = petal_slots[i]["filled"]

    while len(petal_hp) < PETAL_SLOTS:
        petal_hp.append(1)
    while len(petal_hp) > PETAL_SLOTS:
        petal_hp.pop()
    while len(petal_alive) < PETAL_SLOTS:
        petal_alive.append(
            petal_slots[len(petal_alive)]["filled"]
            if len(petal_alive) < len(petal_slots)
            else True
        )
    while len(petal_alive) > PETAL_SLOTS:
        petal_alive.pop()
    while len(petal_max_hp) < PETAL_SLOTS:
        petal_max_hp.append(1)
    while len(petal_max_hp) > PETAL_SLOTS:
        petal_max_hp.pop()
    while len(petal_flash_timers) < PETAL_SLOTS:
        petal_flash_timers.append(0)
    while len(petal_flash_timers) > PETAL_SLOTS:
        petal_flash_timers.pop()
    while len(petal_cooldowns) < PETAL_SLOTS:
        petal_cooldowns.append(0)
    while len(petal_cooldowns) > PETAL_SLOTS:
        petal_cooldowns.pop()
    while len(petal_respawn_timer) < PETAL_SLOTS:
        petal_respawn_timer.append(0)
    while len(petal_respawn_timer) > PETAL_SLOTS:
        petal_respawn_timer.pop()
    while len(petal_respawn_text_timer) < PETAL_SLOTS:
        petal_respawn_text_timer.append(0)
    while len(petal_respawn_text_timer) > PETAL_SLOTS:
        petal_respawn_text_timer.pop()
    while len(petal_deploy) < PETAL_SLOTS:
        petal_deploy.append(1.0)
    while len(petal_deploy) > PETAL_SLOTS:
        petal_deploy.pop()
    while len(light_cooldowns) < PETAL_SLOTS:
        light_cooldowns.append([])
    while len(light_cooldowns) > PETAL_SLOTS:
        light_cooldowns.pop()
    while len(light_hp) < PETAL_SLOTS:
        light_hp.append([])
    while len(light_hp) > PETAL_SLOTS:
        light_hp.pop()
    while len(light_alive) < PETAL_SLOTS:
        light_alive.append([])
    while len(light_alive) > PETAL_SLOTS:
        light_alive.pop()


def find_petal_name(text):
    # Find a petal by name, ignoring case and spaces so "antegg"
    # resolves to "Ant Egg" too.
    cleaned = text.lower().replace(" ", "")
    for name in PETAL_HP:
        if name.lower().replace(" ", "") == cleaned:
            return name
    return None


def dev_equip_petal(rarity, petal_name, slot_index):
    # Replace the petal in a single slot (1-based)
    # Match case-insensitively so multi-word names like
    # "ant egg" resolve to "Ant Egg".
    petal_name = find_petal_name(petal_name) or petal_name
    rarity = rarity.capitalize()
    if petal_name not in PETAL_HP:
        show_error(
            f"Invalid petal type. Valid: {', '.join(PETAL_HP.keys())}"
        )
        return False
    if rarity not in RARITIES:
        show_error(f"Invalid rarity. Valid: {', '.join(RARITIES)}")
        return False
    if not 1 <= slot_index <= len(petal_slots):
        show_error(f"Invalid petal slot. Valid: 1-{len(petal_slots)}")
        return False

    i = slot_index - 1
    slot = petal_slots[i]
    slot["filled"] = True
    slot["petal"] = petal_name
    slot["rarity"] = rarity

    resize_petal_lists()

    petal_type = slot["petal"]
    hp = PETAL_HP[petal_type] * PETAL_HP_MULTIPLIER[rarity]
    if petal_type == "Light":
        light_count = get_petal_count(petal_type, rarity)
        if light_count > 0:
            hp /= light_count
        light_count = get_petal_count(petal_type, rarity)
        light_hp[i] = [hp] * light_count
        light_cooldowns[i] = [0] * light_count
        light_alive[i] = [True] * light_count
    else:
        light_hp[i] = []
        light_cooldowns[i] = []
        light_alive[i] = []
    petal_max_hp[i] = hp
    petal_hp[i] = hp
    petal_alive[i] = True
    petal_respawn_timer[i] = 0
    petal_respawn_text_timer[i] = 0
    petal_cooldowns[i] = 0

    save_player()
    return True


def dev_equip_all_petal(rarity, petal_name):
    # Replace every petal slot with the given petal/rarity
    petal_name = find_petal_name(petal_name) or petal_name
    rarity = rarity.capitalize()
    if petal_name not in PETAL_HP:
        show_error(
            f"Invalid petal type. Valid: {', '.join(PETAL_HP.keys())}"
        )
        return False
    if rarity not in RARITIES:
        show_error(f"Invalid rarity. Valid: {', '.join(RARITIES)}")
        return False

    for slot in petal_slots:
        slot["filled"] = True
        slot["petal"] = petal_name
        slot["rarity"] = rarity

    resize_petal_lists()

    for i in range(len(petal_slots)):
        petal_type = petal_slots[i]["petal"]
        hp = PETAL_HP[petal_type] * PETAL_HP_MULTIPLIER[rarity]
        if petal_type == "Light":
            light_count = get_petal_count(petal_type, rarity)
            if light_count > 0:
                hp /= light_count
            light_count = get_petal_count(petal_type, rarity)
            light_hp[i] = [hp] * light_count
            light_cooldowns[i] = [0] * light_count
            light_alive[i] = [True] * light_count
        else:
            light_hp[i] = []
            light_cooldowns[i] = []
            light_alive[i] = []
        petal_max_hp[i] = hp
        petal_hp[i] = hp
        petal_alive[i] = True
        petal_respawn_timer[i] = 0
        petal_respawn_text_timer[i] = 0
        petal_cooldowns[i] = 0

    save_player()
    return True


def dev_empty_slot(slot_index):
    # Empty a single petal slot (1-based) so it does not spawn its petal
    if not 1 <= slot_index <= len(petal_slots):
        show_error(f"Invalid petal slot. Valid: 1-{len(petal_slots)}")
        return False

    i = slot_index - 1
    slot = petal_slots[i]
    slot["filled"] = False
    slot["petal"] = "Basic"
    slot["rarity"] = "Common"

    resize_petal_lists()

    petal_alive[i] = False
    petal_max_hp[i] = 0
    petal_hp[i] = 0
    petal_respawn_timer[i] = 0
    petal_respawn_text_timer[i] = 0
    petal_cooldowns[i] = 0
    light_hp[i] = []
    light_cooldowns[i] = []
    light_alive[i] = []

    save_player()
    return True


def dev_empty_all_slots():
    # Empty every petal slot so no petals spawn
    for slot in petal_slots:
        slot["filled"] = False
        slot["petal"] = "Basic"
        slot["rarity"] = "Common"

    resize_petal_lists()

    for i in range(len(petal_slots)):
        petal_alive[i] = False
        petal_max_hp[i] = 0
        petal_hp[i] = 0
        petal_respawn_timer[i] = 0
        petal_respawn_text_timer[i] = 0
        petal_cooldowns[i] = 0
        light_hp[i] = []
        light_cooldowns[i] = []
        light_alive[i] = []

    save_player()
    return True


def save_muted_users():
    with open("muted.json", "w") as file:
        json.dump(muted_users, file)


def dev_mute_user(target_name, mute):
    # Mute/unmute a user. The developer can never be muted.
    target_key = None
    for existing_name in player_accounts:
        if existing_name.lower() == target_name.lower():
            target_key = existing_name
            break
    if target_key is None:
        show_error(f"No account named {target_name}")
        return False
    if target_key.lower() == "devguard":
        show_error("You can't mute yourself")
        return False

    if mute and target_key not in muted_users:
        muted_users.append(target_key)
        save_muted_users()
        show_error(f"Muted {target_key}")
        return True
    if not mute and target_key in muted_users:
        muted_users.remove(target_key)
        save_muted_users()
        show_error(f"Unmuted {target_key}")
        return True
    show_error(
        f"{target_key} is already "
        + ("muted" if mute else "unmuted")
    )
    return False


def dev_gift_user(target_name, rarity, petal_name, amount):
    # Gift petals straight into a user's saved inventory.
    rarity = rarity.capitalize()
    if petal_name not in PETAL_HP:
        show_error(
            f"Invalid petal type. Valid: {', '.join(PETAL_HP.keys())}"
        )
        return False
    if rarity not in RARITIES:
        show_error(f"Invalid rarity. Valid: {', '.join(RARITIES)}")
        return False
    if amount < 1:
        show_error("Amount must be at least 1")
        return False
    target_key = None
    for existing_name in player_accounts:
        if existing_name.lower() == target_name.lower():
            target_key = existing_name
            break
    if target_key is None:
        show_error(f"No account named {target_name}")
        return False

    user_data = player_data.setdefault(target_key, {})
    user_inventory = user_data.setdefault("inventory", [])
    for item in user_inventory:
        if (
            item.get("petal") == petal_name
            and item.get("rarity") == rarity
        ):
            item["amount"] = int(item.get("amount", 1)) + amount
            break
    else:
        user_inventory.append({
            "petal": petal_name,
            "rarity": rarity,
            "amount": amount
        })

    with open("players.json", "w") as file:
        json.dump(
            player_data,
            file,
            indent=4
        )

    show_error(
        f"Gifted {amount}x {rarity} {petal_name} to {target_key}"
    )
    return True


def dev_take_petal(target_name, rarity, petal_name, amount):
    # Take petals out of a user's saved inventory.
    rarity = rarity.capitalize()
    if petal_name not in PETAL_HP:
        show_error(
            f"Invalid petal type. Valid: {', '.join(PETAL_HP.keys())}"
        )
        return False
    if rarity not in RARITIES:
        show_error(f"Invalid rarity. Valid: {', '.join(RARITIES)}")
        return False
    if amount < 1:
        show_error("Amount must be at least 1")
        return False
    target_key = None
    for existing_name in player_accounts:
        if existing_name.lower() == target_name.lower():
            target_key = existing_name
            break
    if target_key is None:
        show_error(f"No account named {target_name}")
        return False

    user_data = player_data.get(target_key, {})
    user_inventory = user_data.get("inventory", [])
    for item in user_inventory:
        if (
            item.get("petal") == petal_name
            and item.get("rarity") == rarity
        ):
            item["amount"] = int(item.get("amount", 1)) - amount
            if item["amount"] <= 0:
                user_inventory.remove(item)
            with open("players.json", "w") as file:
                json.dump(
                    player_data,
                    file,
                    indent=4
                )
            show_error(
                f"Took {amount}x {rarity} {petal_name} from {target_key}"
            )
            return True
    show_error(
        f"{target_key} has no {rarity} {petal_name}"
    )
    return False


def show_announcement(message):
    # Post the announcement into chat as DevGuard, rendered in red.
    ts = time.time()
    chat_messages.append(("DevGuard", message, ts))
    announcement_times.append(ts)


def dev_kick_user(target_name):
    # Kick the currently logged-in player out to the login screen.
    global game_state

    target_key = None
    for existing_name in player_accounts:
        if existing_name.lower() == target_name.lower():
            target_key = existing_name
            break
    if target_key is None:
        show_error(f"No account named {target_name}")
        return False
    if target_key.lower() == "devguard":
        show_error("You can't kick the developer")
        return False
    if target_key != acc_name_text:
        show_error(
            f"{target_key} is not playing right now"
        )
        return False

    save_player()
    game_state = "login"
    show_error(f"Kicked {target_key}")
    return True


def dev_give_points(target_name, amount):
    # Give upgrade points to a user's saved data.
    target_key = None
    for existing_name in player_accounts:
        if existing_name.lower() == target_name.lower():
            target_key = existing_name
            break
    if target_key is None:
        show_error(f"No account named {target_name}")
        return False
    user_data = player_data.setdefault(target_key, {})
    user_data["upgrade_points"] = (
        int(user_data.get("upgrade_points", 0)) + amount
    )
    with open("players.json", "w") as file:
        json.dump(
            player_data,
            file,
            indent=4
        )
    show_error(f"Gave {amount} points to {target_key}")
    return True


def dev_tp_user(target_name):
    # Teleport to a user's last saved world position.
    global player_x
    global player_y

    target_key = None
    for existing_name in player_accounts:
        if existing_name.lower() == target_name.lower():
            target_key = existing_name
            break
    if target_key is None:
        show_error(f"No account named {target_name}")
        return False
    if target_key == acc_name_text:
        show_error("You can't teleport to yourself")
        return False
    user_data = player_data.get(target_key, {})
    if (
        "player_x" not in user_data
        or "player_y" not in user_data
    ):
        show_error(
            f"{target_key} has no saved position yet"
        )
        return False
    player_x = user_data["player_x"]
    player_y = user_data["player_y"]
    show_error(f"Teleported to {target_key}")
    return True


def dev_self_heal(amount):
    # Heal yourself by the given amount (up to max HP).
    global player_hp

    if amount < 1:
        show_error("Amount must be at least 1")
        return False
    if player_dead:
        show_error("You can't heal while dead")
        return False
    healed = min(amount, PLAYER_MAX_HP - player_hp)
    if healed <= 0:
        show_error("You are already at full HP")
        return False
    player_hp += healed
    show_error(f"Healed {healed} HP")
    return True


def dev_heal_user(target_name, amount, full=False):
    # Heal a user who is currently playing. Since the game runs on one
    # machine, the only player that can be healed is the logged-in one.
    global player_hp

    target_key = None
    for existing_name in player_accounts:
        if existing_name.lower() == target_name.lower():
            target_key = existing_name
            break
    if target_key is None:
        show_error(f"No account named {target_name}")
        return False
    if target_key != acc_name_text:
        show_error(f"{target_key} is not playing right now")
        return False
    if player_dead:
        show_error(f"{target_key} is dead and can't be healed")
        return False

    if full:
        healed = PLAYER_MAX_HP - player_hp
        if healed <= 0:
            show_error(f"{target_key} is already at full HP")
            return False
        player_hp = PLAYER_MAX_HP
        show_error(f"Fully healed {target_key}")
        return True

    if amount < 1:
        show_error("Amount must be at least 1")
        return False
    healed = min(amount, PLAYER_MAX_HP - player_hp)
    if healed <= 0:
        show_error(f"{target_key} is already at full HP")
        return False
    player_hp += healed
    show_error(f"Healed {target_key} by {healed} HP")
    return True


# Kings: one king per mob type (biome regions come later).
kings = {}

# Enemies frozen via /freez_enemies: counts down frames (60 per
# second) and pauses enemy AI while above zero.
enemies_frozen_timer = 0

# True while /p.ghost y is active: enemies can't see the player
# and the flower is drawn semi-transparent.
player_ghost = False

# True while /godmode is active: player cannot take damage or die.
player_godmode = False

# Game theme ('day' or 'night') controlled via /p.theme.
game_theme = "day"

# Game weather ('sunny', 'rainy', 'cloudy', 'snowy', 'hail') via /p.weather.
game_weather = "sunny"
weather_particles = []

# True while /p.mode peaceful is active: mobs do not chase or attack.
game_peaceful_mode = False

# Petal orbit rotation multiplier controlled via /p.petal_speed.
petal_rot_speed_mult = 1.0

# Player movement speed multiplier controlled via /p.speed.
player_speed_mult = 1.0

# HUD visibility (True = show HUD, False = hide HUD) controlled via /hud or /p.hud.
show_hud = True

# Player movement particle trail ('none', 'rainbow', 'fire', 'sparkle') controlled via /p.trail.
player_trail = "none"
player_trail_last_sec = 0.5
player_trail_size_mult = 1.0
player_trail_particles = []

# Magnet mode (True = pull all nearby petal drops toward player) controlled via /magnet_petal_drops.
player_magnet = False
player_magnet_range = None  # None = infinite / whole screen, or a float radius

# Flower center body color controlled via /p.color ('yellow', 'pink', 'cyan', 'black', 'white')
player_color_name = "yellow"
player_body_color = (225, 225, 0)
player_outline_color = (230, 200, 40)
player_face_color = (0, 0, 0)

# Active whirlpools list: [{"x", "y", "initial_damage", "dps", "duration", "max_duration", "radius", "damage_timer", "angle"}]
active_whirlpools = []

# Active black holes: [{"x", "y", "pull_speed", "duration", "max_duration", "radius", "angle"}]
active_blackholes = []

# Active shield domes: [{"x", "y", "radius", "duration", "max_duration", "pulse"}]
active_shield_domes = []

# Dimension / Realm tracking: "regular" (normal biome) or "hole_land"
current_dimension = "regular"
pre_hole_land_x = 25
pre_hole_land_y = 2000
pre_hole_land_grid_color = (60, 180, 75)
hole_land_banner_timer = 0
hole_land_banner_alpha = 0

# How far the king and its minions will chase before giving up.
KING_CHASE_RANGE = 700

# How far from the flower flower minions can spot enemies to hunt.
FLOWER_MINION_SIGHT = 600
# How far minions orbit their king while guarding it.
KING_GUARD_ORBIT = 70
KING_GUARD_SPEED = 3.2

# King rose volley: 8 roses fired every 8 seconds, 45 degrees apart.
KING_ROSE_VOLLEY_COUNT = 8
KING_ROSE_SPEED = 7
# Rose stats scale with the king: damage and heal are one third of
# the king's damage, and the rose is one third of the king's size.
KING_ROSE_SIZE_FRACTION = 3
KING_ROSE_DMG_FRACTION = 3
KING_ROSE_HEAL_FRACTION = 3
KING_ROSE_HOMING_RANGE = 500
KING_ROSE_LIFETIME = 120

# Bee king stinger volley: 10 stingers fired every 8 seconds, 36
# degrees apart (8 * 45 == 10 * 36 == 360). Stinger damage matches
# the bee king's damage, HP is one fourth of the bee king's HP.
KING_STINGER_VOLLEY_COUNT = 10
KING_STINGER_SPEED = 8
KING_STINGER_HP_FRACTION = 4
KING_STINGER_HOMING_RANGE = 500
KING_STINGER_LIFETIME = 120

# Flying king rose projectiles (damage the flower, heal ladybugs).
king_rose_projectiles = []

# Flying bee-king stinger projectiles (damage the flower).
king_stinger_projectiles = []

# Baby ant king's orbiting rice petals. They are killable: the
# flower's petals can shoot them down and they respawn after a bit.
BABY_ANT_RICE_COUNT = 6
BABY_ANT_RICE_RESPAWN = 120
baby_ant_rice = []

# Soldier ant king wing projectile: one giant spinning wing petal
# fired every 6 seconds that chases the flower. HP/damage are 2x
# the king's, and it is 2x bigger than the king.
SOLDIER_WING_INTERVAL = 360
SOLDIER_WING_SPEED = 4
SOLDIER_WING_LIFETIME = 900
soldier_wing_projectiles = []

# Worker ant king's defensive corn: 3 circles of 6 corn around the
# king. Killable by the flower's petals, and they damage the
# flower's petals on contact.
WORKER_CORN_RINGS = 7
WORKER_CORN_PER_RING = 6
WORKER_CORN_RESPAWN = 120
worker_ant_corn = []

# Hornet missiles: fired backward from the hornet's rear when it
# stops near the flower, then they fly at the flower.
HORNET_MISSILE_SPEED = 6
HORNET_MISSILE_LIFETIME = 150
hornet_missiles = []

# Rock projectiles: normal rocks shoot 5 rocks every 8 seconds;
# the rock king shoots 10 every 2 seconds (1/3 of its damage/HP).
ROCK_VOLLEY_COUNT = 5
ROCK_KING_VOLLEY_COUNT = 10
ROCK_VOLLEY_INTERVAL = 480      # 8 seconds
ROCK_KING_VOLLEY_INTERVAL = 120 # 2 seconds
ROCK_PROJECTILE_SPEED = 6
ROCK_PROJECTILE_LIFETIME = 150

# Hole Ladybug yellow orb projectiles
HOLE_LADYBUG_PROJECTILE_SPEED = 7
HOLE_LADYBUG_PROJECTILE_LIFETIME = 140
hole_ladybug_projectiles = []
rock_projectiles = []

# Spider king webs: transparent webs that slow the flower.
KING_WEB_INTERVAL = 120     # every 2 seconds
KING_WEB_LIFETIME = 300     # webs last 5 seconds
KING_WEB_SLOWDOWN = 0.45    # flower moves at 45% speed inside
king_webs = []
player_in_web = False
player_in_web_slowdown = KING_WEB_SLOWDOWN

# Flower projectiles (not made yet): projectiles launched by the flower or its petals.
flower_projectiles = []
player_projectiles = flower_projectiles

# Mob list lookup for king minion AI (class name -> list name).
KING_MOB_LIST_NAMES = {
    "Ladybug": "ladybugs",
    "Bee": "bees",
    "Spider": "spiders",
    "Rock": "rocks",
    "Hornet": "hornets",
    "BabyAnt": "baby_ants",
    "SoldierAnt": "soldier_ants",
    "WorkerAnt": "worker_ants",
    "AntEgg": "ant_eggs",
}

def get_king_mob_list(mob_name):
    list_name = KING_MOB_LIST_NAMES.get(mob_name)
    if list_name is None:
        return []
    return globals().get(list_name, [])


def build_web_surface(radius):
    # Build a transparent spider web: 12 radial spokes plus 4
    # concentric sagging rings, drawn on a SRCALPHA surface.
    size = int(radius * 2) + 8
    web = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size // 2
    cy = size // 2

    spoke_count = 12
    ring_count = 4
    web_color = (240, 240, 240, 110)
    web_outline = (255, 255, 255, 160)

    spokes = []
    for spoke_index in range(spoke_count):
        a = math.radians(
            spoke_index * (360 / spoke_count)
        )
        spokes.append(
            (
                cx + math.cos(a) * radius,
                cy + math.sin(a) * radius
            )
        )
        pygame.draw.line(
            web,
            web_outline,
            (cx, cy),
            spokes[-1],
            4
        )

    # Concentric rings connect between neighboring spokes.
    for ring_index in range(1, ring_count + 1):
        ring_r = radius * ring_index / ring_count
        ring_points = []
        for spoke_index in range(spoke_count):
            a = math.radians(
                spoke_index * (360 / spoke_count)
            )
            # Slight inward sag between spokes.
            sag = 1.0 - 0.08 * math.sin(
                ring_index * 1.7 + spoke_index
            )
            ring_points.append(
                (
                    cx + math.cos(a) * ring_r * sag,
                    cy + math.sin(a) * ring_r * sag
                )
            )
        pygame.draw.lines(
            web,
            web_color,
            False,
            ring_points,
            4
        )

    return web

# Lines a king posts in chat while it is alive.
KING_CHAT_LINES = [
    "you dare enter my land?",
    "my minions will crush you!",
    "i am the king of this biome!",
    "kneel before your king!",
    "you will make a fine snack!",
    "no one defeats the king!",
]

def king_say(mob_name, message):
    # A king posts a chat message.
    king_title = "King Ant Egg" if mob_name == "AntEgg" else f"King {mob_name}"
    chat_messages.append(
        (king_title, message, time.time())
    )

def cleanup_king(enemy):
    # Free the king slot when a king dies, and announce it in chat.
    if getattr(enemy, "is_king", False):
        mob_name = type(enemy).__name__
        kings.pop(mob_name, None)
        enemy.is_king = False
        king_say(mob_name, "i'll be back...")

        # The king's minions die with their king.
        if mob_name == "AntEgg":
            for minion in soldier_ants:
                if (
                    getattr(minion, "is_minion", False)
                    and (
                        getattr(minion, "king_owner", None) is enemy
                        or getattr(minion, "king_mob_name", None) == "AntEgg"
                    )
                ):
                    if not minion.alive or getattr(minion, "death_registered", False):
                        continue
                    minion.death_registered = True
                    minion.dying = True
                    minion.shrink_scale = 1.0
                    minion.full_radius = minion.radius
        else:
            minion_list_name = KING_MOB_LIST_NAMES.get(mob_name)
            if minion_list_name:
                for minion in globals()[minion_list_name]:
                    if not getattr(minion, "is_minion", False):
                        continue
                    if not minion.alive:
                        continue
                    if getattr(minion, "death_registered", False):
                        continue
                    minion.death_registered = True
                    minion.dying = True
                    minion.shrink_scale = 1.0
                    minion.full_radius = minion.radius

        # The king's projectiles die with the king too.
        for projectile_list in (
            king_stinger_projectiles,
            hornet_missiles,
            rock_projectiles,
        ):
            for projectile in projectile_list:
                if projectile.get("owner") is enemy:
                    projectile["dying"] = True
                    projectile["shrink"] = 1.0

        # Roses have no shrink animation, so remove them at once.
        for rose in king_rose_projectiles[:]:
            if rose.get("owner") is enemy:
                king_rose_projectiles.remove(rose)

        # Spider king webs die with the king as well.
        if mob_name == "Spider":
            king_webs.clear()

        # The baby ant king's rice petals die with the king.
        for rice in baby_ant_rice[:]:
            if rice.get("owner") is enemy:
                baby_ant_rice.remove(rice)

        # The soldier ant king's giant wings die with the king.
        for wing in soldier_wing_projectiles:
            if wing.get("owner") is enemy:
                wing["dying"] = True
                wing["shrink"] = 1.0

        # The worker ant king's corn dies with the king.
        for corn in worker_ant_corn[:]:
            if corn.get("owner") is enemy:
                worker_ant_corn.remove(corn)


def dev_revive_user(target_name):
    # Instantly revive a dead player. Since the game runs on one
    # machine, the only player that can be revived is the logged-in
    # one.
    target_key = None
    for existing_name in player_accounts:
        if existing_name.lower() == target_name.lower():
            target_key = existing_name
            break
    if target_key is None:
        show_error(f"{target_name} does not exist")
        return False
    if target_key != acc_name_text:
        show_error(f"{target_key} is not playing right now")
        return False
    if not player_dead:
        show_error(f"{target_key} is not dead")
        return False

    respawn_player()
    show_error(f"Revived {target_key}")
    return True


def dev_freeze_enemies(seconds):
    # Freeze every enemy's AI movement for the given seconds.
    global enemies_frozen_timer

    if seconds < 1:
        show_error("Amount must be at least 1")
        return False
    enemies_frozen_timer = seconds * 60
    show_error(f"Enemies frozen for {seconds} seconds")
    return True


def dev_rarity_to(enemy, rarity):
    # Change the rarity of the enemy under the mouse. The old
    # rarity multipliers are undone before the new ones apply.
    if rarity not in ENEMY_RARITIES:
        show_error(
            f"Invalid rarity. Valid: {', '.join(ENEMY_RARITIES)}"
        )
        return False
    if enemy.rarity == rarity:
        show_error(f"That enemy is already {rarity}")
        return False
    old_rarity = enemy.rarity
    enemy.max_hp /= MOB_HP_MULTIPLIER[old_rarity]
    enemy.damage /= MOB_DAMAGE_MULTIPLIER[old_rarity]
    enemy.radius /= MOB_SIZE_MULTIPLIER[old_rarity]
    enemy.rarity = rarity
    apply_enemy_rarity_stats(enemy)
    show_error(f"The {type(enemy).__name__} is now {rarity}")
    return True


def dev_change_enemy_size(enemy, amount):
    # Grow (positive) or shrink (negative) the enemy under the
    # mouse by [amount] pixels of radius.
    if amount == 0:
        show_error("Amount must not be 0")
        return False
    new_radius = int(enemy.radius + amount)
    if new_radius < 5:
        show_error("The enemy is too small to shrink")
        return False
    enemy.radius = new_radius
    return True


def get_enemy_attack_damage(enemy):
    if getattr(enemy, "custom_damage", None) is not None:
        return enemy.custom_damage
    return enemy.damage * MOB_DAMAGE_MULTIPLIER.get(enemy.rarity, 1.0)


def dev_make_king(enemy):
    # Promote the enemy under the mouse into a king.
    mob_name = type(enemy).__name__

    if getattr(enemy, "is_king", False):
        show_error("That enemy is already a king")
        return False
    if isinstance(enemy, QueenAnt):
        # The queen ant can never be a king, and she never
        # talks in chat.
        show_error("The Queen Ant can't be a king")
        return False
    if mob_name in kings and kings[mob_name].alive:
        show_error(f"There is already a {mob_name} king")
        return False

    enemy.is_king = True
    if enemy.damage == 0:
        enemy.damage = 40
    else:
        enemy.damage = int(enemy.damage * 2)
    if getattr(enemy, "custom_damage", None) is not None:
        enemy.custom_damage = int(enemy.custom_damage * 2)
    enemy.max_hp = int(enemy.max_hp * 2)
    enemy.hp = enemy.max_hp
    enemy.radius = int(enemy.radius * 1.3)
    kings[mob_name] = enemy

    show_error(f"The {mob_name} is now a KING!")
    return True


def king_chase_or_guard(enemy):
    # King AI: chase the player while nearby, otherwise stand ground.
    if player_dead:
        return True

    # Spider kings freeze in place and spin while weaving a web.
    if getattr(enemy, "king_web_spinning", 0) > 0:
        enemy.king_web_spinning -= 1
        enemy.angle = (enemy.angle + 12) % 360
        enemy.speed = 0
        return True

    dist_to_player = distance(
        enemy.x,
        enemy.y,
        player_x,
        player_y
    )

    if dist_to_player <= KING_CHASE_RANGE:
        # Slow, relentless march toward the flower.
        target_angle = math.degrees(
            math.atan2(
                player_y - enemy.y,
                player_x - enemy.x
            )
        )
        enemy.turn_to(target_angle, 4)
        enemy.speed = enemy.max_speed * 3.1
        rad = math.radians(enemy.angle)
        move_with_collision(
            enemy,
            math.cos(rad) * enemy.speed * 0.15,
            math.sin(rad) * enemy.speed * 0.15
        )

        # The king bumps his own minions aside as he advances.
        for other in ladybugs:
            if not getattr(other, "is_minion", False):
                continue
            if not other.alive:
                continue
            d = distance(
                enemy.x,
                enemy.y,
                other.x,
                other.y
            )
            min_dist = enemy.radius + other.radius
            if 0 < d < min_dist:
                overlap = min_dist - d
                other.x += (
                    (other.x - enemy.x) / d * overlap
                )
                other.y += (
                    (other.y - enemy.y) / d * overlap
                )
        return True

    # Player escaped: stop chasing, hold position.
    enemy.speed = 0
    return False


def minion_ai(minion):
    # Minion AI for one minion: chase with the king,
    # or orbit and guard it.

    king = getattr(minion, "king_owner", None)
    if king is None or not king.alive:
        king = kings.get(getattr(minion, "king_mob_name", type(minion).__name__))
    has_king = (
        king is not None
        and king.alive
    )

    # Minions follow the king's decision: if the king is chasing,
    # they charge too; once the king gives up, they fall back and
    # orbit around him.
    king_chasing = (
        has_king
        and not player_dead
        and distance(
            king.x,
            king.y,
            player_x,
            player_y
        ) <= KING_CHASE_RANGE
    )

    if king_chasing:
        # Much faster than the king: charge the flower.
        target_angle = math.degrees(
            math.atan2(
                player_y - minion.y,
                player_x - minion.x
            )
        )
        minion.turn_to(target_angle, 6)
        # Three times the king's chase speed so the
        # difference is clearly visible.
        king_speed = getattr(king, "max_speed", None)
        if king_speed is None or king_speed <= 0:
            king_speed = 1.0
        minion.speed = king_speed * 3.1 * 3
        rad = math.radians(minion.angle)
        move_with_collision(
            minion,
            math.cos(rad) * minion.speed * 0.15,
            math.sin(rad) * minion.speed * 0.15
        )
        if hasattr(minion, "wing_phase"):
            minion.wing_phase += 0.85

        # Bounce off other minions when they bump while chasing.
        search_list = (
            soldier_ants
            if getattr(minion, "king_mob_name", None) == "AntEgg"
            else get_king_mob_list(type(minion).__name__)
        )
        for other in search_list:
            if other is minion:
                continue
            if not getattr(other, "is_minion", False):
                continue
            if not other.alive:
                continue
            d = distance(
                minion.x,
                minion.y,
                other.x,
                other.y
            )
            min_dist = minion.radius + other.radius
            if 0 < d < min_dist:
                overlap = (min_dist - d) / 2
                minion.x += (
                    (minion.x - other.x) / d * overlap * 2
                )
                minion.y += (
                    (minion.y - other.y) / d * overlap * 2
                )

        # Bounce off the king when chasing, so minions never
        # stack up on top of him.
        kd = distance(
            minion.x,
            minion.y,
            king.x,
            king.y
        )
        king_min_dist = king.radius + minion.radius
        if 0 < kd < king_min_dist:
            overlap = king_min_dist - kd
            minion.x += (
                (minion.x - king.x) / kd * overlap * 2
            )
            minion.y += (
                (minion.y - king.y) / kd * overlap * 2
            )
        return

    # Out of range (or no king): return to the king and orbit it.
    if has_king:
        # The orbit ring scales with the king's size, so bigger
        # kings get a wider guard ring. The +40 gap keeps minions
        # from ever touching the king's body.
        king_orbit = max(
            KING_GUARD_ORBIT,
            int(king.radius * 1.6) + 40
        )

        # Current angle of the minion around the king.
        cur_angle = math.atan2(
            minion.y - king.y,
            minion.x - king.x
        )

        # Slide around the ring over time (guard orbit).
        orbit_slot = getattr(minion, "king_orbit_slot", 0)
        orbit_angle = (
            time.time() * 1.2
            + orbit_slot * (2 * math.pi / 10)
        )

        # Always march FORWARD around the ring. When the minion is
        # behind its slot it speeds up to catch it; when ahead it
        # crawls, so it never walks backward.
        angle_behind = (
            (orbit_angle - cur_angle)
            % (2 * math.pi)
        )
        angle_step = 0.02 + min(angle_behind, 1.5) * 0.03
        new_angle = cur_angle + angle_step

        target_x = (
            king.x
            + math.cos(new_angle) * king_orbit
        )
        target_y = (
            king.y
            + math.sin(new_angle) * king_orbit
        )

        # Move straight toward the ring point at a decent pace.
        dx = target_x - minion.x
        dy = target_y - minion.y
        length = math.sqrt(dx * dx + dy * dy)
        step = KING_GUARD_SPEED * 2.5

        # Slow down when another minion is close ahead on the ring.
        # The closer the minion in front, the bigger the slowdown.
        # Overlapping minions bounce apart from each other.
        separation = minion.radius * 2.2
        bounce_x = 0.0
        bounce_y = 0.0
        search_list = (
            soldier_ants
            if getattr(minion, "king_mob_name", None) == "AntEgg"
            else get_king_mob_list(type(minion).__name__)
        )
        for other in search_list:
            if other is minion:
                continue
            if not getattr(other, "is_minion", False):
                continue
            if not other.alive:
                continue
            d = distance(
                minion.x,
                minion.y,
                other.x,
                other.y
            )
            if d < separation and d > 0:
                # 0 when touching, up to 1 when just at the
                # separation distance.
                closeness = 1.0 - (d / separation)
                step *= 1.0 - closeness * 0.9
                # Bounce away from the minion we bumped into.
                min_dist = minion.radius + other.radius
                if d < min_dist:
                    overlap = (min_dist - d) / 2
                    bounce_x += (
                        (minion.x - other.x) / d * overlap
                    )
                    bounce_y += (
                        (minion.y - other.y) / d * overlap
                    )

        if length > step:
            minion.x += dx / length * step
            minion.y += dy / length * step
        else:
            minion.x = target_x
            minion.y = target_y

        if hasattr(minion, "wing_phase"):
            minion.wing_phase += 0.4

        # Apply the bounce push away from bumped minions.
        if bounce_x or bounce_y:
            minion.x += bounce_x * 2
            minion.y += bounce_y * 2

        # Bounce away from the king if we're pressed against him.
        king_min_dist = king.radius + minion.radius + 4
        kd = distance(
            minion.x,
            minion.y,
            king.x,
            king.y
        )
        if 0 < kd < king_min_dist:
            overlap = king_min_dist - kd
            minion.x += (
                (minion.x - king.x) / kd * overlap
            )
            minion.y += (
                (minion.y - king.y) / kd * overlap
            )

        # Face the direction of travel around the ring.
        minion.angle = math.degrees(new_angle + math.pi / 2)
        minion.speed = 0


def fire_king_rose_volley(king):
    # The king fires 8 rose petals, one every 45 degrees.
    rose_radius = max(4, int(king.radius / KING_ROSE_SIZE_FRACTION))
    # Rose damage/heal matches a minion's damage (1/3 of the king),
    # and the rose has a minion's HP so petals can destroy it.
    rose_damage = max(1, int(king.damage / 3))
    rose_heal = max(1, int(king.damage / 3))
    rose_hp = max(1, int(king.max_hp / 3))
    for rose_index in range(KING_ROSE_VOLLEY_COUNT):
        rose_angle = (
            king.angle
            + rose_index * 45
        )
        rad = math.radians(rose_angle)
        king_rose_projectiles.append(
            {
                "x": king.x,
                "y": king.y,
                "angle": rose_angle,
                "dx": math.cos(rad) * KING_ROSE_SPEED,
                "dy": math.sin(rad) * KING_ROSE_SPEED,
                "damage": rose_damage,
                "heal": rose_heal,
                "radius": rose_radius,
                "hp": rose_hp,
                "max_hp": rose_hp,
                "has_homed": False,
                "timer": KING_ROSE_LIFETIME,
                "owner": king
            }
        )


def fire_king_stinger_volley(king):
    # The bee king fires 10 stinger petals, one every 36 degrees.
    # Each stinger has the king's damage and one fourth of the
    # king's HP, and homes in on the flower once it "sees" it.
    stinger_damage = int(king.damage)
    stinger_hp = max(1, int(king.max_hp / KING_STINGER_HP_FRACTION))
    stinger_radius = max(4, int(king.radius / 3))
    for stinger_index in range(KING_STINGER_VOLLEY_COUNT):
        stinger_angle = (
            king.angle
            + stinger_index * (360 / KING_STINGER_VOLLEY_COUNT)
        )
        rad = math.radians(stinger_angle)
        king_stinger_projectiles.append(
            {
                "x": king.x,
                "y": king.y,
                "angle": stinger_angle,
                "dx": math.cos(rad) * KING_STINGER_SPEED,
                "dy": math.sin(rad) * KING_STINGER_SPEED,
                "damage": stinger_damage,
                "radius": stinger_radius,
                "hp": stinger_hp,
                "max_hp": stinger_hp,
                "has_homed": False,
                "timer": KING_STINGER_LIFETIME,
                "owner": king
            }
        )


def projectile_hits_flower(projectile, damage):
    # Enemy projectiles don't pop instantly when they touch the
    # flower. They grind against it, losing HP over time, and they
    # only die when their HP bar actually reaches 0.
    global player_hp
    global player_bounce_x
    global player_bounce_y

    # The projectile pushes the flower like enemies do.
    # While ghosted the flower can't be pushed at all.
    if not player_ghost:
        push_dx = player_x - projectile["x"]
        push_dy = player_y - projectile["y"]
        push_len = math.sqrt(push_dx * push_dx + push_dy * push_dy)
        if push_len == 0:
            push_dx = 1
            push_len = 1
        player_bounce_x = push_dx / push_len * 6.0
        player_bounce_y = push_dy / push_len * 6.0

    # Drain the projectile's HP while it touches the flower
    # (about 1 second of contact to wear it down fully).
    projectile["hp"] -= max(
        1,
        projectile.get("max_hp", 1) // 60
    )

    # Damage the flower in pulses instead of every frame.
    projectile["touch_timer"] = (
        projectile.get("touch_timer", 0) - 1
    )
    if (
        projectile["touch_timer"] <= 0
        and not player_ghost
        and not player_godmode
        and not game_peaceful_mode
    ):
        projectile["touch_timer"] = 30
        player_hp -= (
            damage
            * MOB_DAMAGE_MULTIPLIER.get(
                projectile["owner"].rarity,
                1.0
            )
        )

        if player_hp < 0:
            player_hp = 0

        if player_hp == 0:
            class _ProjectileKiller:
                __class__ = type(projectile["owner"])
                rarity = projectile["owner"].rarity
                x = projectile["x"]
                y = projectile["y"]

            kill_player(_ProjectileKiller)

    return projectile["hp"] <= 0


def draw_projectile_hp_bar(sx, sy, radius, hp, max_hp):
    # Small HP bar above an enemy projectile so the drain is
    # visible while it grinds against the flower.
    if max_hp <= 0 or hp >= max_hp:
        return
    bar_width = max(20, int(radius * 1.6))
    bar_height = 4
    bar_x = int(sx - bar_width / 2)
    bar_y = int(sy - radius - 12)
    pygame.draw.rect(
        screen,
        (80, 80, 80),
        (bar_x, bar_y, bar_width, bar_height)
    )
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        (
            bar_x,
            bar_y,
            int(bar_width * max(0.0, min(1.0, hp / max_hp))),
            bar_height
        )
    )


def projectile_hits_petals(projectile, damage, hit_radius):
    # Enemy projectiles also chip away at the flower's petals when
    # they touch them, the same way mobs do.
    total_elements = 0
    for i in range(PETAL_SLOTS):
        if not petal_alive[i]:
            continue
        if petal_slots[i]["petal"] == "Light":
            total_elements += get_petal_count(
                "Light",
                petal_slots[i]["rarity"]
            )
        else:
            total_elements += 1
    if total_elements <= 0:
        return

    angle_increment = 360 / total_elements
    element_index = 0

    for i in range(PETAL_SLOTS):
        if not petal_alive[i]:
            continue

        petal_type = petal_slots[i]["petal"]
        petal_distance_extra = (
            40 if petal_slots[i]["petal"] == "Moon" else 0
        )

        if petal_type == "Light":
            light_count = get_petal_count(
                "Light",
                petal_slots[i]["rarity"]
            )
            for li in range(light_count):
                if not light_alive[i][li]:
                    continue
                light_angle = math.radians(
                    petal_angle
                    + (element_index + li) * angle_increment
                )
                light_x = (
                    player_x
                    + math.cos(light_angle)
                    * petal_orbit_distance(i)
                )
                light_y = (
                    player_y
                    + math.sin(light_angle)
                    * petal_orbit_distance(i)
                )
                if distance(
                    projectile["x"],
                    projectile["y"],
                    light_x,
                    light_y
                ) <= PETAL_RADIUS + hit_radius:
                    light_hp[i][li] -= damage
                    if light_hp[i][li] <= 0:
                        light_alive[i][li] = False
                        light_cooldowns[i][li] = (
                            PETAL_RELOAD["Light"]
                        )
        else:
            angle = math.radians(
                petal_angle + element_index * angle_increment
            )
            petal_world_x = (
                player_x
                + math.cos(angle)
                * petal_orbit_distance(i, petal_distance_extra)
            )
            petal_world_y = (
                player_y
                + math.sin(angle)
                * petal_orbit_distance(i, petal_distance_extra)
            )
            if petal_alive[i] and distance(
                projectile["x"],
                projectile["y"],
                petal_world_x,
                petal_world_y
            ) <= PETAL_RADIUS + hit_radius:
                petal_hp[i] -= damage
                if petal_hp[i] <= 0:
                    petal_hp[i] = 0
                    petal_alive[i] = False
                    petal_respawn_timer[i] = PETAL_RELOAD[
                        petal_slots[i]["petal"]
                    ]

        element_index += 1


def update_king_stingers():
    # Move the bee king's stingers; they home toward the flower once
    # and damage it on contact. Petals can destroy them.
    global player_hp

    for stinger in king_stinger_projectiles[:]:

        if stinger.get("dying"):
            stinger["shrink"] -= 0.18
            if stinger["shrink"] <= 0:
                king_stinger_projectiles.remove(stinger)
            continue

        stinger["timer"] -= 1

        if stinger["timer"] <= 0:
            king_stinger_projectiles.remove(stinger)
            continue

        # Once a stinger "sees" the flower it actively chases it,
        # re-aiming every frame while the flower stays within its
        # sight range. If the flower escapes, the stinger flies
        # straight in its last direction.
        dist_to_flower = distance(
            stinger["x"],
            stinger["y"],
            player_x,
            player_y
        )

        stinger_sees = (
            not player_dead
            and dist_to_flower <= KING_STINGER_HOMING_RANGE
        )

        if (
            not stinger["has_homed"]
            and stinger_sees
        ):
            stinger["has_homed"] = True

        if stinger["has_homed"] and stinger_sees:
            chase_angle = math.atan2(
                player_y - stinger["y"],
                player_x - stinger["x"]
            )
            stinger["dx"] = (
                math.cos(chase_angle) * KING_STINGER_SPEED
            )
            stinger["dy"] = (
                math.sin(chase_angle) * KING_STINGER_SPEED
            )

        stinger["x"] += stinger["dx"]
        stinger["y"] += stinger["dy"]

        # Prevent stinger from going past map boundaries
        stinger_hit_radius = stinger.get("radius", 8)
        stinger["x"] = max(stinger_hit_radius, min(stinger["x"], WORLD_WIDTH - stinger_hit_radius))
        stinger["y"] = max(stinger_hit_radius, min(stinger["y"], WORLD_HEIGHT - stinger_hit_radius))
        if (
            stinger["x"] <= stinger_hit_radius
            or stinger["x"] >= WORLD_WIDTH - stinger_hit_radius
            or stinger["y"] <= stinger_hit_radius
            or stinger["y"] >= WORLD_HEIGHT - stinger_hit_radius
        ):
            stinger["dying"] = True
            stinger["shrink"] = 1.0

        # Stingers chip the flower's petals too.
        projectile_hits_petals(
            stinger,
            stinger["damage"],
            stinger.get("radius", 8)
        )

        stinger_hit_radius = stinger.get("radius", 8)

        # Stingers damage the flower (and grind down against it).
        if (
            not player_dead
            and distance(
                stinger["x"],
                stinger["y"],
                player_x,
                player_y
            ) <= PLAYER_RADIUS + stinger_hit_radius
        ):
            if projectile_hits_flower(
                stinger,
                stinger["damage"]
            ):
                stinger["dying"] = True
                stinger["shrink"] = 1.0


def baby_ant_rice_pos(rice):
    # World position of a rice petal on its king's orbit ring.
    king = rice["owner"]
    rice_orbit = king.radius * 1.8
    rice_angle = math.radians(
        time.time() * 90
        + rice["slot"] * (360 / BABY_ANT_RICE_COUNT)
    )
    return (
        king.x + math.cos(rice_angle) * rice_orbit,
        king.y + math.sin(rice_angle) * rice_orbit
    )


def update_baby_ant_rice():
    # Keep six killable rice petals orbiting every baby ant king.
    king = kings.get("BabyAnt")
    if (
        king is not None
        and king.__class__.__name__ == "BabyAnt"
        and king.alive
    ):
        existing_slots = [
            rice["slot"]
            for rice in baby_ant_rice
            if rice["owner"] is king
        ]
        for slot in range(BABY_ANT_RICE_COUNT):
            if slot in existing_slots:
                continue
            rice_hp = max(1, int(king.max_hp / 10))
            baby_ant_rice.append(
                {
                    "owner": king,
                    "slot": slot,
                    "hp": rice_hp,
                    "max_hp": rice_hp,
                    "radius": 8,
                    "dying": False,
                    "shrink": 1.0,
                    "respawn": 0,
                }
            )

    for rice in baby_ant_rice[:]:
        king = rice["owner"]
        # Drop rices whose king is gone.
        if (
            kings.get("BabyAnt") is not king
            or not king.alive
        ):
            baby_ant_rice.remove(rice)
            continue

        if rice.get("dying"):
            rice["shrink"] -= 0.18
            if rice["shrink"] <= 0:
                rice["dying"] = False
                rice["shrink"] = 1.0
                rice["respawn"] = BABY_ANT_RICE_RESPAWN
            continue

        if rice["respawn"] > 0:
            rice["respawn"] -= 1
            continue

        rice["x"], rice["y"] = baby_ant_rice_pos(rice)
        rice_r = rice.get("radius", 8)
        rice["x"] = max(rice_r, min(rice["x"], WORLD_WIDTH - rice_r))
        rice["y"] = max(rice_r, min(rice["y"], WORLD_HEIGHT - rice_r))

        # Rice also damages the flower on contact (grinding down).
        if (
            not player_dead
            and distance(
                rice["x"],
                rice["y"],
                player_x,
                player_y
            ) <= PLAYER_RADIUS + rice.get("radius", 8)
        ):
            if projectile_hits_flower(
                rice,
                king.damage
            ):
                rice["dying"] = True
                rice["shrink"] = 1.0


def fire_soldier_wing(king):
    # The soldier ant king fires one giant spinning wing petal with
    # 2x the king's HP and 2x the king's damage. It is 2x bigger
    # than the king and chases the flower.
    soldier_wing_projectiles.append(
        {
            "x": king.x,
            "y": king.y,
            "dx": SOLDIER_WING_SPEED,
            "dy": 0,
            "damage": max(1, int(king.damage * 2)),
            "hp": max(1, int(king.max_hp * 2)),
            "max_hp": max(1, int(king.max_hp * 2)),
            "radius": king.radius * 2,
            "spin": random.uniform(0, 360),
            "spin_speed": 12,
            "timer": SOLDIER_WING_LIFETIME,
            "owner": king,
        }
    )


def update_soldier_wings():
    # Giant soldier ant king wings spin and chase the flower.
    global player_hp

    for wing in soldier_wing_projectiles[:]:

        # Dying wings shrink away fast.
        if wing.get("dying"):
            wing["shrink"] -= 0.12
            if wing["shrink"] <= 0:
                soldier_wing_projectiles.remove(wing)
            continue

        wing["timer"] -= 1

        if wing["timer"] <= 0:
            wing["dying"] = True
            wing["shrink"] = 1.0
            continue

        wing["spin"] = (
            (wing["spin"] + wing["spin_speed"]) % 360
        )

        # Chase the flower.
        if not player_dead:
            chase_angle = math.degrees(
                math.atan2(
                    player_y - wing["y"],
                    player_x - wing["x"]
                )
            )
            rad = math.radians(chase_angle)
            wing["dx"] = math.cos(rad) * SOLDIER_WING_SPEED
            wing["dy"] = math.sin(rad) * SOLDIER_WING_SPEED

        wing["x"] += wing["dx"]
        wing["y"] += wing["dy"]

        # Prevent soldier wing from going past map boundaries
        wing_r = wing.get("radius", 8)
        wing["x"] = max(wing_r, min(wing["x"], WORLD_WIDTH - wing_r))
        wing["y"] = max(wing_r, min(wing["y"], WORLD_HEIGHT - wing_r))

        # The giant wing chips the flower's petals too.
        projectile_hits_petals(
            wing,
            wing.get("damage", 10),
            wing.get("radius", 8)
        )

        # Damage the flower on contact (and grind down against it).
        if (
            not player_dead
            and distance(
                wing["x"],
                wing["y"],
                player_x,
                player_y
            ) <= PLAYER_RADIUS + wing["radius"] * 0.7
        ):
            if projectile_hits_flower(
                wing,
                wing.get("damage", 10)
            ):
                wing["dying"] = True
                wing["shrink"] = 1.0


def worker_corn_ring_count(king):
    # How many corn rings a worker ant king gets, by rarity:
    # one extra ring every 2 rarity tiers, capped at 7.
    rarity_order = [
        "Common", "Unusual", "Rare", "Epic", "Legendary",
        "Mythic", "Ultra", "Super", "Omega", "Unique",
        "Eternal", "Cosmo", "Jeddiful", "Tacnic", "Radium",
        "Ancient", "Omnient", "Celestial", "Infino"
    ]
    tier = 0
    if king.rarity in rarity_order:
        tier = rarity_order.index(king.rarity)
    return max(1, min(WORKER_CORN_RINGS, 1 + tier // 2))


def worker_corn_pos(corn):
    # World position of a corn on its king's rings. Each ring spins
    # at its own speed (degrees per second).
    king = corn["owner"]
    ring_speeds = (
        45, 80, 115, 150, 185, 220, 255
    )
    corn_orbit = (
        king.radius * 1.8
        + corn["ring"] * (king.radius * 1.1 + 8)
    )
    corn_angle = math.radians(
        time.time() * ring_speeds[corn["ring"]]
        + corn["slot"] * (360 / WORKER_CORN_PER_RING)
    )
    return (
        king.x + math.cos(corn_angle) * corn_orbit,
        king.y + math.sin(corn_angle) * corn_orbit
    )


def update_worker_ant_corn():
    # Keep 3 circles of 6 corn orbiting every worker ant king.
    king = kings.get("WorkerAnt")
    if (
        king is not None
        and king.__class__.__name__ == "WorkerAnt"
        and king.alive
    ):
        existing = [
            (corn["ring"], corn["slot"])
            for corn in worker_ant_corn
            if corn["owner"] is king
        ]
        ring_count = worker_corn_ring_count(king)
        for ring in range(ring_count):
            for slot in range(WORKER_CORN_PER_RING):
                if (ring, slot) in existing:
                    continue
                # Corn damage is 1/2 of the king's damage, and its
                # HP equals that same amount.
                corn_damage = max(1, int(king.damage / 2))
                worker_ant_corn.append(
                    {
                        "owner": king,
                        "ring": ring,
                        "slot": slot,
                        "hp": corn_damage,
                        "max_hp": corn_damage,
                        "damage": corn_damage,
                        "radius": 10,
                        "x": king.x,
                        "y": king.y,
                        "dying": False,
                        "shrink": 1.0,
                        "respawn": 0,
                    }
                )

    for corn in worker_ant_corn[:]:
        king = corn["owner"]
        if (
            kings.get("WorkerAnt") is not king
            or not king.alive
        ):
            worker_ant_corn.remove(corn)
            continue

        if corn.get("dying"):
            corn["shrink"] -= 0.18
            if corn["shrink"] <= 0:
                corn["dying"] = False
                corn["shrink"] = 1.0
                corn["respawn"] = WORKER_CORN_RESPAWN
            continue

        if corn["respawn"] > 0:
            corn["respawn"] -= 1
            continue

        corn["x"], corn["y"] = worker_corn_pos(corn)
        corn_r = corn.get("radius", 10)
        corn["x"] = max(corn_r, min(corn["x"], WORLD_WIDTH - corn_r))
        corn["y"] = max(corn_r, min(corn["y"], WORLD_HEIGHT - corn_r))

        # Corn also damages the flower on contact (grinding down).
        if (
            not player_dead
            and distance(
                corn["x"],
                corn["y"],
                player_x,
                player_y
            ) <= PLAYER_RADIUS + corn["radius"]
        ):
            if projectile_hits_flower(
                corn,
                corn["damage"]
            ):
                corn["dying"] = True
                corn["shrink"] = 1.0

        # Corn damages the flower's petals on contact.
        projectile_hits_petals(
            corn,
            corn["damage"],
            corn["radius"]
        )


def update_king_roses():
    # Move the king's roses; they hurt the flower and heal
    # ladybugs (including the king and minions).
    global player_hp

    for rose in king_rose_projectiles[:]:

        rose["timer"] -= 1

        if rose["timer"] <= 0:
            king_rose_projectiles.remove(rose)
            continue

        # Once the rose spots the flower it locks on and shoots
        # itself toward it — but only once per rose.
        if (
            not rose["has_homed"]
            and not player_dead
            and distance(
                rose["x"],
                rose["y"],
                player_x,
                player_y
            ) <= KING_ROSE_HOMING_RANGE
        ):
            rose["has_homed"] = True
            home_angle = math.atan2(
                player_y - rose["y"],
                player_x - rose["x"]
            )
            rose["dx"] = math.cos(home_angle) * KING_ROSE_SPEED
            rose["dy"] = math.sin(home_angle) * KING_ROSE_SPEED

        rose["x"] += rose["dx"]
        rose["y"] += rose["dy"]

        # Prevent king rose from going past map boundaries
        rose_r = rose.get("radius", 8)
        rose["x"] = max(rose_r, min(rose["x"], WORLD_WIDTH - rose_r))
        rose["y"] = max(rose_r, min(rose["y"], WORLD_HEIGHT - rose_r))
        if (
            rose["x"] <= rose_r
            or rose["x"] >= WORLD_WIDTH - rose_r
            or rose["y"] <= rose_r
            or rose["y"] >= WORLD_HEIGHT - rose_r
        ):
            king_rose_projectiles.remove(rose)
            continue

        # Roses chip the flower's petals too.
        projectile_hits_petals(
            rose,
            rose["damage"],
            rose.get("radius", 8)
        )

        hit_something = False

        rose_hit_radius = rose.get("radius", 8)

        # Roses damage the flower (and grind down against it).
        if (
            not player_dead
            and distance(
                rose["x"],
                rose["y"],
                player_x,
                player_y
            ) <= PLAYER_RADIUS + rose_hit_radius
        ):
            if projectile_hits_flower(
                rose,
                rose["damage"]
            ):
                hit_something = True

        # Roses heal ladybugs on contact. Minions get healed and
        # the rose bounces away from them. Regular ladybugs absorb
        # the rose; the king is immune to rose healing and the rose
        # passes through him.
        if not hit_something:
            for bug in ladybugs:
                if not bug.alive:
                    continue
                if getattr(bug, "is_king", False):
                    continue
                d = distance(
                    rose["x"],
                    rose["y"],
                    bug.x,
                    bug.y
                )
                if d <= bug.radius + rose_hit_radius:
                    if bug.hp < bug.max_hp:
                        bug.hp = min(
                            bug.max_hp,
                            bug.hp + rose["heal"]
                        )
                    if (
                        getattr(bug, "is_minion", False)
                        or not getattr(bug, "is_king", False)
                    ) and d > 0:
                        # Bounce the rose away from the minion, and
                        # from ladybugs that don't belong to the king.
                        away_x = (rose["x"] - bug.x) / d
                        away_y = (rose["y"] - bug.y) / d
                        rose["x"] = (
                            bug.x
                            + away_x
                            * (bug.radius + rose_hit_radius + 2)
                        )
                        rose["y"] = (
                            bug.y
                            + away_y
                            * (bug.radius + rose_hit_radius + 2)
                        )
                        speed = math.sqrt(
                            rose["dx"] ** 2 + rose["dy"] ** 2
                        )
                        rose["dx"] = away_x * speed
                        rose["dy"] = away_y * speed
                    break

        if hit_something:
            king_rose_projectiles.remove(rose)


def get_web_slowdown(rarity):
    # Web slowdown by spider rarity: 45% speed for Common,
    # down to 10% speed for the rarest kings.
    rarity_order = [
        "Common", "Unusual", "Rare", "Epic", "Legendary",
        "Mythic", "Ultra", "Super", "Omega", "Unique",
        "Eternal", "Cosmo", "Jeddiful", "Tacnic", "Radium",
        "Ancient", "Omnient", "Celestial", "Infino"
    ]
    if rarity in rarity_order:
        tier = rarity_order.index(rarity)
    else:
        tier = 0
    slowdown = 0.45 - tier * 0.018
    return max(0.10, slowdown)


def fire_rock_volley(rock, is_king):
    # Rocks shoot a spread of rock projectiles at the flower.
    # Normal rocks: 5 every 8s. Rock kings: 10 every 2s, with
    # damage/HP equal to 1/3 of the rock king's.
    if is_king:
        count = ROCK_KING_VOLLEY_COUNT
        damage = max(1, int(rock.damage / 3))
        projectile_hp = max(1, int(rock.max_hp / 3))
        radius = max(4, int(rock.radius / 3))
    else:
        count = ROCK_VOLLEY_COUNT
        damage = max(1, int(rock.damage / 3))
        projectile_hp = max(1, int(rock.max_hp / 3))
        radius = max(4, int(rock.radius / 3))

    # Aim the spread at the flower: center the volley on the
    # direction to the flower so the rocks spread out around it.
    base_angle = math.degrees(
        math.atan2(
            player_y - rock.y,
            player_x - rock.x
        )
    )

    is_hole = getattr(rock, "is_hole_land_mob", False) or type(rock).__name__ == "HoleRock"

    for rock_index in range(count):
        rock_angle = (
            base_angle
            + rock_index * (360 / count)
        )
        rad = math.radians(rock_angle)

        if is_hole:
            # 80% spikier void shard silhouette
            point_count = random.randint(12, 16)
            shape_points = []
            for point_i in range(point_count):
                point_angle = (
                    math.pi * 2 * point_i / point_count
                    + random.uniform(-0.15, 0.15)
                )
                point_dist = random.uniform(1.65, 2.15) if point_i % 2 == 1 else random.uniform(0.45, 0.65)
                shape_points.append(
                    (
                        math.cos(point_angle) * point_dist,
                        math.sin(point_angle) * point_dist
                    )
                )
        else:
            # Random rocky silhouette for normal rock projectile.
            point_count = random.randint(6, 8)
            shape_points = []
            for point_i in range(point_count):
                point_angle = (
                    math.pi * 2 * point_i / point_count
                    + random.uniform(-0.35, 0.35)
                )
                point_distance = random.uniform(0.82, 1.15)
                shape_points.append(
                    (
                        math.cos(point_angle) * point_distance,
                        math.sin(point_angle) * point_distance
                    )
                )

        rock_projectiles.append(
            {
                "x": rock.x,
                "y": rock.y,
                "angle": rock_angle,
                "dx": math.cos(rad) * ROCK_PROJECTILE_SPEED,
                "dy": math.sin(rad) * ROCK_PROJECTILE_SPEED,
                "damage": damage,
                "radius": radius,
                "hp": projectile_hp,
                "max_hp": projectile_hp,
                "shape": shape_points,
                "is_king_shot": is_king,
                "is_hole_projectile": is_hole,
                "timer": ROCK_PROJECTILE_LIFETIME,
                "owner": rock
            }
        )


def generic_minion_ai(minion):
    # Baby ant king minions: chase with the king at 3x the king's
    # speed; when the king stops chasing, return to the king and
    # orbit him. HP is 1/5 of the king's, damage 1/3 (set at spawn).
    king = kings.get(type(minion).__name__)
    has_king = (
        king is not None
        and king.alive
    )

    king_chasing = (
        has_king
        and not player_dead
        and distance(
            king.x,
            king.y,
            player_x,
            player_y
        ) <= KING_CHASE_RANGE
    )

    if king_chasing:
        target_angle = math.degrees(
            math.atan2(
                player_y - minion.y,
                player_x - minion.x
            )
        )
        minion.turn_to(target_angle, 7)
        minion.speed = king.max_speed * 3.1 * 3
        rad = math.radians(minion.angle)
        move_with_collision(
            minion,
            math.cos(rad) * minion.speed * 0.15,
            math.sin(rad) * minion.speed * 0.15
        )

        # Bounce off other minions and the king.
        for other in get_king_mob_list(type(minion).__name__):
            if other is minion:
                continue
            if not other.alive:
                continue
            d = distance(
                minion.x,
                minion.y,
                other.x,
                other.y
            )
            min_dist = minion.radius + other.radius
            if 0 < d < min_dist:
                overlap = (min_dist - d) / 2
                minion.x += (
                    (minion.x - other.x) / d * overlap * 2
                )
                minion.y += (
                    (minion.y - other.y) / d * overlap * 2
                )

        kd = distance(
            minion.x,
            minion.y,
            king.x,
            king.y
        )
        king_min_dist = king.radius + minion.radius
        if 0 < kd < king_min_dist:
            overlap = king_min_dist - kd
            minion.x += (
                (minion.x - king.x) / kd * overlap * 2
            )
            minion.y += (
                (minion.y - king.y) / kd * overlap * 2
            )
        return

    # King stopped: return to the king and orbit him.
    if has_king:
        king_orbit = max(
            70,
            int(king.radius * 1.6) + 40
        )
        orbit_slot = getattr(minion, "king_orbit_slot", 0)
        orbit_angle = (
            time.time() * 1.2
            + orbit_slot * (2 * math.pi / 6)
        )
        target_x = (
            king.x
            + math.cos(orbit_angle) * king_orbit
        )
        target_y = (
            king.y
            + math.sin(orbit_angle) * king_orbit
        )
        dx = target_x - minion.x
        dy = target_y - minion.y
        length = math.sqrt(dx * dx + dy * dy)
        step = KING_GUARD_SPEED * 2.5
        if length > step:
            minion.x += dx / length * step
            minion.y += dy / length * step
        else:
            minion.x = target_x
            minion.y = target_y

        kd = distance(
            minion.x,
            minion.y,
            king.x,
            king.y
        )
        king_min_dist = king.radius + minion.radius + 4
        if 0 < kd < king_min_dist:
            overlap = king_min_dist - kd
            minion.x += (
                (minion.x - king.x) / kd * overlap
            )
            minion.y += (
                (minion.y - king.y) / kd * overlap
            )


def hornet_minion_ai(minion):
    # Hornet king minions: chase with the king; when the king stops
    # chasing, return to the king and orbit him. While stopped near
    # the flower they turn 180 degrees and shoot from the rear like
    # normal hornets.

    king = kings.get("Hornet")
    has_king = (
        king is not None
        and king.alive
    )

    king_chasing = (
        has_king
        and not player_dead
        and distance(
            king.x,
            king.y,
            player_x,
            player_y
        ) <= KING_CHASE_RANGE
    )

    if king_chasing:
        target_angle = math.degrees(
            math.atan2(
                player_y - minion.y,
                player_x - minion.x
            )
        )

        dist_to_player = distance(
            minion.x,
            minion.y,
            player_x,
            player_y
        )

        minion.speed = king.max_speed * 3.1 * 3

        if dist_to_player > 250:
            # Approach the flower.
            minion.turn_to(target_angle, 7)
            rad = math.radians(minion.angle)
            move_with_collision(
                minion,
                math.cos(rad) * minion.speed * 0.15,
                math.sin(rad) * minion.speed * 0.15
            )
        else:
            # Stopped: whip around fast and fire from the rear.
            back_angle = (target_angle + 180) % 360
            minion.turn_to(back_angle, 14)

            minion.shoot_timer += 1
            if minion.shoot_timer >= minion.missile_cooldown:
                minion.shoot_timer = 0
                fire_hornet_missile(minion)

        # Bounce off other hornet minions and the king.
        for other in hornets:
            if other is minion:
                continue
            if not other.alive:
                continue
            d = distance(
                minion.x,
                minion.y,
                other.x,
                other.y
            )
            min_dist = minion.radius + other.radius
            if 0 < d < min_dist:
                overlap = (min_dist - d) / 2
                minion.x += (
                    (minion.x - other.x) / d * overlap * 2
                )
                minion.y += (
                    (minion.y - other.y) / d * overlap * 2
                )

        kd = distance(
            minion.x,
            minion.y,
            king.x,
            king.y
        )
        king_min_dist = king.radius + minion.radius
        if 0 < kd < king_min_dist:
            overlap = king_min_dist - kd
            minion.x += (
                (minion.x - king.x) / kd * overlap * 2
            )
            minion.y += (
                (minion.y - king.y) / kd * overlap * 2
            )
        return

    # King stopped chasing (or dead): return to the king and orbit.
    if has_king:
        king_orbit = max(
            70,
            int(king.radius * 1.6) + 40
        )
        orbit_slot = getattr(minion, "king_orbit_slot", 0)
        orbit_angle = (
            time.time() * 1.2
            + orbit_slot * (2 * math.pi / 6)
        )
        target_x = (
            king.x
            + math.cos(orbit_angle) * king_orbit
        )
        target_y = (
            king.y
            + math.sin(orbit_angle) * king_orbit
        )
        dx = target_x - minion.x
        dy = target_y - minion.y
        length = math.sqrt(dx * dx + dy * dy)
        step = KING_GUARD_SPEED * 2.5
        if length > step:
            minion.x += dx / length * step
            minion.y += dy / length * step
        else:
            minion.x = target_x
            minion.y = target_y

        # Never touch the king.
        kd = distance(
            minion.x,
            minion.y,
            king.x,
            king.y
        )
        king_min_dist = king.radius + minion.radius + 4
        if 0 < kd < king_min_dist:
            overlap = king_min_dist - kd
            minion.x += (
                (minion.x - king.x) / kd * overlap
            )
            minion.y += (
                (minion.y - king.y) / kd * overlap
            )


def fire_hornet_missile(hornet):
    # After the hornet whips around, its rear-mounted missile faces
    # the flower. The missile launches from the rear and flies at
    # the flower.
    angle = math.radians(hornet.angle)
    back_x = -math.cos(angle)
    back_y = -math.sin(angle)

    aim_angle = math.atan2(
        player_y - hornet.y,
        player_x - hornet.x
    )

    is_king = getattr(hornet, "is_king", False)
    is_minion = getattr(hornet, "is_minion", False)

    # King missiles deal 1/4 of the king's damage and have 1/4 of
    # the king's HP so petals can shoot them down.
    missile_damage = (
        max(1, int(hornet.damage / 4))
        if is_king
        else hornet.damage
    )
    missile_hp = (
        max(1, int(hornet.max_hp / 4))
        if is_king
        else max(1, int(hornet.max_hp / 4))
    )

    is_hole_hornet = getattr(hornet, "is_hole_land_mob", False) or type(hornet).__name__ == "HoleHornet"

    hornet_missiles.append(
        {
            "x": hornet.x + back_x * hornet.radius,
            "y": hornet.y + back_y * hornet.radius,
            "dx": (
                math.cos(aim_angle) * (HORNET_MISSILE_SPEED * 1.15 if is_hole_hornet else HORNET_MISSILE_SPEED)
            ),
            "dy": (
                math.sin(aim_angle) * (HORNET_MISSILE_SPEED * 1.15 if is_hole_hornet else HORNET_MISSILE_SPEED)
            ),
            "damage": missile_damage,
            "hp": missile_hp,
            "max_hp": missile_hp,
            "is_hole_projectile": is_hole_hornet,
            "timer": HORNET_MISSILE_LIFETIME,
            "owner": hornet
        }
    )


def update_hornet_missiles():
    # Move missiles and damage the flower on contact.
    global player_hp

    for missile in hornet_missiles[:]:

        # Dying missiles shrink away fast.
        if missile.get("dying"):
            missile["shrink"] -= 0.18
            if missile["shrink"] <= 0:
                hornet_missiles.remove(missile)
            continue

        missile["timer"] -= 1

        if missile["timer"] <= 0:
            missile["dying"] = True
            missile["shrink"] = 1.0
            continue

        # Hole Hornet missiles home in on the player
        if missile.get("is_hole_projectile") and not player_dead and not player_ghost and not game_peaceful_mode:
            target_angle = math.atan2(
                player_y - missile["y"],
                player_x - missile["x"]
            )
            current_angle = math.atan2(missile["dy"], missile["dx"])
            # Smooth steering turn towards flower
            diff = (target_angle - current_angle + math.pi) % (2 * math.pi) - math.pi
            turn_rate = 0.08  # agile tracking turn rate
            if abs(diff) <= turn_rate:
                new_angle = target_angle
            else:
                new_angle = current_angle + (turn_rate if diff > 0 else -turn_rate)
            speed = math.hypot(missile["dx"], missile["dy"])
            missile["dx"] = math.cos(new_angle) * speed
            missile["dy"] = math.sin(new_angle) * speed

        missile["x"] += missile["dx"]
        missile["y"] += missile["dy"]

        # Prevent hornet missile from going past map boundaries
        missile_r = missile["owner"].radius * 0.5
        missile["x"] = max(missile_r, min(missile["x"], WORLD_WIDTH - missile_r))
        missile["y"] = max(missile_r, min(missile["y"], WORLD_HEIGHT - missile_r))
        if (
            missile["x"] <= missile_r
            or missile["x"] >= WORLD_WIDTH - missile_r
            or missile["y"] <= missile_r
            or missile["y"] >= WORLD_HEIGHT - missile_r
        ):
            missile["dying"] = True
            missile["shrink"] = 1.0

        # Missiles chip the flower's petals too.
        projectile_hits_petals(
            missile,
            missile.get(
                "damage",
                missile["owner"].damage
            ),
            missile["owner"].radius * 0.5
        )

        if (
            not player_dead
            and distance(
                missile["x"],
                missile["y"],
                player_x,
                player_y
            ) <= PLAYER_RADIUS + missile["owner"].radius * 0.5
        ):
            if projectile_hits_flower(
                missile,
                missile.get(
                    "damage",
                    missile["owner"].damage
                )
            ):
                missile["dying"] = True
                missile["shrink"] = 1.0


def update_hole_ladybug_projectiles():
    global player_hp
    for orb in hole_ladybug_projectiles[:]:
        if orb.get("dying"):
            orb["shrink"] -= 0.18
            if orb["shrink"] <= 0:
                hole_ladybug_projectiles.remove(orb)
            continue

        orb["timer"] -= 1
        if orb["timer"] <= 0:
            orb["dying"] = True
            orb["shrink"] = 1.0
            continue

        orb["x"] += orb["dx"]
        orb["y"] += orb["dy"]

        orb_r = orb.get("radius", 10)
        if (
            orb["x"] <= orb_r
            or orb["x"] >= WORLD_WIDTH - orb_r
            or orb["y"] <= orb_r
            or orb["y"] >= WORLD_HEIGHT - orb_r
        ):
            orb["dying"] = True
            orb["shrink"] = 1.0

        # Hits flower's petals
        projectile_hits_petals(
            orb,
            orb["damage"],
            orb_r
        )

        # Hits flower body
        if (
            not player_dead
            and distance(orb["x"], orb["y"], player_x, player_y) <= PLAYER_RADIUS + orb_r
        ):
            if projectile_hits_flower(orb, orb["damage"]):
                orb["dying"] = True
                orb["shrink"] = 1.0


def update_rock_projectiles():
    # Move rock projectiles and damage the flower on contact.
    # Petals can destroy them.
    global player_hp

    for rock_p in rock_projectiles[:]:

        # Dying rocks shrink away fast.
        if rock_p.get("dying"):
            rock_p["shrink"] -= 0.18
            if rock_p["shrink"] <= 0:
                rock_projectiles.remove(rock_p)
            continue

        rock_p["timer"] -= 1

        if rock_p["timer"] <= 0:
            rock_p["dying"] = True
            rock_p["shrink"] = 1.0
            continue

        rock_p["x"] += rock_p["dx"]
        rock_p["y"] += rock_p["dy"]

        # Prevent rock projectile from going past map boundaries
        rock_r = rock_p.get("radius", 8)
        rock_p["x"] = max(rock_r, min(rock_p["x"], WORLD_WIDTH - rock_r))
        rock_p["y"] = max(rock_r, min(rock_p["y"], WORLD_HEIGHT - rock_r))
        if (
            rock_p["x"] <= rock_r
            or rock_p["x"] >= WORLD_WIDTH - rock_r
            or rock_p["y"] <= rock_r
            or rock_p["y"] >= WORLD_HEIGHT - rock_r
        ):
            rock_p["dying"] = True
            rock_p["shrink"] = 1.0

        # Rocks chip the flower's petals too.
        projectile_hits_petals(
            rock_p,
            rock_p["damage"],
            rock_p.get("radius", 8)
        )

        hit_radius = rock_p.get("radius", 8)

        # Rocks damage the flower (and grind down against it).
        if (
            not player_dead
            and distance(
                rock_p["x"],
                rock_p["y"],
                player_x,
                player_y
            ) <= PLAYER_RADIUS + hit_radius
        ):
            if projectile_hits_flower(
                rock_p,
                rock_p["damage"]
            ):
                rock_p["dying"] = True
                rock_p["shrink"] = 1.0


def update_king_webs():
    # Age the spider king's webs and slow the flower inside them.
    global player_in_web
    global player_in_web_slowdown

    player_in_web = False
    player_in_web_slowdown = KING_WEB_SLOWDOWN

    for web in king_webs[:]:
        web["timer"] -= 1
        # Webs grow from tiny to full size while the spider spins.
        if web["radius"] < web["target_radius"]:
            web["radius"] = min(
                web["target_radius"],
                web["radius"] + web["growth_per_frame"]
            )
        if web["timer"] <= 0:
            king_webs.remove(web)
            continue
        web_r = web.get("radius", 60)
        web["x"] = max(web_r, min(web["x"], WORLD_WIDTH - web_r))
        web["y"] = max(web_r, min(web["y"], WORLD_HEIGHT - web_r))

        if distance(
            web["x"],
            web["y"],
            player_x,
            player_y
        ) <= web["radius"] + PLAYER_RADIUS:
            player_in_web = True
            player_in_web_slowdown = web["slowdown"]


def update_flower_projectiles():
    # Move flower projectiles (not made yet) and ensure they cannot
    # go past the edge of the map.
    for fp in flower_projectiles[:]:
        if isinstance(fp, dict):
            if fp.get("dying"):
                fp["shrink"] = fp.get("shrink", 1.0) - 0.18
                if fp["shrink"] <= 0:
                    flower_projectiles.remove(fp)
                continue
            if "timer" in fp:
                fp["timer"] -= 1
                if fp["timer"] <= 0:
                    fp["dying"] = True
                    fp["shrink"] = 1.0
                    continue
            fp["x"] = fp.get("x", 0) + fp.get("dx", 0)
            fp["y"] = fp.get("y", 0) + fp.get("dy", 0)
            r = fp.get("radius", 8)
            fp["x"] = max(r, min(fp["x"], WORLD_WIDTH - r))
            fp["y"] = max(r, min(fp["y"], WORLD_HEIGHT - r))
            if (
                fp["x"] <= r
                or fp["x"] >= WORLD_WIDTH - r
                or fp["y"] <= r
                or fp["y"] >= WORLD_HEIGHT - r
            ):
                fp["dying"] = True
                fp["shrink"] = 1.0
        elif hasattr(fp, "update"):
            fp.update()
            r = getattr(fp, "radius", 8)
            fp.x = max(r, min(fp.x, WORLD_WIDTH - r))
            fp.y = max(r, min(fp.y, WORLD_HEIGHT - r))
            if (
                fp.x <= r
                or fp.x >= WORLD_WIDTH - r
                or fp.y <= r
                or fp.y >= WORLD_HEIGHT - r
            ):
                if hasattr(fp, "dying"):
                    fp.dying = True
                elif hasattr(fp, "alive"):
                    fp.alive = False
                if not getattr(fp, "alive", True) and fp in flower_projectiles:
                    flower_projectiles.remove(fp)
        elif hasattr(fp, "x") and hasattr(fp, "y"):
            r = getattr(fp, "radius", 8)
            fp.x = max(r, min(fp.x, WORLD_WIDTH - r))
            fp.y = max(r, min(fp.y, WORLD_HEIGHT - r))
            if (
                fp.x <= r
                or fp.x >= WORLD_WIDTH - r
                or fp.y <= r
                or fp.y >= WORLD_HEIGHT - r
            ):
                if hasattr(fp, "dying"):
                    fp.dying = True
                elif hasattr(fp, "alive"):
                    fp.alive = False
                if not getattr(fp, "alive", True) and fp in flower_projectiles:
                    flower_projectiles.remove(fp)


def spawn_king_minions():
    # Kings summon minions around them and talk in chat.
    if not all_enemies:
        return

    for enemy in all_enemies:

        if not getattr(enemy, "is_king", False):
            continue
        if not enemy.alive:
            continue

        enemy.king_minion_timer += 1

        # Kings talk in chat every ~8 seconds (rocks never talk).
        enemy.king_chat_timer = (
            getattr(enemy, "king_chat_timer", 0) + 1
        )
        if (
            enemy.king_chat_timer >= 480
            and type(enemy).__name__ != "Rock"
        ):
            enemy.king_chat_timer = 0
            mob_name = type(enemy).__name__
            king_say(
                mob_name,
                random.choice(KING_CHAT_LINES)
            )

        # Kings fire their volley: the bee king every 0.5 seconds,
        # the ladybug king every 8 seconds.
        enemy.king_rose_timer = (
            getattr(enemy, "king_rose_timer", 0) + 1
        )
        if type(enemy).__name__ == "Bee":
            if enemy.king_rose_timer >= 30:
                enemy.king_rose_timer = 0
                fire_king_stinger_volley(enemy)
        elif type(enemy).__name__ == "Ladybug":
            if enemy.king_rose_timer >= 480:
                enemy.king_rose_timer = 0
                fire_king_rose_volley(enemy)
        elif type(enemy).__name__ == "SoldierAnt":
            # The soldier ant king fires one giant wing every 6
            # seconds.
            if enemy.king_rose_timer >= SOLDIER_WING_INTERVAL:
                enemy.king_rose_timer = 0
                fire_soldier_wing(enemy)

        # The spider king stops and spins a web every second.
        # While spinning it can't move, and the web grows under it
        # until it reaches twice the spider's size.
        if type(enemy).__name__ == "Spider":
            enemy.king_web_timer = (
                getattr(enemy, "king_web_timer", 0) + 1
            )
            if (
                enemy.king_web_timer >= KING_WEB_INTERVAL
                and getattr(enemy, "king_web_spinning", 0) <= 0
            ):
                enemy.king_web_timer = 0
                # Freeze and spin for 0.5 seconds.
                enemy.king_web_spinning = 30
                target_radius = enemy.radius * 7
                king_webs.append(
                    {
                        "x": enemy.x,
                        "y": enemy.y,
                        "radius": 4,
                        "target_radius": target_radius,
                        "growth_per_frame": target_radius / 30,
                        "timer": KING_WEB_LIFETIME,
                        "surface": build_web_surface(
                            target_radius
                        ),
                        "spin": random.uniform(0, 360),
                        "slowdown": get_web_slowdown(
                            enemy.rarity
                        ),
                    }
                )

        # The spider and rock kings spawn minions every 0.5 seconds;
        # other kings every 3 seconds.
        minion_interval = (
            30
            if type(enemy).__name__ in ("Spider", "Rock")
            else 180
        )
        # The baby ant king spawns a minion every 0.01 sec
        # (about every frame).
        if type(enemy).__name__ == "BabyAnt":
            minion_interval = 1
        # The worker ant king spawns a minion every 0.5 seconds.
        if type(enemy).__name__ == "WorkerAnt":
            minion_interval = 30
        # Hornets volley too: king missiles every 0.2s handled in
        # Hornet.update.
        if enemy.king_minion_timer < minion_interval:
            continue

        enemy.king_minion_timer = 0

        mob_name = type(enemy).__name__
        if mob_name not in (
            "Ladybug", "Spider", "Rock", "Hornet", "BabyAnt",
            "SoldierAnt", "WorkerAnt", "AntEgg"
        ):
            continue

        if mob_name == "AntEgg":
            mob_list = soldier_ants
            minion_class = SoldierAnt
        else:
            mob_list = get_king_mob_list(mob_name)
            minion_class = {
                "Ladybug": Ladybug,
                "Spider": Spider,
                "Hole Spider": HoleSpider,
                "Rock": Rock,
                "Hole Rock": HoleRock,
                "Hornet": Hornet,
                "Hole Hornet": HoleHornet,
                "BabyAnt": BabyAnt,
                "SoldierAnt": SoldierAnt,
                "WorkerAnt": WorkerAnt,
            }[mob_name]

        if mob_name == "AntEgg":
            alive_minions = sum(
                1
                for e in mob_list
                if getattr(e, "is_minion", False) and getattr(e, "king_owner", None) is enemy and e.alive
            )
        else:
            alive_minions = sum(
                1
                for e in mob_list
                if getattr(e, "is_minion", False) and e.alive
            )
        minion_cap = 30 if mob_name == "Spider" else 10
        if mob_name == "Rock":
            minion_cap = 5
        if mob_name == "BabyAnt":
            minion_cap = 20
        # The soldier ant king spawns only 1 minion.
        if mob_name == "SoldierAnt":
            minion_cap = 1
        if mob_name == "AntEgg":
            minion_cap = 10
        if alive_minions >= minion_cap:
            continue

        minion = minion_class()
        minion.is_minion = True
        minion.angry = True
        minion.rarity = enemy.rarity
        if mob_name == "AntEgg":
            minion.king_owner = enemy
            minion.king_mob_name = "AntEgg"
            minion.radius = max(6, int(enemy.radius / 4))
            minion.base_radius = minion.radius
            minion.max_hp = max(1, int(enemy.max_hp / 4))
            minion.damage = max(1, int(get_enemy_attack_damage(enemy) / 4))
            minion.custom_damage = minion.damage
        # The soldier ant king's minion is 2x bigger than the king.
        elif mob_name == "SoldierAnt":
            minion.radius = enemy.radius * 2
        else:
            minion.radius = max(6, int(enemy.radius * 0.35))
        # A minion has one third of the king's HP and damage,
        # and chases at three times the king's speed.
        if mob_name == "AntEgg":
            pass
        elif mob_name == "BabyAnt":
            minion.max_hp = max(1, int(enemy.max_hp / 5))
            minion.damage = max(1, int(enemy.damage / 3))
        elif mob_name == "SoldierAnt":
            # Same HP and damage as the king's giant wing.
            minion.max_hp = max(1, int(enemy.max_hp * 2))
            minion.damage = max(1, int(enemy.damage * 2))
        elif mob_name == "WorkerAnt":
            # Same HP and damage as the king's corn: 1/2 of the
            # king's damage.
            minion.max_hp = max(1, int(enemy.damage / 2))
            minion.damage = max(1, int(enemy.damage / 2))
        else:
            minion.max_hp = max(1, int(enemy.max_hp / 3))
            minion.damage = max(1, int(enemy.damage / 3))
        minion.hp = minion.max_hp
        if hasattr(enemy, "max_speed"):
            minion.max_speed = enemy.max_speed * 3
        minion.king_orbit_slot = alive_minions
        minion.x = max(
            minion.radius,
            min(enemy.x + random.randint(-60, 60), WORLD_WIDTH - minion.radius)
        )
        minion.y = max(
            minion.radius,
            min(enemy.y + random.randint(-60, 60), WORLD_HEIGHT - minion.radius)
        )
        mob_list.append(minion)


def flower_minion_ai(minion):
    # Flower minions (from Ant Egg petals) orbit the flower using
    # the same guard-ring behavior as king minions: they always
    # march forward around the ring and never walk backward.
    # When an enemy is near the flower the minion leaves the ring
    # and charges it instead.
    target = getattr(minion, "target_enemy", None)

    if (
        target is not None
        and target.alive
        and not getattr(target, "dying", False)
    ):
        # Charge the spotted enemy (using Ladybug King's minion AI style: rapid approach with wing animation)
        target_angle = math.degrees(
            math.atan2(
                target.y - minion.y,
                target.x - minion.x
            )
        )
        if hasattr(minion, "turn_to"):
            minion.turn_to(target_angle, 6)
        else:
            minion.angle = target_angle
        chase_spd = getattr(minion, "custom_speed", None)
        if chase_spd is None:
            chase_spd = PLAYER_SPEED * 2
        minion.speed = chase_spd
        rad = math.radians(minion.angle)
        move_with_collision(
            minion,
            math.cos(rad) * minion.speed,
            math.sin(rad) * minion.speed
        )
        if hasattr(minion, "wing_phase"):
            minion.wing_phase += 0.85
        return

    minion.target_enemy = None

    if player_dead:
        minion.speed = 0
        return

    orbit = 140 + PLAYER_RADIUS
    cur_angle = math.atan2(
        minion.y - player_y,
        minion.x - player_x
    )
    orbit_slot = getattr(minion, "king_orbit_slot", 0)
    orbit_angle = (
        time.time() * 1.2
        + orbit_slot * (2 * math.pi / 10)
    )

    # Always march forward around the ring, speeding up when the
    # minion falls behind its slot.
    angle_behind = (
        (orbit_angle - cur_angle)
        % (2 * math.pi)
    )
    angle_step = 0.02 + min(angle_behind, 1.5) * 0.03
    new_angle = cur_angle + angle_step

    target_x = (
        player_x
        + math.cos(new_angle) * orbit
    )
    target_y = (
        player_y
        + math.sin(new_angle) * orbit
    )

    dx = target_x - minion.x
    dy = target_y - minion.y
    length = math.sqrt(dx * dx + dy * dy)
    step = KING_GUARD_SPEED * 2.5

    # Overlapping minions slow each other down and bounce apart.
    separation = minion.radius * 2.2
    bounce_x = 0.0
    bounce_y = 0.0
    for other in flower_minions:
        if other is minion:
            continue
        if not other.alive:
            continue
        d = distance(
            minion.x,
            minion.y,
            other.x,
            other.y
        )
        if 0 < d < separation:
            closeness = 1.0 - (d / separation)
            step *= 1.0 - closeness * 0.9
            min_dist = minion.radius + other.radius
            if d < min_dist:
                overlap = (min_dist - d) / 2
                bounce_x += (
                    (minion.x - other.x) / d * overlap
                )
                bounce_y += (
                    (minion.y - other.y) / d * overlap
                )

    if length > step:
        minion.x += dx / length * step
        minion.y += dy / length * step
    else:
        minion.x = target_x
        minion.y = target_y

    if bounce_x or bounce_y:
        minion.x += bounce_x * 2
        minion.y += bounce_y * 2

    # Face the direction of travel around the ring.
    if hasattr(minion, "angle"):
        minion.angle = math.degrees(new_angle + math.pi / 2)
    minion.speed = 0


def spawn_custom_flower_minion(rarity, mob_name, custom_damage=None, custom_hp=None, custom_speed=None, custom_size=None, custom_view_range=None):
    enemy_classes = {
        "Ladybug": Ladybug,
        "Hole Ladybug": HoleLadybug,
        "Bee": Bee,
        "Hole Bee": HoleBee,
        "Hole Bee": HoleBee,
        "Spider": Spider,
        "Rock": Rock,
        "Hornet": Hornet,
        "Hole Hornet": HoleHornet,
        "Baby Ant": BabyAnt,
        "Hole Baby Ant": HoleBabyAnt,
        "Hole Baby Ant": HoleBabyAnt,
        "Soldier Ant": SoldierAnt,
        "Hole Soldier Ant": HoleSoldierAnt,
        "BabyAnt": BabyAnt,
        "SoldierAnt": SoldierAnt,
        "Worker Ant": WorkerAnt,
        "Hole Worker Ant": HoleWorkerAnt,
        "WorkerAnt": WorkerAnt,
        "Queen Ant": QueenAnt,
        "Hole Queen Ant": HoleQueenAnt,
        "QueenAnt": QueenAnt,
        "Ant Egg": AntEgg,
        "AntEgg": AntEgg,
    }
    cls = enemy_classes.get(mob_name, SoldierAnt)
    minion = cls()
    minion.is_minion = True
    minion.yellow_minion = True
    minion.is_command_minion = True
    minion.king_orbit_slot = sum(1 for m in flower_minions if m.alive)

    valid_rarity = rarity.capitalize() if rarity.capitalize() in MOB_HP_MULTIPLIER else "Common"
    minion.rarity = valid_rarity
    apply_enemy_rarity_stats(minion)

    if custom_size is not None:
        minion.radius = max(4, int(custom_size))
        minion.base_radius = minion.radius
    else:
        minion.radius = min(minion.radius, PLAYER_RADIUS * MOB_SIZE_MULTIPLIER.get(valid_rarity, 1.0))

    if custom_damage is not None:
        minion.damage = int(custom_damage)
        minion.custom_damage = int(custom_damage)

    if custom_hp is not None:
        minion.max_hp = int(custom_hp)
        minion.hp = int(custom_hp)

    if custom_speed is not None:
        minion.custom_speed = float(custom_speed)

    if custom_view_range is not None:
        minion.custom_view_range = float(custom_view_range)

    minion.x = max(minion.radius, min(player_x + random.randint(-60, 60), WORLD_WIDTH - minion.radius))
    minion.y = max(minion.radius, min(player_y + random.randint(-60, 60), WORLD_HEIGHT - minion.radius))
    flower_minions.append(minion)
    return minion


def spawn_flower_minion(slot_index):
    # Hatch a yellow SoldierAnt minion from an alive Ant Egg petal.
    egg_rarity = petal_slots[slot_index]["rarity"]
    if egg_rarity not in MOB_HP_MULTIPLIER:
        egg_rarity = "Celestial"

    minion = SoldierAnt()
    minion.is_minion = True
    minion.yellow_minion = True
    minion.egg_slot = slot_index
    minion.king_orbit_slot = sum(
        1 for m in flower_minions if m.alive
    )
    # Same base HP and damage as an enemy soldier ant, scaled by
    # the egg petal's rarity with the mob multipliers.
    minion.rarity = egg_rarity
    apply_enemy_rarity_stats(minion)
    # Cap the minion at the flower's size scaled by its rarity's
    # mob size multiplier.
    minion.radius = min(
        minion.radius,
        PLAYER_RADIUS * MOB_SIZE_MULTIPLIER.get(egg_rarity, 1.0)
    )
    minion.x = max(
        minion.radius,
        min(player_x + random.randint(-60, 60), WORLD_WIDTH - minion.radius)
    )
    minion.y = max(
        minion.radius,
        min(player_y + random.randint(-60, 60), WORLD_HEIGHT - minion.radius)
    )
    flower_minions.append(minion)


def update_flower_minions():
    # Hatch, move and fight with the Ant Egg minions.

    # 0) Spot enemies near the flower and split the minions across
    # them: minion N hunts enemy N, wrapping around when there are
    # more minions than enemies.
    hunting_minions = [
        m
        for m in flower_minions
        if m.alive and not getattr(m, "dying", False)
    ]
    for minion_index, minion in enumerate(hunting_minions):
        v_range = getattr(minion, "custom_view_range", FLOWER_MINION_SIGHT)
        minion_sight_enemies = [
            e
            for e in all_enemies
            if e.alive
            and not getattr(e, "dying", False)
            and distance(
                player_x,
                player_y,
                e.x,
                e.y
            ) <= v_range
        ]
        if minion_sight_enemies:
            minion.target_enemy = minion_sight_enemies[
                minion_index % len(minion_sight_enemies)
            ]
        else:
            minion.target_enemy = None

    # 1) Spawn minions for every alive Ant Egg petal slot: how many
    # minions hatch depends on the egg's petal count (parts).
    for i in range(PETAL_SLOTS):
        if (
            petal_slots[i]["filled"]
            and petal_slots[i]["petal"] == "Ant Egg"
            and petal_alive[i]
        ):
            egg_count = get_petal_count(
                "Ant Egg",
                petal_slots[i]["rarity"]
            )
            owned = sum(
                1
                for m in flower_minions
                if getattr(m, "egg_slot", None) == i and m.alive
            )
            for _ in range(owned, egg_count):
                spawn_flower_minion(i)

    # 2) Update every minion: orbit, fight, die.
    for minion in flower_minions[:]:
        if not minion.alive:
            flower_minions.remove(minion)
            continue

        if getattr(minion, "dying", False):
            minion.shrink_scale -= 0.08
            if minion.shrink_scale <= 0:
                minion.shrink_scale = 0
                minion.dying = False
                minion.alive = False
            else:
                minion.radius = (
                    minion.full_radius * minion.shrink_scale
                )
            continue

        # If the slot no longer holds the egg, despawn the minion (unless spawned via command).
        slot = getattr(minion, "egg_slot", None)
        is_cmd_minion = getattr(minion, "is_command_minion", False)
        if not is_cmd_minion:
            if (
                slot is None
                or not petal_slots[slot]["filled"]
                or petal_slots[slot]["petal"] != "Ant Egg"
            ):
                minion.dying = True
                minion.shrink_scale = 1.0
                minion.full_radius = minion.radius
                continue

        flower_minion_ai(minion)

        # Solid collision with its owner: never overlap the flower.
        if not player_dead:
            d = distance(
                minion.x,
                minion.y,
                player_x,
                player_y
            )
            min_dist = PLAYER_RADIUS + minion.radius
            if 0 < d < min_dist:
                minion.x = player_x + (
                    (minion.x - player_x) / d * min_dist
                )
                minion.y = player_y + (
                    (minion.y - player_y) / d * min_dist
                )

        if minion.attack_cooldown > 0:
            minion.attack_cooldown -= 1
        if minion.flash_timer > 0:
            minion.flash_timer -= 1

        # Fight: bumping an enemy deals minion damage to it and
        # enemy damage back to the minion.
        for enemy in all_enemies:
            if not enemy.alive:
                continue
            if getattr(enemy, "dying", False):
                continue
            d = distance(
                minion.x,
                minion.y,
                enemy.x,
                enemy.y
            )
            if 0 < d < minion.radius + enemy.radius:
                if minion.attack_cooldown <= 0:
                    minion.attack_cooldown = 30
                    enemy.take_damage(minion.damage)
                    dmg = get_enemy_attack_damage(enemy)
                    minion.hp -= dmg
                    minion.flash_timer = 4
                    if type(enemy).__name__ in ("Rock", "AntEgg"):
                        # Push minion back strongly on attack so minions don't spam damage
                        p_dist = max(0.001, d)
                        p_x = (minion.x - enemy.x) / p_dist
                        p_y = (minion.y - enemy.y) / p_dist
                        minion.x += p_x * 50
                        minion.y += p_y * 50
                    if minion.hp <= 0:
                        minion.hp = 0
                        # The minion dies: its egg is consumed and
                        # reloads like a destroyed petal.
                        minion.dying = True
                        minion.shrink_scale = 1.0
                        minion.full_radius = minion.radius
                        if slot is not None and 0 <= slot < len(petal_alive):
                            petal_alive[slot] = False
                            petal_respawn_timer[slot] = PETAL_RELOAD[
                                "Ant Egg"
                            ]
                break

        # Mobs push the minion around: every overlapping enemy
        # (regular mobs, kings and king minions alike) shoves the
        # minion, and the minion shoves back.
        for enemy in all_enemies:
            if not enemy.alive:
                continue
            if getattr(enemy, "dying", False):
                continue
            d = distance(
                minion.x,
                minion.y,
                enemy.x,
                enemy.y
            )
            min_dist = minion.radius + enemy.radius
            if 0 < d < min_dist:
                push_x = (minion.x - enemy.x) / d
                push_y = (minion.y - enemy.y) / d
                if type(enemy).__name__ in ("Rock", "AntEgg"):
                    # Rock and Ant Egg are stationary mobs and push minions back strongly
                    extra_push = 20
                    minion.x += push_x * (min_dist - d + extra_push)
                    minion.y += push_y * (min_dist - d + extra_push)
                else:
                    overlap = (min_dist - d) / 2
                    minion.x += push_x * overlap
                    minion.y += push_y * overlap
                    enemy.x -= push_x * overlap
                    enemy.y -= push_y * overlap

    # 3) Solid collision between minions: push overlapping pairs
    # apart so they never stack on each other.
    for a_index in range(len(flower_minions)):
        minion_a = flower_minions[a_index]
        if not minion_a.alive or getattr(minion_a, "dying", False):
            continue
        for b_index in range(a_index + 1, len(flower_minions)):
            minion_b = flower_minions[b_index]
            if not minion_b.alive or getattr(minion_b, "dying", False):
                continue
            d = distance(
                minion_a.x,
                minion_a.y,
                minion_b.x,
                minion_b.y
            )
            min_dist = minion_a.radius + minion_b.radius
            if 0 < d < min_dist:
                overlap = (min_dist - d) / 2
                push_x = (minion_a.x - minion_b.x) / d
                push_y = (minion_a.y - minion_b.y) / d
                minion_a.x += push_x * overlap
                minion_a.y += push_y * overlap
                minion_b.x -= push_x * overlap
                minion_b.y -= push_y * overlap

    # Keep all flower minions inside map boundaries
    for minion in flower_minions:
        rad = getattr(minion, "radius", 0)
        minion.x = max(rad, min(minion.x, WORLD_WIDTH - rad))
        minion.y = max(rad, min(minion.y, WORLD_HEIGHT - rad))


def projectile_fight_flower_minions(projectile, damage, hit_radius):
    # Enemy projectiles that touch a flower minion get pushed away,
    # grind down from the minion's damage, and hurt the minion in
    # return. Returns True when the projectile should start dying.
    for minion in flower_minions:
        if not minion.alive:
            continue
        if getattr(minion, "dying", False):
            continue
        d = distance(
            minion.x,
            minion.y,
            projectile["x"],
            projectile["y"]
        )
        if 0 < d <= minion.radius + hit_radius:
            # Push the projectile out of the minion.
            push = minion.radius + hit_radius - d
            projectile["x"] += (
                (projectile["x"] - minion.x) / d * push
            )
            projectile["y"] += (
                (projectile["y"] - minion.y) / d * push
            )
            # The projectile damages the minion...
            minion.hp -= damage
            minion.flash_timer = 4
            if minion.hp <= 0:
                slot = getattr(minion, "egg_slot", None)
                minion.dying = True
                minion.shrink_scale = 1.0
                minion.full_radius = minion.radius
                if (
                    slot is not None
                    and petal_slots[slot]["filled"]
                    and petal_slots[slot]["petal"] == "Ant Egg"
                ):
                    petal_alive[slot] = False
                    petal_respawn_timer[slot] = PETAL_RELOAD[
                        "Ant Egg"
                    ]
            # ...and the minion grinds the projectile down.
            projectile["hp"] -= max(
                1,
                int(minion.damage / 10)
            )
            if projectile["hp"] <= 0:
                return True
    return False


def update_flower_minion_projectile_fight():
    # Run the minion vs projectile fight for every enemy projectile
    # list. Dying projectiles are skipped.
    enemy_projectile_lists = (
        king_stinger_projectiles
        + king_rose_projectiles
        + baby_ant_rice
        + worker_ant_corn
        + hornet_missiles
        + rock_projectiles
        + soldier_wing_projectiles
    )
    for projectile in enemy_projectile_lists:
        if projectile.get("dying"):
            continue
        if projectile_fight_flower_minions(
            projectile,
            projectile.get("damage", 1),
            projectile.get("radius", 8)
        ):
            projectile["dying"] = True
            projectile["shrink"] = 1.0


def update_queen_eggs():
    # Queen ant eggs wobble for 1.5 seconds, then hatch into an
    # enemy soldier ant minion whose rarity is two lower than the
    # queen's.
    global player_x
    global player_y

    for egg in queen_eggs[:]:

        egg["timer"] -= 1

        if egg["timer"] > 0:
            # Egg hitbox: the flower and mobs bump into the egg
            # and both get pushed apart.
            egg_r = egg["radius"]
            d = distance(
                player_x,
                player_y,
                egg["x"],
                egg["y"]
            )
            if (
                not player_dead
                and 0 < d < PLAYER_RADIUS + egg_r
            ):
                push = PLAYER_RADIUS + egg_r - d
                push_x = (egg["x"] - player_x) / d
                push_y = (egg["y"] - player_y) / d
                egg["x"] += push_x * push / 2
                egg["y"] += push_y * push / 2
                player_x -= push_x * push / 2
                player_y -= push_y * push / 2
            for enemy in all_enemies:
                if not enemy.alive:
                    continue
                if getattr(enemy, "dying", False):
                    continue
                for c_x, c_y, c_r in entity_hit_circles(enemy):
                    d = distance(
                        c_x,
                        c_y,
                        egg["x"],
                        egg["y"]
                    )
                    if 0 < d < c_r + egg_r:
                        push = c_r + egg_r - d
                        push_x = (egg["x"] - c_x) / d
                        push_y = (egg["y"] - c_y) / d
                        egg["x"] += push_x * push / 2
                        egg["y"] += push_y * push / 2
                        enemy.x -= push_x * push / 2
                        enemy.y -= push_y * push / 2
            continue

        queen_eggs.remove(egg)

        rarity_index = ENEMY_RARITIES.index(
            egg["rarity"]
        ) if egg["rarity"] in ENEMY_RARITIES else 0
        lower_rarity = ENEMY_RARITIES[
            max(0, rarity_index - 2)
        ]

        if egg.get("is_void_egg", False):
            ant = HoleSoldierAnt()
            ant.rarity = lower_rarity
            apply_enemy_rarity_stats(ant)
            ant.radius = egg["radius"]
            ant.base_radius = ant.radius
            ant.charging = True
            ant.x = egg["x"] + random.randint(-10, 10)
            ant.y = egg["y"] + random.randint(-10, 10)
            ant.queen = egg.get("queen")
            hole_soldier_ants.append(ant)
        else:
            ant = SoldierAnt()
            ant.rarity = lower_rarity
            apply_enemy_rarity_stats(ant)
            # The hatched soldier ant is the size of the egg it
            # hatched from.
            ant.radius = egg["radius"]
            ant.base_radius = ant.radius
            ant.charging = True
            ant.x = egg["x"] + random.randint(-10, 10)
            ant.y = egg["y"] + random.randint(-10, 10)
            ant.queen = egg.get("queen")
            soldier_ants.append(ant)

    # Keep all queen ant eggs inside map boundaries
    for egg in queen_eggs:
        egg_r = egg.get("radius", 15)
        egg["x"] = max(egg_r, min(egg["x"], WORLD_WIDTH - egg_r))
        egg["y"] = max(egg_r, min(egg["y"], WORLD_HEIGHT - egg_r))

    # Eggs push each other apart too.
    for a_index in range(len(queen_eggs)):
        egg_a = queen_eggs[a_index]
        for b_index in range(a_index + 1, len(queen_eggs)):
            egg_b = queen_eggs[b_index]
            d = distance(
                egg_a["x"],
                egg_a["y"],
                egg_b["x"],
                egg_b["y"]
            )
            min_dist = egg_a["radius"] + egg_b["radius"]
            if 0 < d < min_dist:
                overlap = (min_dist - d) / 2
                push_x = (egg_a["x"] - egg_b["x"]) / d
                push_y = (egg_a["y"] - egg_b["y"]) / d
                egg_a["x"] += push_x * overlap
                egg_a["y"] += push_y * overlap
                egg_b["x"] -= push_x * overlap
                egg_b["y"] -= push_y * overlap


def dev_ban_user(target_name):
    # Delete a user's account and saved player data.
    # Accounts allowed to ban:
    ban_allowed = {"devguard"}
    # The developer can never be banned.
    banned_protected = {"devguard"}

    if acc_name_text.lower() not in ban_allowed:
        show_error("Unknown command: /ban")
        return False
    target_key = None
    for existing_name in player_accounts:
        if existing_name.lower() == target_name.lower():
            target_key = existing_name
            break
    if target_key is None:
        show_error(f"No account named {target_name}")
        return False
    if target_key.lower() in banned_protected:
        show_error("You can't ban yourself")
        return False

    del player_accounts[target_key]
    with open("accounts.json", "w") as file:
        json.dump(player_accounts, file)

    player_data.pop(target_key, None)
    with open("players.json", "w") as file:
        json.dump(
            player_data,
            file,
            indent=4
        )

    if target_key in muted_users:
        muted_users.remove(target_key)
        save_muted_users()

    show_error(f"Banned {target_key}")
    return True


def pad_petal_slots():
    while len(petal_slots) < PETAL_SLOTS:
        petal_slots.append({
            "filled": False,
            "petal": "Basic",
            "rarity": "Common"
        })

def pad_swap_petal_slots():
    while len(swap_petal_slots) < PETAL_SLOTS:
        swap_petal_slots.append({
            "filled": False,
            "petal": "Basic",
            "rarity": "Common"
        })

for i in range(PETAL_SLOTS):
    petal_respawn_timer.append(0)
    petal_flash_timers.append(0)
for i in range(PETAL_SLOTS):
    petal_respawn_text_timer.append(0)

# Initialize petal lists based on PETAL_SLOTS
resize_petal_lists()

for i in range(PETAL_SLOTS):

    if i >= len(petal_slots):
        continue

    petal_type = petal_slots[i]["petal"]

    hp = (
        PETAL_HP[petal_type]
        *
        PETAL_HP_MULTIPLIER[petal_slots[i]["rarity"]]
    )

    if petal_type == "Light":
        light_count = get_petal_count(petal_type, petal_slots[i]["rarity"])
        if light_count > 0:
            hp /= light_count

    petal_max_hp[i] = hp
    petal_hp[i] = hp

    # Initialize per-light state for Light petal
    if petal_type == "Light":
        light_count = get_petal_count(petal_type, petal_slots[i]["rarity"])
        light_hp[i] = [hp] * light_count
        light_cooldowns[i] = [0] * light_count
        light_alive[i] = [True] * light_count
    else:
        light_hp[i] = []
        light_cooldowns[i] = []
        light_alive[i] = []

    petal_alive[i] = petal_slots[i]["filled"]

# ---------------- PETAL RARITY SYSTEM ----------------

RARITIES = [
    "Common",
    "Unusual",
    "Rare",
    "Epic",
    "Legendary",
    "Mythic",
    "Ultra",
    "Super",
    "Omega",
    "Unique",
    "Eternal",
    "Cosmo",
    "Jeddiful",
    "Tacnic",
    "Radium",
    "Ancient",
    "Omnient",
    "Celestial",
    "Infino"
]

THIRD_EYE_RANGE = {
    "Mythic":200,
    "Ultra":210,
    "Super":220,
    "Omega":230,
    "Unique":240,
    "Eternal":250,
    "Cosmo":260,
    "Jeddiful":270,
    "Tacnic":280,
    "Radium":290,
    "Ancient":300,
    "Omnient":310,
    "Celestial":320,
    "Infino":330
}

PETAL_NORMAL = 70
PETAL_ATTACK = 120
PETAL_DEFEND = 40
login_error = ""

PETAL_DISTANCE = PETAL_NORMAL
petal_distance = PETAL_NORMAL
petal_target = PETAL_NORMAL

RARITY_COLORS = {

    "Common": (0, 255, 0),          # Green

    "Unusual": (255, 255, 120),     # Light Yellow

    "Rare": (0, 140, 255),         # Blue

    "Epic": (160, 0, 255),          # Purple

    "Legendary": (255, 0, 0),       # Red

    "Mythic": (100, 220, 255),      # Sky Blue

    "Ultra": (255, 80, 150),        # Red Pink

    "Super": (100, 255, 170),       # Greenish Sky Blue

    "Omega": (255, 150, 220),       # Pink

    "Unique": (100, 100, 100),      # Grey

    "Eternal": (255, 255, 255),     # White

    "Cosmo": (255, 140, 0),          # Orange

    "Jeddiful": (130, 153, 64),      # COOL GREEN

    "Tacnic": (150, 100, 50),

    "Radium": (157, 197, 218),

    "Ancient": (225, 80, 0),

    "Omnient": (225, 200, 0), # Gradient Red --> yellow, red down to yellow

    "Celestial": (225, 255, 225),

    "Infino": (255,0,255)

}

def lighten_color(color, factor):

    return tuple(
        int(channel + (255 - channel) * factor)
        for channel in color
    )

def darken_color(color, factor):

    return tuple(
        int(channel * factor)
        for channel in color
    )

RARITY_ORDER = [
    "Infino",
    "Celestial",
    "Omnient",
    "Ancient",
    "Radium",
    "Tacnic",
    "Jeddiful",
    "Cosmo",
    "Eternal",
    "Unique",
    "Omega",
    "Super",
    "Ultra",
    "Mythic",
    "Legendary",
    "Epic",
    "Rare",
    "Unusual",
    "Common"
]

# ---------------- RARITY STATS ----------------

PETALS = [
    "Basic",
    "Heavy",
    "Light",
    "Fast",
    "Rose",
    "Stinger",
    "Wing",
    "Cactus",
    "Leaf",
    "Pea",
    "Missile",
    "Bone",
    "Web",
    "Rock",
    "Faster",
    "Magnet",
    "Bubble",
    "Honey",
    "Poison",
    "Shark",
    "Rice",
    "Corn",
    "Stick",
    "Clover",
    "Glass",
    "Antenna",
    "Pollen",
    "Soil",
    "Ant Egg",
    "Sand",
    "Lentil",
    "Pincer",
    "Shell",
    "Beetle Egg",
    "Third Eye",
    "Cice",
    "Boubloom",
    "Boulder",
    "Moon",
    "Grape"
]

RARITY_DAMAGE_MULTIPLIER = {

    "Common": 1.0 * 1,
    "Unusual": 9.7 * 1,
    "Rare": 30.1 * 1,
    "Epic": 65.9 * 1,
    "Legendary": 102.9 * 1,
    "Mythic": 400.5 * 1,
    "Ultra": 1221.9 * 1,
    "Super": 3534.4 * 1.25,
    "Omega": 8435.2 * 1.25,
    "Unique": 11320.2 * 1.25,
    "Eternal": 32100.5 * 1.25,
    "Cosmo": 72300.7 * 4,
    "Jeddiful": 125300.3 * 4,
    "Tacnic": 324657.6 * 4,
    "Radium": 634536.7 * 4,
    "Ancient": 1254665.4 * 4,
    "Omnient": 3234425.1 * 4,
    "Celestial": 5000000.0 * 4,
    "Infino": 12465000.0 * 4
}

# ---------------- PETAL DAMAGE ----------------

PETAL_DAMAGE = {

    "Basic": 5* 2,
    "Light": 15* 2,
    "Stinger": 85* 2,
    "Heavy": 0.1* 2,
    "Rose": 12* 2,
    "Wing": 8* 2,
    "Cactus": 20* 2,
    "Leaf": 12* 2,
    "Pea": 18* 2,
    "Missile": 35* 2,
    "Bone": 22* 2,
    "Web": 5* 2,
    "Rock": 40* 2,
    "Faster": 7* 2,
    "Magnet": 10* 2,
    "Bubble": 14* 2,
    "Honey": 0.01* 2,
    "Poison": 16* 2,
    "Shark": 55* 2,
    "Rice": 5* 2,
    "Corn": 5* 2,
    "Stick": 25* 2,
    "Clover": 2* 2,
    "Glass": 40* 2,
    "Antenna": 3* 2,
    "Pollen": 30* 2,
    "Soil": 2* 2,
    "Ant Egg": 0.1* 2,
    "Sand": 19* 2,
    "Lentil": 0.1* 2,
    "Pincer": 1* 2,
    "Shell": 0.1* 2,
    "Beetle Egg": 0.1* 2,
    "Third Eye": 0.1* 2,
    "Cice": 5* 2,
    "Boubloom": 52* 2,
    "Boulder": 90* 2,
    "Moon": 0.01 * 2,
    "Grape": 1 * 2
}

# ---------------- PETAL RELOAD ----------------
# lower = faster

PETAL_RELOAD = {

    "Basic": 60,

    "Light": 36,

    "Stinger": 75,

    "Heavy": 45,

    "Rose": 30,

    "Wing": 45,

    "Cactus": 120,

    "Leaf": 66,

    "Pea": 54,

    "Missile": 150,

    "Bone": 90,

    "Web": 180,

    "Rock": 165,

    "Faster": 30,

    "Magnet": 75,

    "Bubble": 15,

    "Honey": 105,

    "Poison": 90,

    "Shark": 210,

    "Rice": 3,

    "Corn": 240,

    "Stick": 60,

    "Clover": 42,

    "Glass": 90,

    "Antenna": 3,

    "Pollen": 45,

    "Soil": 30,

    "Ant Egg": 450,

    "Sand": 30,

    "Lentil": 15,

    "Pincer": 30,

    "Shell": 30,

    "Beetle Egg": 180,

    "Third Eye": 30,

    "Cice": 21,

    "Boubloom": 75,

    "Boulder": 450,

    "Moon": 375,

    "Grape": 54
}

# ---------------- ENEMY RARITY MULTIPLIER ----------------

ENEMY_RARITY_MULTIPLIER = {

    "Common": 1.0,

    "Unusual": 9.0,

    "Rare": 20.0,

    "Epic": 70.0,

    "Legendary": 100.0,

    "Mythic": 400.0,

    "Ultra": 1000.0,

    "Super": 4000.0,

    "Omega": 9000.0,

    "Unique": 12000.0,

    "Eternal": 40000.0,

    "Cosmo": 90000.0,

    "Jeddiful": 120000.0,

    "Tacnic": 300000.0,

    "Radium": 700000.0,

    "Ancient": 1100000.0,

    "Omnient": 5000000.0,

    "Celestial": 7500000.0,

}

MULTIPLYING_PETALS = [
    "Light",
    "Rock",
    "Faster",
    "Rice",
    "Corn"
]

hp_menu_open = False

hp_button_rect = pygame.Rect(
    20,
    HEIGHT - 70,
    120,
    40
)

hp_upgrade_rect = pygame.Rect(
    WIDTH//2 - 100,
    HEIGHT//2,
    200,
    50
)

close_button_rect = pygame.Rect(
    WIDTH//2 + 50,
    HEIGHT//2 - 120,
    80,
    40
)

game_state = "login"

# Green-grid overlay shown briefly after a successful login / account
# creation. The grid tiles scroll right and a little down (clipped to the
# screen) until welcome_timer runs out, then the real game starts.

welcome_scroll_x = 0.0
welcome_scroll_y = 0.0
welcome_timer = 0

# Petal "reload": frames until the next batch of petals spawns. Groups of
# petals arrive together, then there's a lull before the next reload.

welcome_petal_reload = 40

# Currently highlighted biome on the welcome screen (None until one is
# pressed, then one of "garden", "desert", "ocean", "eagle", "farm").
welcome_selected_biome = None

# Smooth biome grid color transition on the welcome screen.
# BIOME_COLORS maps each biome name to its grid background color.
BIOME_COLORS = {
    "garden": (80, 200, 90),
    "desert": (222, 204, 150),
    "ocean": (80, 150, 200),
    "eagle": (180, 220, 60),
    "farm": (80, 200, 90),
}

welcome_grid_color = (80, 200, 90)
welcome_target_grid_color = (80, 200, 90)

# Biome selected on the welcome screen; persists into the game state so
# the real grid can use the same color.
selected_biome = None

# Game state grid color transition (used when transitioning from welcome to game)
game_grid_color = (60, 180, 75)
game_target_grid_color = (60, 180, 75)

# Set to True when the player clicks the green Play button
welcome_play_pressed = False
# Chat text visibility flag
chat_text_visible = True
# Chat input text
chat_input_text = ""
# Frame counter for chat cursor blinking
chat_cursor_frame = 0
chat_arrow_up = True
# Chat message history (list of (username, message) tuples)
chat_messages = []
# Chat scroll state
chat_scroll = 0
chat_scroll_target = 0
chat_scroll_position = 0.0
chat_dragging = False
chat_drag_offset = 0
chat_scrollbar_rect = pygame.Rect(0, 0, 12, 30)
chat_max_scroll = 0

# Set once per mouse click on the welcome screen so biome buttons only fire
# on the exact frame the button is pressed, not every frame the mouse is held.

welcome_click_pending = False

# Iris wipe transition used when the player clicks Play on the welcome screen.
# Phase "close": a full-screen black rectangle with a big circular hole in the
# center shrinks the hole down until the screen is fully black. Phase "open":
# after the game is shown, the hole expands back out until it is bigger than
# the screen (so no black edges are visible). progress runs 0 -> 1 in each
# phase.

welcome_transition_active = False
welcome_transition_phase = "close"   # "close" then "open"
welcome_transition_progress = 0.0

# radius of the circular hole in the black rect, in pixels
WELCOME_IRIS_START_RADIUS = 1200
WELCOME_IRIS_END_RADIUS = 0
# how many frames each phase takes
WELCOME_TRANSITION_LENGTH = 24

# Flying petals that sweep across the welcome grid. Each one starts offscreen
# on the left edge with a random y and size, and flies right (clipped to the
# screen).

welcome_petals = []
WELCOME_PETAL_COLORS = [
    (255, 232, 244),
    (255, 214, 230),
    (248, 214, 235),
    (255, 240, 210),
    (255, 224, 178),
    (224, 255, 231),
    (214, 227, 255),
    (255, 216, 216),
    (255, 255, 255),
]

WELCOME_PETAL_NAMES = [
    "Moon", "Basic", "Stinger", "Light", "Heavy", "Rice", "Rose",
    "Wing", "Cactus", "Leaf", "Pea", "Missile", "Bone", "Web",
    "Rock", "Faster", "Magnet", "Bubble", "Honey", "Poison", "Shark",
    "Corn", "Stick", "Clover", "Glass", "Antenna", "Pollen", "Soil",
    "Ant Egg", "Sand", "Lentil", "Pincer", "Shell", "Beetle Egg",
    "Third Eye", "Cice", "Boubloom", "Boulder", "Grape",
]

def init_welcome_petals():

    global welcome_petals
    global welcome_petal_reload

    welcome_petals = []
    welcome_petal_reload = random.randint(20, 60)

    for _ in range(random.randint(3, 8)):

        welcome_petals.append({
            "x": -random.randint(10, 300),
            "y": random.uniform(0, HEIGHT),
            "speed": random.uniform(1.0, 3.0),
            "size": random.uniform(8, 22),
            "wobble": random.uniform(0.0, 360.0),
            "spin": random.uniform(0.0, 360.0),
            "spin_speed": random.uniform(-6.0, 6.0),
            "name": random.choice(WELCOME_PETAL_NAMES),
            "surf": None,
        })

def draw_iris_wipe(radius):

    # full-screen black rectangle with a circular transparent hole of the
    # given radius centered on the screen. If the hole radius is 0 the whole
    # screen is black; if it is big enough to reach off-screen no black is
    # visible.

    wipe = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    wipe.fill((0, 0, 0, 255))
    if radius > 0:
        pygame.draw.circle(wipe, (0, 0, 0, 0), (WIDTH // 2, HEIGHT // 2), radius)
    screen.blit(wipe, (0, 0))

def wrap_text(font, text, max_width):
    """Split text into lines that fit within max_width pixels."""
    lines = []
    for word in text.split():
        if not lines:
            lines.append(word)
        else:
            test_line = f"{lines[-1]} {word}"
            if font.size(test_line)[0] <= max_width:
                lines[-1] = test_line
            else:
                lines.append(word)
    # Handle words that are too long to fit on a line (break at character level)
    final_lines = []
    for line in lines:
        if font.size(line)[0] <= max_width:
            final_lines.append(line)
        else:
            # Break the long word/line character by character
            current = ""
            for char in line:
                test = current + char
                if font.size(test)[0] <= max_width:
                    current = test
                else:
                    if current:
                        final_lines.append(current)
                    current = char
            if current:
                final_lines.append(current)
    return final_lines if final_lines else [""]

# ---------------- CHAT BAD WORD FILTER ----------------
BAD_WORDS = [
    "fucking", "shit", "bitch", "bastard", "fuck", "asshole",
    "cunt", "damn", "dick", "piss", "prick", "slut", "whore",
    "retard", "retarded", "kike", "nigger", "faggot", "dyke",
]

def is_bad_word(text):
    """Check if text contains any bad word (case-insensitive)."""
    text_lower = text.lower()
    for word in BAD_WORDS:
        if word in text_lower:
            return True
    return False

def format_elapsed(seconds):
    """Format elapsed time as a compact readable string."""
    seconds = int(max(0, seconds))
    if seconds < 60:
        return f"{seconds}s"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours, mins = divmod(minutes, 60)
    if hours < 24:
        return f"{hours}h {mins}m"
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h"

def draw_light_preview(x, y, rarity):

    count = get_petal_count("Light", rarity)

    light_color = (255, 255, 255)
    light_outline = (190, 190, 190)
    r = PETAL_RADIUS * 0.55

    for i in range(count):

        if count == 1:
            draw_x = x
            draw_y = y
            scale = 1.0
        else:
            angle_rad = math.radians(i * (360 / count))
            distance = PETAL_RADIUS * 0.55
            draw_x = x + math.cos(angle_rad) * distance
            draw_y = y + math.sin(angle_rad) * distance
            scale = 0.8

        pygame.draw.circle(
            screen,
            light_outline,
            (int(draw_x), int(draw_y)),
            int(r * scale + 2)
        )

        pygame.draw.circle(
            screen,
            light_color,
            (int(draw_x), int(draw_y)),
            int(r * scale)
        )

def make_petal_surface(name, x, y, rarity, size_scale=1.0):

    # renders one of the game's real petal pictures into an offscreen
    # surface and returns it, using the same draw_petal the game uses

    global screen
    global petal_angle

    old_screen = screen
    old_angle = petal_angle

    pad = 80
    surf = pygame.Surface((pad * 2, pad * 2), pygame.SRCALPHA)

    try:
        petal_angle = 0
        screen = surf
        if name == "Light":
            draw_light_preview(pad, pad, rarity)
        else:
            draw_petal(
                name,
                pad,
                pad,
                rarity,
                size_scale=size_scale
            )
    finally:
        screen = old_screen
        petal_angle = old_angle

    return surf

password_box = pygame.Rect(
    WIDTH//2 - 20,
    HEIGHT//2 - 200,
    220,
    45
)

acc_name_box = pygame.Rect(
    WIDTH//2 - 20,
    HEIGHT//2 - 100,
    220,
    45
)

# ---------------- LOGIN BUTTONS ----------------

login_box = pygame.Rect(
    WIDTH//2 - 250,
    HEIGHT//2 + -250,
    500,
    450
)
# Login button

login_rect = pygame.Rect(
    WIDTH//2 - 100,
    HEIGHT//2 - (-10),
    200,
    50
)


create_acc_button_rect = pygame.Rect(
    WIDTH//2 + -100,
    HEIGHT//2 + 70,
    200,
    50
)

# ---------------- INVENTORY ----------------

inventory_open = False

inventory_button_rect = pygame.Rect(
    hp_button_rect.x,
    hp_button_rect.y - 70,
    60,
    60
)

above_inventory_button_rect = pygame.Rect(
    inventory_button_rect.x,
    inventory_button_rect.y - 70,
    inventory_button_rect.width,
    inventory_button_rect.height
)

above_craft_button_rect = pygame.Rect(
    above_inventory_button_rect.x,
    above_inventory_button_rect.y - 70,
    above_inventory_button_rect.width,
    above_inventory_button_rect.height
)

settings_button_rect = pygame.Rect(
    above_craft_button_rect.x,
    above_craft_button_rect.y - 70,
    above_craft_button_rect.width,
    above_craft_button_rect.height
)

cmd_button_rect = pygame.Rect(
    settings_button_rect.x,
    settings_button_rect.y - 70,
    settings_button_rect.width,
    settings_button_rect.height
)

# ---------------- CMD PANEL ----------------

cmd_panel_open = False
# Sits to the right of the flower hp upgrade button, slides down from
# offscreen above the top edge and stops close to the bottom edge.
cmd_panel_target_rect = pygame.Rect(
    hp_button_rect.right + 10,
    10,
    280,
    max(200, HEIGHT - 40)
)
cmd_panel_rect = cmd_panel_target_rect.copy()
# Start fully offscreen above the top edge.
cmd_panel_rect.y = -cmd_panel_rect.height - 20
cmd_panel_slide_velocity = 0.0
# Scroll offset (in pixels) for the command list.
cmd_panel_scroll = 0

# ---------------- SETTINGS PANEL ----------------

settings_panel_open = False
# Close to the left edge without touching it, and stops just above the
# settings button.
settings_panel_target_rect = pygame.Rect(
    14,
    10,
    280,
    max(
        200,
        settings_button_rect.top - 40
    )
)
settings_panel_rect = settings_panel_target_rect.copy()
# Start fully offscreen above the top edge.
settings_panel_rect.y = -settings_panel_rect.height - 20
settings_panel_slide_velocity = 0.0
# Knob animation state for the settings button.
settings_button_knob_phase = 0.0
settings_button_knob_amplitude = 0.0
# Diamond spin state for the mob gallery button.
gallery_button_diamond_angle = 0.0
# Circle split state for the craft button.
craft_button_split_amount = 0.0
craft_button_spin_angle = 0.0
# Mob hp bar size slider in the settings panel.
settings_hp_bar_scale = 1.0
settings_hp_bar_knob_progress = 0.0
settings_hp_bar_dragging = False
settings_hp_bar_track_rect = pygame.Rect(0, 0, 10, 14)
settings_label_font = pygame.font.Font(None, 18)
cmd_button_font = pygame.font.Font(None, 25)
cmd_button_font.set_italic(True)
# Toggle switch in the settings panel.
settings_switch_on = False
settings_switch_rect = pygame.Rect(0, 0, 60, 14)
settings_switch_knob_progress = 0.0
settings_switch_slide_velocity = 0.0
# Second toggle switch in the settings panel.
settings_switch2_on = False
settings_switch2_rect = pygame.Rect(0, 0, 60, 14)
settings_switch2_knob_progress = 0.0
settings_switch2_slide_velocity = 0.0
# Third toggle switch: show hitbox.
settings_switch3_on = False
settings_switch3_rect = pygame.Rect(0, 0, 60, 14)
settings_switch3_knob_progress = 0.0
settings_switch3_slide_velocity = 0.0

new_button_panel_open = False
new_button_panel_target_rect = pygame.Rect(
    10,
    10,
    280,
    max(400, above_craft_button_rect.y - 30)
)
mob_gallery_grid_top = above_craft_button_rect.y - 168
new_button_panel_rect = new_button_panel_target_rect.copy()
new_button_panel_rect.x = -new_button_panel_rect.width
new_button_panel_slide_velocity = 0.0
mob_gallery_names = (
    "Ladybug",
    "Hole Ladybug",
    "Bee",
    "Hole Bee",
    "Spider",
    "Hole Spider",
    "Rock",
    "Hole Rock",
    "Hornet",
    "Hole Hornet",
    "Baby Ant",
    "Hole Baby Ant",
    "Soldier Ant",
    "Hole Soldier Ant",
    "Worker Ant",
    "Hole Worker Ant",
    "Queen Ant",
    "Hole Queen Ant",
    "Ant Egg"
)
mob_gallery_scroll_target = 0
mob_gallery_scroll_position = 0.0
GALLERY_MAX_VISIBLE_ROWS = 3
GALLERY_CELL_SIZE = 42
GALLERY_GRID_WINDOW_HEIGHT = (
    GALLERY_MAX_VISIBLE_ROWS * GALLERY_CELL_SIZE
)
mob_gallery_horizontal_scroll_target = 0
mob_gallery_horizontal_scroll_position = 0.0
mob_gallery_dragging = False
mob_gallery_x_dragging = False
mob_gallery_scrollbar_rect = pygame.Rect(0, 0, 12, 30)
mob_gallery_horizontal_scrollbar_rect = pygame.Rect(0, 0, 30, 12)
mob_gallery_unlocks = {}
mob_gallery_hover_key = None
mob_gallery_hover_spin = 0.0

craft_open = False
craft_scroll = 0
craft_scroll_target = 0
craft_scroll_position = 0.0
craft_dragging = False
craft_drag_offset = 0
craft_horizontal_scroll = 0
craft_horizontal_scroll_target = 0
craft_horizontal_scroll_position = 0.0
craft_x_dragging = False
craft_x_drag_offset = 0
craft_selected_items = []
craft_animation_active = False
craft_animation_timer = 0
craft_animation_duration = 0
craft_will_succeed = False
craft_should_converge = False
craft_animation_outcome = None
craft_result_text = ""
craft_result_item = None
craft_post_result_items = []
craft_animation_slot_amounts = []
craft_animation_grid_amount = None
craft_petals_cache = tuple(PETAL_HP.keys())
craft_rarities_cache = tuple(RARITY_COLORS.keys())
craft_button_font = pygame.font.Font(None, 22)
craft_count_font = pygame.font.Font(None, 18)
craft_success_font = pygame.font.Font(None, 17)
craft_grid_count_font = pygame.font.Font(None, 16)
respawn_timer_font = pygame.font.Font(None, 30)
hud_font = pygame.font.Font(None, 32)
large_hud_font = pygame.font.Font(None, 45)
game_hp_font = pygame.font.Font(None, 28)
spawn_message_font = pygame.font.Font(None, 48)
login_error_font = pygame.font.Font(None, 28)
flower_name_font = pygame.font.Font(None, 24)
flower_info_font = pygame.font.Font(None, 22)
gallery_count_font = pygame.font.Font(None, 14)
gallery_hover_name_font = pygame.font.Font(None, 24)
gallery_hover_desc_font = pygame.font.Font(None, 16)
moon_surface_cache = {}
craft_inventory_signature = None
craft_slot_items_cache = []
craft_slot_lookup_cache = {}
craft_panel_target_rect = pygame.Rect(
    above_inventory_button_rect.right + 12,
    HEIGHT - 560,
    280,
    540
)
craft_panel_rect = craft_panel_target_rect.copy()
craft_panel_rect.y = HEIGHT + 20
craft_panel_slide_velocity = 0.0
craft_scrollbar_rect = pygame.Rect(0, 0, 12, 40)
craft_horizontal_scrollbar_rect = pygame.Rect(0, 0, 40, 12)

def open_only_panel(panel_name):

    # The game allows only one panel to be open at a time.
    global new_button_panel_open
    global settings_panel_open
    global craft_open
    global inventory_open
    global hp_menu_open
    global cmd_panel_open

    new_button_panel_open = panel_name == "gallery"
    settings_panel_open = panel_name == "settings"
    craft_open = panel_name == "craft"
    inventory_open = panel_name == "inventory"
    hp_menu_open = panel_name == "hp"
    cmd_panel_open = panel_name == "cmd"


inventory_panel_rect = pygame.Rect(
    inventory_button_rect.centerx - 30,
    inventory_button_rect.y - 520,
    250,
    500
)

# Sliding inventory panel. It starts fully offscreen at the left edge of the
# game and accelerates back to its resting x position (above) when the
# inventory button is pressed. The y position is never changed.

inv_panel_x = float(-inventory_panel_rect.width)
inv_panel_vx = 0.0
inv_panel_target_x = inventory_panel_rect.x

def get_third_eye_range(petal_slots):

    best_range = PETAL_ATTACK

    for petal in petal_slots:

        if petal["petal"] == "Third Eye":

            rarity = petal["rarity"]

            if rarity in THIRD_EYE_RANGE:
                best_range = max(
                    best_range,
                    THIRD_EYE_RANGE[rarity]
                )

    return best_range

petal_attack = get_third_eye_range(petal_slots)

class Wall:

    def __init__(self, x, y, width, height):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

    def draw(self):

        # plain fill; connected rendering happens via the merged
        # wall_visual_surface blit in the render loop
        pygame.draw.rect(
            screen,
            (110, 70, 35),
            pygame.Rect(
                self.rect.x - camera_x,
                self.rect.y - camera_y,
                self.rect.width,
                self.rect.height
            )
        )

    def draw_map(self):

        pygame.draw.rect(
            screen,
            (255,255,255),
            pygame.Rect(
                MINIMAP_X + self.rect.x * MINIMAP_SIZE / WORLD_WIDTH,
                MINIMAP_Y + self.rect.y * MINIMAP_SIZE / WORLD_HEIGHT,
                self.rect.width * MINIMAP_SIZE / WORLD_WIDTH,
                self.rect.height * MINIMAP_SIZE / WORLD_HEIGHT
            )
        )

        MINIMAP_WALL_OFFSET_X = 0
        MINIMAP_WALL_OFFSET_Y = 0

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            pygame.Rect(
                MINIMAP_X + self.rect.x * MINIMAP_SIZE / MAP_SIZE + MINIMAP_WALL_OFFSET_X,
                MINIMAP_Y + self.rect.y * MINIMAP_SIZE / MAP_SIZE + MINIMAP_WALL_OFFSET_Y,
                self.rect.width * MINIMAP_SIZE / MAP_SIZE,
                self.rect.height * MINIMAP_SIZE / MAP_SIZE
            )
        )
# ---------------- LADYBUG ----------------

class Ladybug:

    def __init__(self):

        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.knockback_x = 0
        self.knockback_y = 0
        self.rarity = "Common"
        self.angry = False

        # bigger
        # HP
        self.damage = 50
        self.max_hp = (
            50 *
            MOB_HP_MULTIPLIER[self.rarity]
        )

        self.hp = self.max_hp
        self.alive = True
        self.flash_timer = 0
        self.radius = random.randint(20, 35)
        self.base_radius = self.radius
        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2   # <-- add this

        # King / minion flags (set by the /king command)
        self.is_king = False
        self.is_minion = False
        self.king_minion_timer = 0

        # direction
        self.angle = random.uniform(0,360)
        self.target_angle = self.angle

        # movement
        self.speed = 2.5
        self.max_speed = 2.5

        self.acceleration = 0.3
        self.friction = 0.4

        # AI
        self.state = "turn"
        self.timer = 0

        self.spots = []

        spot_count = random.randint(0, 5)

        for _ in range(spot_count):

            angle = random.uniform(
                0,
                math.pi * 2
            )

            distance = random.uniform(
                0,
                self.radius * 0.65
            )

            size = random.uniform(
                self.radius * 0.12,
                self.radius * 0.3
            )

            self.spots.append({
                "x": math.cos(angle) * distance,
                "y": math.sin(angle) * distance,
                "size": size
            })


    def turn_to(self, target_angle, turn_speed):

        difference = (target_angle - self.angle + 180) % 360 - 180

        if abs(difference) <= turn_speed:
            self.angle = target_angle
            return True

        self.angle += turn_speed if difference > 0 else -turn_speed

        return False


    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return

        self.timer += 1



        # ---------------- KING / MINION AI ----------------

        if getattr(self, "is_king", False):

            if king_chase_or_guard(self):
                return

        if getattr(self, "is_minion", False):

            minion_ai(self)
            return

        # ---------------- ANGRY LADYBUG ----------------

        if self.angry:

            # keep your existing angry movement here

            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )


            self.turn_to(
                target_angle,
                8
            )


            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.speed
            dy = math.sin(rad) * self.speed


            move_with_collision(
                self,
                dx,
                dy
            )


            return




        # ---------------- NORMAL CALM LADYBUG MOVEMENT ----------------


        # TURN

        if self.state == "turn":


            if self.turn_to(
                self.target_angle,
                2
            ):


                self.state = "walk"

                self.timer = 0




        # WALK

        elif self.state == "walk":


            if self.speed < self.max_speed:

                self.speed += self.acceleration



            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.speed * 0.15

            dy = math.sin(rad) * self.speed * 0.15


            move_with_collision(
                self,
                dx,
                dy
            )



            if self.timer >= 80:

                self.state = "slow"

                self.timer = 0





        # SLOW

        elif self.state == "slow":


            self.speed -= self.friction


            if self.speed < 0:

                self.speed = 0



            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.speed * 0.15

            dy = math.sin(rad) * self.speed * 0.15


            move_with_collision(
                self,
                dx,
                dy
            )



            if self.speed == 0:

                self.state = "pause"

                self.timer = 0





        # PAUSE

        elif self.state == "pause":


            if self.timer >= 50:


                self.target_angle = random.uniform(
                    0,
                    360
                )


                self.state = "turn"

                self.timer = 0

    def take_damage(self, amount):

        if not self.alive:
            return

        self.hp -= int(amount)
        self.flash_timer = 4
        # When damaged, become angry and chase the player
        if not getattr(self, "is_minion", False):
            self.angry = True

        if self.hp <= 0:

            if getattr(self, "death_registered", False):
                return
            self.death_registered = True

            cleanup_king(self)
            register_mob_kill(self)
            drop_mob_loot(self)

            # Die with a fast shrink instead of vanishing.
            self.dying = True
            self.shrink_scale = 1.0
            self.full_radius = self.radius

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    getattr(
                        self,
                        "custom_xp",
                        10 * MOB_XP_MULTIPLIER[self.rarity]
                    )
                )
            )

    def draw(self):

        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y


        if (
            sx < -100 or
            sx > WIDTH + 100 or
            sy < -100 or
            sy > HEIGHT + 100
        ):
            return



        # ---------------- HP BAR ----------------

        if self.hp < self.max_hp:

            bar_width = max(1, int(40 * settings_hp_bar_scale))
            bar_height = max(
                1,
                int(5 * settings_hp_bar_scale)
            )

            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))


            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )



        angle = math.radians(
            self.angle
        )



        # ---------------- LADYBUG BODY SURFACE ----------------

        size = self.radius * 2


        body_surface = pygame.Surface(
            (
                int(size),
                int(size)
            ),
            pygame.SRCALPHA
        )


        center = (
            int(self.radius),
            int(self.radius)
        )



        # red body (or yellow if flower minion)
        lb_body_col = (255, 230, 100) if getattr(self, "yellow_minion", False) else (220, 30, 30)
        lb_out_col = (210, 160, 40) if getattr(self, "yellow_minion", False) else (105, 25, 25)

        pygame.draw.circle(
            body_surface,
            flash_color(lb_body_col, self.flash_timer),
            center,
            int(self.radius)
        )



        # black spots

        for spot in self.spots:

            pygame.draw.circle(
                body_surface,
                flash_color((0,0,0), self.flash_timer),
                (
                    int(self.radius + spot["x"]),
                    int(self.radius + spot["y"])
                ),
                int(spot["size"])
            )



        # clip everything outside body circle

        mask = pygame.Surface(
            (
                int(size),
                int(size)
            ),
            pygame.SRCALPHA
        )


        pygame.draw.circle(
            mask,
            (255,255,255),
            center,
            int(self.radius)
        )


        body_surface.blit(
            mask,
            (0,0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        # Dark outline around the body.
        pygame.draw.circle(
            body_surface,
            flash_color(lb_out_col, self.flash_timer),
            center,
            int(self.radius),
            max(2, int(self.radius * 0.14))
        )



        screen.blit(
            body_surface,
            (
                int(sx - self.radius),
                int(sy - self.radius)
            )
        )



        # ---------------- HEAD ----------------

        head_x = (
            sx +
            math.cos(angle) * self.radius * 0.8
        )


        head_y = (
            sy +
            math.sin(angle) * self.radius * 0.8
        )


        pygame.draw.circle(
            screen,
            flash_color((0,0,0), self.flash_timer),
            (
                int(head_x),
                int(head_y)
            ),
            int(self.radius * 0.45)
        )

        # ---------------- KING CROWN ----------------

        if getattr(self, "is_king", False):

            crown_y = int(sy - self.radius - 14)
            crown_w = int(self.radius * 1.2)
            crown_h = int(self.radius * 0.6)
            crown_left = int(sx - crown_w / 2)
            crown_right = int(sx + crown_w / 2)

            # Base band + three points.
            crown_points = [
                (crown_left, crown_y + crown_h),
                (crown_left, crown_y + crown_h * 0.4),
                (
                    crown_left + crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (
                    int(sx - crown_w * 0.15),
                    crown_y
                ),
                (
                    int(sx + crown_w * 0.15),
                    crown_y + crown_h * 0.4
                ),
                (
                    crown_right - crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (crown_right, crown_y + crown_h * 0.4),
                (crown_right, crown_y + crown_h)
            ]

            pygame.draw.polygon(
                screen,
                flash_color((255, 200, 0), self.flash_timer),
                crown_points
            )
            pygame.draw.polygon(
                screen,
                flash_color((160, 110, 0), self.flash_timer),
                crown_points,
                2
            )

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- HOLE LADYBUG ----------------
# A weird abyss-corrupted Ladybug native exclusively to Hole Land.
# Exactly 2x the stats & size of a normal ladybug with eerie pulsing void aesthetics.
class HoleLadybug(Ladybug):
    is_hole_land_mob = True

    def __init__(self):
        super().__init__()
        # 2x size of regular ladybug
        self.radius = self.radius * 2
        self.base_radius = self.radius

        # 2x damage and 2x HP of regular ladybug
        self.damage = 100
        self.max_hp = (
            100 *
            MOB_HP_MULTIPLIER[self.rarity]
        )
        self.hp = self.max_hp

        # Weird void pulsation and twitching
        self.void_pulse = random.uniform(0, math.pi * 2)
        self.twitch_timer = 0
        self.speed = 2.8
        self.max_speed = 2.8
        self.shoot_cooldown = 0

    def update(self):
        if not self.alive or getattr(self, "dying", False):
            return
        super().update()
        if not self.alive or getattr(self, "dying", False):
            return
        self.void_pulse += 0.08
        self.twitch_timer += 1
        # Weird erratic twitching: sudden small angle snaps
        if self.twitch_timer >= 45:
            self.twitch_timer = 0
            if random.random() < 0.35:
                self.angle += random.uniform(-40, 40)

        # When chasing the player, shoot yellow circle projectiles
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.alive and not getattr(self, "dying", False) and self.angry and not player_dead and not player_ghost:
            p_dist = distance(self.x, self.y, player_x, player_y)
            if p_dist < 800 and self.shoot_cooldown <= 0:
                self.shoot_cooldown = random.randint(45, 75)
                aim_angle = math.atan2(player_y - self.y, player_x - self.x)
                orb_r = max(6, int(self.radius * 0.22))
                hole_ladybug_projectiles.append({
                    "x": self.x + math.cos(aim_angle) * (self.radius + orb_r),
                    "y": self.y + math.sin(aim_angle) * (self.radius + orb_r),
                    "dx": math.cos(aim_angle) * HOLE_LADYBUG_PROJECTILE_SPEED,
                    "dy": math.sin(aim_angle) * HOLE_LADYBUG_PROJECTILE_SPEED,
                    "damage": max(10, int(self.damage * 0.4)),
                    "hp": max(15, int(self.max_hp * 0.15)),
                    "max_hp": max(15, int(self.max_hp * 0.15)),
                    "radius": orb_r,
                    "timer": HOLE_LADYBUG_PROJECTILE_LIFETIME,
                    "owner": self
                })

    def draw(self):
        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if (
            sx < -150 or
            sx > WIDTH + 150 or
            sy < -150 or
            sy > HEIGHT + 150
        ):
            return

        # ---------------- HP BAR ----------------
        if self.hp < self.max_hp:
            bar_width = max(1, int(70 * settings_hp_bar_scale))
            bar_height = max(1, int(6 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (60, 20, 90),
                (int(sx - bar_width/2), int(sy - self.radius - 12 - bar_height), bar_width, bar_height)
            )
            pygame.draw.rect(
                screen,
                (180, 50, 255),
                (int(sx - bar_width/2), int(sy - self.radius - 12 - bar_height), int(bar_width * hp_percent), bar_height)
            )

        angle = math.radians(self.angle)
        size = self.radius * 2

        # Weird aura pulsing around hole ladybug
        pulse_val = math.sin(self.void_pulse) * 4
        aura_r = int(self.radius + 6 + pulse_val)
        aura_surf = pygame.Surface((aura_r * 2 + 4, aura_r * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (150, 40, 230, 45), (aura_r + 2, aura_r + 2), aura_r)
        screen.blit(aura_surf, (int(sx - aura_r - 2), int(sy - aura_r - 2)))

        # ---------------- WEIRD BODY SURFACE ----------------
        body_surface = pygame.Surface((int(size), int(size)), pygame.SRCALPHA)
        center = (int(self.radius), int(self.radius))

        # Deep cosmic void dark-purple body with corrupted streaks
        hl_body_col = (45, 12, 65)
        hl_out_col = (180, 60, 255)

        pygame.draw.circle(
            body_surface,
            flash_color(hl_body_col, self.flash_timer),
            center,
            int(self.radius)
        )

        # Weird glowing cyan/purple eye-spots on shell
        for spot in self.spots:
            spot_r = max(2, int(spot["size"]))
            sp_x = int(self.radius + spot["x"])
            sp_y = int(self.radius + spot["y"])
            # Glowing void spot
            pygame.draw.circle(
                body_surface,
                flash_color((0, 230, 255), self.flash_timer),
                (sp_x, sp_y),
                spot_r
            )
            pygame.draw.circle(
                body_surface,
                flash_color((180, 0, 255), self.flash_timer),
                (sp_x, sp_y),
                max(1, spot_r - 2)
            )

        # Body outline
        pygame.draw.circle(
            body_surface,
            flash_color(hl_out_col, self.flash_timer),
            center,
            int(self.radius),
            max(2, int(self.radius * 0.10))
        )

        screen.blit(body_surface, (int(sx - self.radius), int(sy - self.radius)))

        # ---------------- WEIRD HEAD & GLOWING EYES ----------------
        head_dist = self.radius * 0.8
        head_x = sx + math.cos(angle) * head_dist
        head_y = sy + math.sin(angle) * head_dist
        head_r = int(self.radius * 0.42)

        # Eyeless dark abyss head circle with glowing void outline
        pygame.draw.circle(
            screen,
            flash_color((10, 3, 18), self.flash_timer),
            (int(head_x), int(head_y)),
            head_r
        )
        pygame.draw.circle(
            screen,
            flash_color((180, 60, 255), self.flash_timer),
            (int(head_x), int(head_y)),
            head_r,
            max(2, int(head_r * 0.18))
        )

        # ---------------- RARITY TEXT ----------------
        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 18)
            )

class Bee:

    def __init__(self):

        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.knockback_x = 0
        self.knockback_y = 0
        self.angry = False

        # random size
        self.damage = 100
        self.radius = random.randint(12, 25)
        self.base_radius = self.radius
        self.rarity = "Common"

        # HP
        self.max_hp = (
            50 *
            MOB_HP_MULTIPLIER[self.rarity]
        )

        self.hp = self.max_hp
        self.alive = True
        self.flash_timer = 0
        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2   # <-- add this

        # Bees wander like slow slugs, but keep their original chase speed.
        self.wander_speed = 0.28
        self.chase_speed = 2.5
        self.speed = self.wander_speed

        self.max_speed = self.chase_speed

        self.acceleration = 0.015

        # direction

        # Wander left and right for a random number of turns on each side.
        self.wander_side = -1
        self.wander_steps_remaining = random.randint(2, 5)
        self.base_angle = 180
        self.angle = self.base_angle
        self.turn_velocity = 0

        # wave movement

        self.wave_offset = random.random() * 100
        self.time = random.random() * 100

        self.view_range = 250

        self.wave = random.uniform(
            0,
            100
        )
        self.angry = False

        # King / minion flags (set by the /king command)
        self.is_king = False
        self.is_minion = False
        self.king_minion_timer = 0
        self.king_chat_timer = 0
        self.king_rose_timer = 0

    def turn_to(self, target, speed):

        difference = (target - self.angle + 180) % 360 - 180

        if abs(difference) <= speed:
            self.angle = target
            return True

        if difference > 0:
            self.angle += speed
        else:
            self.angle -= speed

        return False

    def turn_with_acceleration(self, target):

        difference = (target - self.angle + 180) % 360 - 180

        if abs(difference) < 0.5:
            self.angle = target
            self.turn_velocity = 0
            return

        direction = 1 if difference > 0 else -1

        # Start with a large turn, then make smaller turns as the bee lines
        # up with its target direction.
        turn_speed = min(
            3.0,
            max(0.18, abs(difference) * 0.12)
        )
        self.turn_velocity = direction * turn_speed

        if turn_speed >= abs(difference):
            self.angle = target
            self.turn_velocity = 0
        else:
            self.angle += self.turn_velocity

    def take_damage(self, amount):

        if not self.alive:
            return

        self.angry = True
        self.hp -= int(amount)
        self.flash_timer = 4

        if self.hp <= 0:

            if getattr(self, "death_registered", False):
                return
            self.death_registered = True

            cleanup_king(self)
            register_mob_kill(self)
            drop_mob_loot(self)

            # Die with a fast shrink instead of vanishing.
            self.dying = True
            self.shrink_scale = 1.0
            self.full_radius = self.radius

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    getattr(
                        self,
                        "custom_xp",
                        10 * MOB_XP_MULTIPLIER[self.rarity]
                    )
                )
            )

        else:

            # bee becomes angry when hit
            self.angry = True

    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return

        self.time += 1

        # ---------------- KING AI ----------------
        # The bee king hunts the flower like the ladybug king: same
        # chase range and speed, always aggro while king.

        if getattr(self, "is_king", False):

            if king_chase_or_guard(self):
                return

        # ---------------- CHECK PLAYER ----------------

        distance_to_player = math.sqrt(
            (player_x - self.x) ** 2 +
            (player_y - self.y) ** 2
        )


        if distance_to_player <= self.view_range and self.angry:

            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )

            self.turn_to(
                target_angle,
                7
            )

        # ---------------- NORMAL WANDER ----------------

        else:

            difference_to_target = (
                self.base_angle - self.angle + 180
            ) % 360 - 180

            if abs(difference_to_target) < 0.5:

                self.wander_steps_remaining -= 1

                if self.wander_steps_remaining <= 0:
                    self.wander_side *= -1
                    self.wander_steps_remaining = random.randint(2, 5)

                center_angle = 180 if self.wander_side == -1 else 0
                self.base_angle = center_angle + random.uniform(-18, 18)



            self.turn_with_acceleration(self.base_angle)



        # ---------------- MOVE ----------------

        rad = math.radians(
            self.angle
        )


        current_speed = (
            self.chase_speed
            if self.angry
            else self.wander_speed
        )

        dx = math.cos(rad) * current_speed

        dy = math.sin(rad) * current_speed



        # flying movement

        dy += math.sin(
            pygame.time.get_ticks() / 300 + self.wave
        ) * 0.05



        move_with_collision(
            self,
            dx,
            dy
        )

    def draw(self):

        if not self.alive:
            return


        sx = self.x - camera_x
        sy = self.y - camera_y


        if (
            sx < -100 or
            sx > WIDTH + 100 or
            sy < -100 or
            sy > HEIGHT + 100
        ):
            return



        # ---------------- HP BAR ----------------

        if self.hp < self.max_hp:

            bar_width = max(1, int(35 * settings_hp_bar_scale))
            bar_height = max(
                1,
                int(5 * settings_hp_bar_scale)
            )



            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))



            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )



        # ---------------- BEE ----------------
        # Draw in local coordinates first, then rotate it with the bee's
        # direction.  The result matches the simple icon: yellow oval,
        # diagonal black bands, dark head/tail, and two antennae.
        length = self.radius * 3.0
        width = self.radius * 1.55
        padding = self.radius * 1.7

        bee = pygame.Surface(
            (int(length + padding * 2), int(width + padding * 2)),
            pygame.SRCALPHA
        )
        cx = bee.get_width() // 2
        cy = bee.get_height() // 2
        body_rect = pygame.Rect(
            int(cx - length / 2),
            int(cy - width / 2),
            int(length),
            int(width)
        )

        # Yellow body.
        pygame.draw.ellipse(bee, flash_color((255, 220, 40), self.flash_timer), body_rect)

        # Diagonal bands, clipped to the body ellipse.
        stripes = pygame.Surface(bee.get_size(), pygame.SRCALPHA)
        for x in (-length * 0.24, length * 0.08, length * 0.36):
            pygame.draw.line(
                stripes,
                flash_color((38, 38, 31), self.flash_timer),
                (cx + x, cy - width * 0.65),
                (cx + x, cy + width * 0.65),
                max(3, int(self.radius * 0.42))
            )
        body_mask = pygame.mask.from_surface(bee)
        stripes.blit(
            body_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0)),
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )
        bee.blit(stripes, (0, 0))

        # Dark golden petal-style outline around the oval body.
        pygame.draw.ellipse(
            bee,
            flash_color((190, 150, 25), self.flash_timer),
            body_rect,
            max(2, int(self.radius * 0.14))
        )

        # The head faces the movement direction; the pointed tail trails
        # behind it.
        head_x = int(cx + length * 0.43)
        stinger_tip = (
            0.82
            if type(self).__name__ == "Hornet"
            else 0.63
        )
        stinger_outline_points = [
            (int(cx - length * (stinger_tip + 0.04)), cy),
            (int(cx - length * 0.48), int(cy - width * 0.23)),
            (int(cx - length * 0.48), int(cy + width * 0.23)),
        ]
        stinger_points = [
            (int(cx - length * stinger_tip), cy),
            (int(cx - length * 0.50), int(cy - width * 0.18)),
            (int(cx - length * 0.50), int(cy + width * 0.18)),
        ]
        pygame.draw.polygon(
            bee,
            flash_color((82, 52, 24), self.flash_timer),
            stinger_outline_points
        )
        pygame.draw.polygon(
            bee,
            flash_color((42, 42, 35), self.flash_timer),
            stinger_points
        )
        pygame.draw.aalines(
            bee,
            flash_color((42, 42, 35), self.flash_timer),
            True,
            stinger_points
        )

        # Antennae extend from the head, with round tips.
        antenna_color = flash_color((42, 42, 35), self.flash_timer)
        antenna_width = max(2, int(self.radius * 0.16))
        antenna_start_x = head_x + self.radius * 0.12

        if type(self).__name__ == "Hornet":
            # Hornet antennae are simple and straight.
            antennae = [
                [
                    (antenna_start_x, cy - self.radius * 0.22),
                    (head_x + self.radius * 0.78,
                     cy - self.radius * 0.75),
                ],
                [
                    (antenna_start_x, cy + self.radius * 0.22),
                    (head_x + self.radius * 0.78,
                     cy + self.radius * 0.75),
                ],
            ]
        else:
            correct_antenna = [
                (antenna_start_x, cy + self.radius * 0.22),
                (head_x + self.radius * 0.55, cy + self.radius * 0.55),
                (head_x + self.radius * 0.65, cy + self.radius * 0.85),
            ]

            # Copy the correct antenna, flip it 180 degrees, and move it to
            # the other side of the head.
            other_start = (antenna_start_x, cy - self.radius * 0.22)
            correct_start = correct_antenna[0]
            flipped_antenna = [
                (
                    other_start[0] - (point[0] - correct_start[0]),
                    other_start[1] - (point[1] - correct_start[1])
                )
                for point in correct_antenna
            ]

            # Turn the copied antenna 90 degrees around its base.
            flipped_antenna = [
                (
                    other_start[0] - (point[1] - other_start[1]),
                    other_start[1] + (point[0] - other_start[0])
                )
                for point in flipped_antenna
            ]
            antennae = [correct_antenna, flipped_antenna]

        for points in antennae:
            # Draw each segment as a clean rotated rectangle so thick
            # antennae do not get slanted parallelogram ends.
            for segment_index in range(len(points) - 1):
                draw_clean_line(
                    bee,
                    antenna_color,
                    points[segment_index],
                    points[segment_index + 1],
                    antenna_width
                )
            end = points[-1]
            if type(self).__name__ != "Hornet":
                pygame.draw.circle(
                    bee, antenna_color,
                    (int(end[0]), int(end[1])),
                    max(2, int(self.radius * 0.22))
                )

        bee = pygame.transform.rotate(bee, -self.angle)
        screen.blit(bee, bee.get_rect(center=(int(sx), int(sy))))

        # ---------------- KING CROWN ----------------

        if getattr(self, "is_king", False):

            crown_y = int(sy - self.radius - 18)
            crown_w = int(self.radius * 1.2)
            crown_h = int(self.radius * 0.6)
            crown_left = int(sx - crown_w / 2)
            crown_right = int(sx + crown_w / 2)

            crown_points = [
                (crown_left, crown_y + crown_h),
                (crown_left, crown_y + crown_h * 0.4),
                (
                    crown_left + crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (
                    int(sx - crown_w * 0.15),
                    crown_y
                ),
                (
                    int(sx + crown_w * 0.15),
                    crown_y + crown_h * 0.4
                ),
                (
                    crown_right - crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (crown_right, crown_y + crown_h * 0.4),
                (crown_right, crown_y + crown_h)
            ]

            pygame.draw.polygon(
                screen,
                flash_color((255, 200, 0), self.flash_timer),
                crown_points
            )
            pygame.draw.polygon(
                screen,
                flash_color((160, 110, 0), self.flash_timer),
                crown_points,
                2
            )

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- HOLE BEE ----------------
# A deeply weird, corrupted abyss insect native exclusively to Hole Land.
# 2x stats & size of regular Bee.
# Morphologically warped: segmented chitin body, 4 erratic fluttering void wings,
# dual jagged stingers, and twisting tendril antennae.
class HoleBee(Bee):
    is_hole_land_mob = True

    def __init__(self):
        super().__init__()
        # 2x stats & size of regular Bee
        self.radius = self.radius * 2
        self.base_radius = self.radius
        self.damage = 200
        self.max_hp = 100 * MOB_HP_MULTIPLIER[self.rarity]
        self.hp = self.max_hp

        # Weird twitching & void animation
        self.void_pulse = random.uniform(0, math.pi * 2)
        self.wing_jitter = random.uniform(0, math.pi * 2)
        self.twitch_timer = 0
        self.chase_speed = 3.6
        self.wander_speed = 0.5
        self.speed = self.wander_speed
        self.max_speed = self.chase_speed

    def update(self):
        if not self.alive or getattr(self, "dying", False):
            return
        super().update()
        if not self.alive or getattr(self, "dying", False):
            return
        self.void_pulse += 0.09
        self.wing_jitter += 0.45
        self.twitch_timer += 1
        # Erratic unpredictable twitching
        if self.twitch_timer >= 35:
            self.twitch_timer = 0
            if random.random() < 0.4:
                self.angle += random.uniform(-45, 45)

    def draw(self):
        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if sx < -160 or sx > WIDTH + 160 or sy < -160 or sy > HEIGHT + 160:
            return

        # ---------------- HP BAR ----------------
        if self.hp < self.max_hp:
            bar_width = max(1, int(65 * settings_hp_bar_scale))
            bar_height = max(1, int(6 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (50, 15, 75),
                (int(sx - bar_width/2), int(sy - self.radius - 14 - bar_height), bar_width, bar_height)
            )
            pygame.draw.rect(
                screen,
                (200, 40, 255),
                (int(sx - bar_width/2), int(sy - self.radius - 14 - bar_height), int(bar_width * hp_percent), bar_height)
            )

        # ---------------- PULSING VOID AURA ----------------
        pulse = math.sin(self.void_pulse) * 5
        aura_r = int(self.radius * 1.35 + pulse)
        aura_surf = pygame.Surface((aura_r * 2 + 6, aura_r * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (140, 30, 220, 45), (aura_r + 3, aura_r + 3), aura_r)
        screen.blit(aura_surf, (int(sx - aura_r - 3), int(sy - aura_r - 3)))

        # ---------------- WARPED SURFACE RENDERING ----------------
        length = self.radius * 3.4
        width = self.radius * 1.8
        padding = self.radius * 2.2

        surf_w = int(length + padding * 2)
        surf_h = int(width + padding * 2)
        bee_surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        cx = surf_w // 2
        cy = surf_h // 2

        # 1. FOUR FLUTTERING WEIRD VOID WINGS (translucent cyan-violet membranous fins)
        wing_w = int(self.radius * 1.5)
        wing_h = int(self.radius * 0.75)
        w_flap1 = math.sin(self.wing_jitter) * (self.radius * 0.3)
        w_flap2 = math.cos(self.wing_jitter * 1.2) * (self.radius * 0.3)

        # Left wings (top and bottom offset)
        w1_pts = [
            (cx - int(length * 0.05), cy - int(width * 0.35)),
            (cx - int(length * 0.45), cy - int(width * 0.95 + w_flap1)),
            (cx + int(length * 0.25), cy - int(width * 0.85 + w_flap2)),
        ]
        pygame.draw.polygon(bee_surf, (0, 240, 255, 90), w1_pts)
        pygame.draw.polygon(bee_surf, (180, 50, 255, 180), w1_pts, 2)

        w2_pts = [
            (cx - int(length * 0.05), cy + int(width * 0.35)),
            (cx - int(length * 0.45), cy + int(width * 0.95 + w_flap2)),
            (cx + int(length * 0.25), cy + int(width * 0.85 + w_flap1)),
        ]
        pygame.draw.polygon(bee_surf, (0, 240, 255, 90), w2_pts)
        pygame.draw.polygon(bee_surf, (180, 50, 255, 180), w2_pts, 2)

        # Secondary smaller back wings
        w3_pts = [
            (cx - int(length * 0.25), cy - int(width * 0.25)),
            (cx - int(length * 0.65), cy - int(width * 0.70 + w_flap2)),
            (cx - int(length * 0.15), cy - int(width * 0.60 + w_flap1)),
        ]
        pygame.draw.polygon(bee_surf, (180, 40, 240, 80), w3_pts)
        pygame.draw.polygon(bee_surf, (0, 240, 255, 160), w3_pts, 1)

        w4_pts = [
            (cx - int(length * 0.25), cy + int(width * 0.25)),
            (cx - int(length * 0.65), cy + int(width * 0.70 + w_flap1)),
            (cx - int(length * 0.15), cy + int(width * 0.60 + w_flap2)),
        ]
        pygame.draw.polygon(bee_surf, (180, 40, 240, 80), w4_pts)
        pygame.draw.polygon(bee_surf, (0, 240, 255, 160), w4_pts, 1)

        # 2. SEGMENTED WARPED CHITIN BODY
        # Segment A: Rear Abdomen (dark obsidian violet)
        seg_rear_rect = pygame.Rect(int(cx - length * 0.48), int(cy - width * 0.38), int(length * 0.42), int(width * 0.76))
        pygame.draw.ellipse(bee_surf, flash_color((30, 8, 45), self.flash_timer), seg_rear_rect)
        pygame.draw.ellipse(bee_surf, flash_color((170, 45, 255), self.flash_timer), seg_rear_rect, 2)

        # Segment B: Middle Thorax (eerie dark indigo)
        seg_mid_rect = pygame.Rect(int(cx - length * 0.15), int(cy - width * 0.48), int(length * 0.38), int(width * 0.96))
        pygame.draw.ellipse(bee_surf, flash_color((20, 5, 35), self.flash_timer), seg_mid_rect)
        pygame.draw.ellipse(bee_surf, flash_color((0, 230, 255), self.flash_timer), seg_mid_rect, 2)

        # Corrupted neon glowing rib stripes on thorax
        for st_x in (cx - length * 0.05, cx + length * 0.08):
            pygame.draw.line(
                bee_surf,
                flash_color((0, 255, 240), self.flash_timer),
                (st_x, cy - width * 0.40),
                (st_x, cy + width * 0.40),
                max(2, int(self.radius * 0.16))
            )

        # Segment C: Weird Eyeless Head (tilted jagged dome)
        head_cx = int(cx + length * 0.32)
        head_r = int(self.radius * 0.58)
        pygame.draw.circle(bee_surf, flash_color((15, 3, 25), self.flash_timer), (head_cx, cy), head_r)
        pygame.draw.circle(bee_surf, flash_color((190, 60, 255), self.flash_timer), (head_cx, cy), head_r, 2)

        # 3. DUAL JAGGED SPLIT STINGERS AT TAIL
        stinger_base_x = int(cx - length * 0.48)
        stinger_tip_x = int(cx - length * 0.72)
        stinger_upper = [
            (stinger_base_x, cy - int(width * 0.18)),
            (stinger_base_x, cy - int(width * 0.04)),
            (stinger_tip_x, cy - int(width * 0.22)),
        ]
        pygame.draw.polygon(bee_surf, flash_color((0, 240, 255), self.flash_timer), stinger_upper)

        stinger_lower = [
            (stinger_base_x, cy + int(width * 0.04)),
            (stinger_base_x, cy + int(width * 0.18)),
            (stinger_tip_x, cy + int(width * 0.22)),
        ]
        pygame.draw.polygon(bee_surf, flash_color((0, 240, 255), self.flash_timer), stinger_lower)

        # 4. TWISTED ASYMMETRIC TENDRIL ANTENNAE WITH GLOWING NODES
        ant_col = flash_color((160, 50, 240), self.flash_timer)
        ant_node_col = flash_color((0, 255, 255), self.flash_timer)
        # Upper antenna
        pygame.draw.lines(
            bee_surf, ant_col, False,
            [
                (head_cx + int(head_r * 0.5), cy - int(head_r * 0.4)),
                (head_cx + int(head_r * 1.3), cy - int(head_r * 1.1)),
                (head_cx + int(head_r * 1.7), cy - int(head_r * 0.7)),
            ],
            max(2, int(self.radius * 0.14))
        )
        pygame.draw.circle(bee_surf, ant_node_col, (head_cx + int(head_r * 1.7), cy - int(head_r * 0.7)), max(3, int(self.radius * 0.16)))

        # Lower antenna (curved differently for asymmetric weirdness)
        pygame.draw.lines(
            bee_surf, ant_col, False,
            [
                (head_cx + int(head_r * 0.5), cy + int(head_r * 0.4)),
                (head_cx + int(head_r * 1.1), cy + int(head_r * 1.3)),
                (head_cx + int(head_r * 1.8), cy + int(head_r * 1.4)),
            ],
            max(2, int(self.radius * 0.14))
        )
        pygame.draw.circle(bee_surf, ant_node_col, (head_cx + int(head_r * 1.8), cy + int(head_r * 1.4)), max(3, int(self.radius * 0.16)))

        # Blit rotated
        rot_surf = pygame.transform.rotate(bee_surf, -self.angle)
        screen.blit(rot_surf, rot_surf.get_rect(center=(int(sx), int(sy))))

        # ---------------- RARITY TEXT ----------------
        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 18)
            )

# ---------------- SPIDER ----------------

class Spider:

    def __init__(self):

        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.knockback_x = 0
        self.knockback_y = 0
        self.rarity = "Common"
                # HP
        self.damage = 75
        self.max_hp = (
            75 *
            MOB_HP_MULTIPLIER[self.rarity]
        )

        self.hp = self.max_hp
        self.alive = True
        self.flash_timer = 0
        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2   # <-- add this
        self.charging = False
        self.charge_speed = 0


        # size

        self.radius = random.randint(18, 25)
        self.base_radius = self.radius



        # movement (ladybug style)

        self.speed = 2

        self.max_speed = 10

        self.acceleration = 0.3

        self.friction = 0.4



        # rotation

        self.angle = random.uniform(0,360)

        self.target_angle = self.angle



        # AI

        self.state = "turn"

        self.timer = 0



        # detection

        self.view_range = self.radius * 20



        # attack behavior

        self.following = False

        self.attack_distance = 45

        self.follow_speed = 2.5
        self.leg_phase = 0.0

        # King / minion flags (set by the /king command)
        self.is_king = False
        self.is_minion = False
        self.king_minion_timer = 0
        self.king_chat_timer = 0
        self.king_rose_timer = 0
        self.king_web_timer = 0




    def turn_to(self, target, amount=2):

        difference = target - self.angle


        if difference > 180:
            difference -= 360

        if difference < -180:
            difference += 360



        if abs(difference) <= amount:

            self.angle = target

            return True



        if difference > 0:

            self.angle += amount

        else:

            self.angle -= amount


        return False



    def take_damage(self, amount):

        if not self.alive:
            return

        self.hp -= int(amount)
        self.flash_timer = 4

        if self.hp <= 0:

            if getattr(self, "death_registered", False):
                return
            self.death_registered = True

            cleanup_king(self)
            register_mob_kill(self)
            drop_mob_loot(self)

            # Die with a fast shrink instead of vanishing.
            self.dying = True
            self.shrink_scale = 1.0
            self.full_radius = self.radius

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    getattr(
                        self,
                        "custom_xp",
                        10 * MOB_XP_MULTIPLIER[self.rarity]
                    )
                )
            )

    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return

        self.timer += 1

        # ---------------- KING AI ----------------
        # The spider king hunts the flower like the other kings:
        # same chase range and speed, always aggro while king.

        if getattr(self, "is_king", False):

            if king_chase_or_guard(self):
                return

        # ---------------- CHECK PLAYER DISTANCE ----------------

        distance = math.sqrt(
            (player_x - self.x) ** 2 +
            (player_y - self.y) ** 2
        )

        self.following = distance <= self.view_range
        self.leg_phase += 0.48 if self.following else 0.08


        # ---------------- CHASE PLAYER ----------------

        if self.following:


            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )


            self.turn_to(
                target_angle,
                7
            )


            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.speed

            dy = math.sin(rad) * self.speed


            move_with_collision(
                self,
                dx,
                dy
            )

        # ---------------- NORMAL WANDER ----------------

        else:


            if self.timer >= 120:

                self.target_angle = random.uniform(
                    0,
                    360
                )


                self.timer = 0



            self.turn_to(
                self.target_angle,
                1
            )


            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.speed * 0.3

            dy = math.sin(rad) * self.speed * 0.3


            move_with_collision(
                self,
                dx,
                dy
            )


    def draw(self):

        if not self.alive:
            return


        sx = self.x - camera_x
        sy = self.y - camera_y


        # ---------------- HP BAR ----------------

        if self.hp < self.max_hp:

            bar_width = max(1, int(40 * settings_hp_bar_scale))
            bar_height = max(
                1,
                int(5 * settings_hp_bar_scale)
            )

            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    bar_width,
                    bar_height
                )
            )

            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )



        # ---------------- OFF SCREEN CHECK ----------------

        if (
            sx < -100 or
            sx > WIDTH + 100 or
            sy < -100 or
            sy > HEIGHT + 100
        ):
            return



        # ---------------- VISION RANGE ----------------

        angle = math.radians(
            self.angle
        )


        fx = math.cos(angle)

        fy = math.sin(angle)

        side_x = -fy

        side_y = fx



        # ---------------- LEGS ----------------

        for side in [-1, 1]:

            for i in range(4):

                offset = (
                    i - 1.5
                ) * self.radius * 0.35



                start_x = (
                    sx
                    + side_x * side * self.radius * 0.6
                    + fx * offset
                )

                start_y = (
                    sy
                    + side_y * side * self.radius * 0.6
                    + fy * offset
                )



                end_x = (
                    sx
                    + side_x * side * self.radius * 1.8
                    + fx * offset
                )

                end_y = (
                    sy
                    + side_y * side * self.radius * 1.8
                    + fy * offset
                )

                # Alternate legs forward and backward.  The motion is
                # faster while chasing and gentle while wandering.
                leg_swing = math.sin(
                    self.leg_phase
                    + i * 0.85
                    + (math.pi if side == 1 else 0)
                ) * self.radius * (0.24 if self.following else 0.07)
                end_x += fx * leg_swing
                end_y += fy * leg_swing



                # Leg thickness follows body size so small portraits
                # (mob gallery) do not get oversized legs.
                leg_thickness = max(1, int(self.radius * 0.2))

                draw_clean_line(
                    screen,
                    flash_color((20,20,20), self.flash_timer),
                    (start_x, start_y),
                    (end_x, end_y),
                    leg_thickness
                )



        # ---------------- BODY ----------------
        sp_out_col = (210, 160, 40) if getattr(self, "yellow_minion", False) else (18, 18, 18)
        sp_body_col = (255, 230, 100) if getattr(self, "yellow_minion", False) else (40, 40, 40)

        pygame.draw.circle(
            screen,
            flash_color(sp_out_col, self.flash_timer),
            (
                int(sx),
                int(sy)
            ),
            self.radius + 2
        )

        pygame.draw.circle(
            screen,
            flash_color(sp_body_col, self.flash_timer),
            (
                int(sx),
                int(sy)
            ),
            self.radius
        )

        # ---------------- KING CROWN ----------------

        if getattr(self, "is_king", False):

            crown_y = int(sy - self.radius - 16)
            crown_w = int(self.radius * 1.2)
            crown_h = int(self.radius * 0.6)
            crown_left = int(sx - crown_w / 2)
            crown_right = int(sx + crown_w / 2)

            crown_points = [
                (crown_left, crown_y + crown_h),
                (crown_left, crown_y + crown_h * 0.4),
                (
                    crown_left + crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (
                    int(sx - crown_w * 0.15),
                    crown_y
                ),
                (
                    int(sx + crown_w * 0.15),
                    crown_y + crown_h * 0.4
                ),
                (
                    crown_right - crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (crown_right, crown_y + crown_h * 0.4),
                (crown_right, crown_y + crown_h)
            ]

            pygame.draw.polygon(
                screen,
                flash_color((255, 200, 0), self.flash_timer),
                crown_points
            )
            pygame.draw.polygon(
                screen,
                flash_color((160, 110, 0), self.flash_timer),
                crown_points,
                2
            )

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- HOLE SPIDER ----------------
# A nightmarish, eyeless void arachnid native exclusively to Hole Land.
# 2x size, 2x HP, 2x damage.
# Morphologically warped: completely eyeless obsidian abdomen, 8 elongated
# jointed barbed legs that twitch erratically, and glowing void runes.
class HoleSpider(Spider):
    is_hole_land_mob = True

    def __init__(self):
        super().__init__()
        # 2x size, HP, damage of regular Spider
        self.radius = self.radius * 2
        self.base_radius = self.radius
        self.damage = 150
        self.max_hp = 150 * MOB_HP_MULTIPLIER[self.rarity]
        self.hp = self.max_hp

        # Weird twitching & void animation
        self.void_pulse = random.uniform(0, math.pi * 2)
        self.twitch_timer = 0
        self.speed = 3.2
        self.follow_speed = 3.8
        self.max_speed = 12

    def update(self):
        if not self.alive or getattr(self, "dying", False):
            return
        super().update()
        if not self.alive or getattr(self, "dying", False):
            return
        self.void_pulse += 0.08
        self.twitch_timer += 1
        # Erratic twitching
        if self.twitch_timer >= 40:
            self.twitch_timer = 0
            if random.random() < 0.35:
                self.angle += random.uniform(-40, 40)

    def draw(self):
        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if sx < -180 or sx > WIDTH + 180 or sy < -180 or sy > HEIGHT + 180:
            return

        # ---------------- HP BAR ----------------
        if self.hp < self.max_hp:
            bar_width = max(1, int(70 * settings_hp_bar_scale))
            bar_height = max(1, int(6 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (45, 12, 65),
                (int(sx - bar_width/2), int(sy - self.radius - 14 - bar_height), bar_width, bar_height)
            )
            pygame.draw.rect(
                screen,
                (190, 50, 255),
                (int(sx - bar_width/2), int(sy - self.radius - 14 - bar_height), int(bar_width * hp_percent), bar_height)
            )

        # ---------------- PULSING VOID AURA ----------------
        pulse = math.sin(self.void_pulse) * 5
        aura_r = int(self.radius * 1.3 + pulse)
        aura_surf = pygame.Surface((aura_r * 2 + 6, aura_r * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (130, 25, 210, 40), (aura_r + 3, aura_r + 3), aura_r)
        screen.blit(aura_surf, (int(sx - aura_r - 3), int(sy - aura_r - 3)))

        # ---------------- VISION / ANGLE VECTORS ----------------
        angle = math.radians(self.angle)
        fx = math.cos(angle)
        fy = math.sin(angle)
        side_x = -fy
        side_y = fx

        # ---------------- 8 WEIRD JOINTED BARBED VOID LEGS ----------------
        # Deep obsidian purple leg base with electric cyan joint accents
        leg_col = flash_color((30, 10, 45), self.flash_timer)
        leg_joint_col = flash_color((0, 230, 255), self.flash_timer)
        leg_tip_col = flash_color((180, 50, 255), self.flash_timer)
        leg_thickness = max(2, int(self.radius * 0.16))

        for side in [-1, 1]:
            for i in range(4):
                offset = (i - 1.5) * self.radius * 0.42

                start_x = sx + side_x * side * self.radius * 0.65 + fx * offset
                start_y = sy + side_y * side * self.radius * 0.65 + fy * offset

                # Swing phase
                leg_swing = math.sin(
                    self.leg_phase + i * 0.9 + (math.pi if side == 1 else 0)
                ) * self.radius * (0.30 if self.following else 0.10)

                # Mid-joint (elbow) elevated further outward
                joint_dist = self.radius * 1.5
                joint_x = sx + side_x * side * joint_dist + fx * (offset + leg_swing * 0.5)
                joint_y = sy + side_y * side * joint_dist + fy * (offset + leg_swing * 0.5)

                # Sharp hooked end tip
                tip_dist = self.radius * 2.3
                tip_x = sx + side_x * side * tip_dist + fx * (offset + leg_swing)
                tip_y = sy + side_y * side * tip_dist + fy * (offset + leg_swing)

                # First segment (body to joint)
                draw_clean_line(screen, leg_col, (start_x, start_y), (joint_x, joint_y), leg_thickness)
                # Second segment (joint to barbed tip)
                draw_clean_line(screen, leg_col, (joint_x, joint_y), (tip_x, tip_y), max(1, leg_thickness - 1))

                # Glowing node on joint
                pygame.draw.circle(screen, leg_joint_col, (int(joint_x), int(joint_y)), max(2, int(self.radius * 0.10)))
                # Glowing tip barb
                pygame.draw.circle(screen, leg_tip_col, (int(tip_x), int(tip_y)), max(2, int(self.radius * 0.08)))

        # ---------------- COMPLETELY EYELESS ABYSS BODY ----------------
        # Outer corrupted boundary
        pygame.draw.circle(
            screen,
            flash_color((170, 50, 240), self.flash_timer),
            (int(sx), int(sy)),
            int(self.radius + 3)
        )
        # Deep obsidian void core (strictly eyeless)
        pygame.draw.circle(
            screen,
            flash_color((16, 5, 26), self.flash_timer),
            (int(sx), int(sy)),
            int(self.radius)
        )

        # Weird internal pulsing void marks (not eyes, rune-like vein arcs)
        rune_col = flash_color((0, 240, 255), self.flash_timer)
        p1 = (int(sx + fx * self.radius * 0.35), int(sy + fy * self.radius * 0.35))
        p2 = (int(sx - fx * self.radius * 0.40 + side_x * self.radius * 0.35), int(sy - fy * self.radius * 0.40 + side_y * self.radius * 0.35))
        p3 = (int(sx - fx * self.radius * 0.40 - side_x * self.radius * 0.35), int(sy - fy * self.radius * 0.40 - side_y * self.radius * 0.35))
        pygame.draw.polygon(screen, rune_col, [p1, p2, p3], max(1, int(self.radius * 0.08)))

        # ---------------- RARITY TEXT ----------------
        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 18)
            )

# ---------------- ROCK ----------------

class Rock:

    def __init__(self):

        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.knockback_x = 0
        self.knockback_y = 0
        self.rarity = "Common"
        self.angry = False

        # HP
        self.damage = random.randint(50, 120)
        self.max_hp = (
            random.randint(40, 120) *
            MOB_HP_MULTIPLIER[self.rarity]
        )

        self.hp = self.max_hp
        self.alive = True
        self.flash_timer = 0
        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2   # <-- add this

        # random size
        self.radius = int(self.max_hp / 4)

        # Random rocky silhouette: uneven number of sides, each corner
        # at its own random distance from the center.
        point_count = random.randint(6, 9)
        self.shape_points = []
        for point_index in range(point_count):
            point_angle = (
                math.pi * 2 * point_index / point_count
                + random.uniform(-0.35, 0.35)
            )
            point_distance = random.uniform(0.82, 1.15)
            self.shape_points.append(
                (
                    math.cos(point_angle) * point_distance,
                    math.sin(point_angle) * point_distance
                )
            )

        # King flags (set by the /king command) and rock volley timer
        self.is_king = False
        self.is_minion = False
        self.king_minion_timer = 0
        self.king_orbit_slot = 0
        self.rock_volley_timer = 0
        self.angle = 0
        self.speed = 0

    def turn_to(self, target_angle, speed=6):
        difference = (target_angle - self.angle + 180) % 360 - 180
        if abs(difference) <= speed:
            self.angle = target_angle
            return True
        self.angle += speed if difference > 0 else -speed
        return False

    def take_damage(self, amount):

        self.hp -= int(amount)
        self.flash_timer = 4

        if self.hp <= 0:

            if getattr(self, "death_registered", False):
                return
            self.death_registered = True

            cleanup_king(self)
            register_mob_kill(self)
            drop_mob_loot(self)

            # Die with a fast shrink instead of vanishing.
            self.dying = True
            self.shrink_scale = 1.0
            self.full_radius = self.radius

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    getattr(
                        self,
                        "custom_xp",
                        10 * MOB_XP_MULTIPLIER[self.rarity]
                    )
                )
            )


    def push(self, dx, dy):

        if not self.alive:
            return

        self.x += dx
        self.y += dy
        self.x = max(self.radius, min(self.x, WORLD_WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, WORLD_HEIGHT - self.radius))


    def update(self):

        if not self.alive:
            return

        # Rock minions orbit their king and shoot at the flower
        # every 0.5 seconds.
        if getattr(self, "is_minion", False):

            king = kings.get("Rock")
            if (
                king is not None
                and king.alive
            ):
                # March around the king's guard ring.
                king_orbit = max(
                    70,
                    int(king.radius * 1.6) + 40
                )
                orbit_slot = getattr(
                    self,
                    "king_orbit_slot",
                    0
                )
                orbit_angle = (
                    time.time() * 1.2
                    + orbit_slot * (2 * math.pi / 5)
                )
                target_x = (
                    king.x
                    + math.cos(orbit_angle) * king_orbit
                )
                target_y = (
                    king.y
                    + math.sin(orbit_angle) * king_orbit
                )
                dx = target_x - self.x
                dy = target_y - self.y
                length = math.sqrt(dx * dx + dy * dy)
                step = KING_GUARD_SPEED * 2.5
                if length > step:
                    self.x += dx / length * step
                    self.y += dy / length * step
                else:
                    self.x = target_x
                    self.y = target_y

                # Never touch the king: bounce away from him.
                kd = distance(
                    self.x,
                    self.y,
                    king.x,
                    king.y
                )
                king_min_dist = king.radius + self.radius + 4
                if 0 < kd < king_min_dist:
                    overlap = king_min_dist - kd
                    self.x += (
                        (self.x - king.x) / kd * overlap
                    )
                    self.y += (
                        (self.y - king.y) / kd * overlap
                    )

            # Orbiting rocks aim and shoot a single rock at the
            # flower every 1 second.
            if not player_dead:
                self.rock_volley_timer += 1
                if self.rock_volley_timer >= 60:
                    self.rock_volley_timer = 0
                    aim_angle = math.degrees(
                        math.atan2(
                            player_y - self.y,
                            player_x - self.x
                        )
                    )
                    rock_projectiles.append(
                        {
                            "x": self.x,
                            "y": self.y,
                            "angle": aim_angle,
                            "dx": (
                                math.cos(
                                    math.radians(aim_angle)
                                )
                                * ROCK_PROJECTILE_SPEED
                            ),
                            "dy": (
                                math.sin(
                                    math.radians(aim_angle)
                                )
                                * ROCK_PROJECTILE_SPEED
                            ),
                            "damage": max(
                                1, int(self.damage / 3)
                            ),
                            "radius": max(
                                4, int(self.radius / 3)
                            ),
                            "hp": max(1, int(self.max_hp / 3)),
                            "max_hp": max(
                                1, int(self.max_hp / 3)
                            ),
                            "shape": self.shape_points,
                            "is_king_shot": False,
                            "timer": ROCK_PROJECTILE_LIFETIME,
                            "owner": self
                        }
                    )
            return

        # Normal rocks volley every 8 seconds; rock kings every 2.
        if not player_dead:
            self.rock_volley_timer += 1
            interval = (
                ROCK_KING_VOLLEY_INTERVAL
                if getattr(self, "is_king", False)
                else ROCK_VOLLEY_INTERVAL
            )
            if self.rock_volley_timer >= interval:
                self.rock_volley_timer = 0
                fire_rock_volley(
                    self,
                    getattr(self, "is_king", False)
                )


    def draw(self):

        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y


        if (
            sx < -100 or
            sx > WIDTH + 100 or
            sy < -100 or
            sy > HEIGHT + 100
        ):
            return


        # HP bar

        if self.hp < self.max_hp:

            bar_width = max(1, int(50 * settings_hp_bar_scale))
            bar_height = max(
                1,
                int(6 * settings_hp_bar_scale)
            )

            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    bar_width,
                    bar_height
                )
            )

            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )


        # rock body
        rk_body_col = (255, 230, 100) if getattr(self, "yellow_minion", False) else (120, 120, 120)
        rk_out_col = (210, 160, 40) if getattr(self, "yellow_minion", False) else (75, 75, 75)

        rock_points = [
            (
                int(sx + point_x * self.radius),
                int(sy + point_y * self.radius)
            )
            for point_x, point_y in self.shape_points
        ]

        pygame.draw.polygon(
            screen,
            flash_color(rk_body_col, self.flash_timer),
            rock_points
        )


        # rock outline

        pygame.draw.polygon(
            screen,
            flash_color(rk_out_col, self.flash_timer),
            rock_points,
            max(2, int(self.radius * 0.12))
        )

        # ---------------- KING CROWN ----------------

        if getattr(self, "is_king", False):

            crown_y = int(sy - self.radius - 16)
            crown_w = int(self.radius * 1.2)
            crown_h = int(self.radius * 0.6)
            crown_left = int(sx - crown_w / 2)
            crown_right = int(sx + crown_w / 2)

            crown_points = [
                (crown_left, crown_y + crown_h),
                (crown_left, crown_y + crown_h * 0.4),
                (
                    crown_left + crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (
                    int(sx - crown_w * 0.15),
                    crown_y
                ),
                (
                    int(sx + crown_w * 0.15),
                    crown_y + crown_h * 0.4
                ),
                (
                    crown_right - crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (crown_right, crown_y + crown_h * 0.4),
                (crown_right, crown_y + crown_h)
            ]

            pygame.draw.polygon(
                screen,
                flash_color((255, 200, 0), self.flash_timer),
                crown_points
            )
            pygame.draw.polygon(
                screen,
                flash_color((160, 110, 0), self.flash_timer),
                crown_points,
                2
            )

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- HOLE ROCK ----------------
# A violently jagged, spike-encrusted obsidian mineral native to Hole Land.
# 2x size, 2x HP, 2x damage.
# ~80% more spikier: 14 to 20 alternating deeply recessed valleys and razor-sharp
# protruding spikes with glowing void crystal tips and pulsing fissures.
class HoleRock(Rock):
    is_hole_land_mob = True

    def __init__(self):
        super().__init__()
        # 2x stats & size
        self.radius = self.radius * 2
        self.base_radius = self.radius
        self.damage = int(self.damage * 2)
        self.max_hp = int(self.max_hp * 2)
        self.hp = self.max_hp

        # ~80% more spikier: alternating deep valleys and elongated jutting spikes
        spike_count = random.randint(14, 20)
        self.shape_points = []
        for i in range(spike_count):
            angle = (math.pi * 2 * i / spike_count) + random.uniform(-0.15, 0.15)
            # Alternating valleys (0.45 - 0.65) and extreme protruding spikes (1.65 - 2.15)
            if i % 2 == 1:
                dist = random.uniform(1.65, 2.15)  # 80%+ spike protrusion
            else:
                dist = random.uniform(0.45, 0.65)  # deep valley cleft
            self.shape_points.append((math.cos(angle) * dist, math.sin(angle) * dist))

        # Void animation
        self.void_pulse = random.uniform(0, math.pi * 2)
        self.twitch_timer = 0

    def update(self):
        if not self.alive or getattr(self, "dying", False):
            return
        super().update()
        if not self.alive or getattr(self, "dying", False):
            return
        self.void_pulse += 0.08
        self.twitch_timer += 1
        if self.twitch_timer >= 50:
            self.twitch_timer = 0
            if random.random() < 0.3:
                self.angle = (self.angle + random.uniform(-30, 30)) % 360

    def draw(self):
        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if sx < -180 or sx > WIDTH + 180 or sy < -180 or sy > HEIGHT + 180:
            return

        # ---------------- HP BAR ----------------
        if self.hp < self.max_hp:
            bar_width = max(1, int(80 * settings_hp_bar_scale))
            bar_height = max(1, int(6 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (45, 12, 60),
                (int(sx - bar_width/2), int(sy - self.radius * 1.5 - 12 - bar_height), bar_width, bar_height)
            )
            pygame.draw.rect(
                screen,
                (190, 50, 255),
                (int(sx - bar_width/2), int(sy - self.radius * 1.5 - 12 - bar_height), int(bar_width * hp_percent), bar_height)
            )

        # ---------------- PULSING VOID AURA ----------------
        pulse = math.sin(self.void_pulse) * 4
        aura_r = int(self.radius * 1.6 + pulse)
        aura_surf = pygame.Surface((aura_r * 2 + 6, aura_r * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (120, 20, 200, 38), (aura_r + 3, aura_r + 3), aura_r)
        screen.blit(aura_surf, (int(sx - aura_r - 3), int(sy - aura_r - 3)))

        # ---------------- 80% SPIKIER ROCK POLYGON ----------------
        rock_points = [
            (
                int(sx + point_x * self.radius),
                int(sy + point_y * self.radius)
            )
            for point_x, point_y in self.shape_points
        ]

        # Dark abyss body fill
        hl_rock_body = (25, 8, 38)
        hl_rock_out = (180, 50, 255)
        pygame.draw.polygon(
            screen,
            flash_color(hl_rock_body, self.flash_timer),
            rock_points
        )

        # Corrupted glowing jagged perimeter
        pygame.draw.polygon(
            screen,
            flash_color(hl_rock_out, self.flash_timer),
            rock_points,
            max(2, int(self.radius * 0.10))
        )

        # Electric glowing crystals at outer spike tips
        for i, (point_x, point_y) in enumerate(self.shape_points):
            if i % 2 == 1:  # Outer spike apex
                tip_px = int(sx + point_x * self.radius)
                tip_py = int(sy + point_y * self.radius)
                pygame.draw.circle(
                    screen,
                    flash_color((0, 240, 255), self.flash_timer),
                    (tip_px, tip_py),
                    max(2, int(self.radius * 0.08))
                )

        # Internal glowing void fissures radiating from core
        fissure_col = flash_color((150, 30, 230), self.flash_timer)
        for i in range(0, len(self.shape_points), 3):
            vx, vy = self.shape_points[i]
            target_pt = (int(sx + vx * self.radius * 0.65), int(sy + vy * self.radius * 0.65))
            draw_clean_line(screen, fissure_col, (int(sx), int(sy)), target_pt, max(1, int(self.radius * 0.06)))

        # ---------------- RARITY TEXT ----------------
        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius * 1.5 + 16)
            )

class Hornet:

    def __init__(self):

        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.knockback_x = 0
        self.knockback_y = 0
        self.rarity = "Common"

        # HP
        self.damage = 100
        self.max_hp = (
            50 *
            MOB_HP_MULTIPLIER[self.rarity]
        )

        self.hp = self.max_hp
        self.alive = True
        self.flash_timer = 0
        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2
        # <-- add this

        # size

        self.radius = random.randint(18, 25)
        self.base_radius = self.radius

        # direction

        self.angle = random.uniform(0, 360)
        self.target_angle = self.angle

        # bee style movement

        self.speed = 0.5
        self.max_speed = 0.75
        self.acceleration = 0.03

        # wave movement

        self.wave = random.random() * 10

        # turning timer

        self.timer = random.randint(0, 100)

        # player detection

        self.view_range = 450
        self.following = False
        self.follow_speed = 2.4

        # missile

        self.shoot_timer = 0
        self.missile_cooldown = 90

        # King / minion flags (set by the /king command)
        self.is_king = False
        self.is_minion = False
        self.king_minion_timer = 0
        self.king_chat_timer = 0
        self.king_rose_timer = 0
        self.king_orbit_slot = 0


    def take_damage(self, amount):

        if not self.alive:
            return

        self.hp -= int(amount)
        self.flash_timer = 4

        if self.hp <= 0:

            if getattr(self, "death_registered", False):
                return
            self.death_registered = True

            cleanup_king(self)
            register_mob_kill(self)
            drop_mob_loot(self)

            # Die with a fast shrink instead of vanishing.
            self.dying = True
            self.shrink_scale = 1.0
            self.full_radius = self.radius

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    getattr(
                        self,
                        "custom_xp",
                        10 * MOB_XP_MULTIPLIER[self.rarity]
                    )
                )
            )


    def turn_to(self, target, amount):

        difference = target - self.angle

        if difference > 180:
            difference -= 360

        if difference < -180:
            difference += 360

        if abs(difference) < amount:

            self.angle = target

        else:

            if difference > 0:
                self.angle += amount
            else:
                self.angle -= amount


    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return


        self.timer += 1

        # ---------------- KING AI ----------------
        # The hornet king never moves. It spins 15 degrees per
        # frame and fires missiles every 0.2 seconds.

        if getattr(self, "is_king", False):

            self.angle = (self.angle + 15) % 360

            self.shoot_timer += 1
            if self.shoot_timer >= 3:
                self.shoot_timer = 0
                fire_hornet_missile(self)

            return

        if getattr(self, "is_minion", False):
            hornet_minion_ai(self)
            return



        # ---------------- DISTANCE TO PLAYER ----------------

        distance_to_player = math.hypot(
            player_x - self.x,
            player_y - self.y
        )



        # ---------------- SEE PLAYER ----------------

        if distance_to_player <= self.view_range:

            self.following = True


        elif distance_to_player > self.view_range * 1.5:

            self.following = False



        # ---------------- FOLLOW PLAYER ----------------

        if self.following:


            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )


            self.turn_to(
                target_angle,
                7
            )


            rad = math.radians(
                self.angle
            )


            if distance_to_player > 250:


                dx = math.cos(rad) * self.follow_speed

                dy = math.sin(rad) * self.follow_speed


                move_with_collision(
                    self,
                    dx,
                    dy
                )

            else:
                # Stopped next to the flower: whip around fast so
                # the rear-mounted missile faces it, then fire.
                back_angle = (target_angle + 180) % 360
                self.turn_to(back_angle, 14)

                self.shoot_timer += 1
                if self.shoot_timer >= self.missile_cooldown:
                    self.shoot_timer = 0
                    fire_hornet_missile(self)

            return



        # ---------------- BEE STYLE MOVEMENT ----------------


        if self.speed < self.max_speed:

            self.speed += self.acceleration



        rad = math.radians(
            self.angle
        )


        dx = math.cos(rad) * self.speed

        dy = math.sin(rad) * self.speed



        # flying wave

        dx += math.cos(
            pygame.time.get_ticks() / 300 + self.wave
        ) * 0.1


        dy += math.sin(
            pygame.time.get_ticks() / 300 + self.wave
        ) * 0.3



        move_with_collision(
            self,
            dx,
            dy
        )



        # change direction

        if self.timer >= 180:

            self.timer = 0

            self.target_angle = random.uniform(
                0,
                360
            )


        self.turn_to(
            self.target_angle,
            1.5
        )

    def draw(self):

        if not self.alive:
            return

        # Hornets use the finished bee appearance for now; their movement
        # and attack behavior remain specific to Hornet.
        Bee.draw(self)
        return


        sx = self.x - camera_x
        sy = self.y - camera_y



        if (
            sx < -100 or
            sx > WIDTH + 100 or
            sy < -100 or
            sy > HEIGHT + 100
        ):
            return



        # ---------------- HP BAR ----------------

        if self.hp < self.max_hp:

            bar_width = max(1, int(45 * settings_hp_bar_scale))
            bar_height = max(
                1,
                int(5 * settings_hp_bar_scale)
            )

            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))


            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 11 - bar_height),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 11 - bar_height),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )



        angle = math.radians(
            self.angle
        )


        fx = math.cos(angle)

        fy = math.sin(angle)

        side_x = -fy

        side_y = fx



        # ---------------- MISSILE ----------------

        back_x = -fx
        back_y = -fy


        missile_length = self.radius * 2.5

        missile_width = self.radius * 0.45



        missile_points = [

            (
                sx + back_x * missile_length,
                sy + back_y * missile_length
            ),

            (
                sx + back_x * self.radius
                + side_x * missile_width,

                sy + back_y * self.radius
                + side_y * missile_width
            ),

            (
                sx + back_x * self.radius
                - side_x * missile_width,

                sy + back_y * self.radius
                - side_y * missile_width
            )

        ]


        pygame.draw.polygon(
            screen,
            (0,0,0),
            missile_points
        )



        # ---------------- BODY ----------------

        length = self.radius * 3

        width = self.radius * 1.1



        hornet = pygame.Surface(
            (
                int(length*2),
                int(width*2)
            ),
            pygame.SRCALPHA
        )


        cx = hornet.get_width()//2

        cy = hornet.get_height()//2



        pygame.draw.ellipse(
            hornet,
            (255,220,0),
            (
                cx-length/2,
                cy-width/2,
                length,
                width
            )
        )



        for offset in [-0.35, 0, 0.35]:

            pygame.draw.line(
                hornet,
                (0,0,0),
                (
                    cx + offset * length,
                    cy - width/2
                ),
                (
                    cx + offset * length,
                    cy + width/2
                ),
                3
            )



        hornet = pygame.transform.rotate(
            hornet,
            -self.angle
        )


        rect = hornet.get_rect(
            center=(int(sx), int(sy))
        )


        screen.blit(
            hornet,
            rect
        )



        # ---------------- ANTENNAS ----------------

        head_x = (
            sx +
            fx * self.radius * 1.2
        )

        head_y = (
            sy +
            fy * self.radius * 1.2
        )



        for side in [-1, 1]:

            end_x = (
                head_x
                + side_x * side * self.radius * 0.8
                + fx * self.radius * 0.5
            )

            end_y = (
                head_y
                + side_y * side * self.radius * 0.8
                + fy * self.radius * 0.5
            )


            pygame.draw.line(
                screen,
                (0,0,0),
                (
                    int(head_x),
                    int(head_y)
                ),
                (
                    int(end_x),
                    int(end_y)
                ),
                2
            )

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- HOLE HORNET ----------------
# A nightmarish, eyeless void bio-interceptor native exclusively to Hole Land.
# 2x size, 2x HP, 2x damage.
# Morphologically warped: segmented obsidian armor, 4 trembling void wings,
# dual rear-mounted void torpedo stingers, and twitching tendril antennae.
class HoleHornet(Hornet):
    is_hole_land_mob = True

    def __init__(self):
        super().__init__()
        # 2x stats & size
        self.radius = self.radius * 2
        self.base_radius = self.radius
        self.damage = 200
        self.max_hp = 100 * MOB_HP_MULTIPLIER[self.rarity]
        self.hp = self.max_hp

        # Weird twitching & void animation
        self.void_pulse = random.uniform(0, math.pi * 2)
        self.wing_jitter = random.uniform(0, math.pi * 2)
        self.twitch_timer = 0
        self.follow_speed = 3.6
        self.missile_cooldown = 70

    def update(self):
        if not self.alive or getattr(self, "dying", False):
            return
        super().update()
        if not self.alive or getattr(self, "dying", False):
            return
        self.void_pulse += 0.09
        self.wing_jitter += 0.50
        self.twitch_timer += 1
        if self.twitch_timer >= 35:
            self.twitch_timer = 0
            if random.random() < 0.35:
                self.angle = (self.angle + random.uniform(-35, 35)) % 360

    def draw(self):
        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if sx < -180 or sx > WIDTH + 180 or sy < -180 or sy > HEIGHT + 180:
            return

        # ---------------- HP BAR ----------------
        if self.hp < self.max_hp:
            bar_width = max(1, int(70 * settings_hp_bar_scale))
            bar_height = max(1, int(6 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (45, 12, 60),
                (int(sx - bar_width/2), int(sy - self.radius - 14 - bar_height), bar_width, bar_height)
            )
            pygame.draw.rect(
                screen,
                (190, 50, 255),
                (int(sx - bar_width/2), int(sy - self.radius - 14 - bar_height), int(bar_width * hp_percent), bar_height)
            )

        # ---------------- PULSING VOID AURA ----------------
        pulse = math.sin(self.void_pulse) * 5
        aura_r = int(self.radius * 1.4 + pulse)
        aura_surf = pygame.Surface((aura_r * 2 + 6, aura_r * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (140, 25, 210, 42), (aura_r + 3, aura_r + 3), aura_r)
        screen.blit(aura_surf, (int(sx - aura_r - 3), int(sy - aura_r - 3)))

        # ---------------- BIO-INTERCEPTOR FIGHTER CHASSIS ----------------
        # Distinct aerodynamic dart design with swept delta wings, underwing missiles,
        # and pulsing exhaust jets so it looks completely distinct from Hole Bee.
        length = self.radius * 3.8
        width = self.radius * 2.6
        padding = self.radius * 2.2

        surf_w = int(length + padding * 2)
        surf_h = int(width + padding * 2)
        hornet_surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        cx = surf_w // 2
        cy = surf_h // 2

        # 1. TWIN REAR VOID JET EXHAUST PLUMES (flickering electric cyan and magenta thrust)
        flame_len = self.radius * (0.8 + 0.3 * math.sin(self.wing_jitter * 2.0))
        for jet_offset_y in (-int(width * 0.16), int(width * 0.16)):
            flame_pts = [
                (cx - int(length * 0.42), cy + jet_offset_y - int(self.radius * 0.14)),
                (cx - int(length * 0.42 + flame_len), cy + jet_offset_y),
                (cx - int(length * 0.42), cy + jet_offset_y + int(self.radius * 0.14)),
            ]
            pygame.draw.polygon(hornet_surf, (0, 240, 255, 180), flame_pts)
            inner_flame = [
                (cx - int(length * 0.42), cy + jet_offset_y - int(self.radius * 0.07)),
                (cx - int(length * 0.42 + flame_len * 0.6), cy + jet_offset_y),
                (cx - int(length * 0.42), cy + jet_offset_y + int(self.radius * 0.07)),
            ]
            pygame.draw.polygon(hornet_surf, (255, 255, 255, 230), inner_flame)

        # 2. SWEPT-BACK SHARP DELTA WINGS (angular interceptor wings)
        wing_flare = math.sin(self.wing_jitter) * (self.radius * 0.15)
        # Left (top) swept delta wing
        w_top = [
            (cx + int(length * 0.05), cy - int(width * 0.18)),
            (cx - int(length * 0.38), cy - int(width * 0.95 + wing_flare)),
            (cx - int(length * 0.28), cy - int(width * 0.22)),
        ]
        pygame.draw.polygon(hornet_surf, (20, 8, 38, 240), w_top)
        pygame.draw.polygon(hornet_surf, flash_color((0, 240, 255), self.flash_timer), w_top, 2)

        # Right (bottom) swept delta wing
        w_bot = [
            (cx + int(length * 0.05), cy + int(width * 0.18)),
            (cx - int(length * 0.38), cy + int(width * 0.95 - wing_flare)),
            (cx - int(length * 0.28), cy + int(width * 0.22)),
        ]
        pygame.draw.polygon(hornet_surf, (20, 8, 38, 240), w_bot)
        pygame.draw.polygon(hornet_surf, flash_color((0, 240, 255), self.flash_timer), w_bot, 2)

        # Glowing neon chevron decals along the wings
        pygame.draw.line(
            hornet_surf,
            flash_color((210, 50, 255), self.flash_timer),
            (cx - int(length * 0.08), cy - int(width * 0.30)),
            (cx - int(length * 0.32), cy - int(width * 0.85 + wing_flare)),
            max(2, int(self.radius * 0.10))
        )
        pygame.draw.line(
            hornet_surf,
            flash_color((210, 50, 255), self.flash_timer),
            (cx - int(length * 0.08), cy + int(width * 0.30)),
            (cx - int(length * 0.32), cy + int(width * 0.85 - wing_flare)),
            max(2, int(self.radius * 0.10))
        )

        # 3. MOUNTED UNDER-WING MISSILE PODS (clearly visible void ordnance)
        for pod_y in (-int(width * 0.48), int(width * 0.48)):
            # Missile body (dark purple cylindrical dart)
            missile_rect = pygame.Rect(
                cx - int(length * 0.28),
                cy + pod_y - int(self.radius * 0.12),
                int(length * 0.32),
                int(self.radius * 0.24)
            )
            pygame.draw.rect(hornet_surf, flash_color((15, 5, 25), self.flash_timer), missile_rect)
            pygame.draw.rect(hornet_surf, flash_color((0, 255, 240), self.flash_timer), missile_rect, 1)
            # Glowing warhead tip
            warhead = [
                (cx + int(length * 0.04), cy + pod_y),
                (cx - int(length * 0.04), cy + pod_y - int(self.radius * 0.12)),
                (cx - int(length * 0.04), cy + pod_y + int(self.radius * 0.12)),
            ]
            pygame.draw.polygon(hornet_surf, flash_color((255, 0, 120), self.flash_timer), warhead)

        # 4. SLEEK ANGULAR FUSELAGE / HULL (sharp diamond/arrowhead body)
        hull_pts = [
            (cx + int(length * 0.44), cy),                                # Needle nose
            (cx + int(length * 0.18), cy - int(width * 0.24)),           # Forward port shoulder
            (cx - int(length * 0.38), cy - int(width * 0.20)),           # Port engine bay
            (cx - int(length * 0.44), cy),                                # Rear centerline exhaust
            (cx - int(length * 0.38), cy + int(width * 0.20)),           # Starboard engine bay
            (cx + int(length * 0.18), cy + int(width * 0.24)),           # Forward starboard shoulder
        ]
        pygame.draw.polygon(hornet_surf, flash_color((18, 6, 32), self.flash_timer), hull_pts)
        pygame.draw.polygon(hornet_surf, flash_color((180, 45, 255), self.flash_timer), hull_pts, max(2, int(self.radius * 0.10)))

        # Center spine ridge with energy conduit
        pygame.draw.line(
            hornet_surf,
            flash_color((0, 255, 255), self.flash_timer),
            (cx - int(length * 0.35), cy),
            (cx + int(length * 0.38), cy),
            max(2, int(self.radius * 0.12))
        )

        # Sleek eyeless cockpit visor slit (horizontal cyan visor stripe instead of eyes)
        visor_pts = [
            (cx + int(length * 0.12), cy - int(width * 0.10)),
            (cx + int(length * 0.28), cy),
            (cx + int(length * 0.12), cy + int(width * 0.10)),
        ]
        pygame.draw.lines(hornet_surf, flash_color((0, 255, 240), self.flash_timer), False, visor_pts, max(2, int(self.radius * 0.10)))

        # 5. SHARP NEEDLE PROBOSCIS & SWEPT MECHANICAL SENSORS
        # Needle probe jutting far out the front
        probe_tip = (cx + int(length * 0.65), cy)
        pygame.draw.line(
            hornet_surf,
            flash_color((0, 240, 255), self.flash_timer),
            (cx + int(length * 0.40), cy),
            probe_tip,
            max(2, int(self.radius * 0.14))
        )
        pygame.draw.circle(hornet_surf, flash_color((255, 60, 200), self.flash_timer), probe_tip, max(2, int(self.radius * 0.10)))

        # Swept-forward sensor antennae
        ant_col = flash_color((190, 50, 255), self.flash_timer)
        ant_tip_col = flash_color((0, 255, 255), self.flash_timer)
        for s_mult in (-1, 1):
            s_base = (cx + int(length * 0.26), cy + s_mult * int(width * 0.12))
            s_mid = (cx + int(length * 0.45), cy + s_mult * int(width * 0.28))
            s_tip = (cx + int(length * 0.58), cy + s_mult * int(width * 0.22))
            draw_clean_line(hornet_surf, ant_col, s_base, s_mid, max(2, int(self.radius * 0.10)))
            draw_clean_line(hornet_surf, ant_col, s_mid, s_tip, max(2, int(self.radius * 0.08)))
            pygame.draw.circle(hornet_surf, ant_tip_col, s_tip, max(2, int(self.radius * 0.10)))

        # Blit rotated
        rot_surf = pygame.transform.rotate(hornet_surf, -self.angle)
        screen.blit(rot_surf, rot_surf.get_rect(center=(int(sx), int(sy))))

        # ---------------- RARITY TEXT ----------------
        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 18)
            )

# ---------------- BABY ANT ----------------

class BabyAnt:

    def __init__(self):

        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.knockback_x = 0
        self.knockback_y = 0
        self.rarity = "Common"

        # Stats
        self.damage = 25
        self.max_hp = (
            35 *
            MOB_HP_MULTIPLIER[self.rarity]
        )

        self.hp = self.max_hp
        self.alive = True
        self.flash_timer = 0
        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2   # <-- add this

        # Size
        self.radius = random.randint(12, 18)

        # Direction
        self.angle = random.uniform(0, 360)
        self.target_angle = self.angle

        # Movement (Ladybug style)
        self.speed = 0
        self.max_speed = 2.5

        self.acceleration = 0.3
        self.friction = 0.4

        # AI
        self.state = "turn"
        self.timer = 0

        # King / minion flags (set by the /king command)
        self.is_king = False
        self.is_minion = False
        self.king_minion_timer = 0
        self.king_chat_timer = 0
        self.king_rose_timer = 0
        self.king_orbit_slot = 0

    def turn_to(self, target_angle, speed):

        difference = (
            target_angle - self.angle + 180
        ) % 360 - 180


        if abs(difference) <= speed:

            self.angle = target_angle

            return True


        if difference > 0:

            self.angle += speed

        else:

            self.angle -= speed


        return False


    def take_damage(self, amount):

        if not self.alive:
            return

        self.hp -= int(amount)
        self.flash_timer = 4

        if self.hp <= 0:

            if getattr(self, "death_registered", False):
                return
            self.death_registered = True

            cleanup_king(self)
            register_mob_kill(self)
            drop_mob_loot(self)

            # Die with a fast shrink instead of vanishing.
            self.dying = True
            self.shrink_scale = 1.0
            self.full_radius = self.radius

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    getattr(
                        self,
                        "custom_xp",
                        10 * MOB_XP_MULTIPLIER[self.rarity]
                    )
                )
            )


    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return


        self.timer += 1

        # ---------------- KING AI ----------------
        # The baby ant king hunts like the other kings; its rice
        # petals orbit it (drawn in draw()).

        if getattr(self, "is_king", False):

            if king_chase_or_guard(self):
                return

        if getattr(self, "is_minion", False):

            minion_ai(self)
            return

        # ---------------- ANGRY BABY ANT ----------------
        # Chases the player when angry (e.g. hatched from broken Ant Egg)
        if getattr(self, "angry", False) and not player_dead:
            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )
            self.turn_to(target_angle, 6)
            rad = math.radians(self.angle)
            chase_speed = 3.0
            dx = math.cos(rad) * chase_speed
            dy = math.sin(rad) * chase_speed
            move_with_collision(self, dx, dy)
            return

        # ---------------- NORMAL BABY ANT MOVEMENT ----------------


        # TURN

        if self.state == "turn":


            if self.turn_to(
                self.target_angle,
                2
            ):


                self.state = "walk"

                self.timer = 0




        # WALK

        elif self.state == "walk":


            if self.speed < self.max_speed:

                self.speed += self.acceleration



            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.speed * 0.15

            dy = math.sin(rad) * self.speed * 0.15



            move_with_collision(
                self,
                dx,
                dy
            )



            if self.timer >= 80:

                self.state = "slow"

                self.timer = 0





        # SLOW

        elif self.state == "slow":


            self.speed -= self.friction


            if self.speed < 0:

                self.speed = 0



            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.speed * 0.15

            dy = math.sin(rad) * self.speed * 0.15



            move_with_collision(
                self,
                dx,
                dy
            )



            if self.speed == 0:

                self.state = "pause"

                self.timer = 0





        # PAUSE

        elif self.state == "pause":


            if self.timer >= 50:


                self.target_angle = random.uniform(
                    0,
                    360
                )


                self.state = "turn"

                self.timer = 0

    def draw(self):

        if not self.alive:
            return



        sx = self.x - camera_x
        sy = self.y - camera_y



        if (
            sx < -100 or
            sx > WIDTH + 100 or
            sy < -100 or
            sy > HEIGHT + 100
        ):
            return



        # ---------------- HP BAR ----------------

        if self.hp < self.max_hp and not getattr(self, "dying", False):

            bar_width = max(1, int(30 * settings_hp_bar_scale))
            bar_height = max(
                1,
                int(5 * settings_hp_bar_scale)
            )

            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))



            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    int(sx-bar_width/2),
                    int(sy-self.radius-7-bar_height),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx-bar_width/2),
                    int(sy-self.radius-7-bar_height),
                    int(bar_width*hp_percent),
                    bar_height
                )
            )



        # ---------------- HEAD ----------------
        # The baby ant is drawn as just the head of a soldier ant.
        ba_head_col = (250, 215, 80) if getattr(self, "yellow_minion", False) else (48, 48, 48)
        ba_hi_col = (255, 245, 150) if getattr(self, "yellow_minion", False) else (78, 78, 78)

        head_x = sx
        head_y = sy

        pygame.draw.circle(
            screen,
            flash_color(ba_head_col, self.flash_timer),
            (
                int(head_x),
                int(head_y)
            ),
            int(self.radius)
        )

        # Soft gray (or golden) center highlight like the reference image.
        pygame.draw.circle(
            screen,
            flash_color(ba_hi_col, self.flash_timer),
            (
                int(head_x),
                int(head_y)
            ),
            int(self.radius * 0.74)
        )

        # ---------------- MOUTH / MANDIBLES ----------------

        rad = math.radians(
            self.angle
        )

        front_x = math.cos(rad)
        front_y = math.sin(rad)

        side_x = math.cos(rad + math.pi / 2)
        side_y = math.sin(rad + math.pi / 2)

        mouth_start_x = (
            head_x +
            front_x * self.radius * 0.75
        )

        mouth_start_y = (
            head_y +
            front_y * self.radius * 0.75
        )

        mouth_end_x = (
            head_x +
            front_x * self.radius * 1.25
        )

        mouth_end_y = (
            head_y +
            front_y * self.radius * 1.25
        )

        jaw_base = max(2, int(self.radius * 0.3))
        jaw_tip = max(3, int(self.radius * 0.5))
        jaw_thickness = max(1, int(self.radius * 0.15))

        draw_clean_line(
            screen,
            flash_color((40,40,40), self.flash_timer),
            (
                mouth_start_x + side_x * jaw_base,
                mouth_start_y + side_y * jaw_base
            ),
            (
                mouth_end_x + side_x * jaw_tip,
                mouth_end_y + side_y * jaw_tip
            ),
            jaw_thickness
        )

        draw_clean_line(
            screen,
            flash_color((40,40,40), self.flash_timer),
            (
                mouth_start_x - side_x * jaw_base,
                mouth_start_y - side_y * jaw_base
            ),
            (
                mouth_end_x - side_x * jaw_tip,
                mouth_end_y - side_y * jaw_tip
            ),
            jaw_thickness
        )

        # ---------------- KING RICE ORBIT ----------------

        if getattr(self, "is_king", False):

            # Six rice petals circle the baby ant king. They are
            # killable, so draw the live ones from baby_ant_rice.
            rice_orbit = self.radius * 1.8
            for rice in baby_ant_rice:
                if rice["owner"] is not self:
                    continue
                if rice["respawn"] > 0:
                    continue
                rice_angle = math.radians(
                    time.time() * 90
                    + rice["slot"] * (360 / BABY_ANT_RICE_COUNT)
                )
                rice_x = (
                    sx
                    + math.cos(rice_angle) * rice_orbit
                )
                rice_y = (
                    sy
                    + math.sin(rice_angle) * rice_orbit
                )
                draw_petal(
                    "Rice",
                    rice_x,
                    rice_y,
                    self.rarity,
                    size_scale=rice["shrink"]
                )
                draw_projectile_hp_bar(
                    rice_x,
                    rice_y,
                    rice.get("radius", 8),
                    rice["hp"],
                    rice["max_hp"]
                )
                pygame.draw.circle(
                    screen,
                    (255, 60, 60),
                    (int(rice_x), int(rice_y)),
                    int(rice.get("radius", 8)),
                    2
                )

            # ---------------- KING CROWN ----------------

            crown_y = int(sy - self.radius - 14)
            crown_w = int(self.radius * 1.2)
            crown_h = int(self.radius * 0.6)
            crown_left = int(sx - crown_w / 2)
            crown_right = int(sx + crown_w / 2)
            crown_color = (255, 215, 0)
            crown_points = [
                (crown_left, crown_y + crown_h),
                (crown_left, crown_y + crown_h * 0.4),
                (
                    crown_left + crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (
                    int(sx - crown_w * 0.15),
                    crown_y
                ),
                (
                    int(sx + crown_w * 0.15),
                    crown_y + crown_h * 0.4
                ),
                (
                    crown_right - crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (crown_right, crown_y + crown_h * 0.4),
                (crown_right, crown_y + crown_h)
            ]
            pygame.draw.polygon(
                screen,
                crown_color,
                crown_points
            )

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- HOLE BABY ANT ----------------
# A nightmarish, eyeless void larvling native to Hole Land.
# 2x size, 2x HP, 2x damage.
# Quadruple snapping obsidian mandibles, twitching void dorsal tendrils,
# and an erratic skittering hunting pattern.
class HoleBabyAnt(BabyAnt):
    is_hole_land_mob = True

    def __init__(self):
        super().__init__()
        # 2x stats & size
        self.radius = self.radius * 2
        self.base_radius = self.radius
        self.damage = 50
        self.max_hp = 70 * MOB_HP_MULTIPLIER[self.rarity]
        self.hp = self.max_hp

        # Increased skitter agility
        self.max_speed = 3.8
        self.acceleration = 0.5
        self.friction = 0.45

        # Void animation
        self.void_pulse = random.uniform(0, math.pi * 2)
        self.mandible_snap = random.uniform(0, math.pi * 2)
        self.twitch_timer = 0

    def take_damage(self, amount):
        super().take_damage(amount)
        # Enrage and chase player when hurt
        self.angry = True

    def update(self):
        if not self.alive or getattr(self, "dying", False):
            return
        super().update()
        if not self.alive or getattr(self, "dying", False):
            return
        self.void_pulse += 0.09
        self.mandible_snap += 0.22
        self.twitch_timer += 1
        if self.twitch_timer >= 28:
            self.twitch_timer = 0
            if random.random() < 0.35 and not getattr(self, "angry", False):
                self.target_angle = (self.angle + random.uniform(-60, 60)) % 360

    def draw(self):
        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if sx < -120 or sx > WIDTH + 120 or sy < -120 or sy > HEIGHT + 120:
            return

        # ---------------- HP BAR ----------------
        if self.hp < self.max_hp and not getattr(self, "dying", False):
            bar_width = max(1, int(50 * settings_hp_bar_scale))
            bar_height = max(1, int(5 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (45, 12, 60),
                (int(sx - bar_width/2), int(sy - self.radius - 10 - bar_height), bar_width, bar_height)
            )
            pygame.draw.rect(
                screen,
                (190, 50, 255),
                (int(sx - bar_width/2), int(sy - self.radius - 10 - bar_height), int(bar_width * hp_percent), bar_height)
            )

        # ---------------- PULSING VOID AURA ----------------
        pulse = math.sin(self.void_pulse) * 4
        aura_r = int(self.radius * 1.35 + pulse)
        aura_surf = pygame.Surface((aura_r * 2 + 6, aura_r * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (140, 20, 220, 38), (aura_r + 3, aura_r + 3), aura_r)
        screen.blit(aura_surf, (int(sx - aura_r - 3), int(sy - aura_r - 3)))

        # ---------------- HEAD ANGLES ----------------
        rad = math.radians(self.angle)
        front_x = math.cos(rad)
        front_y = math.sin(rad)
        side_x = -front_y
        side_y = front_x

        # 1. TWITCHING DORSAL VOID TENDRILS (sprouting from back of head)
        tendril_col = flash_color((180, 50, 240), self.flash_timer)
        node_col = flash_color((0, 240, 255), self.flash_timer)
        back_base_x = sx - front_x * (self.radius * 0.75)
        back_base_y = sy - front_y * (self.radius * 0.75)
        for t_idx, s_mult in enumerate((-1.2, -0.5, 0.5, 1.2)):
            t_wave = math.sin(self.void_pulse * 1.5 + t_idx) * 4
            t_tip_x = back_base_x - front_x * (self.radius * 0.6) + side_x * (s_mult * self.radius * 0.7 + t_wave)
            t_tip_y = back_base_y - front_y * (self.radius * 0.6) + side_y * (s_mult * self.radius * 0.7 + t_wave)
            draw_clean_line(
                screen,
                tendril_col,
                (int(back_base_x + side_x * s_mult * self.radius * 0.3), int(back_base_y + side_y * s_mult * self.radius * 0.3)),
                (int(t_tip_x), int(t_tip_y)),
                max(2, int(self.radius * 0.12))
            )
            pygame.draw.circle(screen, node_col, (int(t_tip_x), int(t_tip_y)), max(2, int(self.radius * 0.10)))

        # 2. CORRUPTED OBSIDIAN HEAD CHITIN (Eyeless dome)
        pygame.draw.circle(
            screen,
            flash_color((24, 8, 36), self.flash_timer),
            (int(sx), int(sy)),
            int(self.radius)
        )
        pygame.draw.circle(
            screen,
            flash_color((180, 50, 255), self.flash_timer),
            (int(sx), int(sy)),
            int(self.radius),
            max(2, int(self.radius * 0.12))
        )

        # Inner dark core plate
        pygame.draw.circle(
            screen,
            flash_color((14, 4, 22), self.flash_timer),
            (int(sx), int(sy)),
            int(self.radius * 0.72)
        )

        # 3. BIOLUMINESCENT VOID RUNES (glowing cyan rune crest instead of eyes)
        rune_col = flash_color((0, 240, 255), self.flash_timer)
        crest_center = (int(sx + front_x * self.radius * 0.2), int(sy + front_y * self.radius * 0.2))
        c_left = (int(crest_center[0] - side_x * self.radius * 0.35 - front_x * self.radius * 0.15),
                  int(crest_center[1] - side_y * self.radius * 0.35 - front_y * self.radius * 0.15))
        c_right = (int(crest_center[0] + side_x * self.radius * 0.35 - front_x * self.radius * 0.15),
                   int(crest_center[1] + side_y * self.radius * 0.35 - front_y * self.radius * 0.15))
        draw_clean_line(screen, rune_col, crest_center, c_left, max(2, int(self.radius * 0.10)))
        draw_clean_line(screen, rune_col, crest_center, c_right, max(2, int(self.radius * 0.10)))
        pygame.draw.circle(screen, rune_col, crest_center, max(2, int(self.radius * 0.12)))

        # 4. QUADRUPLE JAGGED VOID MANDIBLES (two outer large curved pincers, two inner needle jaws)
        snap_angle = math.sin(self.mandible_snap) * 0.25
        jaw_col = flash_color((35, 10, 50), self.flash_timer)
        jaw_edge_col = flash_color((0, 255, 240), self.flash_timer)

        # Outer heavy mandibles
        for s_mult in (-1, 1):
            base_pt = (sx + front_x * self.radius * 0.7 + side_x * s_mult * self.radius * 0.55,
                       sy + front_y * self.radius * 0.7 + side_y * s_mult * self.radius * 0.55)
            mid_pt = (sx + front_x * self.radius * 1.35 + side_x * s_mult * (self.radius * 0.85 + snap_angle * self.radius),
                      sy + front_y * self.radius * 1.35 + side_y * s_mult * (self.radius * 0.85 + snap_angle * self.radius))
            tip_pt = (sx + front_x * self.radius * 1.65 + side_x * s_mult * (self.radius * 0.25 - snap_angle * self.radius * 0.5),
                      sy + front_y * self.radius * 1.65 + side_y * s_mult * (self.radius * 0.25 - snap_angle * self.radius * 0.5))

            draw_clean_line(screen, jaw_col, base_pt, mid_pt, max(3, int(self.radius * 0.18)))
            draw_clean_line(screen, jaw_col, mid_pt, tip_pt, max(2, int(self.radius * 0.14)))
            draw_clean_line(screen, jaw_edge_col, mid_pt, tip_pt, max(1, int(self.radius * 0.08)))
            pygame.draw.circle(screen, jaw_edge_col, (int(tip_pt[0]), int(tip_pt[1])), max(2, int(self.radius * 0.10)))

        # Inner razor pincers
        for s_mult in (-1, 1):
            in_base = (sx + front_x * self.radius * 0.85 + side_x * s_mult * self.radius * 0.22,
                       sy + front_y * self.radius * 0.85 + side_y * s_mult * self.radius * 0.22)
            in_tip = (sx + front_x * self.radius * 1.30 + side_x * s_mult * (self.radius * 0.10 - snap_angle * self.radius * 0.3),
                      sy + front_y * self.radius * 1.30 + side_y * s_mult * (self.radius * 0.10 - snap_angle * self.radius * 0.3))
            draw_clean_line(screen, flash_color((190, 50, 255), self.flash_timer), in_base, in_tip, max(2, int(self.radius * 0.10)))

        # ---------------- RARITY TEXT ----------------
        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- SOLDIER ANT ----------------

# ---------------- SOLDIER ANT ----------------

# ---------------- SOLDIER ANT ----------------

class SoldierAnt:

    def __init__(self):

        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.knockback_x = 0
        self.knockback_y = 0
        self.rarity = "Common"


        # HP

        self.damage = 40

        self.max_hp = (
            90 *
            MOB_HP_MULTIPLIER[self.rarity]
        )

        self.hp = self.max_hp

        self.alive = True
        self.flash_timer = 0

        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2   # <-- add this



        # size

        self.radius = random.randint(22, 30)
        self.base_radius = self.radius



        # baby ant style movement

        self.speed = 0

        self.max_speed = 2.5

        self.acceleration = 0.3

        self.friction = 0.4



        # direction

        self.angle = random.uniform(0,360)

        self.target_angle = self.angle



        # AI

        self.state = "turn"

        self.timer = 0



        # player detection

        self.view_range = 400

        self.charging = False
        self.charge_speed = 2.5
        self.wing_phase = 0.0

        # King / minion flags (set by the /king command)
        self.is_king = False
        self.is_minion = False
        self.king_minion_timer = 0
        self.king_chat_timer = 0
        self.king_rose_timer = 0
        self.king_orbit_slot = 0
        self.king_wing_timer = 0





    def take_damage(self, amount):

        if not self.alive:
            return


        self.hp -= int(amount)


        if self.hp <= 0:

            if getattr(self, "death_registered", False):
                return
            self.death_registered = True

            cleanup_king(self)
            register_mob_kill(self)
            drop_mob_loot(self)

            # Die with a fast shrink instead of vanishing.
            self.dying = True
            self.shrink_scale = 1.0
            self.full_radius = self.radius

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    getattr(
                        self,
                        "custom_xp",
                        10 * MOB_XP_MULTIPLIER[self.rarity]
                    )
                )
            )

    def turn_to(self, target, amount=2):

        difference = target - self.angle


        if difference > 180:
            difference -= 360

        if difference < -180:
            difference += 360



        if abs(difference) <= amount:

            self.angle = target

            return True



        if difference > 0:

            self.angle += amount

        else:

            self.angle -= amount


        return False





    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return


        self.timer += 1

        # ---------------- KING AI ----------------

        if getattr(self, "is_king", False):

            if king_chase_or_guard(self):
                return

        if getattr(self, "is_minion", False):

            minion_ai(self)
            return



        # ---------------- DISTANCE TO PLAYER ----------------

        distance_to_player = math.hypot(
            player_x - self.x,
            player_y - self.y
        )



        # ---------------- SEE PLAYER ----------------

        if distance_to_player <= self.view_range:

            self.charging = True


        elif distance_to_player > self.view_range * 1.5:

            self.charging = False



        # ---------------- CHARGE ----------------

        if self.charging:

            # Fast left/right wing motion while chasing.
            self.wing_phase += 0.85


            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )


            self.turn_to(
                target_angle,
                10
            )


            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.charge_speed

            dy = math.sin(rad) * self.charge_speed



            move_with_collision(
                self,
                dx,
                dy
            )


            return



        # ---------------- NORMAL SOLDIER ANT MOVEMENT ----------------


        if self.state == "turn":


            if self.turn_to(
                self.target_angle,
                2
            ):


                self.state = "walk"

                self.timer = 0





        elif self.state == "walk":


            if self.speed < self.max_speed:

                self.speed += self.acceleration



            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.speed * 0.15

            dy = math.sin(rad) * self.speed * 0.15



            move_with_collision(
                self,
                dx,
                dy
            )



            if self.timer >= 80:

                self.state = "slow"

                self.timer = 0





        elif self.state == "slow":


            self.speed -= self.friction


            if self.speed < 0:

                self.speed = 0



            rad = math.radians(
                self.angle
            )


            dx = math.cos(rad) * self.speed * 0.15

            dy = math.sin(rad) * self.speed * 0.15



            move_with_collision(
                self,
                dx,
                dy
            )



            if self.speed == 0:

                self.state = "pause"

                self.timer = 0





        elif self.state == "pause":


            if self.timer >= 50:


                self.target_angle = random.uniform(
                    0,
                    360
                )


                self.state = "turn"

                self.timer = 0

    def draw(self):

        if not self.alive:
            return


        sx = self.x - camera_x
        sy = self.y - camera_y


        if (
            sx < -100 or
            sx > WIDTH + 100 or
            sy < -100 or
            sy > HEIGHT + 100
        ):
            return



        angle = math.radians(
            self.angle
        )



        # ---------------- SIZE ----------------

        head_size = self.radius * 0.80

        body_width = (
            self.radius
            * 1.2
            * getattr(self, "body_length_scale", 1.0)
        )
        body_height = self.radius * 0.8

        # Yellow flower minions are recolored golden yellow instead
        # of the usual dark gray soldier ant.
        def ant_color(base):
            if getattr(self, "yellow_minion", False):
                return {
                    (62, 62, 62): (255, 230, 100),
                    (22, 22, 22): (210, 160, 40),
                    (48, 48, 48): (250, 215, 80),
                    (78, 78, 78): (255, 245, 150),
                    (40, 40, 40): (200, 150, 35),
                }.get(base, base)
            return flash_color(base, self.flash_timer)



        # ---------------- OVAL BODY (BACK) ----------------

        body_length_scale = getattr(
            self,
            "body_length_scale",
            1.0
        )

        if body_length_scale > 1.0:
            # Queen ants have three round body parts: the big
            # abdomen at the back, a thorax in the middle that is
            # a little bigger than the head, and the head at the
            # front (drawn later, on top of both).
            for part_offset, part_scale in (
                (-0.65, 1.2),
                (0.0, 1.1),
            ):
                part_x = (
                    sx
                    + math.cos(angle)
                    * self.radius
                    * part_offset
                )
                part_y = (
                    sy
                    + math.sin(angle)
                    * self.radius
                    * part_offset
                )
                part_r = int(head_size * part_scale)
                pygame.draw.circle(
                    screen,
                    ant_color((62, 62, 62)),
                    (int(part_x), int(part_y)),
                    part_r
                )
                pygame.draw.circle(
                    screen,
                    ant_color((22, 22, 22)),
                    (int(part_x), int(part_y)),
                    part_r,
                    max(2, int(self.radius * 0.10))
                )
        else:
            body_surface = pygame.Surface(
                (
                    int(body_width * 2),
                    int(body_height * 2)
                ),
                pygame.SRCALPHA
            )


            pygame.draw.ellipse(
                body_surface,
                ant_color((62, 62, 62)),
                (
                    0,
                    0,
                    int(body_width * 2),
                    int(body_height * 2)
                )
            )
            pygame.draw.ellipse(
                body_surface,
                ant_color((22, 22, 22)),
                (
                    0,
                    0,
                    int(body_width * 2),
                    int(body_height * 2)
                ),
                max(2, int(self.radius * 0.10))
            )


            body_surface = pygame.transform.rotate(
                body_surface,
                -self.angle
            )


            # Longer-bodied ants (the queen) shift the body backward
            # along their angle so its front tip stays hidden behind
            # the head instead of sticking out of it.
            body_shift = (
                self.radius
                * 0.8
                * (getattr(self, "body_length_scale", 1.0) - 1.0)
            )
            body_rect = body_surface.get_rect(
                center=(
                    int(sx - math.cos(angle) * body_shift),
                    int(sy - math.sin(angle) * body_shift)
                )
            )


            screen.blit(
                body_surface,
                body_rect
            )



        # ---------------- WINGS (MIDDLE LAYER) ----------------

        wing_flap = math.sin(self.wing_phase) * 25
        wing_size = int(self.radius * 3)
        cx = self.radius * 1.5
        cy = self.radius * 1.5

        # The wings move in opposite directions, like mirrored antennae.
        for wing_side in (-1, 1):
            wing_surface = pygame.Surface(
                (wing_size, wing_size),
                pygame.SRCALPHA
            )
            wing_x = (
                cx - self.radius * 0.9
                if wing_side == -1
                else cx + self.radius * 0.1
            )
            pygame.draw.ellipse(
                wing_surface,
                (220, 245, 245, 125),
                (
                    wing_x,
                    cy - self.radius * 1.2,
                    self.radius * 0.8,
                    self.radius * 1.5
                )
            )
            pygame.draw.ellipse(
                wing_surface,
                (105, 170, 180, 180),
                (
                    wing_x,
                    cy - self.radius * 1.2,
                    self.radius * 0.8,
                    self.radius * 1.5
                ),
                max(1, int(self.radius * 0.08))
            )
            wing_angle = -self.angle + 90 - wing_side * wing_flap
            wing_surface = pygame.transform.rotate(
                wing_surface,
                wing_angle
            )
            wing_rect = wing_surface.get_rect(
                center=(int(sx), int(sy))
            )
            screen.blit(wing_surface, wing_rect)

        # ---------------- HEAD (FRONT) ----------------

        head_x = (
            sx +
            math.cos(angle) * self.radius * 0.7
        )


        head_y = (
            sy +
            math.sin(angle) * self.radius * 0.7
        )



        pygame.draw.circle(
            screen,
            ant_color((48, 48, 48)),
            (
                int(head_x),
                int(head_y)
            ),
            int(head_size)
        )

        # Soft gray center highlight like the reference image.
        pygame.draw.circle(
            screen,
            ant_color((78, 78, 78)),
            (
                int(head_x),
                int(head_y)
            ),
            int(head_size * 0.74)
        )



        # ---------------- MOUTH / MANDIBLES ----------------

        front_x = math.cos(angle)
        front_y = math.sin(angle)


        side_x = math.cos(angle + math.pi/2)
        side_y = math.sin(angle + math.pi/2)



        mouth_start_x = (
            head_x +
            front_x * head_size * 0.75
        )

        mouth_start_y = (
            head_y +
            front_y * head_size * 0.75
        )



        mouth_end_x = (
            head_x +
            front_x * head_size * 1.25
        )

        mouth_end_y = (
            head_y +
            front_y * head_size * 1.25
        )

        right_jaw_motion = 0
        left_jaw_motion = 0



        jaw_scale = max(0.25, self.radius / 24.0)
        jaw_w = max(1, int(3 * jaw_scale))
        draw_clean_line(
            screen,
            ant_color((40, 40, 40)),
            (
                mouth_start_x + side_x * ((5 + right_jaw_motion) * jaw_scale),
                mouth_start_y + side_y * ((5 + right_jaw_motion) * jaw_scale)
            ),
            (
                mouth_end_x + side_x * ((8 + right_jaw_motion) * jaw_scale),
                mouth_end_y + side_y * ((8 + right_jaw_motion) * jaw_scale)
            ),
            jaw_w
        )



        draw_clean_line(
            screen,
            ant_color((40, 40, 40)),
            (
                mouth_start_x - side_x * ((5 + left_jaw_motion) * jaw_scale),
                mouth_start_y - side_y * ((5 + left_jaw_motion) * jaw_scale)
            ),
            (
                mouth_end_x - side_x * ((8 + left_jaw_motion) * jaw_scale),
                mouth_end_y - side_y * ((8 + left_jaw_motion) * jaw_scale)
            ),
            jaw_w
        )

        # ---------------- HP BAR ----------------

        if (
            not getattr(self, "yellow_minion", False)
            and not getattr(self, "dying", False)
            and self.hp < self.max_hp
        ):

            bar_width = max(10, int(min(35, max(10, self.radius * 1.5)) * settings_hp_bar_scale))
            bar_height = max(
                1,
                int(4 * settings_hp_bar_scale)
            )

            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))


            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 10 - bar_height),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )

        # ---------------- KING CROWN ----------------

        if getattr(self, "is_king", False):

            crown_y = int(sy - self.radius - 14)
            crown_w = int(self.radius * 1.2)
            crown_h = int(self.radius * 0.6)
            crown_left = int(sx - crown_w / 2)
            crown_right = int(sx + crown_w / 2)
            crown_color = (255, 215, 0)
            crown_points = [
                (crown_left, crown_y + crown_h),
                (crown_left, crown_y + crown_h * 0.4),
                (
                    crown_left + crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (
                    int(sx - crown_w * 0.15),
                    crown_y
                ),
                (
                    int(sx + crown_w * 0.15),
                    crown_y + crown_h * 0.4
                ),
                (
                    crown_right - crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (crown_right, crown_y + crown_h * 0.4),
                (crown_right, crown_y + crown_h)
            ]
            pygame.draw.polygon(
                screen,
                crown_color,
                crown_points
            )

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- HOLE SOLDIER ANT ----------------
# A heavily armored, 2x void dreadnought ant from Hole Land.
# 2x size, 2x HP, 2x damage.
# Strictly eyeless: jagged obsidian carapace plates, 4 razor void wings,
# pulsing bioluminescent energy conduits, and massive serrated executioner mandibles.
class HoleSoldierAnt(SoldierAnt):
    is_hole_land_mob = True

    def __init__(self):
        super().__init__()
        # 2x stats & size
        self.radius = self.radius * 2
        self.base_radius = self.radius
        self.damage = 80
        self.max_hp = 180 * MOB_HP_MULTIPLIER[self.rarity]
        self.hp = self.max_hp

        # Heavy aggressive charge
        self.max_speed = 3.2
        self.charge_speed = 3.6
        self.view_range = 550

        # Void aesthetics
        self.void_pulse = random.uniform(0, math.pi * 2)
        self.wing_jitter = random.uniform(0, math.pi * 2)
        self.mandible_snap = random.uniform(0, math.pi * 2)

    def update(self):
        if not self.alive or getattr(self, "dying", False):
            return
        super().update()
        if not self.alive or getattr(self, "dying", False):
            return
        self.void_pulse += 0.08
        self.wing_jitter += 0.55
        self.mandible_snap += 0.20

    def draw(self):
        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if sx < -160 or sx > WIDTH + 160 or sy < -160 or sy > HEIGHT + 160:
            return

        angle = math.radians(self.angle)
        front_x = math.cos(angle)
        front_y = math.sin(angle)
        side_x = -front_y
        side_y = front_x

        # ---------------- HP BAR ----------------
        if self.hp < self.max_hp and not getattr(self, "dying", False):
            bar_width = max(1, int(65 * settings_hp_bar_scale))
            bar_height = max(1, int(6 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (45, 12, 60),
                (int(sx - bar_width/2), int(sy - self.radius - 12 - bar_height), bar_width, bar_height)
            )
            pygame.draw.rect(
                screen,
                (190, 50, 255),
                (int(sx - bar_width/2), int(sy - self.radius - 12 - bar_height), int(bar_width * hp_percent), bar_height)
            )

        # ---------------- PULSING VOID AURA ----------------
        pulse = math.sin(self.void_pulse) * 5
        aura_r = int(self.radius * 1.35 + pulse)
        aura_surf = pygame.Surface((aura_r * 2 + 6, aura_r * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (140, 25, 210, 42), (aura_r + 3, aura_r + 3), aura_r)
        screen.blit(aura_surf, (int(sx - aura_r - 3), int(sy - aura_r - 3)))

        # ---------------- 1. HEAVY OBSIDIAN ABDOMEN (BACK) ----------------
        abd_x = sx - front_x * (self.radius * 0.75)
        abd_y = sy - front_y * (self.radius * 0.75)
        abd_r = int(self.radius * 0.88)
        pygame.draw.circle(screen, flash_color((20, 6, 32), self.flash_timer), (int(abd_x), int(abd_y)), abd_r)
        pygame.draw.circle(screen, flash_color((180, 45, 255), self.flash_timer), (int(abd_x), int(abd_y)), abd_r, max(2, int(self.radius * 0.08)))
        # Abdomen chitin spikes / ribs
        for rib_i in (-1, 0, 1):
            rx = abd_x + front_x * (rib_i * self.radius * 0.3)
            ry = abd_y + front_y * (rib_i * self.radius * 0.3)
            draw_clean_line(
                screen,
                flash_color((0, 240, 255), self.flash_timer),
                (int(rx - side_x * abd_r * 0.7), int(ry - side_y * abd_r * 0.7)),
                (int(rx + side_x * abd_r * 0.7), int(ry + side_y * abd_r * 0.7)),
                max(2, int(self.radius * 0.07))
            )

        # ---------------- 2. FOUR SERRATED VOID WINGS ----------------
        w_flap1 = math.sin(self.wing_jitter) * 22
        w_flap2 = math.cos(self.wing_jitter * 1.3) * 22
        wing_len = self.radius * 2.2
        wing_w = self.radius * 0.8
        for w_idx, (w_side, flap_ang) in enumerate(((-1, w_flap1), (1, w_flap2), (-1, -w_flap2 * 0.7), (1, -w_flap1 * 0.7))):
            w_surf = pygame.Surface((int(wing_len * 2), int(wing_w * 2)), pygame.SRCALPHA)
            w_cx = int(wing_len)
            w_cy = int(wing_w)
            w_pts = [
                (w_cx - int(wing_len * 0.8), w_cy),
                (w_cx + int(wing_len * 0.6), w_cy - int(wing_w * 0.8)),
                (w_cx + int(wing_len * 0.8), w_cy),
                (w_cx + int(wing_len * 0.4), w_cy + int(wing_w * 0.8)),
            ]
            wing_col = (0, 240, 255, 95) if w_idx < 2 else (180, 45, 240, 85)
            edge_col = (200, 60, 255, 200) if w_idx < 2 else (0, 255, 240, 180)
            pygame.draw.polygon(w_surf, wing_col, w_pts)
            pygame.draw.polygon(w_surf, edge_col, w_pts, 2)
            rot_w = pygame.transform.rotate(w_surf, -self.angle + 90 - w_side * (55 + flap_ang))
            screen.blit(rot_w, rot_w.get_rect(center=(int(sx - front_x * self.radius * 0.2), int(sy - front_y * self.radius * 0.2))))

        # ---------------- 3. THORAX (MIDDLE CORE) ----------------
        mid_r = int(self.radius * 0.78)
        pygame.draw.circle(screen, flash_color((25, 8, 38), self.flash_timer), (int(sx), int(sy)), mid_r)
        pygame.draw.circle(screen, flash_color((0, 240, 255), self.flash_timer), (int(sx), int(sy)), mid_r, max(2, int(self.radius * 0.08)))

        # ---------------- 4. ARMORED HEAD (EYELESS DOME) ----------------
        head_x = sx + front_x * (self.radius * 0.65)
        head_y = sy + front_y * (self.radius * 0.65)
        head_r = int(self.radius * 0.72)
        pygame.draw.circle(screen, flash_color((18, 5, 28), self.flash_timer), (int(head_x), int(head_y)), head_r)
        pygame.draw.circle(screen, flash_color((190, 50, 255), self.flash_timer), (int(head_x), int(head_y)), head_r, max(2, int(self.radius * 0.10)))

        # Glowing cyan energy chevron crest across forehead
        crest_tip = (int(head_x + front_x * head_r * 0.45), int(head_y + front_y * head_r * 0.45))
        c_left = (int(head_x - side_x * head_r * 0.65 - front_x * head_r * 0.15), int(head_y - side_y * head_r * 0.65 - front_y * head_r * 0.15))
        c_right = (int(head_x + side_x * head_r * 0.65 - front_x * head_r * 0.15), int(head_y + side_y * head_r * 0.65 - front_y * head_r * 0.15))
        draw_clean_line(screen, flash_color((0, 255, 255), self.flash_timer), crest_tip, c_left, max(2, int(self.radius * 0.10)))
        draw_clean_line(screen, flash_color((0, 255, 255), self.flash_timer), crest_tip, c_right, max(2, int(self.radius * 0.10)))
        pygame.draw.circle(screen, flash_color((255, 60, 200), self.flash_timer), crest_tip, max(2, int(self.radius * 0.12)))

        # ---------------- 5. SERRATED EXECUTIONER MANDIBLES ----------------
        snap_val = math.sin(self.mandible_snap) * 0.35
        jaw_col = flash_color((30, 8, 45), self.flash_timer)
        jaw_blade_col = flash_color((0, 255, 240), self.flash_timer)
        for s_mult in (-1, 1):
            m_base = (head_x + front_x * head_r * 0.65 + side_x * s_mult * (head_r * 0.60),
                      head_y + front_y * head_r * 0.65 + side_y * s_mult * (head_r * 0.60))
            m_elbow = (head_x + front_x * head_r * 1.50 + side_x * s_mult * (head_r * 1.15 + snap_val * head_r),
                       head_y + front_y * head_r * 1.50 + side_y * s_mult * (head_r * 1.15 + snap_val * head_r))
            m_tip = (head_x + front_x * head_r * 1.95 + side_x * s_mult * (head_r * 0.35 - snap_val * head_r * 0.6),
                     head_y + front_y * head_r * 1.95 + side_y * s_mult * (head_r * 0.35 - snap_val * head_r * 0.6))
            draw_clean_line(screen, jaw_col, m_base, m_elbow, max(3, int(self.radius * 0.16)))
            draw_clean_line(screen, jaw_col, m_elbow, m_tip, max(3, int(self.radius * 0.14)))
            draw_clean_line(screen, jaw_blade_col, m_elbow, m_tip, max(1, int(self.radius * 0.08)))
            # Serrated teeth on inner blade edge
            tooth_pt = (m_elbow[0] * 0.5 + m_tip[0] * 0.5 - side_x * s_mult * head_r * 0.25,
                        m_elbow[1] * 0.5 + m_tip[1] * 0.5 - side_y * s_mult * head_r * 0.25)
            draw_clean_line(screen, jaw_blade_col, (m_elbow[0]*0.5+m_tip[0]*0.5, m_elbow[1]*0.5+m_tip[1]*0.5), tooth_pt, max(2, int(self.radius * 0.08)))
            pygame.draw.circle(screen, jaw_blade_col, (int(m_tip[0]), int(m_tip[1])), max(2, int(self.radius * 0.10)))

        # ---------------- RARITY TEXT ----------------
        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 16)
            )

class QueenAnt(SoldierAnt):

    def __init__(self):

        super().__init__()

        # Bigger than a soldier ant, with a longer body.
        self.radius = random.randint(32, 40)
        self.base_radius = self.radius
        self.body_length_scale = 1.6

        # Queen stats: 115 main HP and the soldier ant's main
        # damage + 10.
        self.max_hp = 115
        self.hp = 115
        self.damage = 50

        # Egg laying: one egg every 0.9 seconds of chasing, then a
        # 0.3 second freeze right after laying.
        self.egg_timer = 0
        self.lay_freeze_timer = 0

    def count_active_minions(self):
        eggs = globals().get("queen_eggs", [])
        ants = globals().get("soldier_ants", [])
        egg_count = sum(
            1 for egg in eggs
            if egg.get("queen") is self
        )
        minion_count = sum(
            1 for ant in ants
            if getattr(ant, "queen", None) is self
            and ant.alive
            and not getattr(ant, "dying", False)
        )
        return egg_count + minion_count

    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return

        # Laying freeze: stand still for 0.3 seconds, then chase.
        if self.lay_freeze_timer > 0:
            self.lay_freeze_timer -= 1
            return

        # While chasing the player, lay an egg every 0.9 seconds
        # (54 frames) if this queen currently has fewer than 5 active
        # minions (including unhatched eggs). The egg is laid behind
        # the queen, never in the middle of her body, and hatches in 1.5s.
        if self.charging and not player_dead:
            if self.count_active_minions() < 5:
                self.egg_timer += 1
                if self.egg_timer >= 54:
                    self.egg_timer = 0
                    self.lay_freeze_timer = 18
                    lay_rad = math.radians(self.angle)
                    queen_eggs.append(
                        {
                            "x": (
                                self.x
                                - math.cos(lay_rad)
                                * self.radius * 1.3
                            ),
                            "y": (
                                self.y
                                - math.sin(lay_rad)
                                * self.radius * 1.3
                            ),
                            "timer": 90,
                            # Egg size scales with the queen's size.
                            "radius": max(
                                10,
                                int(self.radius * 0.45)
                            ),
                            "rarity": self.rarity,
                            "wobble": random.uniform(0, 360),
                            "queen": self
                        }
                    )
            else:
                self.egg_timer = 0

        super().update()

    def hitbox_circles(self):
        # The queen's hitbox is three circles that match her three
        # body parts: abdomen (back), thorax (middle) and head
        # (front). Offsets follow the same layout as her drawing.
        head_size = self.radius * 0.8
        rad = math.radians(self.angle)
        circles = []
        for part_offset, part_scale in (
            (-0.65, 1.2),
            (0.0, 1.1),
            (0.7, 1.0),
        ):
            circles.append(
                (
                    self.x
                    + math.cos(rad) * self.radius * part_offset,
                    self.y
                    + math.sin(rad) * self.radius * part_offset,
                    head_size * part_scale
                )
            )
        return circles


def entity_hit_circles(entity):
    # Collision circles for any mob: queen ants use their three
    # body-part circles, everything else a single body circle.
    if isinstance(entity, (QueenAnt, HoleQueenAnt)):
        return entity.hitbox_circles()
    return [(entity.x, entity.y, entity.radius)]


# ---------------- HOLE QUEEN ANT ----------------
# The colossal, eyeless abyss matriarch native to Hole Land.
# 2x size, 2x HP, 2x damage.
# Eyeless crystalline obsidian armor, pulsing cyan & magenta biomechanical void runes,
# 4 fluttering void-glitch wings, and an egg incubator chamber laying Void Eggs.
class HoleQueenAnt(QueenAnt):
    is_hole_land_mob = True

    def __init__(self):
        super().__init__()
        # 2x stats & size
        self.radius = self.radius * 2
        self.base_radius = self.radius
        self.body_length_scale = 1.65
        self.damage = 100
        self.max_hp = 230 * MOB_HP_MULTIPLIER[self.rarity]
        self.hp = self.max_hp

        # Movement & Charge
        self.max_speed = 2.8
        self.charge_speed = 3.2
        self.view_range = 600

        # Void aesthetics
        self.void_pulse = random.uniform(0, math.pi * 2)
        self.wing_jitter = random.uniform(0, math.pi * 2)
        self.mandible_snap = random.uniform(0, math.pi * 2)

    def count_active_minions(self):
        eggs = globals().get("queen_eggs", [])
        ants = globals().get("hole_soldier_ants", [])
        egg_count = sum(
            1 for egg in eggs
            if egg.get("queen") is self
        )
        minion_count = sum(
            1 for ant in ants
            if getattr(ant, "queen", None) is self
            and ant.alive
            and not getattr(ant, "dying", False)
        )
        return egg_count + minion_count

    def update(self):
        if not self.alive or getattr(self, "dying", False):
            return
        if dead_flower_ai(self):
            return

        if self.lay_freeze_timer > 0:
            self.lay_freeze_timer -= 1
            return

        self.void_pulse += 0.08
        self.wing_jitter += 0.55
        self.mandible_snap += 0.20

        # Lays dark Void Eggs that hatch into HoleSoldierAnts
        if self.charging and not player_dead:
            if self.count_active_minions() < 5:
                self.egg_timer += 1
                if self.egg_timer >= 54:
                    self.egg_timer = 0
                    self.lay_freeze_timer = 18
                    lay_rad = math.radians(self.angle)
                    queen_eggs.append(
                        {
                            "x": (
                                self.x
                                - math.cos(lay_rad)
                                * self.radius * 1.3
                            ),
                            "y": (
                                self.y
                                - math.sin(lay_rad)
                                * self.radius * 1.3
                            ),
                            "timer": 90,
                            "radius": max(
                                16,
                                int(self.radius * 0.45)
                            ),
                            "rarity": self.rarity,
                            "wobble": random.uniform(0, 360),
                            "queen": self,
                            "is_void_egg": True
                        }
                    )
            else:
                self.egg_timer = 0

        # Call SoldierAnt.update logic for movement and turning
        super(QueenAnt, self).update()

    def draw(self):
        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if sx < -200 or sx > WIDTH + 200 or sy < -200 or sy > HEIGHT + 200:
            return

        angle = math.radians(self.angle)
        front_x = math.cos(angle)
        front_y = math.sin(angle)
        side_x = -front_y
        side_y = front_x

        head_size = self.radius * 0.80

        # ---------------- HP BAR ----------------
        if self.hp < self.max_hp and not getattr(self, "dying", False):
            bar_width = max(1, int(80 * settings_hp_bar_scale))
            bar_height = max(1, int(7 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (45, 12, 60),
                (int(sx - bar_width/2), int(sy - self.radius - 14 - bar_height), bar_width, bar_height)
            )
            pygame.draw.rect(
                screen,
                (190, 50, 255),
                (int(sx - bar_width/2), int(sy - self.radius - 14 - bar_height), int(bar_width * hp_percent), bar_height)
            )

        # ---------------- PULSING VOID AURA ----------------
        pulse = math.sin(self.void_pulse) * 6
        aura_r = int(self.radius * 1.45 + pulse)
        aura_surf = pygame.Surface((aura_r * 2 + 8, aura_r * 2 + 8), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (140, 20, 220, 48), (aura_r + 4, aura_r + 4), aura_r)
        screen.blit(aura_surf, (int(sx - aura_r - 4), int(sy - aura_r - 4)))

        # ---------------- 1. THREE-SEGMENT CORRUPTED QUEEN CHASSIS ----------------
        # Abdomen (back) and Thorax (middle)
        for part_offset, part_scale, is_abdomen in (
            (-0.65, 1.25, True),
            (0.0, 1.12, False),
        ):
            part_x = sx + front_x * self.radius * part_offset
            part_y = sy + front_y * self.radius * part_offset
            part_r = int(head_size * part_scale)

            pygame.draw.circle(
                screen,
                flash_color((20, 6, 32), self.flash_timer),
                (int(part_x), int(part_y)),
                part_r
            )
            pygame.draw.circle(
                screen,
                flash_color((180, 45, 255), self.flash_timer),
                (int(part_x), int(part_y)),
                part_r,
                max(2, int(self.radius * 0.08))
            )

            # Abdomen bio-luminescent void ribs & egg incubator glow
            if is_abdomen:
                for rib_i in (-1, 0, 1):
                    rx = part_x + front_x * (rib_i * part_r * 0.35)
                    ry = part_y + front_y * (rib_i * part_r * 0.35)
                    draw_clean_line(
                        screen,
                        flash_color((0, 240, 255), self.flash_timer),
                        (int(rx - side_x * part_r * 0.72), int(ry - side_y * part_r * 0.72)),
                        (int(rx + side_x * part_r * 0.72), int(ry + side_y * part_r * 0.72)),
                        max(2, int(self.radius * 0.07))
                    )
                # Glowing void core center in abdomen
                pygame.draw.circle(
                    screen,
                    flash_color((255, 60, 220), self.flash_timer),
                    (int(part_x), int(part_y)),
                    max(3, int(part_r * 0.32))
                )

        # ---------------- 2. FOUR GLITCHING VOID WINGS ----------------
        w_flap1 = math.sin(self.wing_jitter) * 25
        w_flap2 = math.cos(self.wing_jitter * 1.3) * 25
        wing_len = self.radius * 2.5
        wing_w = self.radius * 0.95
        for w_idx, (w_side, flap_ang) in enumerate(((-1, w_flap1), (1, w_flap2), (-1, -w_flap2 * 0.7), (1, -w_flap1 * 0.7))):
            w_surf = pygame.Surface((int(wing_len * 2), int(wing_w * 2)), pygame.SRCALPHA)
            w_cx = int(wing_len)
            w_cy = int(wing_w)
            w_pts = [
                (w_cx - int(wing_len * 0.85), w_cy),
                (w_cx + int(wing_len * 0.7), w_cy - int(wing_w * 0.85)),
                (w_cx + int(wing_len * 0.9), w_cy),
                (w_cx + int(wing_len * 0.5), w_cy + int(wing_w * 0.85)),
            ]
            wing_col = (0, 240, 255, 105) if w_idx < 2 else (200, 50, 255, 95)
            edge_col = (200, 60, 255, 220) if w_idx < 2 else (0, 255, 240, 200)
            pygame.draw.polygon(w_surf, wing_col, w_pts)
            pygame.draw.polygon(w_surf, edge_col, w_pts, 2)
            rot_w = pygame.transform.rotate(w_surf, -self.angle + 90 - w_side * (55 + flap_ang))
            screen.blit(rot_w, rot_w.get_rect(center=(int(sx), int(sy))))

        # ---------------- 3. ARMORED MATRIARCH HEAD (FRONT, EYELESS) ----------------
        head_x = sx + front_x * self.radius * 0.7
        head_y = sy + front_y * self.radius * 0.7
        pygame.draw.circle(
            screen,
            flash_color((24, 6, 36), self.flash_timer),
            (int(head_x), int(head_y)),
            int(head_size)
        )
        pygame.draw.circle(
            screen,
            flash_color((180, 50, 255), self.flash_timer),
            (int(head_x), int(head_y)),
            int(head_size),
            max(2, int(self.radius * 0.09))
        )

        # Royal void crown crest (tri-spike crown emblazoned on forehead, strictly eyeless)
        crown_mid = (int(head_x + front_x * head_size * 0.55), int(head_y + front_y * head_size * 0.55))
        c_left = (int(head_x + front_x * head_size * 0.35 - side_x * head_size * 0.6), int(head_y + front_y * head_size * 0.35 - side_y * head_size * 0.6))
        c_right = (int(head_x + front_x * head_size * 0.35 + side_x * head_size * 0.6), int(head_y + front_y * head_size * 0.35 + side_y * head_size * 0.6))
        c_base = (int(head_x), int(head_y))
        draw_clean_line(screen, flash_color((0, 255, 255), self.flash_timer), c_base, crown_mid, max(2, int(self.radius * 0.08)))
        draw_clean_line(screen, flash_color((0, 255, 255), self.flash_timer), c_base, c_left, max(2, int(self.radius * 0.08)))
        draw_clean_line(screen, flash_color((0, 255, 255), self.flash_timer), c_base, c_right, max(2, int(self.radius * 0.08)))
        pygame.draw.circle(screen, flash_color((255, 60, 200), self.flash_timer), crown_mid, max(2, int(self.radius * 0.10)))
        pygame.draw.circle(screen, flash_color((0, 240, 255), self.flash_timer), c_left, max(2, int(self.radius * 0.08)))
        pygame.draw.circle(screen, flash_color((0, 240, 255), self.flash_timer), c_right, max(2, int(self.radius * 0.08)))

        # ---------------- 4. MASSIVE MATRIARCH EXECUTIONER MANDIBLES ----------------
        snap_val = math.sin(self.mandible_snap) * 0.35
        jaw_col = flash_color((32, 8, 48), self.flash_timer)
        jaw_blade_col = flash_color((0, 255, 240), self.flash_timer)
        for s_mult in (-1, 1):
            m_base = (head_x + front_x * head_size * 0.65 + side_x * s_mult * (head_size * 0.60),
                      head_y + front_y * head_size * 0.65 + side_y * s_mult * (head_size * 0.60))
            m_elbow = (head_x + front_x * head_size * 1.55 + side_x * s_mult * (head_size * 1.20 + snap_val * head_size),
                       head_y + front_y * head_size * 1.55 + side_y * s_mult * (head_size * 1.20 + snap_val * head_size))
            m_tip = (head_x + front_x * head_size * 2.05 + side_x * s_mult * (head_size * 0.30 - snap_val * head_size * 0.6),
                     head_y + front_y * head_size * 2.05 + side_y * s_mult * (head_size * 0.30 - snap_val * head_size * 0.6))
            draw_clean_line(screen, jaw_col, m_base, m_elbow, max(3, int(self.radius * 0.16)))
            draw_clean_line(screen, jaw_col, m_elbow, m_tip, max(3, int(self.radius * 0.14)))
            draw_clean_line(screen, jaw_blade_col, m_elbow, m_tip, max(1, int(self.radius * 0.08)))
            # Serrated tooth on inner edge
            tooth_pt = (m_elbow[0] * 0.5 + m_tip[0] * 0.5 - side_x * s_mult * head_size * 0.3,
                        m_elbow[1] * 0.5 + m_tip[1] * 0.5 - side_y * s_mult * head_size * 0.3)
            draw_clean_line(screen, jaw_blade_col, (m_elbow[0]*0.5+m_tip[0]*0.5, m_elbow[1]*0.5+m_tip[1]*0.5), tooth_pt, max(2, int(self.radius * 0.08)))
            pygame.draw.circle(screen, jaw_blade_col, (int(m_tip[0]), int(m_tip[1])), max(2, int(self.radius * 0.10)))

        # ---------------- RARITY TEXT ----------------
        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 18)
            )


# ----- DIF SECTION -----

class WorkerAnt:

    def __init__(self):

        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.knockback_x = 0
        self.knockback_y = 0
        self.rarity = "Common"

        # Stats
        # Worker ants deal damage now: Soldier Ant HP (90) minus 10.
        self.damage = 90 - 10
        self.petal_damage = 30
        self.max_hp = (
            50 *
            MOB_HP_MULTIPLIER[self.rarity]
        )

        self.hp = self.max_hp
        self.alive = True
        self.flash_timer = 0
        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2

        # Size
        self.radius = random.randint(14, 20)
        self.base_radius = self.radius

        # Direction
        self.angle = random.uniform(0, 360)
        self.target_angle = self.angle

        # Movement
        self.speed = 0
        self.max_speed = 2.5
        self.acceleration = 0.3
        self.friction = 0.4

        # AI
        self.state = "turn"
        self.timer = 0



        # player detection

        self.view_range = 400

        self.charging = False

        self.charge_speed = 2.5
        self.wing_phase = 0.0

        # Worker ants flee/wander until attacked, then they chase.
        self.angry = False

        # King / minion flags (set by the /king command)
        self.is_king = False
        self.is_minion = False
        self.king_minion_timer = 0
        self.king_chat_timer = 0
        self.king_rose_timer = 0
        self.king_orbit_slot = 0

    def take_damage(self, amount):

        if not self.alive:
            return

        # Getting hit makes the worker ant chase the player.
        self.angry = True

        self.hp -= int(amount)
        self.flash_timer = 4

        if self.hp <= 0:

            if getattr(self, "death_registered", False):
                return
            self.death_registered = True

            cleanup_king(self)
            register_mob_kill(self)
            drop_mob_loot(self)

            # Die with a fast shrink instead of vanishing.
            self.dying = True
            self.shrink_scale = 1.0
            self.full_radius = self.radius

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    getattr(
                        self,
                        "custom_xp",
                        10 * MOB_XP_MULTIPLIER[self.rarity]
                    )
                )
            )

    def turn_to(self, target_angle, speed):

        difference = (
            target_angle - self.angle + 180
        ) % 360 - 180

        if abs(difference) <= speed:

            self.angle = target_angle

            return True

        if difference > 0:

            self.angle += speed

        else:

            self.angle -= speed

        return False

    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return

        self.timer += 1

        # ---------------- KING AI ----------------

        if getattr(self, "is_king", False):

            if king_chase_or_guard(self):
                return

        if getattr(self, "is_minion", False):

            minion_ai(self)
            return

        # ---------------- ANGRY WORKER ANT ----------------
        # Chases the player once it has been damaged.

        if self.angry:

            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )

            self.turn_to(
                target_angle,
                8
            )

            if self.speed < self.max_speed:

                self.speed += self.acceleration

            rad = math.radians(
                self.angle
            )

            dx = math.cos(rad) * self.speed * 0.15
            dy = math.sin(rad) * self.speed * 0.15

            move_with_collision(
                self,
                dx,
                dy
            )

            return

        # ---------------- CALM WANDER ----------------

        if self.state == "turn":

            if self.turn_to(
                self.target_angle,
                2
            ):

                self.state = "walk"

                self.timer = 0

        elif self.state == "walk":

            if self.speed < self.max_speed:

                self.speed += self.acceleration

            rad = math.radians(
                self.angle
            )

            dx = math.cos(rad) * self.speed * 0.15

            dy = math.sin(rad) * self.speed * 0.15

            move_with_collision(
                self,
                dx,
                dy
            )

            if self.timer >= 80:

                self.state = "slow"

                self.timer = 0

        elif self.state == "slow":

            self.speed -= self.friction

            if self.speed < 0:

                self.speed = 0

            rad = math.radians(
                self.angle
            )

            dx = math.cos(rad) * self.speed * 0.15

            dy = math.sin(rad) * self.speed * 0.15

            move_with_collision(
                self,
                dx,
                dy
            )

            if self.speed == 0:

                self.state = "pause"

                self.timer = 0

        elif self.state == "pause":

            if self.timer >= 50:

                self.target_angle = random.uniform(
                    0,
                    360
                )

                self.state = "turn"

                self.timer = 0

    def draw(self):

        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if (
            sx < -100 or
            sx > WIDTH + 100 or
            sy < -100 or
            sy > HEIGHT + 100
        ):
            return

        angle = math.radians(self.angle)

        # ---------------- SIZE ----------------

        head_size = self.radius * 0.80

        body_width = self.radius * 1.2
        body_height = self.radius * 0.8

        # ---------------- OVAL BODY (BACK) ----------------

        body_surface = pygame.Surface(
            (
                int(body_width * 2),
                int(body_height * 2)
            ),
            pygame.SRCALPHA
        )

        wa_body_col = (255, 230, 100) if getattr(self, "yellow_minion", False) else (62, 62, 62)
        wa_out_col = (210, 160, 40) if getattr(self, "yellow_minion", False) else (22, 22, 22)
        pygame.draw.ellipse(
            body_surface,
            flash_color(wa_body_col, self.flash_timer),
            (
                0,
                0,
                int(body_width * 2),
                int(body_height * 2)
            )
        )
        pygame.draw.ellipse(
            body_surface,
            flash_color(wa_out_col, self.flash_timer),
            (
                0,
                0,
                int(body_width * 2),
                int(body_height * 2)
            ),
            max(2, int(self.radius * 0.10))
        )

        body_surface = pygame.transform.rotate(
            body_surface,
            -self.angle
        )

        body_rect = body_surface.get_rect(
            center=(int(sx), int(sy))
        )

        screen.blit(
            body_surface,
            body_rect
        )

        # (No wings: worker ants travel on foot.)

        # ---------------- HEAD (FRONT) ----------------

        head_x = (
            sx +
            math.cos(angle) * self.radius * 0.7
        )

        head_y = (
            sy +
            math.sin(angle) * self.radius * 0.7
        )

        wa_head_col = (250, 215, 80) if getattr(self, "yellow_minion", False) else (48, 48, 48)
        wa_hi_col = (255, 245, 150) if getattr(self, "yellow_minion", False) else (78, 78, 78)

        pygame.draw.circle(
            screen,
            flash_color(wa_head_col, self.flash_timer),
            (
                int(head_x),
                int(head_y)
            ),
            int(head_size)
        )

        # Soft highlight like the soldier ant / baby ant minion.
        pygame.draw.circle(
            screen,
            flash_color(wa_hi_col, self.flash_timer),
            (
                int(head_x),
                int(head_y)
            ),
            int(head_size * 0.74)
        )

        # ---------------- MOUTH / MANDIBLES ----------------

        front_x = math.cos(angle)
        front_y = math.sin(angle)

        side_x = math.cos(angle + math.pi/2)
        side_y = math.sin(angle + math.pi/2)

        mouth_start_x = (
            head_x +
            front_x * head_size * 0.75
        )

        mouth_start_y = (
            head_y +
            front_y * head_size * 0.75
        )

        mouth_end_x = (
            head_x +
            front_x * head_size * 1.25
        )

        mouth_end_y = (
            head_y +
            front_y * head_size * 1.25
        )

        draw_clean_line(
            screen,
            flash_color((40,40,40), self.flash_timer),
            (
                mouth_start_x + side_x * 5,
                mouth_start_y + side_y * 5
            ),
            (
                mouth_end_x + side_x * 8,
                mouth_end_y + side_y * 8
            ),
            3
        )

        draw_clean_line(
            screen,
            flash_color((40,40,40), self.flash_timer),
            (
                mouth_start_x - side_x * 5,
                mouth_start_y - side_y * 5
            ),
            (
                mouth_end_x - side_x * 8,
                mouth_end_y - side_y * 8
            ),
            3
        )

        # ---------------- HP BAR ----------------

        if self.hp < self.max_hp:

            bar_width = max(1, int(45 * settings_hp_bar_scale))
            bar_height = max(
                1,
                int(5 * settings_hp_bar_scale)
            )

            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 13 - bar_height),
                    bar_width,
                    bar_height
                )
            )

            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 13 - bar_height),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )

        # ---------------- KING CORN ----------------

        if getattr(self, "is_king", False):

            # Three circles of six corn orbit the worker ant king.
            for corn in worker_ant_corn:
                if corn["owner"] is not self:
                    continue
                if corn["respawn"] > 0:
                    continue
                corn_x, corn_y = worker_corn_pos(corn)
                draw_petal(
                    "Corn",
                    corn_x - camera_x,
                    corn_y - camera_y,
                    self.rarity,
                    size_scale=corn["shrink"]
                )
                draw_projectile_hp_bar(
                    corn_x - camera_x,
                    corn_y - camera_y,
                    corn["radius"],
                    corn["hp"],
                    corn["max_hp"]
                )
                pygame.draw.circle(
                    screen,
                    (255, 60, 60),
                    (int(corn_x - camera_x), int(corn_y - camera_y)),
                    int(corn["radius"]),
                    2
                )

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- HOLE WORKER ANT ----------------
# A 2x eyeless void harvester from Hole Land.
# 2x size, 2x HP, 2x damage.
# Eyeless crystalline obsidian chitin, 6 scuttling void crawler legs,
# dual heavy grappling pincer mandibles, and glowing void core conduits.
class HoleWorkerAnt(WorkerAnt):
    is_hole_land_mob = True

    def __init__(self):
        super().__init__()
        # 2x stats & size
        self.radius = self.radius * 2
        self.base_radius = self.radius
        self.damage = 160
        self.petal_damage = 60
        self.max_hp = 100 * MOB_HP_MULTIPLIER[self.rarity]
        self.hp = self.max_hp

        # Fast skitter speed
        self.max_speed = 3.5
        self.acceleration = 0.45
        self.friction = 0.4
        self.charge_speed = 3.8
        self.view_range = 450

        # Void aesthetics & animations
        self.void_pulse = random.uniform(0, math.pi * 2)
        self.leg_phase = random.uniform(0, math.pi * 2)
        self.mandible_snap = random.uniform(0, math.pi * 2)

    def update(self):
        if not self.alive or getattr(self, "dying", False):
            return
        super().update()
        if not self.alive or getattr(self, "dying", False):
            return
        self.void_pulse += 0.08
        self.leg_phase += 0.35 if self.speed > 0.1 or getattr(self, "angry", False) else 0.05
        self.mandible_snap += 0.18

    def draw(self):
        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if sx < -140 or sx > WIDTH + 140 or sy < -140 or sy > HEIGHT + 140:
            return

        angle = math.radians(self.angle)
        front_x = math.cos(angle)
        front_y = math.sin(angle)
        side_x = -front_y
        side_y = front_x

        # ---------------- HP BAR ----------------
        if self.hp < self.max_hp and not getattr(self, "dying", False):
            bar_width = max(1, int(55 * settings_hp_bar_scale))
            bar_height = max(1, int(5 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))

            pygame.draw.rect(
                screen,
                (45, 12, 60),
                (int(sx - bar_width/2), int(sy - self.radius - 12 - bar_height), bar_width, bar_height)
            )
            pygame.draw.rect(
                screen,
                (190, 50, 255),
                (int(sx - bar_width/2), int(sy - self.radius - 12 - bar_height), int(bar_width * hp_percent), bar_height)
            )

        # ---------------- PULSING VOID AURA ----------------
        pulse = math.sin(self.void_pulse) * 4
        aura_r = int(self.radius * 1.35 + pulse)
        aura_surf = pygame.Surface((aura_r * 2 + 6, aura_r * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (140, 25, 210, 40), (aura_r + 3, aura_r + 3), aura_r)
        screen.blit(aura_surf, (int(sx - aura_r - 3), int(sy - aura_r - 3)))

        # ---------------- 1. SIX SCUTTLING VOID LEGS ----------------
        leg_col = flash_color((30, 10, 44), self.flash_timer)
        leg_tip_col = flash_color((0, 240, 255), self.flash_timer)
        for l_idx in range(3):
            # 3 pairs of legs along the body
            l_offset = (l_idx - 1) * (self.radius * 0.45)
            l_base_x = sx + front_x * l_offset
            l_base_y = sy + front_y * l_offset
            for s_mult in (-1, 1):
                leg_swing = math.sin(self.leg_phase + l_idx * 1.5 + (0 if s_mult == 1 else math.pi)) * (self.radius * 0.35)
                knee_x = l_base_x + side_x * s_mult * (self.radius * 1.05) + front_x * leg_swing
                knee_y = l_base_y + side_y * s_mult * (self.radius * 1.05) + front_y * leg_swing
                foot_x = l_base_x + side_x * s_mult * (self.radius * 1.55) + front_x * (leg_swing * 1.4)
                foot_y = l_base_y + side_y * s_mult * (self.radius * 1.55) + front_y * (leg_swing * 1.4)

                draw_clean_line(screen, leg_col, (int(l_base_x), int(l_base_y)), (int(knee_x), int(knee_y)), max(2, int(self.radius * 0.12)))
                draw_clean_line(screen, leg_col, (int(knee_x), int(knee_y)), (int(foot_x), int(foot_y)), max(2, int(self.radius * 0.10)))
                pygame.draw.circle(screen, leg_tip_col, (int(foot_x), int(foot_y)), max(2, int(self.radius * 0.09)))

        # ---------------- 2. THORAX & ABDOMEN (BACK CHASSIS) ----------------
        abd_x = sx - front_x * (self.radius * 0.65)
        abd_y = sy - front_y * (self.radius * 0.65)
        abd_r = int(self.radius * 0.85)
        pygame.draw.circle(screen, flash_color((22, 6, 34), self.flash_timer), (int(abd_x), int(abd_y)), abd_r)
        pygame.draw.circle(screen, flash_color((180, 50, 255), self.flash_timer), (int(abd_x), int(abd_y)), abd_r, max(2, int(self.radius * 0.08)))

        # Center thorax core
        mid_r = int(self.radius * 0.70)
        pygame.draw.circle(screen, flash_color((16, 4, 26), self.flash_timer), (int(sx), int(sy)), mid_r)
        pygame.draw.circle(screen, flash_color((0, 240, 255), self.flash_timer), (int(sx), int(sy)), mid_r, max(2, int(self.radius * 0.08)))

        # ---------------- 3. HEAD (EYELESS DOME WITH VOID CONDUIT) ----------------
        head_x = sx + front_x * (self.radius * 0.70)
        head_y = sy + front_y * (self.radius * 0.70)
        head_r = int(self.radius * 0.72)
        pygame.draw.circle(screen, flash_color((25, 8, 38), self.flash_timer), (int(head_x), int(head_y)), head_r)
        pygame.draw.circle(screen, flash_color((190, 50, 255), self.flash_timer), (int(head_x), int(head_y)), head_r, max(2, int(self.radius * 0.09)))

        # Glowing cyan triangular visor prism (strictly eyeless)
        prism_pts = [
            (int(head_x + front_x * head_r * 0.5), int(head_y + front_y * head_r * 0.5)),
            (int(head_x - front_x * head_r * 0.1 - side_x * head_r * 0.45), int(head_y - front_y * head_r * 0.1 - side_y * head_r * 0.45)),
            (int(head_x - front_x * head_r * 0.1 + side_x * head_r * 0.45), int(head_y - front_y * head_r * 0.1 + side_y * head_r * 0.45)),
        ]
        pygame.draw.polygon(screen, flash_color((0, 240, 255), self.flash_timer), prism_pts)
        pygame.draw.circle(screen, flash_color((255, 60, 200), self.flash_timer), (int(head_x), int(head_y)), max(2, int(self.radius * 0.10)))

        # ---------------- 4. HEAVY SERRATED GRAPPLING PINCERS ----------------
        snap_val = math.sin(self.mandible_snap) * 0.28
        pincer_col = flash_color((35, 10, 52), self.flash_timer)
        pincer_blade = flash_color((0, 255, 240), self.flash_timer)
        for s_mult in (-1, 1):
            p_base = (head_x + front_x * head_r * 0.65 + side_x * s_mult * (head_r * 0.55),
                      head_y + front_y * head_r * 0.65 + side_y * s_mult * (head_r * 0.55))
            p_mid = (head_x + front_x * head_r * 1.45 + side_x * s_mult * (head_r * 1.05 + snap_val * head_r),
                     head_y + front_y * head_r * 1.45 + side_y * s_mult * (head_r * 1.05 + snap_val * head_r))
            p_tip = (head_x + front_x * head_r * 1.75 + side_x * s_mult * (head_r * 0.20 - snap_val * head_r * 0.5),
                     head_y + front_y * head_r * 1.75 + side_y * s_mult * (head_r * 0.20 - snap_val * head_r * 0.5))

            draw_clean_line(screen, pincer_col, p_base, p_mid, max(3, int(self.radius * 0.16)))
            draw_clean_line(screen, pincer_col, p_mid, p_tip, max(2, int(self.radius * 0.13)))
            draw_clean_line(screen, pincer_blade, p_mid, p_tip, max(1, int(self.radius * 0.08)))
            pygame.draw.circle(screen, pincer_blade, (int(p_tip[0]), int(p_tip[1])), max(2, int(self.radius * 0.10)))

        # ---------------- RARITY TEXT ----------------
        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ---------------- ANT EGG ----------------

class AntEgg:

    def __init__(self):

        self.x = random.randint(-500, 500)
        self.y = random.randint(-500, 500)
        self.knockback_x = 0
        self.knockback_y = 0
        self.rarity = "Common"

        # Stats: stays still, same damage as baby ant (25), 50 base HP
        self.damage = 25
        self.max_hp = (
            50 *
            MOB_HP_MULTIPLIER[self.rarity]
        )
        self.hp = self.max_hp
        self.alive = True
        self.flash_timer = 0
        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2

        # Size: similar to queen ant egg
        self.radius = 16
        self.base_radius = self.radius

        # Subtle wobble (matching queen ant egg)
        self.wobble = random.uniform(0, 360)
        self.angle = 0

        # King / minion flags
        self.is_king = False
        self.is_minion = False
        self.king_minion_timer = 0
        self.king_chat_timer = 0
        self.king_rose_timer = 0
        self.king_orbit_slot = 0

    def push(self, dx, dy):
        if not self.alive:
            return
        self.x += dx
        self.y += dy
        self.x = max(self.radius, min(self.x, WORLD_WIDTH - self.radius))
        self.y = max(self.radius, min(self.y, WORLD_HEIGHT - self.radius))

    def turn_to(self, target_angle, speed=2):
        return True

    def take_damage(self, amount):

        if not self.alive:
            return

        self.hp -= int(amount)
        self.flash_timer = 4

        if self.hp <= 0:

            if getattr(self, "death_registered", False):
                return
            self.death_registered = True

            cleanup_king(self)
            register_mob_kill(self)
            drop_mob_loot(self)

            # Fast shrink death animation
            self.dying = True
            self.shrink_scale = 1.0
            self.full_radius = self.radius

            if self.rarity in ("Celestial", "Omnient"):
                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    getattr(
                        self,
                        "custom_xp",
                        10 * MOB_XP_MULTIPLIER[self.rarity]
                    )
                )
            )

            # 30% chance a baby ant with same rarity spawns and chases the player
            if random.random() < 0.30:
                spawned_baby = BabyAnt()
                spawned_baby.x = self.x
                spawned_baby.y = self.y
                spawned_baby.rarity = self.rarity
                apply_enemy_rarity_stats(spawned_baby)
                spawned_baby.angry = True
                baby_ants.append(spawned_baby)

    def update(self):
        if not self.alive:
            return
        # Egg stays still

    def draw(self):

        if not self.alive:
            return

        sx = self.x - camera_x
        sy = self.y - camera_y

        if (
            sx < -100 or
            sx > WIDTH + 100 or
            sy < -100 or
            sy > HEIGHT + 100
        ):
            return

        current_radius = int(
            self.radius * getattr(self, "shrink_scale", 1.0)
        )
        if current_radius <= 0:
            return

        wobble_offset = 0
        if not getattr(self, "freeze_animation", False):
            wobble_offset = (
                math.sin(
                    time.time() * 8 + self.wobble
                ) * 1.5
            )

        draw_y = int(sy + wobble_offset)

        # Egg body: soft cream yellow with golden-tan outline (matching queen ant egg)
        base_fill = (250, 240, 180)
        base_outline = (200, 175, 110)

        pygame.draw.circle(
            screen,
            flash_color(base_fill, self.flash_timer),
            (int(sx), draw_y),
            current_radius
        )
        pygame.draw.circle(
            screen,
            flash_color(base_outline, self.flash_timer),
            (int(sx), draw_y),
            current_radius,
            max(2, int(current_radius * 0.18))
        )

        # ---------------- KING CROWN ----------------
        if getattr(self, "is_king", False):
            crown_y = int(draw_y - current_radius - 14)
            crown_w = int(current_radius * 1.2)
            crown_h = int(current_radius * 0.6)
            crown_left = int(sx - crown_w / 2)
            crown_right = int(sx + crown_w / 2)

            crown_points = [
                (crown_left, crown_y + crown_h),
                (crown_left, crown_y + crown_h * 0.4),
                (
                    crown_left + crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (
                    int(sx - crown_w * 0.15),
                    crown_y
                ),
                (
                    int(sx + crown_w * 0.15),
                    crown_y + crown_h * 0.4
                ),
                (
                    crown_right - crown_w * 0.25,
                    crown_y + crown_h * 0.4
                ),
                (crown_right, crown_y + crown_h * 0.4),
                (crown_right, crown_y + crown_h)
            ]

            pygame.draw.polygon(
                screen,
                flash_color((255, 200, 0), self.flash_timer),
                crown_points
            )
            pygame.draw.polygon(
                screen,
                flash_color((160, 110, 0), self.flash_timer),
                crown_points,
                2
            )

        # HP bar
        if self.hp < self.max_hp and not getattr(self, "dying", False):
            bar_width = max(10, int(min(35, max(16, current_radius * 1.4)) * settings_hp_bar_scale))
            bar_height = max(1, int(4 * settings_hp_bar_scale))
            hp_percent = max(0.0, min(1.0, self.hp / max(1, self.max_hp)))
            bar_offset = 24 if getattr(self, "is_king", False) else 10

            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    int(sx - bar_width / 2),
                    int(draw_y - current_radius - bar_offset - bar_height),
                    bar_width,
                    bar_height
                )
            )
            pygame.draw.rect(
                screen,
                (0, 255, 0),
                (
                    int(sx - bar_width / 2),
                    int(draw_y - current_radius - bar_offset - bar_height),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )

        if not getattr(self, "hide_rarity_label", False):
            draw_mob_rarity_label(
                self,
                int(sx),
                int(draw_y + current_radius + 15)
            )


def delete_enemy(enemy):

    if acc_name_text != "DevGuard":
        return

    enemy.alive = False

def upgrade_player_hp():

    global PLAYER_MAX_HP
    global player_hp
    global PLAYER_HP_LEVEL
    global upgrade_points
    global hp_upgrade_cost


    if upgrade_points >= hp_upgrade_cost:


        upgrade_points -= hp_upgrade_cost


        PLAYER_HP_LEVEL += 1


        PLAYER_MAX_HP *= 2
        player_hp = PLAYER_MAX_HP

        hp_upgrade_cost = math.ceil(
            hp_upgrade_cost * 1.25
        )

        save_player()

def move(self):

    if not self.alive:
        return

    if self.angry and enemy_can_see_player(self):

        move_speed = self.speed * 1.8

        rad = math.radians(self.angle)

        self.x += math.cos(rad) * move_speed
        self.y += math.sin(rad) * move_speed


    else:

        rad = math.radians(self.angle)

        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

def save_player():

    global player_data

    player_data[acc_name_text] = {

        "inventory": inventory,
        "craft_slots": craft_selected_items,
        "equipped_reserved": [
            {
                "petal": slot["petal"],
                "rarity": slot["rarity"],
                "amount": 1
            }
            for slot in petal_slots
            if slot.get("filled")
        ],
        "petals": petal_slots,
        "swap_petals": swap_petal_slots,
        "flower_level": flower_level,
        "flower_xp": flower_xp,
        "upgrade_points": upgrade_points,
        "hp_level": PLAYER_HP_LEVEL,
        "hp_upgrade_cost": hp_upgrade_cost,
        "mob_gallery_unlocks": mob_gallery_unlocks,
        "player_x": player_x,
        "player_y": player_y

    }

    with open("players.json", "w") as file:

        json.dump(
            player_data,
            file,
            indent=4
        )

def load_player():

    global petal_slots
    global swap_petal_slots
    global petal_hp
    global petal_max_hp
    global petal_alive
    global inventory
    global craft_selected_items
    global craft_animation_active
    global craft_animation_timer
    global craft_animation_duration
    global craft_will_succeed
    global craft_should_converge
    global craft_animation_outcome
    global craft_result_item
    global craft_post_result_items
    global mob_gallery_unlocks

    global PETAL_SLOTS

    global flower_level
    global flower_xp
    global flower_xp_needed
    global upgrade_points

    global PLAYER_HP_LEVEL
    global PLAYER_MAX_HP
    global hp_upgrade_cost
    global player_hp

    global player_x
    global player_y


    if acc_name_text not in player_data:
        # The account can exist in accounts.json without a saved player
        # record yet.  Initialize its normal five-slot starting loadout.
        create_account()
        return


    data = player_data[acc_name_text]


    # ---------------- FLOWER DATA ----------------

    # Compute PETAL_SLOTS from the saved flower level *before* slicing the
    # petal arrays, so older saves with fewer than 10 entries still expand
    # to the full 10-slot layout.
    flower_level = data.get(
        "flower_level",
        1
    )
    PETAL_SLOTS = get_petal_slots(flower_level)

    # Restore the player's saved world position (used by /tp).
    player_x = data.get("player_x", player_x)
    player_y = data.get("player_y", player_y)


    # ---------------- PETALS ----------------

    # Older saves may contain fewer than PETAL_SLOTS entries.  Keep the
    # runtime arrays the same length as the game expects.
    saved_petals = data.get("petals", [])
    # Older saves stored all slots in one list.  Split into main and swap.
    saved_main = saved_petals[:PETAL_SLOTS]
    saved_swap = saved_petals[PETAL_SLOTS:]
    petal_slots = list(saved_main[:PETAL_SLOTS])
    while len(petal_slots) < PETAL_SLOTS:
        petal_slots.append({
            "filled": False,
            "petal": "Basic",
            "rarity": "Common"
        })

    # Load swap petals (older saves stored them in the same list)
    swap_petal_slots = list(saved_swap[:PETAL_SLOTS])
    while len(swap_petal_slots) < PETAL_SLOTS:
        swap_petal_slots.append({
            "filled": False,
            "petal": "Basic",
            "rarity": "Common"
        })

    # ---------------- INVENTORY ----------------

    inventory = [
        dict(item)
        for item in data.get("inventory", [])
    ]

    # Keep equipped petals reserved from the available inventory. Older
    # saves did not track this, so their currently equipped petals are
    # subtracted once. Newer saves reconcile the previous and current loadout.
    previous_reserved = data.get("equipped_reserved")
    if previous_reserved is None:
        previous_reserved = [
            {
                "petal": slot["petal"],
                "rarity": slot["rarity"],
                "amount": 1
            }
            for slot in petal_slots
            if slot.get("filled")
        ]
    else:
        for reserved_item in previous_reserved:
            add_inventory_petal(
                reserved_item["petal"],
                reserved_item["rarity"],
                int(reserved_item.get("amount", 1))
            )

    for slot in petal_slots:
        if slot.get("filled"):
            remove_inventory_petal(
                slot["petal"],
                slot["rarity"],
                1
            )

    craft_selected_items = data.get(
        "craft_slots",
        []
    )
    craft_animation_active = False
    craft_animation_timer = 0
    craft_will_succeed = False
    craft_should_converge = False
    craft_animation_outcome = None
    craft_result_item = None
    craft_post_result_items = []
    mob_gallery_unlocks = {
        str(key): int(value)
        for key, value in data.get(
            "mob_gallery_unlocks",
            {}
        ).items()
    }


    RARITY_ORDER = [
        "Infino",
        "Celestial",
        "Omnient",
        "Ancient",
        "Radium",
        "Tacnic",
        "Jeddiful",
        "Cosmo",
        "Eternal",
        "Unique",
        "Omega",
        "Super",
        "Ultra",
        "Mythic",
        "Legendary",
        "Epic",
        "Rare",
        "Unusual",
        "Common"
    ]


    sort_inventory()


    # ---------------- FLOWER DATA ----------------

    flower_level = data.get(
        "flower_level",
        1
    )
    PETAL_SLOTS = get_petal_slots(flower_level)
    pad_petal_slots()
    pad_swap_petal_slots()
    resize_petal_lists()

    flower_xp = data.get(
        "flower_xp",
        0
    )


    upgrade_points = data.get(
        "upgrade_points",
        0
    )


    # Calculate XP needed from the saved level
    flower_xp_needed = calculate_xp_needed(
        flower_level
    )


    # ---------------- PLAYER HP ----------------

    PLAYER_HP_LEVEL = data.get(
        "hp_level",
        1
    )


    hp_upgrade_cost = data.get(
        "hp_upgrade_cost",
        1
    )


    PLAYER_MAX_HP = (
        50 *
        (2 ** PLAYER_HP_LEVEL)
    )

    player_hp = PLAYER_MAX_HP


    # ---------------- PETAL HP RESET ----------------

    petal_hp = []
    petal_max_hp = []
    petal_alive = []
    petal_flash_timers = []


    for slot in petal_slots:

        if slot["filled"]:

            hp = (
                PETAL_HP[slot["petal"]]
                *
                PETAL_HP_MULTIPLIER[slot["rarity"]]
            )

            if slot["petal"] == "Light":
                light_count = get_petal_count("Light", slot["rarity"])
                if light_count > 0:
                    hp /= light_count

            petal_max_hp.append(
                hp
            )

            petal_hp.append(
                hp
            )

            petal_alive.append(
                True
            )

            petal_flash_timers.append(
                0
            )

            petal_cooldowns.append(
                0
            )

            light_cooldowns.append([])
            light_hp.append([])
            light_alive.append([])


        else:

            petal_max_hp.append(
                0
            )

            petal_hp.append(
                0
            )

            petal_alive.append(
                False
            )

            petal_flash_timers.append(
                0
            )

            petal_cooldowns.append(
                0
            )

            light_cooldowns.append([])
            light_hp.append([])
            light_alive.append([])

    # Ensure all petal lists match PETAL_SLOTS
    resize_petal_lists()

def create_map():

    walls.clear()
    global starter_walls
    global common_zone
    global epic_zone
    global unusual_zone
    global mythic_zone
    global ultra_zone
    global super_BabyAnt_zone

    # Initialize zone lists as empty (used for enemy spawning)
    starter_walls = []
    common_zone = []
    epic_zone = []
    unusual_zone = []
    mythic_zone = []
    ultra_zone = []
    super_BabyAnt_zone = []

    # No walls created - all garden walls removed as requested
    # Enemy spawning uses hardcoded rectangles in spawn_random_mob()

def get_petal_count(petal_name, rarity):

    # ---------------- LIGHT ----------------

    if petal_name == "Light":

        if rarity == "Common":
            return 1

        elif rarity in ["Unusual", "Rare"]:
            return 2

        elif rarity in ["Epic", "Legendary"]:
            return 3

        elif rarity in ["Mythic", "Ultra","Super", "Omega", "Unique"]:
            return 5

        elif rarity in [
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium",
            "Ancient",
            "Omnient",
            "Celestial",
            "Infino"
        ]:
            return 7


    # ---------------- ROCK ----------------

    elif petal_name == "Rock":

        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super"
        ]:
            return 1

        else:
            return 3


    # ---------------- FASTER ----------------

    elif petal_name == "Faster":

        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super"
        ]:
            return 1
        elif rarity in ["Omega",
                        "Unique",
                        "Eternal",
                        "Cosmo",
                        "Jeddiful",
                        "Tacnac",
                        "Radium"
                    ]:
            return 3
        else:
            return 5


    # ---------------- RICE ----------------

    elif petal_name == "Rice":

        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super"
        ]:
            return 1
        elif rarity in [
            "Omega",
            "Unique",
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium",
            "Ancient"
        ]:
            return 2
        else:
            return 3


    # ---------------- CORN ----------------

    elif petal_name == "Corn":

        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 1
        elif rarity in [
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium",
            "Ancient"
        ]:
            return 2
        else:
            return 4

    elif petal_name == "Wing":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega"
        ]:
            return 1
        elif rarity in [
            "Unique",
            "Eternal",
            "Cosmo"
        ]:
            return 2
        else:
            return 3

    elif petal_name == "Leaf":

        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 1

        elif rarity in [
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium",
            "Ancient"
        ]:
            return 3

        else:
            return 5

    elif petal_name == "Glass":

        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega"
        ]:
            return 1

        else:
            return 3

    elif petal_name == "Stinger":

        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary"
        ]:
            return 1

        elif rarity == "Mythic":
            return 3

        else:
            return 5

    elif petal_name == "Cactus":

        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique",
            "Eternal",
            "Cosmo"
        ]:
            return 1

        else:
            return 3

    elif petal_name == "Bone":

        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique",
            "Eternal",
            "Cosmo"
        ]:
            return 1
        elif rarity in [
            "Jeddiful",
            "Tacnic",
            "Radium"
        ]:
            return 3
        else:
            return 5

    elif petal_name == "Poison":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 1
        elif rarity in [
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium"
        ]:
            return 3
        else:
            return 5

    elif petal_name == "Pincer":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 1
        else:
            return 2

    elif petal_name == "Beetle Egg":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 1
        else:
            return 2

    elif petal_name == "Missile":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 1
        elif rarity in [
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium"
        ]:
            return 2
        else:
            return 3

    elif petal_name == "Ant Egg":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega"
        ]:
            return 4
        elif rarity in [
            "Unique",
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium"
        ]:
            return 5
        else:
            return 6

    elif petal_name == "Pea":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 4
        elif rarity in [
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium"
        ]:
            return 5
        else:
            return 6

    elif petal_name == "Web":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega"
        ]:
            return 1
        elif rarity in [
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium"
        ]:
            return 2
        else:
            return 4

    elif petal_name == "Magnet":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 1
        elif rarity in [
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium"
        ]:
            return 2
        else:
            return 3

    elif petal_name == "Grape":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 4
        elif rarity in [
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic",
            "Radium"
        ]:
            return 5
        else:
            return 6

    elif petal_name == "Sand":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique",
            "Eternal",
            "Cosmo"
        ]:
            return 4
        else:
            return 5

    elif petal_name == "Honey":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique",
            "Eternal",
            "Cosmo"
        ]:
            return 1
        else:
            return 3

    elif petal_name == "Rose":
        if rarity in [
            "Common",
            "Unusual",
            "Rare",
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique",
            "Eternal",
            "Cosmo",
            "Jeddiful",
            "Tacnic"
        ]:
            return 1
        else:
            return 2

    elif petal_name == "Pollen":
        Random_Pick_Pollen = [4,5]
        if rarity in [
            "Common"
        ]:
            return 1
        elif rarity in [
            "Unusual",
            "Rare",
        ]:
            return 2
        elif rarity in [
            "Epic",
            "Legendary",
            "Mythic",
            "Ultra",
            "Super",
            "Omega",
            "Unique"
        ]:
            return 3
        else:
            random_APollen = random.choice(Random_Pick_Pollen)
            return random_APollen



    else:
        return 1

def get_petal_damage(petal_name, rarity):

    base_damage = PETAL_DAMAGE[petal_name]

    rarity_multiplier = RARITY_DAMAGE_MULTIPLIER[rarity]

    petal_count = get_petal_count(
        petal_name,
        rarity
    )

    damage = (
        base_damage
        * rarity_multiplier
        * petal_count
    )

    if petal_name == "Light":
        damage /= petal_count

    return damage


def format_number(number):

    suffixes = [
        "",
        "k",
        "m",
        "b",
        "t",
        "qa",
        "qi",
        "sx",
        "sp",
        "oc",
        "no",
        "dc",
        "ud",
        "dd",
        "td",
        "qt",
    ]

    index = 0

    while number >= 1000 and index < len(suffixes) - 1:
        number /= 1000
        index += 1

    # No suffix
    if index == 0:
        return str(int(number))

    # If the ORIGINAL value for this suffix was exact,
    # show no .0
    if number.is_integer():
        return str(int(number)) + suffixes[index]

    # Truncate instead of rounding
    truncated = int(number * 10) / 10

    return f"{truncated:.1f}{suffixes[index]}"

def damage_petal(amount):

    for i in range(PETAL_SLOTS):

        if petal_alive[i]:

            petal_hp[i] -= amount
            petal_flash_timers[i] = 4


            if petal_hp[i] <= 0:

                petal_hp[i] = 0
                petal_alive[i] = False

                petal_respawn_timer[i] = PETAL_RELOAD[
                    petal_slots[i]["petal"]
                ]

                save_player()

def apply_enemy_rarity_stats(enemy):

    enemy.max_hp *= MOB_HP_MULTIPLIER[enemy.rarity]
    enemy.damage *= MOB_DAMAGE_MULTIPLIER[enemy.rarity]
    enemy.radius *= MOB_SIZE_MULTIPLIER[enemy.rarity]
    enemy.hp = enemy.max_hp

def spawn_random_mob():

    # The space bar spawn cheat is only for the developer, and it only
    # spawns the mobs that have a working petal drop table.
    if acc_name_text != "DevGuard":
        return

    enemy_classes = {
        "Ladybug": (Ladybug, ladybugs),
        "Bee": (Bee, bees),
        "Spider": (Spider, spiders),
        "Rock": (Rock, rocks),
        "Hornet": (Hornet, hornets),
        "Baby Ant": (BabyAnt, baby_ants),
        "Soldier Ant": (SoldierAnt, soldier_ants),
        "Worker Ant": (WorkerAnt, worker_ants),
        "Queen Ant": (QueenAnt, queen_ants),
        "Ant Egg": (AntEgg, ant_eggs)
    }

    drop_mob_names = sorted({
        mob_name
        for (mob_name, rarity), drop_table in MOB_DROP_INFO.items()
        if drop_table and mob_name in enemy_classes
    })
    if not drop_mob_names:
        return

    drop_mob_name = random.choice(drop_mob_names)
    enemy_class, enemy_list = enemy_classes[drop_mob_name]

    table_rarities = [
        rarity
        for (mob_name, rarity), drop_table in MOB_DROP_INFO.items()
        if mob_name == drop_mob_name and drop_table
    ]
    if not table_rarities:
        return

    enemy = enemy_class()
    enemy.rarity = random.choice(table_rarities)

    # Update HP after changing rarity
    apply_enemy_rarity_stats(enemy)

    enemy.x = max(enemy.radius, min(player_x + random.randint(-300, 300), WORLD_WIDTH - enemy.radius))
    enemy.y = max(enemy.radius, min(player_y + random.randint(-300, 300), WORLD_HEIGHT - enemy.radius))

    enemy_list.append(enemy)

    if enemy.rarity in ("Celestial", "Omnient"):
        show_spawn_message(
            enemy.rarity,
            type(enemy).__name__
        )

def show_spawn_message(rarity, mob):

    global spawn_message
    global spawn_message_timer
    global spawn_message_alpha

    spawn_message = f"{rarity} {mob} Spawned!"
    spawn_message_timer = 180
    spawn_message_alpha = 255

def show_error(message):

    global error_message
    global error_message_timer
    global error_message_alpha

    error_message = message
    error_message_timer = 180
    error_message_alpha = 255

def show_defeat_message(rarity, mob_name):

    global spawn_message
    global spawn_message_timer

    spawn_message = (
        rarity +
        " " +
        mob_name +
        " is defeated by" + acc_name_text + "!"
    )

    spawn_message_timer = 180   # 3 seconds at 60 FPS

def register_mob_kill(enemy):

    global mob_gallery_unlocks

    mob_name = type(enemy).__name__
    if mob_name in ("HoleLadybug", "Hole Ladybug"):
        mob_name = "Hole Ladybug"
    elif mob_name in ("HoleBee", "Hole Bee"):
        mob_name = "Hole Bee"
    elif mob_name in ("HoleSpider", "Hole Spider"):
        mob_name = "Hole Spider"
    elif mob_name in ("HoleRock", "Hole Rock"):
        mob_name = "Hole Rock"
    elif mob_name in ("HoleHornet", "Hole Hornet"):
        mob_name = "Hole Hornet"
    elif mob_name in ("HoleBabyAnt", "Hole Baby Ant"):
        mob_name = "Hole Baby Ant"
    elif mob_name in ("HoleSoldierAnt", "Hole Soldier Ant"):
        mob_name = "Hole Soldier Ant"
    elif mob_name in ("HoleWorkerAnt", "Hole Worker Ant"):
        mob_name = "Hole Worker Ant"
    elif mob_name in ("HoleQueenAnt", "Hole Queen Ant"):
        mob_name = "Hole Queen Ant"
    elif mob_name == "BabyAnt":
        mob_name = "Baby Ant"
    elif mob_name == "SoldierAnt":
        mob_name = "Soldier Ant"
    elif mob_name == "WorkerAnt":
        mob_name = "Worker Ant"
    elif mob_name in ("HoleQueenAnt", "Hole Queen Ant"):
        mob_name = "Hole Queen Ant"
    elif mob_name == "QueenAnt":
        mob_name = "Queen Ant"
    elif mob_name == "AntEgg":
        mob_name = "Ant Egg"

    key = f"{mob_name}|{enemy.rarity}"
    previous_count = int(mob_gallery_unlocks.get(key, 0))
    mob_gallery_unlocks[key] = previous_count + 1

    # Save a newly discovered entry immediately; repeat kills remain cheap
    # and are saved by the normal player-save flow.
    if previous_count == 0:
        save_player()

def spawn_pickup(x, y, petal, rarity):

    # Stingers last four times as long on the ground before despawning.
    pickup_lifetime = (
        PICKUP_LIFETIME * 4
        if petal == "Stinger"
        else PICKUP_LIFETIME
    )

    PICKUP_LIST.append(
        {
            "x": x,
            "y": y,
            "petal": petal,
            "rarity": rarity,
            "timer": pickup_lifetime
        }
    )

def drop_mob_loot(enemy):

    mob_name = type(enemy).__name__
    if mob_name in ("HoleLadybug", "Hole Ladybug"):
        mob_name = "Hole Ladybug"
    elif mob_name in ("HoleBee", "Hole Bee"):
        mob_name = "Hole Bee"
    elif mob_name in ("HoleSpider", "Hole Spider"):
        mob_name = "Hole Spider"
    elif mob_name in ("HoleRock", "Hole Rock"):
        mob_name = "Hole Rock"
    elif mob_name in ("HoleHornet", "Hole Hornet"):
        mob_name = "Hole Hornet"
    elif mob_name in ("HoleBabyAnt", "Hole Baby Ant"):
        mob_name = "Hole Baby Ant"
    elif mob_name in ("HoleSoldierAnt", "Hole Soldier Ant"):
        mob_name = "Hole Soldier Ant"
    elif mob_name in ("HoleWorkerAnt", "Hole Worker Ant"):
        mob_name = "Hole Worker Ant"
    elif mob_name == "BabyAnt":
        mob_name = "Baby Ant"
    elif mob_name == "SoldierAnt":
        mob_name = "Soldier Ant"
    elif mob_name == "WorkerAnt":
        mob_name = "Worker Ant"
    elif mob_name == "QueenAnt":
        mob_name = "Queen Ant"
    elif mob_name == "AntEgg":
        mob_name = "Ant Egg"

    drop_table = MOB_DROP_INFO.get((mob_name, enemy.rarity))
    if not drop_table:
        return

    # King mobs drop petals more often: every drop chance is
    # boosted by +1.5 percentage points.
    king_drop_bonus = (
        1.5
        if getattr(enemy, "is_king", False)
        else 0.0
    )

    drops = []

    if enemy.rarity != "Common":
        # For non-Common mobs, drop exactly 1 of each petal type.
        # For each petal type, pick the best rarity (mob's first, then Common).
        # Petals with < 5% drop chance: single roll only.
        # Petals with >= 5%: retry up to 10 times.
        # Works correctly for decimal percentages (e.g. 0.06%).
        petal_rows = {}
        for petal, petal_rarity, drop_chance in drop_table:
            petal_rows.setdefault(petal, []).append(
                (petal_rarity, drop_chance)
            )

        for petal, rows in petal_rows.items():
            # Pick best rarity: mob's rarity first, then Common
            chosen_rarity = None
            chosen_chance = None
            for petal_rarity, drop_chance in rows:
                if petal_rarity == enemy.rarity:
                    chosen_rarity = petal_rarity
                    chosen_chance = drop_chance
                    break
            if chosen_rarity is None:
                for petal_rarity, drop_chance in rows:
                    if petal_rarity == "Common":
                        chosen_rarity = petal_rarity
                        chosen_chance = drop_chance
                        break
            if chosen_rarity is None:
                chosen_rarity, chosen_chance = rows[0]

            boosted_chance = chosen_chance + king_drop_bonus
            if boosted_chance < 5:
                # Rare drop: single roll
                if random.random() * 100 < boosted_chance:
                    drops.append((petal, chosen_rarity))
            else:
                # Normal drop: retry up to 10 times
                for _ in range(10):
                    if random.random() * 100 < boosted_chance:
                        drops.append((petal, chosen_rarity))
                        break
    else:
        # For Common mobs, single roll per row (or none)
        for petal, petal_rarity, drop_chance in drop_table:
            boosted_chance = drop_chance + king_drop_bonus
            if random.random() * 100 < boosted_chance:
                drops.append((petal, petal_rarity))

    if not drops:
        return

    # Arrange the dropped boxes the same way multiplied petals are drawn
    # (epic light puts its three dots on triangle points): one box stays
    # in the middle, several boxes spread around a ring so they never
    # stack on top of each other.
    drop_count = len(drops)
    ring_radius = PICKUP_SIZE + 12
    for drop_index, (petal, petal_rarity) in enumerate(drops):

        if drop_count == 1:

            offset_x = 0
            offset_y = 0

        else:

            drop_angle = math.radians(
                drop_index * (360.0 / drop_count)
            )

            offset_x = math.cos(drop_angle) * ring_radius
            offset_y = math.sin(drop_angle) * ring_radius

        spawn_pickup(
            enemy.x + offset_x,
            enemy.y + offset_y,
            petal,
            petal_rarity
        )

def draw_clean_line(surface, color, start_pos, end_pos, width):

    # pygame.draw.line renders thick diagonal lines with slanted,
    # parallelogram-looking ends.  This builds the line as a proper
    # rotated rectangle instead.
    start_x = float(start_pos[0])
    start_y = float(start_pos[1])
    end_x = float(end_pos[0])
    end_y = float(end_pos[1])

    delta_x = end_x - start_x
    delta_y = end_y - start_y
    length = math.hypot(delta_x, delta_y)

    if length <= 0:

        pygame.draw.circle(
            surface,
            color,
            (
                int(start_x),
                int(start_y)
            ),
            max(1, int(width / 2))
        )

        return

    across_x = -delta_y / length
    across_y = delta_x / length
    half_width = width / 2

    pygame.draw.polygon(
        surface,
        color,
        [
            (
                int(start_x + across_x * half_width),
                int(start_y + across_y * half_width)
            ),
            (
                int(end_x + across_x * half_width),
                int(end_y + across_y * half_width)
            ),
            (
                int(end_x - across_x * half_width),
                int(end_y - across_y * half_width)
            ),
            (
                int(start_x - across_x * half_width),
                int(start_y - across_y * half_width)
            )
        ]
    )

def flash_color(color, flash_timer):

    if flash_timer <= 0:
        return color

    r, g, b = color[0], color[1], color[2]

    fade = flash_timer / 4

    return (
        min(255, int(r + 120 * fade)),
        max(0, int(g - 60 * fade)),
        max(0, int(b - 60 * fade))
    )

def draw_mob_rarity_label(mob, label_x, label_y):

    font = pygame.font.SysFont(
        None,
        18
    )


    rarity_color = RARITY_COLORS.get(
        mob.rarity,
        (255,255,255)
    )


    rarity_text = font.render(
        mob.rarity,
        True,
        rarity_color
    )


    text_rect = rarity_text.get_rect(
        center=(
            int(label_x),
            int(label_y)
        )
    )

    # black outline
    for ox in (-1, 0, 1):
        for oy in (-1, 0, 1):
            if ox == 0 and oy == 0:
                continue
            outline = font.render(mob.rarity, True, (0, 0, 0))
            screen.blit(
                outline,
                (text_rect.x + ox, text_rect.y + oy)
            )

    screen.blit(
        rarity_text,
        text_rect
    )

# Fixed portrait sizes so every gallery icon keeps the same size every
# frame (mob classes randomize their radius in __init__, which made some
# icons grow and shrink constantly).
GALLERY_ICON_RADIUS = {
    "Ladybug": 12,
    "Hole Ladybug": 14,
    "Bee": 9,
    "Hole Bee": 11,
    "Spider": 11,
    "Hole Spider": 13,
    "Rock": 11,
    "Hole Rock": 9,
    "Hornet": 11,
    "Hole Hornet": 11,
    "Baby Ant": 8,
    "Hole Baby Ant": 8,
    "Soldier Ant": 10,
    "Hole Soldier Ant": 10,
    "Worker Ant": 10,
    "Hole Worker Ant": 10,
    "Queen Ant": 8,
    "Hole Queen Ant": 8,
    "Ant Egg": 11
}

# Short lore text shown in the gallery hover rectangle.
GALLERY_MOB_DESCRIPTIONS = {
    "Ladybug": (
        "A calm red circle thing that wanders the grass. It never "
        "starts fights, but it will bite back when bothered."
    ),
    "Hole Ladybug": (
        "ladybugs from blackholes might not exist."
    ),
    "Bee": (
        "this striped animal is harmless until you attack it, "
        "it is very dangerous when you touch it."
    ),
    "Hole Bee": (
        "A grotesque 2x abyss bee from Hole Land. Possesses segmented chitin, "
        "four vibrating void wings, and dual stingers."
    ),
    "Spider": (
        "you don't want to go to its webs."
    ),
    "Hole Spider": (
        "A nightmarish 2x eyeless arachnid from Hole Land with 8 barbed "
        "jointed void legs and high pursuit speed."
    ),
    "Rock": (
        "its just a grey rock but becareful from its throwed rocks."
    ),
    "Hole Rock": (
        "A 2x abyss rock covered in 80% longer razor-sharp void spikes, "
        "flinging volatile shards of jagged dark matter."
    ),
    "Hornet": (
        "it uses missles to attack."
    ),
    "Hole Hornet": (
        "A 2x eyeless void hornet from Hole Land equipped with twin rear-mounted "
        "void torpedo launchers and rapid strike agility."
    ),
    "Baby Ant": (
        "its the baby of the ant colony."
    ),
    "Hole Baby Ant": (
        "A 2x eyeless void ant larva equipped with quadruple snapping mandibles "
        "and venomous dorsal tendrils."
    ),
    "Soldier Ant": (
        "it pretects the ant hole and sometimes their lost."
    ),
    "Hole Soldier Ant": (
        "A 2x armored void dreadnought ant from Hole Land with 4 serrated void wings, "
        "eyeless obsidian armor plates, and massive executioner mandibles."
    ),
    "Worker Ant": (
        "this one worker for the queen ant but it chase you"
        "when you damage it."
    ),
    "Hole Worker Ant": (
        "A 2x eyeless void harvester from Hole Land. Possesses 6 barbed scuttling legs, "
        "crystalline obsidian plates, and heavy grappling pincer mandibles."
    ),
    "Queen Ant": (
        "the mother of the ant colony. she lays eggs that hatch "
        "into ants while chasing you."
    ),
    "Hole Queen Ant": (
        "A 2x colossal void matriarch from Hole Land. Eyeless obsidian armor, "
        "4 fluttering void-glitch wings, and an egg incubator chamber that spawns Void Eggs."
    ),
    "Ant Egg": (
        "a fragile ant egg that stays still. when broken, a baby ant "
        "might hatch from it and chase you!"
    )
}

# Petal drop tables.  Each (mob name, mob rarity) entry lists possible
# drops as (petal name, petal rarity, chance percentage).  Every entry
# is rolled independently when the mob dies, so a kill can give several
# petals or nothing at all.
MOB_DROP_INFO = {
    ("Hole Worker Ant", "Common"): [
        ("Corn", "Common", 45),
        ("Corn", "Unusual", 18),
        ("Clover", "Common", 35),
        ("Clover", "Unusual", 14),
        ("Soil", "Common", 25),
        ("Soil", "Unusual", 10),
    ],
    ("Hole Worker Ant", "Unusual"): [
        ("Corn", "Common", 14),
        ("Corn", "Unusual", 50),
        ("Clover", "Common", 10),
        ("Clover", "Unusual", 45),
        ("Soil", "Common", 8),
        ("Soil", "Unusual", 40),
    ],
    ("Hole Soldier Ant", "Common"): [
        ("Wing", "Common", 40),
        ("Wing", "Unusual", 16),
        ("Glass", "Common", 35),
        ("Glass", "Unusual", 14),
        ("Heavy", "Common", 28),
        ("Heavy", "Unusual", 10),
    ],
    ("Hole Soldier Ant", "Unusual"): [
        ("Wing", "Common", 12),
        ("Wing", "Unusual", 48),
        ("Glass", "Common", 10),
        ("Glass", "Unusual", 44),
        ("Heavy", "Common", 8),
        ("Heavy", "Unusual", 38),
    ],
    ("Hole Baby Ant", "Common"): [
        ("Rice", "Common", 40),
        ("Rice", "Unusual", 16),
        ("Corn", "Common", 32),
        ("Corn", "Unusual", 12),
        ("Soil", "Common", 25),
        ("Soil", "Unusual", 8),
    ],
    ("Hole Baby Ant", "Unusual"): [
        ("Rice", "Common", 12),
        ("Rice", "Unusual", 48),
        ("Corn", "Common", 10),
        ("Corn", "Unusual", 44),
        ("Soil", "Common", 8),
        ("Soil", "Unusual", 38),
    ],
    ("Hole Hornet", "Common"): [
        ("Missile", "Common", 38),
        ("Missile", "Unusual", 14),
        ("Wing", "Common", 32),
        ("Wing", "Unusual", 12),
        ("Stinger", "Common", 30),
        ("Stinger", "Unusual", 10),
    ],
    ("Hole Hornet", "Unusual"): [
        ("Missile", "Common", 12),
        ("Missile", "Unusual", 46),
        ("Wing", "Common", 10),
        ("Wing", "Unusual", 42),
        ("Stinger", "Common", 8),
        ("Stinger", "Unusual", 40),
    ],
    ("Hole Rock", "Common"): [
        ("Rock", "Common", 35),
        ("Rock", "Unusual", 14),
        ("Heavy", "Common", 28),
        ("Heavy", "Unusual", 10),
        ("Boubloom", "Common", 1.2),
        ("Boulder", "Common", 0.3),
    ],
    ("Hole Rock", "Unusual"): [
        ("Rock", "Common", 12),
        ("Rock", "Unusual", 45),
        ("Heavy", "Common", 10),
        ("Heavy", "Unusual", 45),
        ("Boubloom", "Common", 2.0),
        ("Boubloom", "Unusual", 0.4),
        ("Boulder", "Common", 1.5),
        ("Boulder", "Unusual", 0.2),
    ],
    ("Hole Spider", "Common"): [
        ("Web", "Common", 40),
        ("Web", "Unusual", 14),
        ("Faster", "Common", 35),
        ("Faster", "Unusual", 12),
    ],
    ("Hole Spider", "Unusual"): [
        ("Web", "Common", 12),
        ("Web", "Unusual", 46),
        ("Faster", "Common", 10),
        ("Faster", "Unusual", 42),
    ],
    ("Hole Bee", "Common"): [
        ("Stinger", "Common", 30),
        ("Stinger", "Unusual", 12),
        ("Pollen", "Common", 40),
        ("Pollen", "Unusual", 14),
        ("Honey", "Common", 35),
        ("Honey", "Unusual", 10),
    ],
    ("Hole Bee", "Unusual"): [
        ("Stinger", "Common", 10),
        ("Stinger", "Unusual", 45),
        ("Pollen", "Common", 10),
        ("Pollen", "Unusual", 45),
        ("Honey", "Common", 8),
        ("Honey", "Unusual", 40),
    ],
    ("Hole Ladybug", "Common"): [
        ("Light", "Common", 40),
        ("Light", "Unusual", 15),
        ("Rose", "Common", 35),
        ("Rose", "Unusual", 10),
    ],
    ("Hole Ladybug", "Unusual"): [
        ("Light", "Common", 10),
        ("Light", "Unusual", 45),
        ("Rose", "Common", 8),
        ("Rose", "Unusual", 42),
    ],
    ("Ladybug", "Common"): [
        ("Light", "Common", 37),
        ("Light", "Unusual", 10),
        ("Rose", "Common", 33),
        ("Rose", "Unusual", 5),
    ],
    ("Bee", "Common"): [
        ("Stinger", "Common", 22),
        ("Stinger", "Unusual", 5),
        ("Pollen", "Common", 37),
        ("Pollen", "Unusual", 10),
        ("Honey", "Common", 30),
        ("Honey", "Unusual", 5),
    ],
    ("Spider", "Common"): [
        ("Web", "Common", 35),
        ("Web", "Unusual", 7),
        ("Faster", "Common", 30),
        ("Faster", "Unusual", 7),
    ],
    ("Rock", "Common"): [
        ("Rock", "Common", 30),
        ("Rock", "Unusual", 9),
        ("Heavy", "Common", 19),
        ("Heavy", "Unusual", 4),
        ("Boubloom", "Common", 0.4),
        ("Boulder", "Common", 0.06),
    ],
    ("Hornet", "Common"): [
        ("Missile", "Common", 20),
        ("Missile", "Unusual", 9),
        ("Antenna", "Common", 21),
    ],
    ("Baby Ant", "Common"): [
        ("Leaf", "Common", 30),
        ("Leaf", "Unusual", 7),
        ("Rice", "Common", 25),
        ("Rice", "Unusual", 10),
        ("Light", "Common", 32),
        ("Light", "Unusual", 6),
        ("Cice", "Common", 0.05)
    ],
    ("Soldier Ant", "Common"): [
        ("Wing", "Common", 30),
        ("Wing", "Unusual", 10),
        ("Glass", "Common", 28),
        ("Glass", "Unusual", 7),
    ],
    ("Worker Ant", "Common"): [
        ("Corn", "Common", 34),
        ("Corn", "Unusual", 11),
        ("Clover", "Common", 30),
        ("Clover", "Unusual", 17),
    ],
    ("Hole Queen Ant", "Common"): [
        ("Ant Egg", "Common", 45),
        ("Ant Egg", "Unusual", 18),
        ("Soil", "Common", 40),
        ("Soil", "Unusual", 16),
        ("Heavy", "Common", 30),
        ("Heavy", "Unusual", 12),
    ],
    ("Hole Queen Ant", "Unusual"): [
        ("Ant Egg", "Common", 14),
        ("Ant Egg", "Unusual", 50),
        ("Soil", "Common", 12),
        ("Soil", "Unusual", 46),
        ("Heavy", "Common", 10),
        ("Heavy", "Unusual", 40),
    ],
    ("Queen Ant", "Common"): [
        ("Ant Egg", "Common", 34),
        ("Ant Egg", "Unusual", 9),
        ("Soil", "Common", 31),
        ("Soil", "Unusual", 11),
    ],
    ("Ant Egg", "Common"): [
        ("Ant Egg", "Common", 35),
        ("Ant Egg", "Unusual", 10),
        ("Soil", "Common", 25),
        ("Soil", "Unusual", 8),
    ],
    ("Ladybug", "Unusual"): [
        ("Light", "Common", 10),
        ("Light", "Unusual", 41),
        ("Rose", "Common", 8),
        ("Rose", "Unusual", 38),
    ],
    ("Bee", "Unusual"): [
        ("Stinger", "Common", 9),
        ("Stinger", "Unusual", 35),
        ("Pollen", "Common", 8),
        ("Pollen", "Unusual", 38),
        ("Honey", "Common", 6),
        ("Honey", "Unusual", 33),
    ],
    ("Spider", "Unusual"): [
        ("Web", "Common", 9),
        ("Web", "Unusual", 37),
        ("Faster", "Common", 7),
        ("Faster", "Unusual", 32),
    ],
    ("Rock", "Unusual"): [
        ("Rock", "Common", 9),
        ("Rock", "Unusual", 34),
        ("Heavy", "Common", 8),
        ("Heavy", "Unusual", 38),
        ("Boubloom", "Common", 1),
        ("Boubloom", "Unusual", 0.1),
        ("Boulder", "Common", 0.7),
        ("Boulder", "Unusual", 0.06),
    ],
}

gallery_enemy_icon_cache = {}

def draw_gallery_enemy_icon(surface, mob_name, center, rarity):

    enemy_classes = {
        "Ladybug": Ladybug,
        "Hole Ladybug": HoleLadybug,
        "Bee": Bee,
        "Hole Bee": HoleBee,
        "Spider": Spider,
        "Hole Spider": HoleSpider,
        "Rock": Rock,
        "Hole Rock": HoleRock,
        "Hornet": Hornet,
        "Hole Hornet": HoleHornet,
        "Baby Ant": BabyAnt,
        "Hole Baby Ant": HoleBabyAnt,
        "Soldier Ant": SoldierAnt,
        "Hole Soldier Ant": HoleSoldierAnt,
        "Worker Ant": WorkerAnt,
        "Hole Worker Ant": HoleWorkerAnt,
        "Queen Ant": QueenAnt,
        "Hole Queen Ant": HoleQueenAnt,
        "Ant Egg": AntEgg
    }
    enemy_class = enemy_classes.get(mob_name)
    if enemy_class is None:
        return

    global screen
    global camera_x
    global camera_y
    old_screen = screen
    old_camera_x = camera_x
    old_camera_y = camera_y
    try:
        screen = surface
        camera_x = 0
        camera_y = 0
        # Reuse one enemy per (mob, rarity): recreating it every frame
        # re-rolled random traits like size and ladybug spots.
        cache_key = (mob_name, rarity)
        enemy = gallery_enemy_icon_cache.get(cache_key)
        if enemy is None:
            enemy = enemy_class()
            enemy.rarity = rarity
            enemy.radius = GALLERY_ICON_RADIUS.get(mob_name, 10)
            enemy.hp = enemy.max_hp
            enemy.hide_rarity_label = True
            # Gallery portraits are static: freeze movement, facing, and limb
            # animation so they do not rotate between frames.
            for animation_attribute in (
                "angle",
                "base_angle",
                "target_angle",
                "turn_velocity",
                "time",
                "timer",
                "leg_phase",
                "wing_phase",
                "wing_jitter",
                "void_pulse",
                "mandible_snap"
            ):
                if hasattr(enemy, animation_attribute):
                    setattr(enemy, animation_attribute, 0)
            gallery_enemy_icon_cache[cache_key] = enemy
        enemy.x, enemy.y = center
        enemy.draw()
    finally:
        screen = old_screen
        camera_x = old_camera_x
        camera_y = old_camera_y

def get_inventory_max_rows():

    top_padding = 40
    bottom_padding = 20

    return (
        inventory_panel_rect.height
        - top_padding
        - bottom_padding
    ) // (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_GAP)

def build_inventory_display_rows():

    # Inventory is sorted highest rarity first.  Each rarity becomes its
    # own section with its own rows (a partial row is filled out so the
    # next rarity always starts on a fresh row), and a divider row is
    # placed between sections and above the top section.
    rows = []
    current_rarity = None
    current_items = []

    for item in inventory:

        item_rarity = item.get("rarity", "Common")

        if item_rarity != current_rarity:

            if current_rarity is not None:

                if current_items:
                    rows.append({
                        "type": "items",
                        "items": current_items
                    })
                    current_items = []

            rows.append({
                "type": "divider",
                "rarity": item_rarity
            })

            current_rarity = item_rarity

        current_items.append(item)

        if len(current_items) == INVENTORY_COLS:

            rows.append({
                "type": "items",
                "items": current_items
            })
            current_items = []

    if current_items:

        rows.append({
            "type": "items",
            "items": current_items
        })

    return rows

def get_inventory_total_rows():

    return len(build_inventory_display_rows())

def update_boss_hp():

    global boss_hp
    global boss_max_hp
    global boss_name
    global boss_rarity

    boss_hp = 0
    boss_max_hp = 0
    boss_name = ""
    boss_rarity = ""


    all_enemies = (
        ladybugs +
        hole_ladybugs +
        bees +
        spiders +
        rocks +
        hornets +
        baby_ants +
        soldier_ants +
        worker_ants +
        queen_ants +
        ant_eggs
    )


    for enemy in all_enemies:

        if enemy.alive:

            # check if player can see enemy
            d = distance(
                player_x,
                player_y,
                enemy.x,
                enemy.y
            )

            if d < 700:

                if enemy.rarity in ("Celestial", "Omnient"):

                    boss_hp = enemy.hp
                    boss_max_hp = enemy.max_hp
                    boss_name = type(enemy).__name__
                    boss_rarity = enemy.rarity

                    break

def enemy_attack(amount, petal_index=None):

    # If no specific petal was chosen,
    # damage the first alive petal

    if petal_index is None:

        for i in range(PETAL_SLOTS):

            if petal_alive[i]:

                petal_index = i
                break


    if petal_index is None:
        return


    if petal_alive[petal_index]:

        petal_hp[petal_index] -= amount

        if petal_hp[petal_index] <= 0:

            petal_hp[petal_index] = 0
            petal_alive[petal_index] = False
            if petal_slots[petal_index]["petal"] == "Rice":
                petal_respawn_timer[petal_index] = 3
            else:
                petal_respawn_timer[petal_index] = 300

def load_settings():

    global settings_switch_on, settings_switch2_on, settings_switch3_on
    global settings_hp_bar_scale, settings_hp_bar_knob_progress

    defaults = {
        "auto_squad": False,
        "equip_collected": False,
        "show_hitbox": False,
        "hp_bar_scale": 1.0,
    }

    try:
        with open("settings.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = defaults
    else:
        for key, default_val in defaults.items():
            data.setdefault(key, default_val)

    settings_switch_on = data["auto_squad"]
    settings_switch2_on = data["equip_collected"]
    settings_switch3_on = data["show_hitbox"]
    settings_hp_bar_scale = data["hp_bar_scale"]
    settings_hp_bar_knob_progress = (
        (settings_hp_bar_scale - 1) / 2
    )

def save_settings():

    data = {
        "auto_squad": settings_switch_on,
        "equip_collected": settings_switch2_on,
        "show_hitbox": settings_switch3_on,
        "hp_bar_scale": settings_hp_bar_scale,
    }

    with open("settings.json", "w") as file:
        json.dump(data, file, indent=4)

load_settings()

def sort_inventory():

    global inventory

    inventory.sort(
        key=lambda item: (
            RARITY_ORDER.index(
                item.get("rarity", "Common")
            )
            if item.get("rarity", "Common") in RARITY_ORDER
            else 999,

            item.get("petal", "Basic")
        )
    )

def add_inventory_petal(petal, rarity, amount=1):

    global inventory

    for item in inventory:

        if (
            item["petal"] == petal
            and
            item["rarity"] == rarity
        ):

            item["amount"] += amount
            sort_inventory()
            return

    inventory.append({
        "petal": petal,
        "rarity": rarity,
        "amount": amount
    })

    sort_inventory()

def remove_inventory_petal(petal, rarity, amount):

    global inventory

    remaining = amount
    for item in inventory[:]:
        if item["petal"] != petal or item["rarity"] != rarity:
            continue

        removed = min(int(item.get("amount", 1)), remaining)
        item["amount"] -= removed
        remaining -= removed

        if item["amount"] <= 0:
            inventory.remove(item)

        if remaining <= 0:
            break

def start_craft():

    global craft_animation_active
    global craft_animation_timer
    global craft_animation_duration
    global craft_will_succeed
    global craft_should_converge
    global craft_animation_outcome
    global craft_result_text
    global craft_animation_slot_amounts
    global craft_animation_grid_amount

    if (
        len(craft_selected_items) != 5
        or not all(item["amount"] > 0 for item in craft_selected_items)
        or craft_animation_active
    ):
        return False

    craft_animation_active = True
    craft_animation_duration = random.randint(
        max(1, int(FPS * 0.5)),
        max(1, int(FPS * 1.0))
    )
    craft_animation_timer = craft_animation_duration
    source_rarity = craft_selected_items[0]["rarity"]
    rarity_level = (
        RARITIES.index(source_rarity)
        if source_rarity in RARITIES
        else 0
    )
    success_percent = min(100, 256 / (2 ** rarity_level))
    craft_will_succeed = random.random() * 100 < success_percent
    craft_should_converge = craft_will_succeed
    craft_animation_outcome = (
        "success" if craft_will_succeed else "failure"
    )
    craft_result_text = ""
    craft_animation_slot_amounts = [
        item["amount"] for item in craft_selected_items
    ]
    selected_key = (
        craft_selected_items[0]["petal"],
        craft_selected_items[0]["rarity"]
    )
    craft_animation_grid_amount = sum(
        int(item.get("amount", 1))
        for item in inventory
        if (
            item.get("petal"),
            item.get("rarity")
        ) == selected_key
    ) - sum(craft_animation_slot_amounts)
    return True

def redistribute_empty_craft_slots():

    # When a slot reaches zero, move a random positive amount from another
    # slot into it. The transferred amount can never be zero.
    while True:
        total_amount = sum(
            item["amount"] for item in craft_selected_items
        )
        if total_amount < len(craft_selected_items):
            available_slots = list(range(len(craft_selected_items)))
            random.shuffle(available_slots)
            for item in craft_selected_items:
                item["amount"] = 0
            for slot_index in available_slots[:total_amount]:
                craft_selected_items[slot_index]["amount"] = 1
            return
        empty_indices = [
            index for index, item in enumerate(craft_selected_items)
            if item["amount"] <= 0
        ]
        if not empty_indices:
            return

        empty_index = random.choice(empty_indices)
        donor_indices = [
            index for index, item in enumerate(craft_selected_items)
            if index != empty_index and item["amount"] > 1
        ]
        if not donor_indices:
            donor_indices = [
                index for index, item in enumerate(craft_selected_items)
                if index != empty_index and item["amount"] > 0
            ]
        if not donor_indices:
            return

        donor_index = random.choice(donor_indices)
        donor_amount = craft_selected_items[donor_index]["amount"]
        maximum_transfer = donor_amount - 1 if donor_amount > 1 else 1
        transfer_amount = random.randint(1, maximum_transfer)
        craft_selected_items[donor_index]["amount"] -= transfer_amount
        craft_selected_items[empty_index]["amount"] = transfer_amount

def finish_craft(save_after=True):

    global craft_selected_items
    global craft_animation_active
    global craft_animation_timer
    global craft_animation_duration
    global craft_will_succeed
    global craft_result_text
    global craft_result_item
    global craft_animation_slot_amounts
    global craft_animation_grid_amount
    global craft_animation_outcome

    if not craft_selected_items:
        craft_animation_active = False
        return

    source_petal = craft_selected_items[0]["petal"]
    source_rarity = craft_selected_items[0]["rarity"]
    remove_inventory_petal(source_petal, source_rarity, 5)

    rarity_level = (
        RARITIES.index(source_rarity)
        if source_rarity in RARITIES
        else 0
    )
    success_percent = min(100, 256 / (2 ** rarity_level))
    returned_amount = 0

    batch_succeeds = craft_will_succeed
    craft_will_succeed = None
    if batch_succeeds is None:
        batch_succeeds = random.random() * 100 < success_percent
    if batch_succeeds:
        next_rarity_index = min(
            len(RARITIES) - 1,
            rarity_level + 1
        )
        add_inventory_petal(
            source_petal,
            RARITIES[next_rarity_index],
            1
        )
        result_rarity = RARITIES[next_rarity_index]
        if (
            craft_result_item
            and craft_result_item["petal"] == source_petal
            and craft_result_item["rarity"] == result_rarity
        ):
            craft_result_item["amount"] += 1
        else:
            craft_result_item = {
                "petal": source_petal,
                "rarity": result_rarity,
                "amount": 1
            }
        craft_result_text = "Success!"
    else:
        returned_amount = random.randint(1, 4)
        add_inventory_petal(
            source_petal,
            source_rarity,
            returned_amount
        )
        craft_result_text = f"Failed: +{returned_amount}"

    # Consume one petal from every slot for this batch. A failed batch
    # returns 1-4 petals to the visible slots.
    for item in craft_selected_items:
        item["amount"] -= 1

    if returned_amount > 0:
        for slot_index in range(returned_amount):
            craft_selected_items[slot_index]["amount"] += 1

    redistribute_empty_craft_slots()

    if all(item["amount"] > 0 for item in craft_selected_items):
        craft_animation_active = True
        craft_animation_timer = 1
    else:
        craft_selected_items = [
            item for item in craft_selected_items
            if item["amount"] > 0
        ]
        craft_animation_active = False
        craft_animation_timer = 0
        craft_animation_duration = 0
        craft_animation_slot_amounts = []
        craft_animation_grid_amount = None

    if save_after:
        save_player()

def distance(x1, y1, x2, y2):

    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

def move_with_collision(enemy, dx, dy):

    # ---------------- MOVE X ----------------

    enemy.x += dx

    enemy_rect = pygame.Rect(
        enemy.x - enemy.radius,
        enemy.y - enemy.radius,
        enemy.radius * 2,
        enemy.radius * 2
    )


    for wall in walls:

        if enemy_rect.colliderect(wall.rect):

            enemy.x -= dx
            break



    # ---------------- MOVE Y ----------------

    enemy.y += dy

    enemy_rect = pygame.Rect(
        enemy.x - enemy.radius,
        enemy.y - enemy.radius,
        enemy.radius * 2,
        enemy.radius * 2
    )


    for wall in walls:

        if enemy_rect.colliderect(wall.rect):

            enemy.y -= dy
            break

    # Keep enemy inside map boundaries
    rad = getattr(enemy, "radius", 0)
    enemy.x = max(rad, min(enemy.x, WORLD_WIDTH - rad))
    enemy.y = max(rad, min(enemy.y, WORLD_HEIGHT - rad))

def dead_flower_ai(enemy):

    global player_bounce_x
    global player_bounce_y
    global player_rot_vel

    # When the player is dead the enemies see the dead flower and
    # randomly decide to keep walking or to play with it like a bouncy
    # ball. While playing, the enemy steers toward the flower and, on
    # touching it, bounces the flower in the direction the enemy is
    # facing. Returns True while the enemy is playing (its normal
    # behavior should be skipped).

    # baby ants, ant eggs, and rocks do not play with the dead flower
    if enemy.__class__.__name__ in ("BabyAnt", "AntEgg", "Rock") or not hasattr(enemy, "angle"):
        return False

    if not hasattr(enemy, "play_mode"):
        enemy.play_mode = None
    if not hasattr(enemy, "play_decision_timer"):
        enemy.play_decision_timer = 0
    if not hasattr(enemy, "play_chase"):
        enemy.play_chase = 0

    if not player_dead:
        enemy.play_mode = None
        enemy.play_decision_timer = 0
        enemy.play_chase = 0
        return False

    view = getattr(enemy, "view_range", 250)

    # cap how far a mob will chase the flower so it only commits to playing
    # when close enough to actually connect a push (avoids mobs starting to
    # "play" from across the map and never reaching the flower)
    play_range = min(view, 220)

    d = math.hypot(
        player_x - enemy.x,
        player_y - enemy.y
    )

    # the enemy must be close enough to see/play with the dead flower
    if d > play_range:
        enemy.play_mode = None
        return False

    enemy.play_decision_timer -= 1

    if enemy.play_mode == "play":

        # give up if the mob has chased too long without connecting a push
        # (e.g. it is blocked by a wall), so it goes back to normal walking
        # instead of standing at the wall uselessly
        enemy.play_chase -= 1

        if enemy.play_chase <= 0:
            enemy.play_mode = "walk"
            enemy.play_decision_timer = 0
            return False

        target_angle = math.degrees(
            math.atan2(
                player_y - enemy.y,
                player_x - enemy.x
            )
        )

        # keep the enemy animated while it plays with the flower
        if hasattr(enemy, "leg_phase"):
            enemy.leg_phase += 0.48
        if hasattr(enemy, "wing_phase"):
            enemy.wing_phase += 0.85

        speed = max(float(getattr(enemy, "speed", 0) or 0), 4.5)

        enemy.turn_to(target_angle, 8)

        # touching the dead flower gives it one push, then the mob wanders off
        # naturally. there's no recoil/bounce-back so the mob never looks like
        # it's being pushed around by the flower.
        if d < PLAYER_RADIUS + enemy.radius:

            bx = math.cos(math.radians(enemy.angle))
            by = math.sin(math.radians(enemy.angle))

            bounce_speed = speed * 1.4 + 4

            player_bounce_x = bx * bounce_speed
            player_bounce_y = by * bounce_speed

            # spin the flower, ending via acceleration (friction) below
            player_rot_vel = 12

            # wander off and re-decide later, so it doesn't keep shoving
            enemy.play_mode = "walk"
            enemy.play_decision_timer = 30

        else:

            move_with_collision(
                enemy,
                math.cos(math.radians(enemy.angle)) * speed,
                math.sin(math.radians(enemy.angle)) * speed
            )

        return True

    # undecided or walking: roll to decide whether to play
    if enemy.play_decision_timer <= 0:

        enemy.play_decision_timer = 90 + random.randint(0, 90)

        if random.random() < 0.5:
            enemy.play_mode = "play"
            enemy.play_chase = 400
        else:
            enemy.play_mode = "walk"

    return False

def move_enemy(enemy, dx, dy):

    # move X first
    enemy.x += dx

    enemy_rect = pygame.Rect(
        enemy.x - enemy.radius,
        enemy.y - enemy.radius,
        enemy.radius * 2,
        enemy.radius * 2
    )

    for wall in walls:

        if enemy_rect.colliderect(wall.rect):

            enemy.x -= dx
            break


    # move Y second
    enemy.y += dy

    enemy_rect = pygame.Rect(
        enemy.x - enemy.radius,
        enemy.y - enemy.radius,
        enemy.radius * 2,
        enemy.radius * 2
    )

    for wall in walls:

        if enemy_rect.colliderect(wall.rect):

            enemy.y -= dy
            break
def get_multiply_position(x, y, count, index):

    if count == 1:
        return x, y, 1.0

    angle = (
        petal_angle
        + index * (360 / count)
    )

    angle_rad = math.radians(angle)

    distance = PETAL_RADIUS * 0.55

    new_x = (
        x
        + math.cos(angle_rad) * distance
    )

    new_y = (
        y
        + math.sin(angle_rad) * distance
    )

    # Smaller petals when there are more copies
    if count <= 3:
        scale = 0.87
    elif count <= 5:
        scale = 0.76
    elif count <= 7:
        scale = 0.67
    else:
        scale = 0.60

    return new_x, new_y, scale

def draw_petal(name, x, y, rarity, size_scale=1.0, flash_timer=0):

    global PETAL_RADIUS
    original_petal_radius = PETAL_RADIUS
    PETAL_RADIUS *= size_scale

    # ---------------- MOON SPOTS ----------------

    # Moon spots are only needed by Moon petals. Avoid creating random
    # dictionaries on every draw for every other petal type.
    moon_spots = []
    if name == "Moon":
        for i in range(3):
            moon_spots.append({
                "x": random.uniform(-PETAL_RADIUS * 0.8, PETAL_RADIUS * 0.8),
                "y": random.uniform(-PETAL_RADIUS * 0.8, PETAL_RADIUS * 0.8),
                "radius": random.uniform(
                    PETAL_RADIUS * 0.15,
                    PETAL_RADIUS * 0.35
                )
            })

    if name == "Basic":

        # inside
        pygame.draw.circle(
            screen,
            (255,255,255),
            (int(x), int(y)),
            PETAL_RADIUS-2
        )

        # outline
        pygame.draw.circle(
            screen,
            (230,230,230),
            (int(x), int(y)),
            PETAL_RADIUS-2,
            2
        )


    elif name == "Stinger":

        count = get_petal_count(
            name,
            rarity
        )

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            r = PETAL_RADIUS * scale

            # ---------------- BLACK TRIANGLE ----------------

            points = [
                (draw_x, draw_y - r),
                (draw_x - r * 0.75, draw_y + r * 0.65),
                (draw_x + r * 0.75, draw_y + r * 0.65)
            ]

            # outline slightly larger than the fill
            outline_points = [
                (draw_x, draw_y - r - 2),
                (draw_x - r * 0.75 - 2, draw_y + r * 0.65 + 2),
                (draw_x + r * 0.75 + 2, draw_y + r * 0.65 + 2)
            ]

            pygame.draw.polygon(
                screen,
                (120, 120, 120),
                outline_points
            )

            pygame.draw.polygon(
                screen,
                (0, 0, 0),
                points
            )

    elif name == "Light":

        # Single light dot (used for orbitting lights in game)
        r = PETAL_RADIUS * 0.55

        light_color = (255, 255, 255)
        light_outline = (190, 190, 190)

        pygame.draw.circle(
            screen,
            light_outline,
            (int(x), int(y)),
            int(r + 2)
        )

        pygame.draw.circle(
            screen,
            light_color,
            (int(x), int(y)),
            int(r)
        )

    elif name == "Heavy":

        r = PETAL_RADIUS

        # ---------------- MAIN BOWLING BALL ----------------

        pygame.draw.circle(
            screen,
            (55, 55, 55),
            (int(x), int(y)),
            int(r + 2)
        )

        pygame.draw.circle(
            screen,
            (90, 90, 90),
            (int(x), int(y)),
            int(r)
        )

        # ---------------- THREE HOLES ----------------

        hole_color = (45, 45, 45)

        hole_radius = int(r * 0.2)

        pygame.draw.circle(
            screen,
            hole_color,
            (
                int(x + r * 0.18),
                int(y - r * 0.28)
            ),
            hole_radius
        )

        pygame.draw.circle(
            screen,
            hole_color,
            (
                int(x + r * 0.42),
                int(y - r * 0.18)
            ),
            hole_radius
        )

        pygame.draw.circle(
            screen,
            hole_color,
            (
                int(x + r * 0.28),
                int(y + r * 0.08)
            ),
            hole_radius
        )

    elif name == "Rice":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            draw_x, draw_y, scale = get_multiply_position(
                x,
                y,
                count,
                multiply_i
            )

            width = PETAL_RADIUS * 0.45 * scale
            height = PETAL_RADIUS * 0.90 * scale

            pygame.draw.ellipse(
                screen,
                (170, 170, 170),
                (
                    int(draw_x - width - 2 * scale),
                    int(draw_y - height - 2 * scale),
                    int(width * 2 + 4 * scale),
                    int(height * 2 + 4 * scale)
                )
            )

            pygame.draw.ellipse(
                screen,
                (255, 255, 255),
                (
                    int(draw_x - width),
                    int(draw_y - height),
                    int(width * 2),
                    int(height * 2)
                )
            )

    elif name == "Rose":

        pygame.draw.circle(
            screen,
            (255,80,120),
            (int(x), int(y)),
            PETAL_RADIUS
        )

        pygame.draw.circle(
            screen,
            (255,150,170),
            (int(x), int(y)),
            PETAL_RADIUS // 2
        )

        pygame.draw.circle(
            screen,
            (220,60,100),
            (int(x), int(y)),
            PETAL_RADIUS,
            2
        )

    elif name == "Wing":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            r = PETAL_RADIUS * scale

            # ---------------- WING SHAPE ----------------

            points = []

            start_x = draw_x - r * 0.9
            start_y = draw_y + r * 0.5

            end_x = draw_x + r * 0.7
            end_y = draw_y - r * 1.0

            control_x = draw_x + r * 0.9
            control_y = draw_y + r * 1.0

            # Outer curve
            for j in range(31):

                t = j / 30

                px = (
                    (1 - t) ** 2 * start_x
                    + 2 * (1 - t) * t * control_x
                    + t ** 2 * end_x
                )

                py = (
                    (1 - t) ** 2 * start_y
                    + 2 * (1 - t) * t * control_y
                    + t ** 2 * end_y
                )

                points.append((px, py))

            # Inner curve
            control_x = draw_x - r * 0.1
            control_y = draw_y + r * 0.1

            for j in range(30, -1, -1):

                t = j / 30

                px = (
                    (1 - t) ** 2 * start_x
                    + 2 * (1 - t) * t * control_x
                    + t ** 2 * end_x
                )

                py = (
                    (1 - t) ** 2 * start_y
                    + 2 * (1 - t) * t * control_y
                    + t ** 2 * end_y
                )

                points.append((px, py))

            # ---------------- WHITE WING ----------------

            pygame.draw.polygon(
                screen,
                (255, 255, 255),
                points
            )

            # ---------------- GRAY OUTLINE ----------------

            pygame.draw.lines(
                screen,
                (150, 150, 150),
                True,
                points,
                2
            )

    elif name == "Cactus":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x +
                    math.cos(angle_rad) * distance
                )

                draw_y = (
                    y +
                    math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            # ---------------- CACTUS ----------------

            points = []

            num_sides = 8

            radius = PETAL_RADIUS * 0.85 * scale

            spike_length = PETAL_RADIUS * 0.28 * scale

            # ---------------- CURVED SIDES + SPIKES ----------------

            for i in range(num_sides):

                angle = (
                    -math.pi / 8
                    + i * (2 * math.pi / num_sides)
                )

                next_angle = (
                    angle +
                    2 * math.pi / num_sides
                )

                start_x = (
                    draw_x +
                    math.cos(angle) * radius
                )

                start_y = (
                    draw_y +
                    math.sin(angle) * radius
                )

                end_x = (
                    draw_x +
                    math.cos(next_angle) * radius
                )

                end_y = (
                    draw_y +
                    math.sin(next_angle) * radius
                )

                mid_angle = (
                    angle +
                    math.pi / num_sides
                )

                curve_radius = radius * 0.88

                curve_x = (
                    draw_x +
                    math.cos(mid_angle) * curve_radius
                )

                curve_y = (
                    draw_y +
                    math.sin(mid_angle) * curve_radius
                )

                # Curved side
                for j in range(8):

                    t = j / 8

                    px = (
                        (1 - t) ** 2 * start_x
                        + 2 * (1 - t) * t * curve_x
                        + t ** 2 * end_x
                    )

                    py = (
                        (1 - t) ** 2 * start_y
                        + 2 * (1 - t) * t * curve_y
                        + t ** 2 * end_y
                    )

                    points.append((px, py))

                # Spike
                spike_x = (
                    draw_x +
                    math.cos(next_angle) *
                    (radius + spike_length)
                )

                spike_y = (
                    draw_y +
                    math.sin(next_angle) *
                    (radius + spike_length)
                )

                points.append(
                    (spike_x, spike_y)
                )

            # ---------------- DARK GREEN OUTLINE ----------------

            pygame.draw.polygon(
                screen,
                (35, 100, 35),
                points
            )

            # ---------------- GREEN BODY ----------------

            inner_points = []

            for px, py in points:

                dx = px - draw_x
                dy = py - draw_y

                inner_points.append(
                    (
                        draw_x + dx * 0.88,
                        draw_y + dy * 0.88
                    )
                )

            pygame.draw.polygon(
                screen,
                (80, 170, 70),
                inner_points
            )

            # ---------------- LIGHT GREEN CENTER ----------------

            pygame.draw.circle(
                screen,
                (145, 220, 105),
                (int(draw_x), int(draw_y)),
                int(PETAL_RADIUS * 0.32 * scale)
            )

    elif name == "Leaf":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            r = PETAL_RADIUS * scale

            # ---------------- SIMPLE DOODLE LEAF ----------------

            points = []

            # Top half
            for j in range(21):

                t = j / 20

                px = (
                    draw_x
                    - r
                    + t * r * 2
                )

                py = (
                    draw_y
                    - math.sin(t * math.pi) * r * 0.75
                )

                points.append((px, py))

            # Bottom half
            for j in range(20, -1, -1):

                t = j / 20

                px = (
                    draw_x
                    - r
                    + t * r * 2
                )

                py = (
                    draw_y
                    + math.sin(t * math.pi) * r * 0.75
                )

                points.append((px, py))

            # ---------------- GREEN LEAF ----------------

            pygame.draw.polygon(
                screen,
                (100, 190, 80),
                points
            )

            # ---------------- DARK OUTLINE ----------------

            pygame.draw.lines(
                screen,
                (45, 110, 45),
                True,
                points,
                2
            )

            # ---------------- SIMPLE CENTER LINE ----------------

            pygame.draw.line(
                screen,
                (45, 110, 45),
                (
                    int(draw_x - r * 0.8),
                    int(draw_y)
                ),
                (
                    int(draw_x + r * 0.8),
                    int(draw_y)
                ),
                2
            )
    elif name == "Pea":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count <= 3:
                    scale = 0.75

                elif count <= 5:
                    scale = 0.65

                else:
                    scale = 0.55

            r = (PETAL_RADIUS - 2) * scale

            # Green Pea
            pygame.draw.circle(
                screen,
                (80, 255, 80),
                (int(draw_x), int(draw_y)),
                int(r)
            )

            # Dark green outline
            pygame.draw.circle(
                screen,
                (40, 180, 40),
                (int(draw_x), int(draw_y)),
                int(r),
                2
            )

    elif name == "Missile":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            r = PETAL_RADIUS * scale

            points = []

            # ---------------- SMOOTH TOP ----------------

            tip_x = draw_x
            tip_y = draw_y - r * 1.15

            left_x = draw_x - r * 0.55
            left_y = draw_y + r * 0.80

            right_x = draw_x + r * 0.55
            right_y = draw_y + r * 0.80

            # Left side
            for j in range(16):

                t = j / 15

                px = (
                    (1 - t) ** 2 * tip_x
                    + 2 * (1 - t) * t * (draw_x - r * 0.35)
                    + t ** 2 * left_x
                )

                py = (
                    (1 - t) ** 2 * tip_y
                    + 2 * (1 - t) * t * (draw_y - r * 0.35)
                    + t ** 2 * left_y
                )

                points.append((px, py))

            # Bottom
            for j in range(1, 16):

                t = j / 15

                px = (
                    left_x * (1 - t)
                    + right_x * t
                )

                py = (
                    left_y * (1 - t)
                    + right_y * t
                    + math.sin(t * math.pi) * r * 0.08
                )

                points.append((px, py))

            # Right side
            for j in range(1, 16):

                t = j / 15

                px = (
                    (1 - t) ** 2 * right_x
                    + 2 * (1 - t) * t * (draw_x + r * 0.35)
                    + t ** 2 * tip_x
                )

                py = (
                    (1 - t) ** 2 * right_y
                    + 2 * (1 - t) * t * (draw_y - r * 0.35)
                    + t ** 2 * tip_y
                )

                points.append((px, py))

            # ---------------- MISSILE ----------------

            pygame.draw.polygon(
                screen,
                (0, 0, 0),
                points
            )

    elif name == "Bone":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            r = PETAL_RADIUS * scale

            bone_color = (245, 245, 225)
            outline_color = (150, 150, 135)

            # ---------------- BONE SHAFT ----------------

            pygame.draw.line(
                screen,
                outline_color,
                (
                    int(draw_x - r * 0.75),
                    int(draw_y)
                ),
                (
                    int(draw_x + r * 0.75),
                    int(draw_y)
                ),
                max(1, int(r * 0.38))
            )

            pygame.draw.line(
                screen,
                bone_color,
                (
                    int(draw_x - r * 0.75),
                    int(draw_y)
                ),
                (
                    int(draw_x + r * 0.75),
                    int(draw_y)
                ),
                max(1, int(r * 0.28))
            )

            # ---------------- LEFT END ----------------

            pygame.draw.circle(
                screen,
                outline_color,
                (
                    int(draw_x - r * 0.78),
                    int(draw_y - r * 0.15)
                ),
                max(1, int(r * 0.32))
            )

            pygame.draw.circle(
                screen,
                outline_color,
                (
                    int(draw_x - r * 0.78),
                    int(draw_y + r * 0.15)
                ),
                max(1, int(r * 0.32))
            )

            pygame.draw.circle(
                screen,
                bone_color,
                (
                    int(draw_x - r * 0.78),
                    int(draw_y - r * 0.15)
                ),
                max(1, int(r * 0.24))
            )

            pygame.draw.circle(
                screen,
                bone_color,
                (
                    int(draw_x - r * 0.78),
                    int(draw_y + r * 0.15)
                ),
                max(1, int(r * 0.24))
            )

            # ---------------- RIGHT END ----------------

            pygame.draw.circle(
                screen,
                outline_color,
                (
                    int(draw_x + r * 0.78),
                    int(draw_y - r * 0.15)
                ),
                max(1, int(r * 0.32))
            )

            pygame.draw.circle(
                screen,
                outline_color,
                (
                    int(draw_x + r * 0.78),
                    int(draw_y + r * 0.15)
                ),
                max(1, int(r * 0.32))
            )

            pygame.draw.circle(
                screen,
                bone_color,
                (
                    int(draw_x + r * 0.78),
                    int(draw_y - r * 0.15)
                ),
                max(1, int(r * 0.24))
            )

        pygame.draw.circle(
            screen,
            bone_color,
            (
                int(draw_x + r * 0.78),
                int(draw_y + r * 0.15)
            ),
            max(1, int(r * 0.24))
        )

    elif name == "Web":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle_offset = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle_offset)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            r = PETAL_RADIUS * scale

            points = []

            # ---------------- WEB OUTLINE ----------------

            for j in range(61):

                angle = (
                    math.radians(j * 360 / 60)
                    - math.pi / 2
                )

                wave = (
                    math.cos(angle * 5) + 1
                ) / 2

                radius = (
                    r * 0.75
                    + wave * r * 0.5
                )

                px = (
                    draw_x
                    + math.cos(angle) * radius
                )

                py = (
                    draw_y
                    + math.sin(angle) * radius
                )

                points.append(
                    (px, py)
                )

            pygame.draw.polygon(
                screen,
                (150, 150, 150),
                points
            )

            # ---------------- WHITE INSIDE ----------------

            inner_points = []

            for j in range(61):

                angle = (
                    math.radians(j * 360 / 60)
                    - math.pi / 2
                )

                wave = (
                    math.cos(angle * 5) + 1
                ) / 2

                radius = (
                    r * 0.68
                    + wave * r * 0.43
                )

                px = (
                    draw_x
                    + math.cos(angle) * radius
                )

                py = (
                    draw_y
                    + math.sin(angle) * radius
                )

                inner_points.append(
                    (px, py)
                )

            pygame.draw.polygon(
                screen,
                (255, 255, 255),
                inner_points
            )

    elif name == "Rock":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            draw_x, draw_y, scale = get_multiply_position(
                x,
                y,
                count,
                multiply_i
            )

            r = PETAL_RADIUS * scale

            outline = (70, 70, 70)
            inside = (150, 150, 150)

            points = [
                (draw_x, draw_y - r),
                (draw_x + r * 0.95, draw_y - r * 0.30),
                (draw_x + r * 0.58, draw_y + r * 0.80),
                (draw_x - r * 0.58, draw_y + r * 0.80),
                (draw_x - r * 0.95, draw_y - r * 0.30)
            ]

            pygame.draw.polygon(
                screen,
                outline,
                points
            )

            inner_points = [
                (draw_x, draw_y - r * 0.82),
                (draw_x + r * 0.78, draw_y - r * 0.24),
                (draw_x + r * 0.48, draw_y + r * 0.65),
                (draw_x - r * 0.48, draw_y + r * 0.65),
                (draw_x - r * 0.78, draw_y - r * 0.24)
            ]

            pygame.draw.polygon(
                screen,
                inside,
                inner_points
            )

    elif name == "Faster":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            draw_x, draw_y, scale = get_multiply_position(
                x,
                y,
                count,
                multiply_i
            )

            # Small yellow circle
            r = PETAL_RADIUS * scale * 0.55

            pygame.draw.circle(
                screen,
                (200, 180, 40),
                (int(draw_x), int(draw_y)),
                int(r + 2)
            )

            pygame.draw.circle(
                screen,
                (255, 240, 100),
                (int(draw_x), int(draw_y)),
                int(r)
            )

    elif name == "Magnet":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            r = PETAL_RADIUS * scale

            # ---------------- MAGNET ----------------

            pygame.draw.arc(
                screen,
                (255, 0, 0),
                (
                    int(draw_x - r),
                    int(draw_y - r),
                    int(r * 2),
                    int(r * 2)
                ),
                math.radians(40),
                math.radians(320),
                max(1, int(5 * scale))
            )

            # Red end

            # Dark red outline
            pygame.draw.arc(
                screen,
                (150, 0, 0),
                (
                    int(draw_x - r),
                    int(draw_y - r),
                    int(r * 2),
                    int(r * 2)
                ),
                math.radians(40),
                math.radians(320),
                max(1, int(2 * scale))
            )

    elif name == "Bubble":

        # render the bubble onto an offscreen alpha surface so it can be 50%
        # transparent, then blend it onto the screen
        bubble_size = int(PETAL_RADIUS * 2) + 8
        bubble_surf = pygame.Surface(
            (bubble_size, bubble_size),
            pygame.SRCALPHA
        )
        bx = bubble_size // 2
        by = bubble_size // 2
        bubble_alpha = 128

        pygame.draw.circle(
            bubble_surf,
            (100, 220, 255, bubble_alpha),
            (bx, by),
            PETAL_RADIUS
        )

        pygame.draw.circle(
            bubble_surf,
            (220, 255, 255, min(255, bubble_alpha + 60)),
            (bx - 4, by - 5),
            4
        )

        pygame.draw.circle(
            bubble_surf,
            (50, 150, 220, min(255, bubble_alpha + 40)),
            (bx, by),
            PETAL_RADIUS,
            2
        )

        screen.blit(
            bubble_surf,
            (int(x - bx), int(y - by))
        )

    elif name == "Honey":

        # ---------------- 6 EQUAL SIDES ----------------

        points = []

        num_sides = 6

        radius = PETAL_RADIUS * 1.2

        start_angle = math.radians(-30)


        for i in range(num_sides):

            angle = (
                start_angle
                + i * (2 * math.pi / num_sides)
            )

            px = (
                x +
                math.cos(angle) * radius
            )

            py = (
                y +
                math.sin(angle) * radius
            )

            points.append(
                (px, py)
            )


        # ---------------- POLLEN ----------------

        pygame.draw.polygon(
            screen,
            (255, 210, 40),
            points
        )


        # ---------------- DARK YELLOW OUTLINE ----------------

        pygame.draw.polygon(
            screen,
            (180, 130, 0),
            points,
            2
        )

    elif name == "Poison":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            r = PETAL_RADIUS * scale * 0.5

            # ---------------- DARK PURPLE OUTLINE ----------------

            pygame.draw.circle(
                screen,
                (70, 30, 90),
                (int(draw_x), int(draw_y)),
                int(r + 2)
            )

            # ---------------- PURPLE BODY ----------------

            pygame.draw.circle(
                screen,
                (170, 70, 210),
                (int(draw_x), int(draw_y)),
                int(r)
            )

    elif name == "Shark":

        # ---------------- SHARK BODY ----------------

        r = PETAL_RADIUS

        points = []

        # Top: tail -> dorsal fin
        for i in range(21):

            t = i / 20

            x_pos = (
                x - r * 0.9
                + (r * 2.1) * t
            )

            y_pos = (
                y - math.sin(t * math.pi) * r * 0.75
            )

            points.append(
                (x_pos, y_pos)
            )


        # Top: dorsal fin -> nose
        for i in range(1, 21):

            t = i / 20

            x_pos = (
                x + r * 1.2
                - (r * 1.2) * t
            )

            y_pos = (
                y - r * 0.75
                + math.sin(t * math.pi * 0.8)
                * r * 0.25
            )

            points.append(
                (x_pos, y_pos)
            )


        # Bottom: nose -> tail
        for i in range(1, 21):

            t = i / 20

            x_pos = (
                x + r * 1.2
                - (r * 2.1) * t
            )

            y_pos = (
                y + math.sin(t * math.pi) * r * 0.55
            )

            points.append(
                (x_pos, y_pos)
            )


        # ---------------- BODY ----------------

        pygame.draw.polygon(
            screen,
            (90, 105, 120),
            points
        )

        pygame.draw.polygon(
            screen,
            (40, 50, 65),
            points,
            2
        )


        # ---------------- TOP FIN ----------------

        dorsal = [
            (
                x - r * 0.1,
                y - r * 0.6
            ),

            (
                x + r * 0.15,
                y - r * 1.25
            ),

            (
                x + r * 0.45,
                y - r * 0.55
            )
        ]

        pygame.draw.polygon(
            screen,
            (90, 105, 120),
            dorsal
        )

        pygame.draw.polygon(
            screen,
            (40, 50, 65),
            dorsal,
            2
        )


        # ---------------- TAIL ----------------

        tail = [
            (
                x - r * 0.9,
                y
            ),

            (
                x - r * 1.35,
                y - r * 0.45
            ),

            (
                x - r * 1.35,
                y + r * 0.45
            )
        ]

        pygame.draw.polygon(
            screen,
            (90, 105, 120),
            tail
        )

        pygame.draw.polygon(
            screen,
            (40, 50, 65),
            tail,
            2
        )


        # ---------------- MOUTH ----------------

        mouth_top = (
            x + r * 0.75,
            y - r * 0.15
        )

        mouth_bottom = (
            x + r * 0.75,
            y + r * 0.15
        )

        nose = (
            x + r * 1.2,
            y
        )

        pygame.draw.polygon(
            screen,
            (230, 230, 240),
            [
                mouth_top,
                mouth_bottom,
                nose
            ]
        )


        # ---------------- TEETH ----------------

        teeth = [
            (
                x + r * 0.72,
                y - r * 0.10
            ),

            (
                x + r * 0.92,
                y
            ),

            (
                x + r * 0.72,
                y + r * 0.10
            )
        ]

        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            teeth
        )


        # ---------------- EYE ----------------

        eye_x = x + r * 0.15
        eye_y = y - r * 0.20

        pygame.draw.circle(
            screen,
            (20, 20, 20),
            (
                int(eye_x),
                int(eye_y)
            ),
            int(r * 0.18)
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                int(eye_x + r * 0.05),
                int(eye_y - r * 0.05)
            ),
            int(r * 0.07)
        )


        # ---------------- GILLS ----------------

        for i in range(3):

            start_x = (
                x - r * 0.15
                - i * r * 0.22
            )

            pygame.draw.arc(
                screen,
                (40, 50, 65),
                (
                    start_x - r * 0.05,
                    y - r * 0.35,
                    r * 0.25,
                    r * 0.70
                ),
                -0.6,
                0.6,
                2
            )

    elif name == "Corn":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            draw_x, draw_y, scale = get_multiply_position(
                x,
                y,
                count,
                multiply_i
            )

            r = PETAL_RADIUS * scale

            points = []

            # ---------------- ONE CORN KERNEL ----------------

            for i in range(31):

                t = i / 30

                px = (
                    draw_x
                    - r * 0.45
                    + t * r * 0.9
                )

                py = (
                    draw_y
                    - r * 0.65
                    + math.sin(t * math.pi) * r * 0.25
                )

                points.append(
                    (px, py)
                )

            for i in range(30, -1, -1):

                t = i / 30

                px = (
                    draw_x
                    - r * 0.45
                    + t * r * 0.9
                )

                py = (
                    draw_y
                    + r * 0.65
                    - math.sin(t * math.pi) * r * 0.25
                )

                points.append(
                    (px, py)
                )

            # ---------------- DARK YELLOW OUTLINE ----------------

            pygame.draw.polygon(
                screen,
                (190, 140, 20),
                points
            )

            # ---------------- YELLOW CORN ----------------

            inner_points = []

            for px, py in points:

                inner_points.append(
                    (
                        draw_x + (px - draw_x) * 0.88,
                        draw_y + (py - draw_y) * 0.88
                    )
                )

            pygame.draw.polygon(
                screen,
                (255, 220, 50),
                inner_points
            )

    elif name == "Stick":

        brown = (120, 70, 20)

        # Main stick
        pygame.draw.line(
            screen,
            brown,
            (
                x - PETAL_RADIUS,
                y
            ),
            (
                x + PETAL_RADIUS - 3,
                y
            ),
            7
        )

        # Smaller < shape
        tip_x = x + PETAL_RADIUS - 3

        pygame.draw.line(
            screen,
            brown,
            (
                tip_x,
                y
            ),
            (
                tip_x + 6,
                y - 7
            ),
            5
        )

        pygame.draw.line(
            screen,
            brown,
            (
                tip_x,
                y
            ),
            (
                tip_x + 6,
                y + 7
            ),
            5
        )

    elif name == "Clover":

        for angle in [45,135,225,315]:

            rad = math.radians(angle)

            cx = x + math.cos(rad) * PETAL_RADIUS * 0.55
            cy = y + math.sin(rad) * PETAL_RADIUS * 0.55

            pygame.draw.circle(
                screen,
                (80,220,80),
                (
                    int(cx),
                    int(cy)
                ),
                PETAL_RADIUS * 0.6
            )

        pygame.draw.circle(
            screen,
            (50,180,50),
            (
                int(x),
                int(y)
            ),
            3
        )

    elif name == "Glass":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                scale = 0.60

            r = PETAL_RADIUS * scale

            # ---------------- PERFECT HEXAGON ----------------

            points = []

            for j in range(6):

                angle = (
                    -math.pi / 2
                    + j * (2 * math.pi / 6)
                )

                px = (
                    draw_x
                    + math.cos(angle) * r
                )

                py = (
                    draw_y
                    + math.sin(angle) * r
                )

                points.append((px, py))

            # ---------------- TRANSPARENT GLASS ----------------

            glass_surface = pygame.Surface(
                (WIDTH, HEIGHT),
                pygame.SRCALPHA
            )

            pygame.draw.polygon(
                glass_surface,
                (180, 230, 255, 70),
                points
            )

            screen.blit(
                glass_surface,
                (0, 0)
            )

            # ---------------- GLASS OUTLINE ----------------

            pygame.draw.polygon(
                screen,
                (130, 190, 220),
                points,
                2
            )

    elif name == "Antenna":

        # ---------------- LEFT ANTENNA ----------------

        points_left = []

        for i in range(31):

            t = i / 30

            px = (
                x - PETAL_RADIUS * 0.25
                - t * PETAL_RADIUS * 0.65
            )

            py = (
                y + PETAL_RADIUS * 0.25
                - t * PETAL_RADIUS * 1.5
                + math.sin(t * math.pi)
                * PETAL_RADIUS * 0.25
            )

            points_left.append(
                (px, py)
            )


        # ---------------- RIGHT ANTENNA ----------------

        points_right = []

        for i in range(31):

            t = i / 30

            px = (
                x + PETAL_RADIUS * 0.25
                + t * PETAL_RADIUS * 0.65
            )

            py = (
                y + PETAL_RADIUS * 0.25
                - t * PETAL_RADIUS * 1.5
                + math.sin(t * math.pi)
                * PETAL_RADIUS * 0.25
            )

            points_right.append(
                (px, py)
            )


        # ---------------- DRAW ----------------

        pygame.draw.lines(
            screen,
            (80, 80, 80),
            False,
            points_left,
            3
        )

        pygame.draw.lines(
            screen,
            (80, 80, 80),
            False,
            points_right,
            3
        )

    elif name == "Pollen":

        pollen_radius = PETAL_RADIUS * 0.55

        # ---------------- LEFT POLLEN ----------------

        pygame.draw.circle(
            screen,
            (180, 130, 0),
            (
                int(x - PETAL_RADIUS * 0.45),
                int(y)
            ),
            int(pollen_radius + 2)
        )

        pygame.draw.circle(
            screen,
            (255, 220, 40),
            (
                int(x - PETAL_RADIUS * 0.45),
                int(y)
            ),
            int(pollen_radius)
        )


        # ---------------- RIGHT POLLEN ----------------

        pygame.draw.circle(
            screen,
            (180, 130, 0),
            (
                int(x + PETAL_RADIUS * 0.45),
                int(y)
            ),
            int(pollen_radius + 2)
        )

        pygame.draw.circle(
            screen,
            (255, 220, 40),
            (
                int(x + PETAL_RADIUS * 0.45),
                int(y)
            ),
            int(pollen_radius)
        )

    elif name == "Soil":

        radius = PETAL_RADIUS * 0.9

        # Dark brown outline
        pygame.draw.circle(
            screen,
            (70, 40, 20),
            (x, y),
            int(radius + 2)
        )

        # Brown inside
        pygame.draw.circle(
            screen,
            (130, 80, 40),
            (x, y),
            int(radius)
        )

    elif name == "Ant Egg":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count <= 3:
                    scale = 0.75

                elif count <= 5:
                    scale = 0.65

                else:
                    scale = 0.55

            # ---------------- ANT EGG ----------------

            egg_radius = PETAL_RADIUS * 0.7 * scale

            # Darker outline
            pygame.draw.circle(
                screen,
                (180, 130, 95),
                (
                    int(draw_x),
                    int(draw_y)
                ),
                int(egg_radius + 2 * scale)
            )

            # Light inside
            pygame.draw.circle(
                screen,
                (245, 205, 165),
                (
                    int(draw_x),
                    int(draw_y)
                ),
                int(egg_radius)
            )

    elif name == "Sand":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            if count == 1:
                draw_x = x
                draw_y = y
                size = PETAL_RADIUS * 0.75

            else:
                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.5

                draw_x = (
                    x +
                    math.cos(angle_rad) * distance
                )

                draw_y = (
                    y +
                    math.sin(angle_rad) * distance
                )

                size = PETAL_RADIUS * 0.4

            # ---------------- SAND HEXAGON ----------------

            points = []

            for side in range(6):

                angle = (
                    math.radians(60 * side)
                    - math.pi / 6
                )

                points.append(
                    (
                        draw_x + math.cos(angle) * size,
                        draw_y + math.sin(angle) * size
                    )
                )

            # Outline
            pygame.draw.polygon(
                screen,
                (190, 145, 70),
                points
            )

            # Smaller light-orange inside
            inner_points = []

            for side in range(6):

                angle = (
                    math.radians(60 * side)
                    - math.pi / 6
                )

                inner_points.append(
                    (
                        draw_x + math.cos(angle) * size * 0.82,
                        draw_y + math.sin(angle) * size * 0.82
                    )
                )

            pygame.draw.polygon(
                screen,
                (245, 205, 105),
                inner_points
            )

    elif name == "Lentil":

        radius = PETAL_RADIUS * 0.65

        pygame.draw.circle(
            screen,
            (220, 150, 15),
            (x, y),
            int(radius + 2.75)
        )

        pygame.draw.circle(
            screen,
            (240, 170, 35),
            (x, y),
            int(radius)
        )

    elif name == "Pincer":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            r = PETAL_RADIUS * 0.85 * scale

            outline = (30, 30, 30)
            inside = (50, 50, 50)

            # ---------------- PINCER OUTLINE ----------------

            points = [
                (draw_x - r * 0.85, draw_y - r * 0.15),
                (draw_x - r * 0.80, draw_y - r * 0.45),
                (draw_x - r * 0.60, draw_y - r * 0.70),
                (draw_x - r * 0.30, draw_y - r * 0.78),
                (draw_x + r * 0.05, draw_y - r * 0.65),
                (draw_x + r * 0.40, draw_y - r * 0.48),
                (draw_x + r * 0.75, draw_y - r * 0.28),

                # Sharp point
                (draw_x + r * 1.05, draw_y),

                (draw_x + r * 0.75, draw_y + r * 0.12),
                (draw_x + r * 0.35, draw_y + r * 0.18),
                (draw_x - r * 0.05, draw_y + r * 0.18),
                (draw_x - r * 0.35, draw_y + r * 0.30),
                (draw_x - r * 0.60, draw_y + r * 0.50),
                (draw_x - r * 0.80, draw_y + r * 0.40),
                (draw_x - r * 0.88, draw_y + r * 0.10)
            ]

            pygame.draw.polygon(
                screen,
                outline,
                points
            )

            # ---------------- PINCER INSIDE ----------------

            inner_points = [
                (draw_x - r * 0.72, draw_y - r * 0.13),
                (draw_x - r * 0.68, draw_y - r * 0.38),
                (draw_x - r * 0.50, draw_y - r * 0.58),
                (draw_x - r * 0.25, draw_y - r * 0.65),
                (draw_x + r * 0.05, draw_y - r * 0.54),
                (draw_x + r * 0.38, draw_y - r * 0.38),
                (draw_x + r * 0.68, draw_y - r * 0.20),

                # Sharp inner point
                (draw_x + r * 0.95, draw_y),

                (draw_x + r * 0.65, draw_y + r * 0.08),
                (draw_x + r * 0.30, draw_y + r * 0.13),
                (draw_x - r * 0.05, draw_y + r * 0.13),
                (draw_x - r * 0.30, draw_y + r * 0.23),
                (draw_x - r * 0.50, draw_y + r * 0.40),
                (draw_x - r * 0.68, draw_y + r * 0.32),
                (draw_x - r * 0.75, draw_y + r * 0.08)
            ]

            pygame.draw.polygon(
                screen,
                inside,
                inner_points
            )

    elif name == "Shell":

        r = PETAL_RADIUS * 0.9

        outline = (150, 105, 75)
        inside = (245, 205, 165)

        # ---------------- SHELL FAN ----------------

        points = [
            # Bottom
            (x, y + r * 0.75),

            # Left side
            (x - r * 0.30, y + r * 0.55),
            (x - r * 0.55, y + r * 0.15),
            (x - r * 0.75, y - r * 0.30),
            (x - r * 0.70, y - r * 0.65),

            # Top curve
            (x - r * 0.45, y - r * 0.85),
            (x, y - r * 0.95),
            (x + r * 0.45, y - r * 0.85),
            (x + r * 0.70, y - r * 0.65),

            # Right side
            (x + r * 0.75, y - r * 0.30),
            (x + r * 0.55, y + r * 0.15),
            (x + r * 0.30, y + r * 0.55)
        ]

        # Dark outline
        pygame.draw.polygon(
            screen,
            outline,
            points
        )

        # Smaller fan inside
        inner_points = [
            (x, y + r * 0.60),

            (x - r * 0.25, y + r * 0.43),
            (x - r * 0.48, y + r * 0.08),
            (x - r * 0.65, y - r * 0.30),
            (x - r * 0.60, y - r * 0.55),

            (x - r * 0.38, y - r * 0.72),
            (x, y - r * 0.82),
            (x + r * 0.38, y - r * 0.72),
            (x + r * 0.60, y - r * 0.55),

            (x + r * 0.65, y - r * 0.30),
            (x + r * 0.48, y + r * 0.08),
            (x + r * 0.25, y + r * 0.43)
        ]

        pygame.draw.polygon(
            screen,
            inside,
            inner_points
        )

    elif name == "Beetle Egg":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            # ---------------- COPY POSITION ----------------

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count == 2:
                    scale = 0.75

                elif count == 3:
                    scale = 0.65

                else:
                    scale = 0.55

            width = PETAL_RADIUS * 0.75 * scale
            height = PETAL_RADIUS * 1.05 * scale

            outline = (155, 110, 80)
            inside = (245, 205, 165)

            # ---------------- DARK OUTLINE ----------------

            pygame.draw.ellipse(
                screen,
                outline,
                (
                    int(draw_x - width - 2 * scale),
                    int(draw_y - height - 2 * scale),
                    int(width * 2 + 4 * scale),
                    int(height * 2 + 4 * scale)
                )
            )

            # ---------------- LIGHT SKIN-COLORED INSIDE ----------------

            pygame.draw.ellipse(
                screen,
                inside,
                (
                    int(draw_x - width),
                    int(draw_y - height),
                    int(width * 2),
                    int(height * 2)
                )
            )

    elif name == "Third Eye":

        r = PETAL_RADIUS

        # ---------------- BLACK OUTER EYE ----------------

        pygame.draw.ellipse(
            screen,
            (0, 0, 0),
            (
                int(x - r * 0.55),
                int(y - r * 0.85),
                int(r * 1.10),
                int(r * 1.70)
            )
        )

        # ---------------- WHITE INNER EYE ----------------

        pygame.draw.ellipse(
            screen,
            (255, 255, 255),
            (
                int(x - r * 0.32),
                int(y - r * 0.58),
                int(r * 0.64),
                int(r * 1.16)
            )
        )

        # ---------------- SMALL BLACK CENTER ----------------

        pygame.draw.ellipse(
            screen,
            (0, 0, 0),
            (
                int(x - r * 0.10),
                int(y - r * 0.20),
                int(r * 0.20),
                int(r * 0.40)
            )
        )

    elif name == "Cice":

        r = PETAL_RADIUS

        # ---------------- CORN ----------------

        corn_outline = (120, 80, 20)
        corn_color = (255, 200, 40)

        pygame.draw.ellipse(
            screen,
            corn_outline,
            (
                int(x - r * 0.95),
                int(y - r * 1.05),
                int(r * 1.9),
                int(r * 2.1)
            )
        )

        pygame.draw.ellipse(
            screen,
            corn_color,
            (
                int(x - r * 0.80),
                int(y - r * 0.90),
                int(r * 1.6),
                int(r * 1.8)
            )
        )

        # ---------------- RICE INSIDE ----------------

        rice_outline = (120, 110, 90)
        rice_color = (255, 250, 235)

        pygame.draw.ellipse(
            screen,
            rice_outline,
            (
                int(x - r * 0.28),
                int(y - r * 0.65),
                int(r * 0.56),
                int(r * 1.30)
            )
        )

        pygame.draw.ellipse(
            screen,
            rice_color,
            (
                int(x - r * 0.21),
                int(y - r * 0.57),
                int(r * 0.42),
                int(r * 1.14)
            )
        )

    elif name == "Boubloom":

        r = PETAL_RADIUS

        outline = (25, 80, 30)
        inside = (70, 180, 75)

        # ---------------- GREEN PENTAGON ----------------

        points = [
            (x, y - r),                    # Top
            (x + r * 0.95, y - r * 0.30), # Upper-right
            (x + r * 0.58, y + r * 0.80), # Bottom-right
            (x - r * 0.58, y + r * 0.80), # Bottom-left
            (x - r * 0.95, y - r * 0.30)  # Upper-left
        ]

        # Dark green outline
        pygame.draw.polygon(
            screen,
            outline,
            points
        )

        # Smaller green pentagon inside
        inner_points = [
            (x, y - r * 0.82),
            (x + r * 0.78, y - r * 0.24),
            (x + r * 0.48, y + r * 0.65),
            (x - r * 0.48, y + r * 0.65),
            (x - r * 0.78, y - r * 0.24)
        ]

        pygame.draw.polygon(
            screen,
            inside,
            inner_points
        )

    elif name == "Boulder":

        r = PETAL_RADIUS

        # Random number of sides
        sides = random.randint(6, 6)

        outline = (70, 70, 70)
        inside = (150, 150, 150)

        # ---------------- BOULDER ----------------

        points = []

        for i in range(sides):

            angle = (2 * math.pi * i / sides) - math.pi / 2

            px = x + math.cos(angle) * r
            py = y + math.sin(angle) * r

            points.append((int(px), int(py)))

        # Dark gray outline
        pygame.draw.polygon(
            screen,
            outline,
            points
        )

        # Smaller gray polygon
        inner_points = []

        for i in range(sides):

            angle = (2 * math.pi * i / sides) - math.pi / 2

            px = x + math.cos(angle) * r * 0.82
            py = y + math.sin(angle) * r * 0.82

            inner_points.append((int(px), int(py)))

        pygame.draw.polygon(
            screen,
            inside,
            inner_points
        )

    elif name == "Moon":

        r = PETAL_RADIUS

        cache_key = int(round(r * 10))
        moon_surface = moon_surface_cache.get(cache_key)
        center = int(r * 1.2)
        if moon_surface is None:
            moon_color = (180, 180, 180)
            spot_color = (120, 120, 120)
            moon_surface = pygame.Surface(
                (int(r * 2.4), int(r * 2.4)),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                moon_surface,
                moon_color,
                (center, center),
                int(r)
            )
            for spot in moon_spots:
                pygame.draw.circle(
                    moon_surface,
                    spot_color,
                    (
                        center + int(spot["x"]),
                        center + int(spot["y"])
                    ),
                    int(spot["radius"])
                )
            mask_surface = pygame.Surface(
                moon_surface.get_size(),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                mask_surface,
                (255, 255, 255, 255),
                (center, center),
                int(r)
            )
            moon_surface.blit(
                mask_surface,
                (0, 0),
                special_flags=pygame.BLEND_RGBA_MULT
            )
            moon_surface_cache[cache_key] = moon_surface

        # Draw moon
        screen.blit(
            moon_surface,
            (
                int(x - center),
                int(y - center)
            )
        )

        # Moon's own outline, distinct from other petals.
        pygame.draw.circle(
            screen,
            (100, 100, 100),
            (int(x), int(y)),
            int(r),
            3
        )

    elif name == "Grape":

        count = get_petal_count(name, rarity)

        for multiply_i in range(count):

            if count == 1:

                draw_x = x
                draw_y = y
                scale = 1.0

            else:

                angle = (
                    petal_angle
                    + multiply_i * (360 / count)
                )

                angle_rad = math.radians(angle)

                distance = PETAL_RADIUS * 0.55

                draw_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                draw_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                if count <= 3:
                    scale = 0.75

                elif count <= 5:
                    scale = 0.65

                else:
                    scale = 0.55

            r = (PETAL_RADIUS - 2) * scale

            # ---------------- PURPLE GRAPE ----------------

            pygame.draw.circle(
                screen,
                (150, 70, 190),
                (int(draw_x), int(draw_y)),
                int(r)
            )

            # ---------------- LIGHT PART ----------------

            pygame.draw.circle(
                screen,
                (220, 180, 230),
                (
                    int(draw_x - r * 0.25),
                    int(draw_y - r * 0.25)
                ),
                max(1, int(r * 0.22))
            )

            # ---------------- OUTLINE ----------------

            pygame.draw.circle(
                screen,
                (90, 40, 120),
                (int(draw_x), int(draw_y)),
                int(r),
                max(1, int(2 * scale))
            )

    PETAL_RADIUS = original_petal_radius

    if flash_timer > 0:
        flash_r = int(PETAL_RADIUS * size_scale)
        flash_surf = pygame.Surface(
            (flash_r * 2, flash_r * 2),
            pygame.SRCALPHA
        )
        pygame.draw.circle(
            flash_surf,
            (255, 0, 0),
            (flash_r, flash_r),
            flash_r
        )
        screen.blit(
            flash_surf,
            (int(x) - flash_r, int(y) - flash_r),
            special_flags=pygame.BLEND_RGB_ADD
        )

def draw_gradient_circle(surface, center, radius):
    x, y = center

    for r in range(radius, 0, -1):

        # red -> yellow
        t = 1 - (r / radius)

        red = 255
        green = int(255 * t)
        blue = 0

        pygame.draw.circle(
            surface,
            (red, green, blue),
            (x, y),
            r
        )

def draw_celestial_gradient_circle(surface, center, radius):
    x, y = center

    for r in range(radius, 0, -1):

        # white -> black
        t = 1 - (r / radius)

        value = int(255 * (1 - t))

        pygame.draw.circle(
            surface,
            (value, value, value),
            (x, y),
            r
        )

def draw_moving_gradient_rect(surface, rect, colors):
    global gradient_angle

    size = rect.width * 2

    gradient_surface = pygame.Surface(
        (size, size),
        pygame.SRCALPHA
    )

    time = pygame.time.get_ticks() / 500


    # moving direction
    offset_x = math.sin(time) * size
    offset_y = math.cos(time) * size


    for x in range(size):

        for y in range(size):

            # diagonal moving gradient
            pos = (
                x + offset_x +
                y + offset_y
            ) / (size * 2)


            pos %= 1


            # red -> purple -> orange
            if pos < 0.5:

                t = pos * 2

                r = 255
                g = int(0 + 80 * t)
                b = int(120 - 120 * t)

            else:

                t = (pos - 0.5) * 2

                r = 255
                g = int(80 + 90 * t)
                b = int(0 + 20 * t)


            gradient_surface.set_at(
                (x,y),
                (r,g,b,255)
            )



    # rotate the whole gradient

    gradient_angle += 5

    rotated = pygame.transform.rotate(
        gradient_surface,
        gradient_angle
    )


    # crop center into slot

    center = rotated.get_rect(
        center=(
            rect.width//2,
            rect.height//2
        )
    )


    surface.blit(
        rotated,
        (-center.x + rect.x,
         -center.y + rect.y)
    )

def draw_rarity_slot(x, y, size, rarity):

    global infino_gradient_angle
    global infino_gradient_offset

    if rarity == "Omnient":

        gradient_surface = pygame.Surface(
            (size, size),
            pygame.SRCALPHA
        )

        for yy in range(size):

            t = yy / size

            color = (
                255,
                int(255 * t),
                0
            )

            pygame.draw.line(
                gradient_surface,
                color,
                (0, yy),
                (size, yy)
            )

        mask = pygame.Surface(
            (size, size),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            (
                0,
                0,
                size,
                size
            ),
            border_radius=8
        )

        gradient_surface.blit(
            mask,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        screen.blit(
            gradient_surface,
            (x, y)
        )

    elif rarity == "Celestial":

        gradient_surface = pygame.Surface(
            (size, size),
            pygame.SRCALPHA
        )

        for yy in range(size):

            t = yy / size

            if t < 1/3:

                progress = t * 3

                red = 255
                green = 0
                blue = int(150 * progress)

            elif t < 2/3:

                progress = (t - 1/3) * 3

                red = 255
                green = int(255 * progress)
                blue = int(150 - (150 * progress))

            else:

                progress = (t - 2/3) * 3

                red = int(255 - (255 * progress))
                green = 255
                blue = 0

            color = (
                red,
                green,
                blue
            )

            pygame.draw.line(
                gradient_surface,
                color,
                (0, yy),
                (size, yy)
            )

        mask = pygame.Surface(
            (size, size),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            mask,
            (255,255,255,255),
            (
                0,
                0,
                size,
                size
            ),
            border_radius=8
        )

        gradient_surface.blit(
            mask,
            (0,0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        screen.blit(
            gradient_surface,
            (x,y)
        )

    elif rarity == "Infino":
        gradient_surface = pygame.Surface(
            (size, size),
            pygame.SRCALPHA
        )

        for yy in range(size):

            for xx in range(size):

                direction_x = math.cos(
                    infino_gradient_angle
                )

                direction_y = math.sin(
                    infino_gradient_angle
                )

                t = (
                    xx * direction_x +
                    yy * direction_y +
                    infino_gradient_offset
                ) / size

                t %= 3

                if t < 1:

                    progress = t

                    red = 255
                    green = 0
                    blue = int(255 * progress)

                elif t < 2:

                    progress = t - 1

                    red = 255
                    green = int(165 * progress)
                    blue = int(255 - (255 * progress))

                else:

                    progress = t - 2

                    red = 255
                    green = int(165 - (165 * progress))
                    blue = 0

                gradient_surface.set_at(
                    (xx, yy),
                    (
                        red,
                        green,
                        blue,
                        255
                    )
                )

        mask = pygame.Surface(
            (size, size),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            mask,
            (255,255,255,255),
            (
                0,
                0,
                size,
                size
            ),
            border_radius=8
        )

        gradient_surface.blit(
            mask,
            (0,0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        screen.blit(
            gradient_surface,
            (x,y)
        )

    else:

        slot_color = RARITY_COLORS.get(
            rarity,
            (90,90,90)
        )

        pygame.draw.rect(
            screen,
            slot_color,
            (
                x,
                y,
                size,
                size
            ),
            border_radius=8
        )

        border_color = (
            max(slot_color[0] - 40, 0),
            max(slot_color[1] - 40, 0),
            max(slot_color[2] - 40, 0)
        )

        pygame.draw.rect(
            screen,
            border_color,
            (
                x,
                y,
                size,
                size
            ),
            3,
            border_radius=8
        )

def draw_omnient_slot(screen, x, y, size):

    surface = pygame.Surface(
        (size,size),
        pygame.SRCALPHA
    )

    for yy in range(size):

        t = yy / size

        color = (
            255,
            int(255*t),
            0
        )

        pygame.draw.line(
            surface,
            color,
            (0,yy),
            (size,yy)
        )


    mask = pygame.Surface(
        (size,size),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        mask,
        (255,255,255,255),
        (0,0,size,size),
        border_radius=8
    )

    surface.blit(
        mask,
        (0,0),
        special_flags=pygame.BLEND_RGBA_MULT
    )

    screen.blit(surface,(x,y))

def draw_celestial_slot(screen, x, y, size):

    surface = pygame.Surface(
        (size,size),
        pygame.SRCALPHA
    )

    for yy in range(size):

        t = yy / size

        if t < 1/3:

            progress = t * 3

            color = (
                255,
                0,
                int(150 * progress)
            )

        elif t < 2/3:

            progress = (t - 1/3) * 3

            color = (
                255,
                int(255 * progress),
                int(150 - 150 * progress)
            )

        else:

            progress = (t - 2/3) * 3

            color = (
                int(255 - 255 * progress),
                255,
                0
            )


        pygame.draw.line(
            surface,
            color,
            (0,yy),
            (size,yy)
        )


    mask = pygame.Surface(
        (size,size),
        pygame.SRCALPHA
    )

    pygame.draw.rect(
        mask,
        (255,255,255,255),
        (0,0,size,size),
        border_radius=8
    )


    surface.blit(
        mask,
        (0,0),
        special_flags=pygame.BLEND_RGBA_MULT
    )


    screen.blit(
        surface,
        (x,y)
    )

def draw_infino_slot(screen, x, y, size):

    global infino_gradient_angle
    global infino_gradient_offset

    surface = pygame.Surface(
        (size,size),
        pygame.SRCALPHA
    )


    for xx in range(size):

        for yy in range(size):

            direction_x = math.cos(infino_gradient_angle)
            direction_y = math.sin(infino_gradient_angle)


            t = (
                xx * direction_x +
                yy * direction_y +
                infino_gradient_offset
            ) / size


            t %= 3


            if t < 1:

                progress = t

                color = (
                    255,
                    0,
                    int(255 * progress)
                )


            elif t < 2:

                progress = t - 1

                color = (
                    255,
                    int(165 * progress),
                    int(255 - 255 * progress)
                )


            else:

                progress = t - 2

                color = (
                    255,
                    int(165 - 165 * progress),
                    0
                )


            surface.set_at(
                (xx,yy),
                (*color,255)
            )


    mask = pygame.Surface(
        (size,size),
        pygame.SRCALPHA
    )


    pygame.draw.rect(
        mask,
        (255,255,255,255),
        (0,0,size,size),
        border_radius=8
    )


    surface.blit(
        mask,
        (0,0),
        special_flags=pygame.BLEND_RGBA_MULT
    )


    screen.blit(
        surface,
        (x,y)
    )

def calculate_xp_needed(level):

    xp = 100

    for i in range(level - 1):
        xp = round(xp * 1.5)

    return xp

def give_xp(amount):

    global flower_xp
    global flower_level
    global flower_xp_needed
    global upgrade_points

    # ---------------- MAX LEVEL ----------------

    if flower_level >= 250:

        flower_level = 250
        flower_xp = 0
        flower_xp_needed = calculate_xp_needed(250)

        return


    # ---------------- GIVE XP ----------------

    flower_xp += amount


    # ---------------- LEVEL UP ----------------

    while flower_xp >= flower_xp_needed:

        flower_xp -= flower_xp_needed

        flower_level += 1

        # Update petal slots based on level
        PETAL_SLOTS = get_petal_slots(flower_level)
        pad_petal_slots()
        pad_swap_petal_slots()
        resize_petal_lists()


        # ---------------- REWARD ----------------

        upgrade_points += 1


        # Every 5 levels
        # 5, 15, 25, 35...

        if flower_level >= 5 and flower_level % 10 == 5:

            upgrade_points += 5


        # Every 10 levels
        # 10, 20, 30, 40...

        if flower_level % 10 == 0:

            upgrade_points += 10


        # ---------------- MAX LEVEL ----------------

        if flower_level >= 250:

            flower_level = 250
            PETAL_SLOTS = get_petal_slots(flower_level)
            pad_petal_slots()
            pad_swap_petal_slots()
            resize_petal_lists()
            flower_xp = 0
            flower_xp_needed = calculate_xp_needed(250)

            return


        # ---------------- NEXT LEVEL XP ----------------

        flower_xp_needed = calculate_xp_needed(
            flower_level
        )

def enemy_can_see_player(enemy):

    start = pygame.Vector2(
        enemy.x,
        enemy.y
    )

    end = pygame.Vector2(
        player_x,
        player_y
    )


    direction = end - start

    distance_to_player = direction.length()


    if distance_to_player == 0:
        return True

    if hasattr(enemy, "view_range"):
        # Fixed tuned view range per mob type (not size-dependent).
        if distance_to_player > enemy.view_range:
            return False
    elif distance_to_player > enemy.radius * 20:
        # Mobs without a tuned view_range see 20x their size.
        return False


    direction = direction.normalize()


    # check points along the line

    step = 10

    current = start.copy()


    for i in range(0, int(distance_to_player), step):

        current += direction * step


        for wall in walls:

            if wall.rect.collidepoint(
                current.x,
                current.y
            ):

                return False


    return True

def draw_minimap():

    # background

    pygame.draw.rect(
        screen,
        (40,40,40),
        (
            MINIMAP_X,
            MINIMAP_Y,
            MINIMAP_SIZE,
            MINIMAP_SIZE
        )
    )


    # border

    pygame.draw.rect(
        screen,
        (150,150,150),
        (
            MINIMAP_X,
            MINIMAP_Y,
            MINIMAP_SIZE,
            MINIMAP_SIZE
        ),
        3
    )

    pygame.draw.rect(
        screen,
        (255,0,0),
        (
            MINIMAP_X,
            MINIMAP_Y,
            MINIMAP_SIZE,
            MINIMAP_SIZE
        ),
        3
    )

    for wall in walls:
        wall.draw_map()


    # convert world position to map position

    map_x = max(
        0,
        min(
            MINIMAP_SIZE,
            player_x / WORLD_WIDTH * MINIMAP_SIZE
        )
    )

    map_y = max(
        0,
        min(
            MINIMAP_SIZE,
            player_y / WORLD_HEIGHT * MINIMAP_SIZE
        )
    )



    # player dot

    pygame.draw.circle(
        screen,
        (255,255,0),
        (
            int(MINIMAP_X + map_x),
            int(MINIMAP_Y + map_y)
        ),
        5
    )

def create_account():

    global petal_slots
    global swap_petal_slots
    global petal_hp
    global inventory
    global petal_max_hp
    global petal_alive
    global game_state

    # give 5 Common Basic petals

    petal_slots = []

    for i in range(PETAL_SLOTS):

        petal_slots.append({
            "filled": True,
            "petal": "Basic",
            "rarity": "Common"
        })

    # Initialize swap slots as empty
    swap_petal_slots = []
    for i in range(PETAL_SLOTS):
        swap_petal_slots.append({
            "filled": False,
            "petal": "Basic",
            "rarity": "Common"
        })


    # reset petal HP

    petal_hp = []
    petal_max_hp = []
    petal_alive = []
    petal_flash_timers = []


    for i in range(PETAL_SLOTS):

        hp = (
            PETAL_HP["Basic"]
            *
            PETAL_HP_MULTIPLIER["Common"]
        )

        petal_max_hp.append(hp)
        petal_hp.append(hp)
        petal_alive.append(True)
        petal_flash_timers.append(0)


    game_state = "welcome"
    welcome_timer = 90
    init_welcome_petals()
    save_player()

def push_player_from(enemy, speed=6.0):

    # small knockback on the living flower when it gets hit, reusing the
    # same bounce values that the death/bounce movement decays

    global player_bounce_x
    global player_bounce_y

    dx = player_x - enemy.x
    dy = player_y - enemy.y

    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        dx = 1
        dy = 0
        length = 1

    dx /= length
    dy /= length

    player_bounce_x = dx * speed
    player_bounce_y = dy * speed

def kill_player(enemy):

    global player_dead
    global player_hp
    global player_godmode

    if getattr(globals(), "player_godmode", False):
        player_hp = PLAYER_MAX_HP
        return
    global player_death_timer
    global player_bounce_x
    global player_bounce_y
    global player_death_dir_x
    global player_death_dir_y
    global player_rot_vel
    global killer_name
    global killer_rarity

    if player_dead:
        return

    player_dead = True
    player_death_timer = PLAYER_DEATH_DURATION

    killer_name = enemy.__class__.__name__
    killer_rarity = enemy.rarity

    # bounce away from the enemy
    dx = player_x - enemy.x
    dy = player_y - enemy.y

    length = math.sqrt(dx * dx + dy * dy)

    if length == 0:
        dx = 1
        dy = 0
        length = 1

    dx /= length
    dy /= length

    bounce_speed = 11

    player_bounce_x = dx * bounce_speed
    player_bounce_y = dy * bounce_speed

    player_death_dir_x = dx
    player_death_dir_y = dy

    # spin the player on death, ends via acceleration (friction) below
    player_rot_vel = 12

    # petals are gone on death
    for i in range(PETAL_SLOTS):
        petal_alive[i] = False
        petal_hp[i] = 0
        petal_respawn_timer[i] = PETAL_RELOAD[
            petal_slots[i]["petal"]
        ]


def respawn_player():

    global player_dead
    global player_hp
    global player_bounce_x
    global player_bounce_y
    global player_spawn_cooldown
    global player_vel_x
    global player_vel_y
    global player_x
    global player_y
    global player_rot_angle
    global player_rot_vel
    global killer_name
    global killer_rarity

    player_dead = False
    player_hp = PLAYER_MAX_HP
    player_bounce_x = 0
    player_bounce_y = 0
    player_vel_x = 0
    player_vel_y = 0
    player_rot_angle = 0
    player_rot_vel = 0
    killer_name = None
    killer_rarity = None
    global current_dimension
    global pre_hole_land_x
    global pre_hole_land_y
    global pre_hole_land_grid_color
    global game_grid_color
    global game_target_grid_color

    if current_dimension == "hole_land":
        # Respawn back to where the flower came from before entering Hole Land
        player_x = pre_hole_land_x
        player_y = pre_hole_land_y
        current_dimension = "regular"
        game_grid_color = pre_hole_land_grid_color
        game_target_grid_color = pre_hole_land_grid_color
    else:
        current_dimension = "regular"
        player_x, player_y = 25, WORLD_HEIGHT - PLAYER_RADIUS

    for i in range(PETAL_SLOTS):
        if petal_slots[i]["filled"]:
            petal_alive[i] = True
            petal_hp[i] = petal_max_hp[i]
            petal_respawn_timer[i] = 0

    player_spawn_cooldown = PLAYER_SPAWN_PROTECTION_TIME
    save_player()

create_map()
player_x, player_y = 25, WORLD_HEIGHT - PLAYER_RADIUS
# ---------------- GAME LOOP ----------------

# Initialize enemy lists (no enemies spawned - all spawning code removed)
ladybugs = []
hole_ladybugs = []
hole_bees = []
hole_spiders = []
hole_rocks = []
bees = []
spiders = []
rocks = []
hornets = []
hole_hornets = []
baby_ants = []
hole_baby_ants = []
soldier_ants = []
hole_soldier_ants = []
worker_ants = []
hole_worker_ants = []
queen_ants = []
hole_queen_ants = []
ant_eggs = []

# Eggs laid by queen ants while chasing; they hatch into enemy
# soldier ant minions.
queen_eggs = []

# Friendly minions hatched from Ant Egg petals. They live outside
# the enemy lists so petals and enemy AI never target them.
flower_minions = []

def draw_login_screen():

    screen.fill((20,20,30))


    # purple box

    pygame.draw.rect(
        screen,
        (120,50,180),
        login_box,
        border_radius=15
    )


    font = pygame.font.Font(None,50)

    title = font.render(
        "Velora.io",
        True,
        (255,255,255)
    )

    screen.blit(
        title,
        (
            WIDTH//2 - title.get_width()//2,
            120
        )
    )


    font = pygame.font.Font(None, 32)


# Password label

    password_label = font.render(
        "Password:",
        True,
        (255,255,255)
    )

    screen.blit(
        password_label,
        (
            WIDTH//2 - 200,
            HEIGHT//2 - 190
        )
    )


    # Password box

    pygame.draw.rect(
        screen,
        (255,255,255),
        password_box,
        border_radius=5
    )



    # Account name label

    acc_label = font.render(
        "Acc Name:",
        True,
        (255,255,255)
    )

    screen.blit(
        acc_label,
        (
            WIDTH//2 - 200,
            HEIGHT//2 + -90
        )
    )

        # Login button hover

    if login_rect.collidepoint(pygame.mouse.get_pos()):
        login_color = (80,220,100)
    else:
        login_color = (50,180,80)


    pygame.draw.rect(
        screen,
        login_color,
        login_rect,
        border_radius=10
    )
    pygame.draw.rect(
        screen,
        (30, 110, 45),
        login_rect,
        3,
        border_radius=10
    )


    # Login button text

    button_font = pygame.font.Font(None, 32)

    login_text = button_font.render(
        "Login",
        True,
        (255,255,255)
    )

    screen.blit(
        login_text,
        (
            login_rect.centerx - login_text.get_width()//2,
            login_rect.centery - login_text.get_height()//2
        )
    )


    # Account name box

    pygame.draw.rect(
        screen,
        (255,255,255),
        acc_name_box,
        border_radius=5
    )

        # Create account button hover

    if create_acc_button_rect.collidepoint(pygame.mouse.get_pos()):
        create_acc_color = (100,140,255)
    else:
        create_acc_color = (70,100,220)


    pygame.draw.rect(
        screen,
        create_acc_color,
        create_acc_button_rect,
        border_radius=10
    )
    pygame.draw.rect(
        screen,
        (35, 65, 150),
        create_acc_button_rect,
        3,
        border_radius=10
    )


    # Create account button text

    create_text = button_font.render(
        "Create Account",
        True,
        (255,255,255)
    )

    screen.blit(
        create_text,
        (
            create_acc_button_rect.centerx - create_text.get_width()//2,
            create_acc_button_rect.centery - create_text.get_height()//2
        )
    )

    # Login error message

    if login_error != "":

        error_font = pygame.font.Font(None, 28)

        alpha = int(255 * (login_error_timer / 60))

        error_surface = error_font.render(
            login_error,
            True,
            (255,80,80)
        )

        error_surface.set_alpha(alpha)

        screen.blit(
            error_surface,
            (
                login_box.centerx - error_surface.get_width()//2,
                login_box.bottom + 20
            )
        )

running = True

while running:

    all_enemies = (
        ladybugs
        + hole_ladybugs
        + bees
        + spiders
        + rocks
        + hornets
        + baby_ants
        + soldier_ants
        + worker_ants
        + queen_ants
        + ant_eggs
    )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # respawn button on the death overlay
            if player_dead and respawn_button_rect.collidepoint(
                mouse_x, mouse_y
            ):
                respawn_player()


                # open menu

            if hp_button_rect.collidepoint(mouse_x, mouse_y):

                open_only_panel("hp")



                # close menu

            if hp_menu_open:

                if close_button_rect.collidepoint(mouse_x, mouse_y):

                    hp_menu_open = False



                # buy upgrade

            if hp_menu_open:

                if hp_upgrade_rect.collidepoint(mouse_x, mouse_y):

                    upgrade_player_hp()


            if game_state == "welcome" and not welcome_transition_active:

                welcome_click_pending = True

# Chat box click handling
            if game_state == "game" and welcome_play_pressed:
                chat_box_w = 260
                chat_margin = 20
                inner_padding = 10
                inner_height = 30
                # Arrow button stays at fixed position
                arrow_y = HEIGHT - chat_margin - 120
                # Chat box bottom stays fixed; grows upward when taller
                if chat_arrow_up:
                    chat_box_h = 200
                    box_y = arrow_y - 80
                else:
                    chat_box_h = 120
                    box_y = arrow_y
                chat_box_x = WIDTH - chat_margin - chat_box_w
                chat_box_y = box_y
                inner_rect_x = chat_box_x + inner_padding
                inner_rect_y = box_y + chat_box_h - inner_height - inner_padding
                inner_rect_w = chat_box_w - 2 * inner_padding
                inner_rect = pygame.Rect(
                    inner_rect_x, inner_rect_y, inner_rect_w, inner_height
                )
                if chat_text_visible:
                    if inner_rect.collidepoint(mouse_x, mouse_y):
                        chat_text_visible = False
                else:
                    if not inner_rect.collidepoint(mouse_x, mouse_y):
                        chat_text_visible = True

                # Arrow square click handling
                small_square_size = 40
                square_x = chat_box_x - small_square_size - 5
                square_y = arrow_y
                square_rect = pygame.Rect(square_x, square_y, small_square_size, small_square_size)
                if square_rect.collidepoint(mouse_x, mouse_y):
                    chat_arrow_up = not chat_arrow_up

                # Chat scrollbar drag handling
                if len(chat_messages) > 4:
                    small_square_bottom = arrow_y + small_square_size
                    gap = 5
                    vertical_rect_x = chat_box_x - small_square_size - 5
                    vertical_rect_y = small_square_bottom + gap
                    vertical_rect = pygame.Rect(
                        vertical_rect_x, vertical_rect_y, small_square_size, 120 - small_square_size - gap
                    )
                    if vertical_rect.collidepoint(mouse_x, mouse_y):
                        chat_dragging = True
                        chat_drag_offset = mouse_y - chat_scrollbar_rect.y

            if game_state == "login":

                if password_box.collidepoint(event.pos):

                    active_input = "password"


                elif acc_name_box.collidepoint(event.pos):

                    active_input = "acc_name"


                else:

                    active_input = None

            if game_state == "login" and login_rect.collidepoint(event.pos):

                # empty check
                if password_text == "" or acc_name_text == "":

                    login_error = "Password and account name can't be empty"
                    login_error_timer = 60


                # account exists check
                elif (
                    (acc_name_text not in accounts or accounts[acc_name_text] != password_text)
                    and
                    (acc_name_text not in player_accounts or player_accounts[acc_name_text] != password_text)
                ):

                    login_error = "Password or account name does not exist"
                    login_error_timer = 60


                # success
                else:

                    login_error = ""
                    login_error_timer = 0

                    load_player()

                    # The developer account always moves faster, and its
                    # max HP always matches its HP upgrade cost.
                    if acc_name_text == "DevGuard":
                        PLAYER_SPEED = 25
                        PLAYER_MAX_HP = hp_upgrade_cost
                        player_hp = PLAYER_MAX_HP

                    if acc_name_text == "DevGuard":

                        inventory = []

                        flower_level = 250
                        PETAL_SLOTS = get_petal_slots(flower_level)
                        pad_petal_slots()
                        pad_swap_petal_slots()
                        resize_petal_lists()
                        flower_xp = 0
                        upgrade_points = 0
                        PLAYER_MAX_HP = 100000000000000
                        player_hp = PLAYER_MAX_HP
                        hp_upgrade_cost = 100000000000000
                        PLAYER_SPEED = 25

                        flower_xp_needed = calculate_xp_needed(
                            250
                        )

                        for petal in PETAL_HP.keys():

                            for rarity in RARITY_COLORS.keys():

                                add_inventory_petal(
                                    petal,
                                    rarity,
                                    1000
                                )


                    # ADD SORT HERE
                    sort_inventory()

                    game_state = "welcome"
                    welcome_timer = 90
                    init_welcome_petals()


            if game_state == "login" and create_acc_button_rect.collidepoint(event.pos):

                if password_text == "" or acc_name_text == "":

                    login_error = "Password and account name can't be empty"
                    login_error_timer = 60


                elif (
                    acc_name_text.lower() == "devguard"
                    and acc_name_text != "DevGuard"
                ):

                    login_error = "That account name is reserved"
                    login_error_timer = 60


                elif acc_name_text in accounts or acc_name_text in player_accounts:

                    login_error = "Acc name or Password already exists: Dont Hack"
                    login_error_timer = 60


                else:

                    player_accounts[acc_name_text] = password_text
                    with open("accounts.json", "w") as file:
                        json.dump(player_accounts, file)

                    create_account()

            # inventory button

            # Clicks that land inside an open sliding panel must not
            # reach the buttons underneath it.  The hp upgrade button
            # is excluded and always stays clickable.  Only panels
            # that are currently open block clicks.
            ui_click_blocked = (
                (
                    new_button_panel_open
                    and new_button_panel_rect.collidepoint(event.pos)
                )
                or (
                    settings_panel_open
                    and settings_panel_rect.collidepoint(event.pos)
                )
                or (
                    cmd_panel_open
                    and cmd_panel_rect.collidepoint(event.pos)
                )
                or (
                    craft_open
                    and craft_panel_rect.collidepoint(event.pos)
                )
                or (
                    inventory_open
                    and inventory_panel_rect.collidepoint(event.pos)
                )
            )

            if (
                above_inventory_button_rect.collidepoint(
                    event.pos
                )
                and not ui_click_blocked
            ):
                open_only_panel(
                    None if craft_open else "craft"
                )

            if (
                above_craft_button_rect.collidepoint(
                    event.pos
                )
                and not ui_click_blocked
            ):
                open_only_panel(
                    None if new_button_panel_open else "gallery"
                )

            if (
                settings_button_rect.collidepoint(
                    event.pos
                )
                and not ui_click_blocked
            ):
                open_only_panel(
                    None if settings_panel_open else "settings"
                )

            if (
                cmd_button_rect.collidepoint(
                    event.pos
                )
                and not ui_click_blocked
            ):
                open_only_panel(
                    None if cmd_panel_open else "cmd"
                )

            # Grab the mob hp bar size slider (or jump it to the
            # click position).
            if (
                settings_panel_open
                and event.button == 1
                and settings_hp_bar_track_rect.inflate(
                    0, 24
                ).collidepoint(event.pos)
            ):
                settings_hp_bar_dragging = True
                settings_hp_bar_knob_progress = min(
                    1.0,
                    max(
                        0.0,
                        (
                            mouse_x
                            - settings_hp_bar_track_rect.left
                            - 12
                        )
                        / max(
                            1,
                            settings_hp_bar_track_rect.width - 24
                        )
                    )
                )
                settings_hp_bar_scale = (
                    1 + settings_hp_bar_knob_progress * 2
                )

            # Clicking the switch toggles it on or off.
            if (
                settings_panel_open
                and event.button == 1
                and settings_switch_rect.inflate(
                    6, 6
                ).collidepoint(event.pos)
            ):
                settings_switch_on = not settings_switch_on
                save_settings()

            # Clicking the second switch toggles it on or off.
            if (
                settings_panel_open
                and event.button == 1
                and settings_switch2_rect.inflate(
                    6, 6
                ).collidepoint(event.pos)
            ):
                settings_switch2_on = not settings_switch2_on
                save_settings()

            # Clicking the third switch toggles it on or off.
            if (
                settings_panel_open
                and event.button == 1
                and settings_switch3_rect.inflate(
                    6, 6
                ).collidepoint(event.pos)
            ):
                settings_switch3_on = not settings_switch3_on
                save_settings()

            if new_button_panel_open and event.button == 1:
                if mob_gallery_scrollbar_rect.collidepoint(event.pos):
                    mob_gallery_dragging = True
                elif mob_gallery_horizontal_scrollbar_rect.collidepoint(
                    event.pos
                ):
                    mob_gallery_x_dragging = True

            craft_button_hit_rect = pygame.Rect(
                craft_panel_rect.right - 82,
                craft_panel_rect.y + 76,
                70,
                38
            )
            craft_result_rect = pygame.Rect(
                craft_panel_rect.centerx - 55 - 19,
                craft_panel_rect.y + 95 - 19,
                38,
                38
            )
            if (
                craft_open
                and craft_result_item is not None
                and not craft_animation_active
                and craft_result_rect.collidepoint(event.pos)
            ):
                result_rarity_index = (
                    RARITIES.index(craft_result_item["rarity"])
                    if craft_result_item["rarity"] in RARITIES
                    else 0
                )
                follow_up_rarity = RARITIES[max(0, result_rarity_index - 1)]
                craft_post_result_items = [
                    {
                        "petal": craft_result_item["petal"],
                        "rarity": follow_up_rarity,
                        "amount": 1
                    }
                    for _ in range(random.randint(1, 4))
                ]
                craft_result_item = None
                craft_selected_items = []
                craft_result_text = ""

            if (
                craft_open
                and craft_button_hit_rect.collidepoint(event.pos)
            ):
                start_craft()

            if (
                craft_open
                and craft_scrollbar_rect.collidepoint(event.pos)
            ):
                craft_dragging = True
                craft_drag_offset = event.pos[1] - craft_scrollbar_rect.y

            if (
                craft_open
                and craft_horizontal_scrollbar_rect.collidepoint(event.pos)
            ):
                craft_x_dragging = True
                craft_x_drag_offset = event.pos[0] - craft_horizontal_scrollbar_rect.x

            if craft_open and craft_panel_rect.y < HEIGHT + 20:
                craft_slot_size = 38
                craft_center_x = craft_panel_rect.centerx - 55
                craft_center_y = craft_panel_rect.y + 95
                craft_radius = 55
                craft_slot_points = [
                    (
                        int(
                            craft_center_x
                            + math.cos(-math.pi / 2 + i * 2 * math.pi / 5)
                            * craft_radius
                        ),
                        int(
                            craft_center_y
                            + math.sin(-math.pi / 2 + i * 2 * math.pi / 5)
                            * craft_radius
                        )
                    )
                    for i in range(5)
                ]

                clicked_craft_slot = any(
                    pygame.Rect(
                        point_x - craft_slot_size // 2,
                        point_y - craft_slot_size // 2,
                        craft_slot_size,
                        craft_slot_size
                    ).collidepoint(event.pos)
                    for point_x, point_y in craft_slot_points
                )
                if (
                    clicked_craft_slot
                    and craft_selected_items
                    and not craft_animation_active
                ):
                    craft_selected_items = []
                    save_player()
                elif (
                    clicked_craft_slot
                    and craft_post_result_items
                    and not craft_animation_active
                ):
                    post_result_counts = {}
                    for remaining_item in craft_post_result_items:
                        item_key = (
                            remaining_item["petal"],
                            remaining_item["rarity"]
                        )
                        post_result_counts[item_key] = (
                            post_result_counts.get(item_key, 0)
                            + remaining_item.get("amount", 1)
                        )

                    for (petal, rarity), desired_amount in (
                        post_result_counts.items()
                    ):
                        current_amount = sum(
                            int(item.get("amount", 1))
                            for item in inventory
                            if (
                                item.get("petal"),
                                item.get("rarity")
                            ) == (petal, rarity)
                        )
                        if current_amount > desired_amount:
                            remove_inventory_petal(
                                petal,
                                rarity,
                                current_amount - desired_amount
                            )
                        elif current_amount < desired_amount:
                            add_inventory_petal(
                                petal,
                                rarity,
                                desired_amount - current_amount
                            )
                    craft_post_result_items = []
                    save_player()

                craft_grid_rect = pygame.Rect(
                    craft_panel_rect.x + 10,
                    craft_panel_rect.bottom - 350,
                    craft_panel_rect.width - 40,
                    325
                )
                if (
                    craft_grid_rect.collidepoint(event.pos)
                    and not craft_animation_active
                ):
                    craft_row_height = 42
                    craft_cell_width = 42
                    first_row = int(craft_scroll_position)
                    first_column = int(craft_horizontal_scroll_position)
                    grid_x = (
                        craft_panel_rect.x + 10
                        - (
                            craft_horizontal_scroll_position - first_column
                        ) * craft_cell_width
                    )
                    grid_y = (
                        craft_panel_rect.bottom - 350
                        - (craft_scroll_position - first_row)
                        * craft_row_height
                    )
                    clicked_col = int(
                        (event.pos[0] - grid_x) / craft_cell_width
                    )
                    clicked_row = int(
                        (event.pos[1] - grid_y) / craft_row_height
                    )
                    craft_petals = craft_petals_cache
                    craft_rarities = craft_rarities_cache
                    petal_index = first_row + clicked_row
                    rarity_index = first_column + clicked_col

                    if (
                        0 <= petal_index < len(craft_petals)
                        and 0 <= rarity_index < len(craft_rarities)
                    ):
                        selected_key = (
                            craft_petals[petal_index],
                            craft_rarities[rarity_index]
                        )
                        matching_items = [
                            item for item in inventory
                            if (
                                item.get("petal"),
                                item.get("rarity")
                            ) == selected_key
                        ]
                        total_amount = sum(
                            int(item.get("amount", 1))
                            for item in matching_items
                        )
                        if total_amount >= 5 and selected_key[1] != "Infino":
                            craft_post_result_items = []
                            craft_result_item = None
                            craft_result_text = ""
                            alt_clicked = bool(
                                pygame.key.get_mods() & pygame.KMOD_ALT
                            )
                            shift_clicked = bool(
                                pygame.key.get_mods() & pygame.KMOD_SHIFT
                            )
                            same_selection = (
                                craft_selected_items
                                and craft_selected_items[0]["petal"]
                                == selected_key[0]
                                and craft_selected_items[0]["rarity"]
                                == selected_key[1]
                            )
                            if shift_clicked:
                                base_amount, remainder = divmod(
                                    total_amount,
                                    5
                                )
                                craft_selected_items = [
                                    {
                                        "petal": selected_key[0],
                                        "rarity": selected_key[1],
                                        "amount": base_amount
                                        + (1 if slot_index < remainder else 0)
                                    }
                                    for slot_index in range(5)
                                ]
                            elif not same_selection:
                                craft_selected_items = [
                                    {
                                        "petal": selected_key[0],
                                        "rarity": selected_key[1],
                                        "amount": 1
                                    }
                                    for _ in range(5)
                                ]
                            else:
                                selected_amount = sum(
                                    item["amount"]
                                    for item in craft_selected_items
                                )
                                remaining_amount = total_amount - selected_amount
                                if remaining_amount >= 5:
                                    for item in craft_selected_items:
                                        item["amount"] += 1
                                elif remaining_amount > 0:
                                    for slot_index in range(remaining_amount):
                                        craft_selected_items[slot_index]["amount"] += 1

                            if alt_clicked and not shift_clicked:
                                craft_selected_items = [
                                    {
                                        "petal": selected_key[0],
                                        "rarity": selected_key[1],
                                        "amount": 1
                                    }
                                    for _ in range(5)
                                ]
                            if alt_clicked:
                                start_craft()
                            save_player()

            if (
                inventory_button_rect.collidepoint(
                    event.pos
                )
                and not ui_click_blocked
            ):

                open_only_panel(
                    None if inventory_open else "inventory"
                )

            if inventory_open:

                if event.button == 4:  # scroll up
                    inventory_scroll -= 1

                if event.button == 5:  # scroll down
                    inventory_scroll += 1


                total_rows = get_inventory_total_rows()

                max_rows = get_inventory_max_rows()

                max_scroll = max(
                    0,
                    total_rows - max_rows
                )

                inventory_scroll = max(
                    0,
                    min(inventory_scroll, max_scroll)
                )

        if event.type == pygame.KEYDOWN:

            if game_state == "login":

                if active_input == "password":

                    if event.key == pygame.K_BACKSPACE:
                        password_text = password_text[:-1]

                    elif event.key != pygame.K_RETURN:
                        password_text += event.unicode


                elif active_input == "acc_name":

                    if event.key == pygame.K_BACKSPACE:
                        acc_name_text = acc_name_text[:-1]

                    elif event.key != pygame.K_RETURN:
                        acc_name_text += event.unicode

            if game_state == "game":
                if event.key == pygame.K_RETURN:
                    if chat_text_visible:
                        # Pressing Enter while prompt is shown opens the chat box for typing
                        chat_text_visible = False
                    else:
                        # Pressing Enter while typing sends the message
                        if chat_input_text:
                            if chat_input_text.startswith("/"):
                                parts = chat_input_text.split()
                                cmd = parts[0]
                                if cmd in ("/spawn_enemy", "/spawn_custom_enemy") and acc_name_text.lower() == "devguard":
                                    # /spawn_enemy [rarity] [mob] [amount]
                                    # OR /spawn_enemy [rarity] [mob] [mob damage] [mob health] [mob xp] [optional amount]
                                    args = parts[1:]
                                    if len(args) < 2:
                                        show_error("Usage: /spawn_enemy [rarity] [mob] [damage] [health] [xp]")
                                    else:
                                        rarity = args[0].capitalize()
                                        enemy_classes = {
                                            "Ladybug": (Ladybug, ladybugs),
                                            "Hole Ladybug": (HoleLadybug, hole_ladybugs),
                                            "HoleLadybug": (HoleLadybug, hole_ladybugs),
                                            "Hole Bee": (HoleBee, hole_bees),
                                            "HoleBee": (HoleBee, hole_bees),
                                            "Hole Spider": (HoleSpider, hole_spiders),
                                            "HoleSpider": (HoleSpider, hole_spiders),
                                            "Hole Rock": (HoleRock, hole_rocks),
                                            "HoleRock": (HoleRock, hole_rocks),
                                            "Hole Hornet": (HoleHornet, hole_hornets),
                                            "HoleHornet": (HoleHornet, hole_hornets),
                                            "Hole Baby Ant": (HoleBabyAnt, hole_baby_ants),
                                            "HoleBabyAnt": (HoleBabyAnt, hole_baby_ants),
                                            "Hole Soldier Ant": (HoleSoldierAnt, hole_soldier_ants),
                                            "HoleSoldierAnt": (HoleSoldierAnt, hole_soldier_ants),
                                            "Hole Worker Ant": (HoleWorkerAnt, hole_worker_ants),
                                            "HoleWorkerAnt": (HoleWorkerAnt, hole_worker_ants),
                                            "Bee": (Bee, bees),
                                            "Spider": (Spider, spiders),
                                            "Rock": (Rock, rocks),
                                            "Hornet": (Hornet, hornets),
                                            "Baby Ant": (BabyAnt, baby_ants),
                                            "Soldier Ant": (SoldierAnt, soldier_ants),
                                            "BabyAnt": (BabyAnt, baby_ants),
                                            "SoldierAnt": (SoldierAnt, soldier_ants),
                                            "Worker Ant": (WorkerAnt, worker_ants),
                                            "WorkerAnt": (WorkerAnt, worker_ants),
                                            "Queen Ant": (QueenAnt, queen_ants),
                                            "QueenAnt": (QueenAnt, queen_ants),
                                            "Hole Queen Ant": (HoleQueenAnt, hole_queen_ants),
                                            "HoleQueenAnt": (HoleQueenAnt, hole_queen_ants),
                                            "Ant Egg": (AntEgg, ant_eggs),
                                            "AntEgg": (AntEgg, ant_eggs),
                                        }
                                        mob_type = None
                                        trailing_args = []
                                        if len(args) >= 3:
                                            # Try 2-word mob names first
                                            two_word = args[1] + " " + args[2]
                                            for key in enemy_classes:
                                                if key.lower() == two_word.lower():
                                                    mob_type = key
                                                    trailing_args = args[3:]
                                                    break
                                        if mob_type is None and len(args) >= 2:
                                            # Try single-word mob names
                                            for key in enemy_classes:
                                                if key.lower() == args[1].lower():
                                                    mob_type = key
                                                    trailing_args = args[2:]
                                                    break

                                        amount = 1
                                        custom_damage = None
                                        custom_hp = None
                                        custom_xp = None

                                        if len(trailing_args) >= 3:
                                            # Custom stats: [mob damage] [mob health] [mob xp] [optional amount]
                                            try:
                                                custom_damage = float(trailing_args[0])
                                                custom_hp = float(trailing_args[1])
                                                custom_xp = int(trailing_args[2])
                                                if len(trailing_args) >= 4:
                                                    amount = max(1, int(trailing_args[3]))
                                            except ValueError:
                                                show_error("Damage, health, and xp must be numbers")
                                                mob_type = None
                                        elif len(trailing_args) == 1:
                                            try:
                                                amount = max(1, int(trailing_args[0]))
                                            except ValueError:
                                                amount = 1

                                        if mob_type is not None:
                                            enemy_class = None
                                            for key in enemy_classes:
                                                if key.lower() == mob_type.lower():
                                                    enemy_class = enemy_classes[key]
                                                    break
                                            if enemy_class:
                                                mob_class, mob_list = enemy_class
                                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                                world_x = mouse_x + camera_x
                                                world_y = mouse_y + camera_y
                                                # Mobs from hole land cannot be spawned to regular biome
                                                if current_dimension == "regular" and getattr(mob_class, "is_hole_land_mob", False):
                                                    show_error("Hole land mobs cannot be spawned in regular biomes!")
                                                    continue
                                                for _ in range(amount):
                                                    enemy = mob_class()
                                                    enemy.rarity = rarity
                                                    apply_enemy_rarity_stats(enemy)
                                                    enemy.x = max(enemy.radius, min(world_x, WORLD_WIDTH - enemy.radius))
                                                    enemy.y = max(enemy.radius, min(world_y, WORLD_HEIGHT - enemy.radius))
                                                    if custom_damage is not None:
                                                        enemy.damage = int(custom_damage)
                                                        enemy.custom_damage = int(custom_damage)
                                                    if custom_hp is not None:
                                                        enemy.max_hp = int(custom_hp)
                                                        enemy.hp = int(custom_hp)
                                                    if custom_xp is not None:
                                                        enemy.custom_xp = int(custom_xp)
                                                    mob_list.append(enemy)
                                            else:
                                                valid_mobs = ", ".join(enemy_classes.keys())
                                                show_error(f"Invalid mob type. Valid: {valid_mobs}")
                                        else:
                                            valid_mobs = ", ".join(enemy_classes.keys())
                                            show_error(f"Invalid mob type. Valid: {valid_mobs}")
                                elif cmd == "/me":
                                    # /me [action] - roleplay action in chat
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /me [action]")
                                    elif acc_name_text in muted_users:
                                        show_error("You are muted and can't chat")
                                    elif not is_bad_word(" ".join(args)):
                                        chat_messages.append(
                                            (
                                f"* {acc_name_text}",
                                                " ".join(args),
                                                time.time()
                                            )
                                        )
                                    else:
                                        show_error("The chat does not allow bad words")
                                elif cmd == "/whisper":
                                    # /whisper [user] [message] - private
                                    # message only between the two players
                                    args = parts[1:]
                                    if len(args) < 2:
                                        show_error("Usage: /whisper [user] [message]")
                                    elif acc_name_text in muted_users:
                                        show_error("You are muted and can't chat")
                                    elif not is_bad_word(" ".join(args[1:])):
                                        whisper_target = args[0]
                                        account_names = [
                                            name
                                            for name in player_accounts
                                        ]
                                        if whisper_target.lower() not in [
                                            n.lower() for n in account_names
                                        ]:
                                            show_error(
                                                f"{whisper_target} does not exist"
                                            )
                                        else:
                                            online_names = [
                                                sender
                                                for sender, msg, t in chat_messages
                                                if not sender.startswith("* ")
                                            ]
                                            online_names.append(acc_name_text)
                                            if whisper_target.lower() not in [
                                                n.lower() for n in online_names
                                            ]:
                                                show_error(
                                                    f"{whisper_target} is not playing right now"
                                                )
                                            else:
                                                chat_messages.append(
                                                    (
                                                        f"* {acc_name_text} (whisper to {whisper_target})",
                                                        " ".join(args[1:]),
                                                        time.time()
                                                    )
                                                )
                                    else:
                                        show_error("The chat does not allow bad words")
                                elif cmd == "/stats":
                                    # /stats - show your own stats
                                    total_petals = sum(
                                        int(item.get("amount", 1))
                                        for item in inventory
                                    )
                                    show_error(
                                        f"Level: {flower_level} | "
                                        f"XP: {int(flower_xp)}/{int(flower_xp_needed)} | "
                                        f"Points: {upgrade_points} | "
                                        f"Inventory petals: {total_petals}"
                                    )
                                elif cmd == "/equip" and acc_name_text.lower() == "devguard":
                                    # /equip [rarity] [petal] [petal slot]
                                    args = parts[1:]
                                    if len(args) < 3:
                                        show_error("Usage: /equip [rarity] [petal] [petal slot]")
                                    else:
                                        rarity = args[0]
                                        try:
                                            slot_index = int(args[-1])
                                        except ValueError:
                                            slot_index = None
                                        # Support multi-word petal names (e.g. "Baby Ant")
                                        petal_name = None
                                        if slot_index is not None:
                                            petal_name = find_petal_name(
                                                " ".join(args[1:-1])
                                            )
                                        if slot_index is None:
                                            show_error("Petal slot must be a number")
                                        elif petal_name is None:
                                            show_error(f"Invalid petal type. Valid: {', '.join(PETAL_HP.keys())}")
                                        elif dev_equip_petal(rarity, petal_name, slot_index):
                                            show_error(f"Equipped {rarity.capitalize()} {petal_name} in slot {slot_index}")
                                elif cmd == "/all_equip" and acc_name_text.lower() == "devguard":
                                    # /all_equip [rarity] [petal]
                                    args = parts[1:]
                                    if len(args) < 2:
                                        show_error("Usage: /all_equip [rarity] [petal]")
                                    else:
                                        rarity = args[0]
                                        petal_name = find_petal_name(
                                            " ".join(args[1:])
                                        )
                                        if petal_name is None:
                                            show_error(f"Invalid petal type. Valid: {', '.join(PETAL_HP.keys())}")
                                        elif dev_equip_all_petal(rarity, petal_name):
                                            show_error(f"Equipped {rarity.capitalize()} {petal_name} in all slots")
                                elif cmd == "/empty" and acc_name_text.lower() == "devguard":
                                    # /empty [petal slot]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /empty [petal slot]")
                                    else:
                                        try:
                                            slot_index = int(args[0])
                                        except ValueError:
                                            slot_index = None
                                        if slot_index is None:
                                            show_error("Petal slot must be a number")
                                        elif dev_empty_slot(slot_index):
                                            show_error(f"Emptied slot {slot_index}")
                                elif cmd == "/empty_all" and acc_name_text.lower() == "devguard":
                                    # /empty_all
                                    dev_empty_all_slots()
                                    show_error("Emptied all petal slots")
                                elif cmd == "/ban" and acc_name_text.lower() == "devguard":
                                    # /ban [user]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /ban [user]")
                                    else:
                                        dev_ban_user(" ".join(args))
                                elif cmd == "/mute" and acc_name_text.lower() == "devguard":
                                    # /mute [user]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /mute [user]")
                                    else:
                                        dev_mute_user(" ".join(args), True)
                                elif cmd == "/unmute" and acc_name_text.lower() == "devguard":
                                    # /unmute [user]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /unmute [user]")
                                    else:
                                        dev_mute_user(" ".join(args), False)
                                elif cmd == "/gift" and acc_name_text.lower() == "devguard":
                                    # /gift [user] [rarity] [petal] [amount]
                                    args = parts[1:]
                                    if len(args) < 4:
                                        show_error("Usage: /gift [user] [rarity] [petal] [amount]")
                                    else:
                                        target_name = args[0]
                                        rarity = args[1]
                                        try:
                                            amount = int(args[-1])
                                        except ValueError:
                                            amount = None
                                        petal_name = None
                                        if amount is not None:
                                            petal_name = find_petal_name(
                                                " ".join(args[2:-1])
                                            )
                                        if amount is None:
                                            show_error("Amount must be a number")
                                        elif petal_name is None:
                                            show_error(f"Invalid petal type. Valid: {', '.join(PETAL_HP.keys())}")
                                        else:
                                            dev_gift_user(target_name, rarity, petal_name, amount)
                                elif cmd == "/take" and acc_name_text.lower() == "devguard":
                                    # /take [rarity] [petal] [amount] from.[user]
                                    args = parts[1:]
                                    if len(args) < 4 or not args[-1].startswith("from."):
                                        show_error("Usage: /take [rarity] [petal] [amount] from.[user]")
                                    else:
                                        target_name = args[-1][len("from."):]
                                        rarity = args[0]
                                        try:
                                            amount = int(args[-2])
                                        except ValueError:
                                            amount = None
                                        petal_name = None
                                        if amount is not None:
                                            petal_name = find_petal_name(
                                                " ".join(args[1:-2])
                                            )
                                        if amount is None:
                                            show_error("Amount must be a number")
                                        elif petal_name is None:
                                            show_error(f"Invalid petal type. Valid: {', '.join(PETAL_HP.keys())}")
                                        elif not target_name:
                                            show_error("Usage: /take [rarity] [petal] [amount] from.[user]")
                                        else:
                                            dev_take_petal(target_name, rarity, petal_name, amount)
                                elif cmd == "/kick" and acc_name_text.lower() == "devguard":
                                    # /kick [user]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /kick [user]")
                                    else:
                                        dev_kick_user(" ".join(args))
                                elif cmd == "/give_points" and acc_name_text.lower() == "devguard":
                                    # /give_points [user] [amount]
                                    args = parts[1:]
                                    if len(args) < 2:
                                        show_error("Usage: /give_points [user] [amount]")
                                    else:
                                        try:
                                            amount = int(args[-1])
                                        except ValueError:
                                            amount = None
                                        if amount is None:
                                            show_error("Amount must be a number")
                                        elif amount < 1:
                                            show_error("Amount must be at least 1")
                                        else:
                                            dev_give_points(" ".join(args[:-1]), amount)
                                elif cmd == "/tp" and acc_name_text.lower() == "devguard":
                                    # /tp [user]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /tp [user]")
                                    else:
                                        dev_tp_user(" ".join(args))
                                elif cmd == "/announce" and acc_name_text.lower() == "devguard":
                                    # /announce [message]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /announce [message]")
                                    else:
                                        show_announcement(" ".join(args))
                                elif cmd == "/self_heal" and acc_name_text.lower() == "devguard":
                                    # /self_heal [amount]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /self_heal [amount]")
                                    else:
                                        try:
                                            amount = int(args[0])
                                        except ValueError:
                                            amount = None
                                        if amount is None:
                                            show_error("Amount must be a number")
                                        else:
                                            dev_self_heal(amount)
                                elif cmd == "/heal_user" and acc_name_text.lower() == "devguard":
                                    # /heal_user [user] [amount]
                                    args = parts[1:]
                                    if len(args) < 2:
                                        show_error("Usage: /heal_user [user] [amount]")
                                    else:
                                        try:
                                            amount = int(args[-1])
                                        except ValueError:
                                            amount = None
                                        if amount is None:
                                            show_error("Amount must be a number")
                                        else:
                                            dev_heal_user(" ".join(args[:-1]), amount)
                                elif cmd == "/full_heal_user" and acc_name_text.lower() == "devguard":
                                    # /full_heal_user [user]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /full_heal_user [user]")
                                    else:
                                        dev_heal_user(" ".join(args), 0, full=True)
                                elif cmd == "/king" and acc_name_text.lower() == "devguard":
                                    # /king - turn the enemy under the
                                    # mouse into a king
                                    mouse_x, mouse_y = pygame.mouse.get_pos()
                                    king_target = None
                                    for enemy in all_enemies:
                                        if not enemy.alive:
                                            continue
                                        if getattr(enemy, "dying", False):
                                            continue
                                        if distance(
                                            mouse_x,
                                            mouse_y,
                                            enemy.x - camera_x,
                                            enemy.y - camera_y
                                        ) <= enemy.radius:
                                            king_target = enemy
                                            break
                                    if king_target is None:
                                        show_error("No enemy under your mouse")
                                    else:
                                        dev_make_king(king_target)
                                elif cmd == "/freez_enemies" and acc_name_text.lower() == "devguard":
                                    # /freez_enemies [seconds]
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /freez_enemies [seconds]")
                                    else:
                                        try:
                                            seconds = int(args[0])
                                        except ValueError:
                                            seconds = None
                                        if seconds is None:
                                            show_error("Amount must be a number")
                                        else:
                                            dev_freeze_enemies(seconds)
                                elif cmd == "/unfreeze" and acc_name_text.lower() == "devguard":
                                    # /unfreeze - unfreeze all enemies
                                    enemies_frozen_timer = 0
                                    show_error("Enemies unfrozen")
                                elif cmd in ("/magnet_petal_drops", "/magnet") and acc_name_text.lower() == "devguard":
                                    # /magnet_petal_drops [state] [size] - pull petal drops within [size] range (or whole map)
                                    args = parts[1:]
                                    if len(args) < 1 or args[0].lower() not in ("on", "off", "true", "false", "1", "0", "y", "n"):
                                        show_error("Usage: /magnet_petal_drops [state] [size]")
                                    elif args[0].lower() in ("on", "true", "1", "y"):
                                        player_magnet = True
                                        if len(args) >= 2:
                                            try:
                                                player_magnet_range = max(10.0, float(args[1]))
                                                show_error(f"Magnet ON (range: {int(player_magnet_range)})")
                                            except ValueError:
                                                player_magnet_range = None
                                                show_error("Magnet ON (all drops)")
                                        else:
                                            player_magnet_range = None
                                            show_error("Magnet ON (all drops)")
                                    else:
                                        player_magnet = False
                                        show_error("Magnet OFF")
                                elif cmd == "/trail_size" and acc_name_text.lower() == "devguard":
                                    # /trail_size [size] - adjust trail particle size multiplier
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /trail_size [size]")
                                    else:
                                        try:
                                            new_size = float(args[0])
                                            if new_size <= 0:
                                                show_error("Size must be greater than 0")
                                            else:
                                                player_trail_size_mult = min(10.0, max(0.1, new_size))
                                                show_error(f"Trail size set to {player_trail_size_mult}x")
                                        except ValueError:
                                            show_error("Size must be a number")
                                elif cmd in ("/hud", "/p.hud", "/pick.hud") and acc_name_text.lower() == "devguard":
                                    # /hud [state] (on/off) - toggle HUD visibility
                                    args = parts[1:]
                                    if len(args) < 1 or args[0].lower() not in ("on", "off", "true", "false", "1", "0", "y", "n"):
                                        show_error("Usage: /hud [state] (on/off)")
                                    elif args[0].lower() in ("on", "true", "1", "y"):
                                        show_hud = True
                                        show_error("HUD ON")
                                    else:
                                        show_hud = False
                                        show_error("HUD OFF")
                                elif cmd == "/reload_petals" and acc_name_text.lower() == "devguard":
                                    # /reload_petals - instantly reload and restore all equipped petals to full HP
                                    for i in range(PETAL_SLOTS):
                                        if petal_slots[i]["filled"]:
                                            petal_alive[i] = True
                                            petal_hp[i] = petal_max_hp[i]
                                            petal_cooldowns[i] = 0
                                            petal_respawn_timer[i] = 0
                                            petal_deploy[i] = 1.0
                                            if petal_slots[i]["petal"] == "Light":
                                                light_count = get_petal_count("Light", petal_slots[i]["rarity"])
                                                light_hp[i] = [petal_max_hp[i]] * light_count
                                                light_cooldowns[i] = [0] * light_count
                                                light_alive[i] = [True] * light_count
                                    show_error("All petals reloaded to max HP!")
                                elif cmd == "/spawn_whirlpool" and acc_name_text.lower() == "devguard":
                                    # /spawn_whirlpool [damage] [damage each second] [whirlpool last seconds] [whirlpool size]
                                    # Traps enemies inside, pulls them toward center, and deals continuous dps (or infinity spam attack)
                                    args = parts[1:]
                                    if len(args) < 4:
                                        show_error("Usage: /spawn_whirlpool [damage] [damage each second] [whirlpool last seconds] [whirlpool size]")
                                    else:
                                        try:
                                            wp_init_dmg = float(args[0])
                                            dps_arg = args[1].strip().lower()
                                            if dps_arg in ("infinity", "inf", "spam"):
                                                wp_dps = "infinity"
                                            else:
                                                wp_dps = float(dps_arg)
                                            wp_duration = max(0.5, float(args[2]))
                                            wp_radius = max(20.0, float(args[3]))
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            wp_world_x = mouse_x + camera_x
                                            wp_world_y = mouse_y + camera_y
                                            active_whirlpools.append({
                                                "x": wp_world_x,
                                                "y": wp_world_y,
                                                "initial_damage": wp_init_dmg,
                                                "dps": wp_dps,
                                                "duration": wp_duration,
                                                "max_duration": wp_duration,
                                                "radius": wp_radius,
                                                "damage_timer": 0.0,
                                                "angle": 0.0,
                                                "hit_enemies": set(),
                                            })
                                            dps_label = "infinity spam" if wp_dps == "infinity" else f"{wp_dps}/s"
                                            show_error(f"Whirlpool spawned! (dps: {dps_label}, size: {int(wp_radius)}, {wp_duration}s)")
                                        except ValueError:
                                            show_error("Damage, duration, and size must be numbers (dps can also be 'infinity')")
                                elif cmd == "/spawn_blackhole" and acc_name_text.lower() == "devguard":
                                    # /spawn_blackhole [pull speed] [duration] [size]
                                    # Pulls enemies and petal drops inward toward an event horizon
                                    args = parts[1:]
                                    if len(args) < 3:
                                        show_error("Usage: /spawn_blackhole [pull speed] [duration] [size]")
                                    else:
                                        try:
                                            bh_speed = max(10.0, float(args[0]))
                                            bh_duration = max(0.5, float(args[1]))
                                            bh_radius = max(20.0, float(args[2]))
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            bh_world_x = mouse_x + camera_x
                                            bh_world_y = mouse_y + camera_y
                                            active_blackholes.append({
                                                "x": bh_world_x,
                                                "y": bh_world_y,
                                                "pull_speed": bh_speed,
                                                "duration": bh_duration,
                                                "max_duration": bh_duration,
                                                "radius": bh_radius,
                                                "angle": 0.0,
                                            })
                                            show_error(f"Black hole spawned! (pull: {bh_speed}, size: {int(bh_radius)}, {bh_duration}s)")
                                        except ValueError:
                                            show_error("Pull speed, duration, and size must be numbers")
                                elif cmd == "/delete_blackholes" and acc_name_text.lower() == "devguard":
                                    # /delete_blackholes [amount] or /delete_blackholes
                                    args = parts[1:]
                                    if len(active_blackholes) == 0:
                                        show_error("No active black holes to delete")
                                    else:
                                        if len(args) >= 1:
                                            try:
                                                del_cnt = int(args[0])
                                                del_cnt = max(1, min(del_cnt, len(active_blackholes)))
                                                del active_blackholes[:del_cnt]
                                                show_error(f"Deleted {del_cnt} black hole(s)")
                                            except ValueError:
                                                show_error("Amount must be a whole number")
                                        else:
                                            cleared = len(active_blackholes)
                                            active_blackholes.clear()
                                            show_error(f"Deleted all ({cleared}) black hole(s)")
                                elif cmd == "/spawn_shield_dome" and acc_name_text.lower() == "devguard":
                                    # /spawn_shield_dome [radius] [duration]
                                    # Spawns a protective energy dome that repels enemies and deflects projectiles
                                    args = parts[1:]
                                    if len(args) < 2:
                                        show_error("Usage: /spawn_shield_dome [radius] [duration]")
                                    else:
                                        try:
                                            sd_radius = max(20.0, float(args[0]))
                                            sd_duration = max(0.5, float(args[1]))
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            sd_world_x = mouse_x + camera_x
                                            sd_world_y = mouse_y + camera_y
                                            active_shield_domes.append({
                                                "x": sd_world_x,
                                                "y": sd_world_y,
                                                "radius": sd_radius,
                                                "duration": sd_duration,
                                                "max_duration": sd_duration,
                                                "pulse": 0.0,
                                            })
                                            show_error(f"Shield dome spawned! (radius: {int(sd_radius)}, {sd_duration}s)")
                                        except ValueError:
                                            show_error("Radius and duration must be numbers")
                                elif cmd == "/delete_shield_domes" and acc_name_text.lower() == "devguard":
                                    # /delete_shield_domes [amount] or /delete_shield_domes
                                    args = parts[1:]
                                    if len(active_shield_domes) == 0:
                                        show_error("No active shield domes to delete")
                                    else:
                                        if len(args) >= 1:
                                            try:
                                                del_cnt = int(args[0])
                                                del_cnt = max(1, min(del_cnt, len(active_shield_domes)))
                                                del active_shield_domes[:del_cnt]
                                                show_error(f"Deleted {del_cnt} shield dome(s)")
                                            except ValueError:
                                                show_error("Amount must be a whole number")
                                        else:
                                            cleared = len(active_shield_domes)
                                            active_shield_domes.clear()
                                            show_error(f"Deleted all ({cleared}) shield dome(s)")

                                    # /delete_whirlpools [amount] or /delete_whirlpools - clear whirlpools
                                    args = parts[1:]
                                    if len(active_whirlpools) == 0:
                                        show_error("No active whirlpools to delete")
                                    else:
                                        if len(args) >= 1:
                                            try:
                                                del_cnt = int(args[0])
                                                del_cnt = max(1, min(del_cnt, len(active_whirlpools)))
                                                del active_whirlpools[:del_cnt]
                                                show_error(f"Deleted {del_cnt} whirlpool(s)")
                                            except ValueError:
                                                show_error("Amount must be a whole number")
                                        else:
                                            cleared = len(active_whirlpools)
                                            active_whirlpools.clear()
                                            show_error(f"Deleted all ({cleared}) whirlpool(s)")
                                elif cmd == "/godmode" and acc_name_text.lower() == "devguard":
                                    # /godmode [state] - toggle complete invincibility
                                    args = parts[1:]
                                    if len(args) < 1 or args[0].lower() not in ("on", "off", "true", "false", "1", "0", "y", "n"):
                                        show_error("Usage: /godmode [state] (on/off)")
                                    elif args[0].lower() in ("on", "true", "1", "y"):
                                        player_godmode = True
                                        player_hp = PLAYER_MAX_HP
                                        show_error("Godmode ON")
                                    else:
                                        player_godmode = False
                                        show_error("Godmode OFF")
                                elif cmd in ("/speed", "/p.speed") and acc_name_text.lower() == "devguard":
                                    # /speed [multiplier] - adjust player movement speed
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /speed [multiplier]")
                                    else:
                                        try:
                                            mult = float(args[0])
                                            if mult <= 0 or mult > 20:
                                                show_error("Multiplier must be between 0.1 and 20")
                                            else:
                                                player_speed_mult = mult
                                                show_error(f"Player speed set to {mult}x")
                                        except ValueError:
                                            show_error("Multiplier must be a number")
                                elif cmd == "/tp_pos" and acc_name_text.lower() == "devguard":
                                    # /tp_pos [x] [y] - teleport player to coordinates
                                    args = parts[1:]
                                    if len(args) < 2:
                                        show_error("Usage: /tp_pos [x] [y]")
                                    else:
                                        try:
                                            tx = float(args[0])
                                            ty = float(args[1])
                                            player_x = max(PLAYER_RADIUS, min(tx, WORLD_WIDTH - PLAYER_RADIUS))
                                            player_y = max(PLAYER_RADIUS, min(ty, WORLD_HEIGHT - PLAYER_RADIUS))
                                            show_error(f"Teleported to ({int(player_x)}, {int(player_y)})")
                                        except ValueError:
                                            show_error("Coordinates must be numbers")
                                elif cmd == "/clear_chat" and acc_name_text.lower() == "devguard":
                                    # /clear_chat - clear all messages in the chat history
                                    chat_messages.clear()
                                    show_error("Chat cleared")
                                elif cmd == "/clean_drops" and acc_name_text.lower() == "devguard":
                                    # /clean_drops - remove all dropped items on the map
                                    count = len(pickups)
                                    pickups.clear()
                                    show_error(f"Cleared {count} drops")
                                elif cmd in ("/p.ghost", "/pick.ghost") and acc_name_text.lower() == "devguard":
                                    # /p.ghost [y or n] (or /pick.ghost) - pick ghost mode:
                                    # enemies can't see the player
                                    args = parts[1:]
                                    if len(args) < 1 or args[0].lower() not in ("y", "n"):
                                        show_error("Usage: /p.ghost [y or n]")
                                    elif args[0].lower() == "y":
                                        player_ghost = True
                                        show_error("Ghost mode ON")
                                    else:
                                        player_ghost = False
                                        show_error("Ghost mode OFF")
                                elif cmd == "/revive_user" and acc_name_text.lower() == "devguard":
                                    # /revive_user [user] - instantly
                                    # revive a dead player
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /revive_user [user]")
                                    else:
                                        dev_revive_user(" ".join(args))
                                elif cmd == "/spawn_minion" and acc_name_text.lower() == "devguard":
                                    # /spawn_minion [rarity] [mob] [amount]
                                    # /spawn_minion [rarity] [mob] [damage] [health] [speed] [size] [view range] [amount]
                                    args = parts[1:]
                                    if len(args) < 2:
                                        show_error("Usage: /spawn_minion [rarity] [mob] [damage] [health] [speed] [size] [view range] [amount]")
                                    else:
                                        rarity = args[0].capitalize()
                                        minion_mob_classes = {
                                            "Ladybug": Ladybug,
                                            "Bee": Bee,
                                            "Spider": Spider,
                                            "Rock": Rock,
                                            "Hornet": Hornet,
                                            "Baby Ant": BabyAnt,
                                            "Soldier Ant": SoldierAnt,
                                            "BabyAnt": BabyAnt,
                                            "SoldierAnt": SoldierAnt,
                                            "Worker Ant": WorkerAnt,
                                            "WorkerAnt": WorkerAnt,
                                            "Queen Ant": QueenAnt,
                                            "QueenAnt": QueenAnt,
                                            "Hole Queen Ant": HoleQueenAnt,
                                            "HoleQueenAnt": HoleQueenAnt,
                                            "Ant Egg": AntEgg,
                                            "AntEgg": AntEgg,
                                        }
                                        found_mob = None
                                        trailing = []
                                        if len(args) >= 3:
                                            two_word = args[1] + " " + args[2]
                                            for k in minion_mob_classes:
                                                if k.lower() == two_word.lower():
                                                    found_mob = k
                                                    trailing = args[3:]
                                                    break
                                        if found_mob is None and len(args) >= 2:
                                            for k in minion_mob_classes:
                                                if k.lower() == args[1].lower():
                                                    found_mob = k
                                                    trailing = args[2:]
                                                    break
                                        if found_mob is None:
                                            valid_m = ", ".join(minion_mob_classes.keys())
                                            show_error(f"Invalid mob. Valid: {valid_m}")
                                        else:
                                            c_dmg = None
                                            c_hp = None
                                            c_spd = None
                                            c_sz = None
                                            c_vr = None
                                            spawn_amount = 1
                                            parse_ok = True
                                            if len(trailing) >= 5:
                                                # [damage] [health] [speed] [size] [view range] [amount]
                                                try:
                                                    c_dmg = float(trailing[0])
                                                    c_hp = float(trailing[1])
                                                    c_spd = float(trailing[2])
                                                    c_sz = float(trailing[3])
                                                    c_vr = float(trailing[4])
                                                    if len(trailing) >= 6:
                                                        spawn_amount = max(1, int(trailing[5]))
                                                except ValueError:
                                                    show_error("Damage, health, speed, size, view range, and amount must be numbers")
                                                    parse_ok = False
                                            elif len(trailing) == 1:
                                                # [amount]
                                                try:
                                                    spawn_amount = max(1, int(trailing[0]))
                                                except ValueError:
                                                    show_error("Amount must be a number")
                                                    parse_ok = False
                                            elif len(trailing) > 1:
                                                show_error("Usage: /spawn_minion [rarity] [mob] [damage] [health] [speed] [size] [view range] [amount]")
                                                parse_ok = False
                                            if parse_ok:
                                                for _ in range(spawn_amount):
                                                    spawn_custom_flower_minion(
                                                        rarity=rarity,
                                                        mob_name=found_mob,
                                                        custom_damage=c_dmg,
                                                        custom_hp=c_hp,
                                                        custom_speed=c_spd,
                                                        custom_size=c_sz,
                                                        custom_view_range=c_vr
                                                    )
                                                if spawn_amount > 1:
                                                    show_error(f"Spawned {spawn_amount} {rarity} {found_mob} minions!")
                                                else:
                                                    show_error(f"Spawned {rarity} {found_mob} minion!")
                                elif cmd in ("/p.flower", "/pick.flower", "/p.color", "/pick.color") and acc_name_text.lower() == "devguard":
                                    # /p.flower [color] or [hex] - customize flower color or reset with none
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /p.flower [color] or [hex]")
                                    else:
                                        raw_input = args[0].strip().lower()
                                        # Check for none / default reset
                                        if raw_input in ("none", "default", "reset"):
                                            player_color_name = "yellow"
                                            player_body_color = (225, 225, 0)
                                            player_outline_color = (230, 200, 40)
                                            player_face_color = (0, 0, 0)
                                            show_error("Flower color reset to default (yellow)")
                                        else:
                                            parsed = False
                                            # Try hex color (#RGB, #RRGGBB, RGB, RRGGBB)
                                            hex_cand = raw_input.lstrip("#")
                                            if len(hex_cand) in (3, 6):
                                                try:
                                                    if len(hex_cand) == 3:
                                                        hex_cand = "".join([c * 2 for c in hex_cand])
                                                    r = int(hex_cand[0:2], 16)
                                                    g = int(hex_cand[2:4], 16)
                                                    b = int(hex_cand[4:6], 16)
                                                    out_r = max(0, int(r * 0.8))
                                                    out_g = max(0, int(g * 0.8))
                                                    out_b = max(0, int(b * 0.8))
                                                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                                                    player_face_color = (255, 255, 255) if lum < 120 else (0, 0, 0)
                                                    player_body_color = (r, g, b)
                                                    player_outline_color = (out_r, out_g, out_b)
                                                    player_color_name = f"#{hex_cand}"
                                                    parsed = True
                                                    show_error(f"Flower color set to #{hex_cand}")
                                                except ValueError:
                                                    pass

                                            # Try named color if not parsed as hex
                                            if not parsed:
                                                clean_name = raw_input.replace(" ", "").replace("_", "")
                                                # Check custom presets first
                                                presets = {
                                                    "yellow": ((225, 225, 0), (230, 200, 40), (0, 0, 0)),
                                                    "pink": ((255, 150, 200), (220, 100, 160), (0, 0, 0)),
                                                    "cyan": ((80, 230, 255), (40, 180, 210), (0, 0, 0)),
                                                    "black": ((35, 35, 45), (15, 15, 20), (255, 255, 255)),
                                                    "white": ((245, 245, 250), (190, 190, 205), (0, 0, 0)),
                                                }
                                                if clean_name in presets:
                                                    b_col, o_col, f_col = presets[clean_name]
                                                    player_body_color = b_col
                                                    player_outline_color = o_col
                                                    player_face_color = f_col
                                                    player_color_name = clean_name
                                                    parsed = True
                                                    show_error(f"Flower color set to {clean_name}")
                                                elif clean_name in pygame.color.THECOLORS:
                                                    c = pygame.color.THECOLORS[clean_name]
                                                    r, g, b = c[0], c[1], c[2]
                                                    out_r = max(0, int(r * 0.8))
                                                    out_g = max(0, int(g * 0.8))
                                                    out_b = max(0, int(b * 0.8))
                                                    lum = 0.299 * r + 0.587 * g + 0.114 * b
                                                    player_face_color = (255, 255, 255) if lum < 120 else (0, 0, 0)
                                                    player_body_color = (r, g, b)
                                                    player_outline_color = (out_r, out_g, out_b)
                                                    player_color_name = raw_input
                                                    parsed = True
                                                    show_error(f"Flower color set to {raw_input}")

                                            if not parsed:
                                                show_error("Invalid color or hex code")
                                elif cmd in ("/p.weather", "/pick.weather") and acc_name_text.lower() == "devguard":
                                    # /p.weather [sunny or rainy or cloudy or snowy or hail]
                                    args = parts[1:]
                                    valid_weathers = ("sunny", "rainy", "cloudy", "snowy", "hail")
                                    if len(args) < 1 or args[0].lower() not in valid_weathers:
                                        show_error("Usage: /p.weather [sunny or rainy or cloudy or snowy or hail]")
                                    else:
                                        game_weather = args[0].lower()
                                        weather_particles.clear()
                                        show_error(f"Weather set to {game_weather}")
                                elif cmd in ("/p.theme", "/pick.theme") and acc_name_text.lower() == "devguard":
                                    # /p.theme [day or night] (or /pick.theme) - pick day or night theme
                                    args = parts[1:]
                                    if len(args) < 1 or args[0].lower() not in ("day", "night"):
                                        show_error("Usage: /p.theme [day or night]")
                                    elif args[0].lower() == "night":
                                        game_theme = "night"
                                        game_target_grid_color = (18, 24, 38)
                                        show_error("Night theme ON")
                                    else:
                                        game_theme = "day"
                                        game_target_grid_color = (60, 180, 75)
                                        show_error("Day theme ON")
                                elif cmd in ("/p.trail", "/pick.trail") and acc_name_text.lower() == "devguard":
                                    # /p.trail [none or rainbow or fire or sparkle] [last seconds]
                                    args = parts[1:]
                                    valid_trails = ("none", "rainbow", "fire", "sparkle")
                                    if len(args) < 1 or args[0].lower() not in valid_trails:
                                        show_error("Usage: /p.trail [none or rainbow or fire or sparkle] [last seconds]")
                                    else:
                                        player_trail = args[0].lower()
                                        player_trail_particles.clear()
                                        if len(args) >= 2:
                                            try:
                                                player_trail_last_sec = max(0.05, float(args[1]))
                                            except ValueError:
                                                player_trail_last_sec = 0.5
                                                show_error("Last seconds must be a number; default to 0.5s")
                                        else:
                                            player_trail_last_sec = 0.5

                                        if player_trail == "none":
                                            show_error("Movement trail OFF")
                                        else:
                                            show_error(f"Movement trail set to {player_trail} ({player_trail_last_sec}s)")
                                elif cmd in ("/p.petal_speed", "/pick.petal_speed") and acc_name_text.lower() == "devguard":
                                    # /p.petal_speed [slow or normal or fast] - pick petal rotation speed
                                    args = parts[1:]
                                    if len(args) < 1 or args[0].lower() not in ("slow", "normal", "fast"):
                                        show_error("Usage: /p.petal_speed [slow or normal or fast]")
                                    elif args[0].lower() == "slow":
                                        petal_rot_speed_mult = 0.5
                                        show_error("Petal speed set to slow")
                                    elif args[0].lower() == "fast":
                                        petal_rot_speed_mult = 2.5
                                        show_error("Petal speed set to fast")
                                    else:
                                        petal_rot_speed_mult = 1.0
                                        show_error("Petal speed set to normal")
                                elif cmd in ("/p.mode", "/pick.mode") and acc_name_text.lower() == "devguard":
                                    # /p.mode [peaceful or normal] (or /pick.mode) - pick game mode
                                    args = parts[1:]
                                    if len(args) < 1 or args[0].lower() not in ("peaceful", "normal"):
                                        show_error("Usage: /p.mode [peaceful or normal]")
                                    elif args[0].lower() == "peaceful":
                                        game_peaceful_mode = True
                                        show_error("Peaceful mode ON")
                                    else:
                                        game_peaceful_mode = False
                                        show_error("Normal mode ON")
                                elif cmd in ("/p.size", "/pick.size") and acc_name_text.lower() == "devguard":
                                    # /p.size [small or big] (or /pick.size) - pick your
                                    # flower size
                                    args = parts[1:]
                                    if len(args) < 1 or args[0].lower() not in ("small", "big"):
                                        show_error("Usage: /p.size [small or big]")
                                    elif args[0].lower() == "small":
                                        PLAYER_RADIUS = 12
                                        PETAL_RADIUS = 6
                                        show_error("Small size ON")
                                    else:
                                        PLAYER_RADIUS = 25
                                        PETAL_RADIUS = 12
                                        show_error("Big size ON")
                                elif cmd == "/delete_minion" and acc_name_text.lower() == "devguard":
                                    # /delete_minion [amount] (or /delete_minion to delete all)
                                    args = parts[1:]
                                    active_minions = [m for m in flower_minions if m.alive and not getattr(m, "dying", False)]
                                    if not active_minions:
                                        show_error("No minions to delete")
                                    else:
                                        delete_count = len(active_minions)
                                        if len(args) >= 1:
                                            try:
                                                delete_count = max(1, min(int(args[0]), len(active_minions)))
                                            except ValueError:
                                                show_error("Amount must be a number")
                                                delete_count = 0
                                        if delete_count > 0:
                                            # Shrink away the minions smoothly
                                            for m in active_minions[-delete_count:]:
                                                m.dying = True
                                                m.shrink_scale = 1.0
                                                m.full_radius = m.radius
                                            show_error(f"Deleted {delete_count} minion{'s' if delete_count > 1 else ''}")
                                elif cmd == "/kill_all_enemies" and acc_name_text.lower() == "devguard":
                                    # /kill_all_enemies - instantly defeat all enemies, dropping their loot & xp
                                    killed = 0
                                    for enemy in all_enemies:
                                        if not enemy.alive:
                                            continue
                                        if getattr(enemy, "dying", False):
                                            continue
                                        enemy.take_damage(enemy.hp + 999999)
                                        killed += 1
                                    show_error(f"Defeated {killed} enemies!")
                                elif cmd == "/despawn_mobs" and acc_name_text.lower() == "devguard":
                                    # /despawn_mobs - shrink away every
                                    # enemy on the map
                                    despawned = 0
                                    for enemy in all_enemies:
                                        if not enemy.alive:
                                            continue
                                        if getattr(enemy, "dying", False):
                                            continue
                                        enemy.dying = True
                                        enemy.shrink_scale = 1.0
                                        enemy.full_radius = enemy.radius
                                        despawned += 1
                                    show_error(
                                        f"Despawned {despawned} mobs"
                                    )
                                elif cmd == "/rarity_to" and acc_name_text.lower() == "devguard":
                                    # /rarity_to [rarity] - change the
                                    # rarity of the enemy under the mouse
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error("Usage: /rarity_to [rarity]")
                                    else:
                                        rarity = args[0].capitalize()
                                        mouse_x, mouse_y = pygame.mouse.get_pos()
                                        rarity_target = None
                                        for enemy in all_enemies:
                                            if not enemy.alive:
                                                continue
                                            if getattr(enemy, "dying", False):
                                                continue
                                            if distance(
                                                mouse_x,
                                                mouse_y,
                                                enemy.x - camera_x,
                                                enemy.y - camera_y
                                            ) <= enemy.radius:
                                                rarity_target = enemy
                                                break
                                        if rarity_target is None:
                                            show_error("No enemy under your mouse")
                                        else:
                                            dev_rarity_to(rarity_target, rarity)
                                elif cmd in (
                                    "/s.enemy_increase",
                                    "/s.enemy_decrease"
                                ) and acc_name_text.lower() == "devguard":
                                    # /s.enemy_increase [amount] or
                                    # /s.enemy_decrease [amount] - grow
                                    # or shrink the enemy under the mouse
                                    args = parts[1:]
                                    if len(args) < 1:
                                        show_error(f"Usage: {cmd} [amount]")
                                    else:
                                        try:
                                            amount = int(args[0])
                                        except ValueError:
                                            amount = None
                                        if amount is None:
                                            show_error("Amount must be a number")
                                        else:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            size_target = None
                                            for enemy in all_enemies:
                                                if not enemy.alive:
                                                    continue
                                                if getattr(enemy, "dying", False):
                                                    continue
                                                if distance(
                                                    mouse_x,
                                                    mouse_y,
                                                    enemy.x - camera_x,
                                                    enemy.y - camera_y
                                                ) <= enemy.radius:
                                                    size_target = enemy
                                                    break
                                            if size_target is None:
                                                show_error("No enemy under your mouse")
                                            else:
                                                if cmd == "/s.enemy_decrease":
                                                    amount = -amount
                                                if dev_change_enemy_size(size_target, amount):
                                                    show_error(
                                                        f"The {type(size_target).__name__}'s size changed by {abs(amount)}"
                                                    )
                                elif cmd in (
                                    "/equip",
                                    "/all_equip",
                                    "/empty",
                                    "/empty_all",
                                    "/ban",
                                    "/mute",
                                    "/unmute",
                                    "/gift",
                                    "/take",
                                    "/kick",
                                    "/give_points",
                                    "/tp",
                                    "/announce",
                                    "/self_heal",
                                    "/heal_user",
                                    "/full_heal_user",
                                    "/king",
                                    "/spawn_enemy",
                                    "/freez_enemies",
                                    "/unfreeze",
                                    "/godmode",
                                    "/reload_petals",
                                    "/spawn_whirlpool",
                                    "/delete_whirlpools",
                                    "/spawn_blackhole",
                                    "/delete_blackholes",
                                    "/spawn_shield_dome",
                                    "/delete_shield_domes",
                                    "/magnet_petal_drops",
                                    "/magnet",
                                    "/trail_size",
                                    "/hud",
                                    "/p.hud",
                                    "/pick.hud",
                                    "/speed",
                                    "/p.speed",
                                    "/tp_pos",
                                    "/clear_chat",
                                    "/clean_drops",
                                    "/spawn_minion",
                                    "/p.flower",
                                    "/pick.flower",
                                    "/p.color",
                                    "/pick.color",
                                    "/p.weather",
                                    "/pick.weather",
                                    "/p.theme",
                                    "/pick.theme",
                                    "/p.trail",
                                    "/pick.trail",
                                    "/p.petal_speed",
                                    "/pick.petal_speed",
                                    "/p.ghost",
                                    "/pick.ghost",
                                    "/revive_user",
                                    "/p.size",
                                    "/pick.size",
                                    "/p.mode",
                                    "/pick.mode",
                                    "/delete_minion",
                                    "/kill_all_enemies",
                                    "/despawn_mobs",
                                    "/rarity_to",
                                    "/s.enemy_increase",
                                    "/s.enemy_decrease"
                                ) and acc_name_text.lower() != "devguard":
                                    show_error(
                                        "sorry, this command is only for DevGuard"
                                    )
                                else:
                                    show_error(f"Unknown command: {cmd}")
                            else:
                                if acc_name_text in muted_users:
                                    show_error(
                                        "You are muted and can't chat"
                                    )
                                elif not is_bad_word(chat_input_text):
                                    chat_messages.append((acc_name_text, chat_input_text, time.time()))
                                else:
                                    show_error("The chat does not allow bad words")
                        chat_input_text = ""
                        chat_text_visible = False
                        chat_scroll_target = 0
                elif event.key == pygame.K_BACKSPACE and not chat_text_visible:
                    chat_input_text = chat_input_text[:-1]
                elif event.unicode and not chat_text_visible:
                    if len(chat_input_text) < 100:
                        chat_input_text += event.unicode

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_d:

                    if acc_name_text == "DevGuard":

                        mouse_x, mouse_y = pygame.mouse.get_pos()


                        for enemy in all_enemies:

                            if not enemy.alive:
                                continue


                            # convert enemy world position to screen position

                            enemy_screen_x = enemy.x - camera_x
                            enemy_screen_y = enemy.y - camera_y


                            d = distance(
                                mouse_x,
                                mouse_y,
                                enemy_screen_x,
                                enemy_screen_y
                            )


                            if d <= enemy.radius:

                                # Shrink the enemy away instead of
                                # deleting it instantly.
                                enemy.dying = True
                                enemy.shrink_scale = 1.0
                                enemy.full_radius = enemy.radius

                                break

        if event.type == pygame.MOUSEWHEEL:

            if craft_open:
                craft_visible_rows = max(
                    1,
                    math.ceil(325 / 42)
                )
                craft_max_scroll = max(
                    0,
                    len(PETAL_HP) - craft_visible_rows
                )
                craft_scroll_target = max(
                    0,
                    min(craft_max_scroll, craft_scroll_target - event.y)
                )
            # Chat scrollbar wheel support
            if not craft_open and chat_max_scroll > 0:
                chat_scroll_target = max(0, chat_scroll_target - event.y)

            if new_button_panel_open:
                gallery_visible_rows = max(
                    1,
                    min(
                        GALLERY_MAX_VISIBLE_ROWS,
                        (new_button_panel_target_rect.height - 97) // 42
                    )
                )
                gallery_visible_columns = max(1, (280 - 40) // 42)
                gallery_max_scroll = max(
                    0,
                    len(mob_gallery_names) - gallery_visible_rows
                )
                gallery_max_horizontal_scroll = max(
                    0,
                    len(RARITIES) - gallery_visible_columns
                )
                mob_gallery_scroll_target = max(
                    0,
                    min(
                        gallery_max_scroll,
                        mob_gallery_scroll_target - event.y
                    )
                )

            if inventory_open:

                inventory_scroll -= event.y

                if inventory_scroll < 0:
                    inventory_scroll = 0


                max_scroll = max(
                    0,
                    get_inventory_total_rows()
                    - get_inventory_max_rows()
                )


                if inventory_scroll > max_scroll:
                    inventory_scroll = max_scroll

        if event.type == pygame.MOUSEBUTTONUP:
            craft_dragging = False
            craft_x_dragging = False
            mob_gallery_dragging = False
            mob_gallery_x_dragging = False
            settings_hp_bar_dragging = False
            chat_dragging = False

        if event.type == pygame.MOUSEMOTION and settings_hp_bar_dragging:
            settings_hp_bar_knob_progress = min(
                1.0,
                max(
                    0.0,
                    (
                        pygame.mouse.get_pos()[0]
                        - settings_hp_bar_track_rect.left
                        - 12
                    )
                    / max(
                        1,
                        settings_hp_bar_track_rect.width - 24
                    )
                )
            )
            settings_hp_bar_scale = (
                1 + settings_hp_bar_knob_progress * 2
            )
            save_settings()

        if event.type == pygame.MOUSEMOTION and craft_dragging:
            craft_visible_rows = max(
                1,
                math.ceil(325 / 42)
            )
            craft_max_scroll = max(
                0,
                len(PETAL_HP) - craft_visible_rows
            )
            track_top = craft_panel_rect.bottom - 350
            track_height = 325
            thumb_height = craft_scrollbar_rect.height
            usable_track = max(1, track_height - thumb_height)
            scroll_position = event.pos[1] - track_top - craft_drag_offset
            craft_scroll_target = int(
                max(0, min(usable_track, scroll_position))
                / usable_track
                * craft_max_scroll
            )

        if event.type == pygame.MOUSEMOTION and craft_x_dragging:
            craft_rarity_count = len(RARITY_COLORS)
            craft_visible_columns = max(
                1,
                math.ceil((craft_panel_rect.width - 40) / 42)
            )
            craft_max_horizontal_scroll = max(
                0,
                craft_rarity_count - craft_visible_columns
            )
            track_left = craft_panel_rect.x + 10
            track_width = craft_panel_rect.width - 40
            thumb_width = craft_horizontal_scrollbar_rect.width
            usable_track = max(1, track_width - thumb_width)
            scroll_position = event.pos[0] - track_left - craft_x_drag_offset
            craft_horizontal_scroll_target = int(
                max(0, min(usable_track, scroll_position))
                / usable_track
                * craft_max_horizontal_scroll
            )

        if event.type == pygame.MOUSEMOTION and chat_dragging:
            if len(chat_messages) > 4 and chat_max_scroll > 0:
                chat_box_w = 260
                chat_margin = 20
                inner_padding = 10
                inner_height = 30
                small_square_size = 40
                gap = 5
                # Arrow button stays at fixed position
                arrow_y = HEIGHT - chat_margin - 120
                # Chat box bottom stays fixed; grows upward when taller
                if chat_arrow_up:
                    chat_box_h = 200
                    box_y = arrow_y - 80
                else:
                    chat_box_h = 120
                    box_y = arrow_y
                chat_box_x = WIDTH - chat_margin - chat_box_w
                chat_box_y = box_y
                inner_rect_w = chat_box_w - 2 * inner_padding
                msg_font = pygame.font.SysFont("arial", 14, bold=True)
                total_msg_h = 0
                for u, m, t in chat_messages:
                    name_w = msg_font.render(f"[{u}]", True, (255, 255, 0)).get_width()
                    time_w = msg_font.render(f" [0m 0s]: ", True, (0, 255, 0)).get_width()
                    mw = inner_rect_w - 10 - name_w - time_w
                    lines = wrap_text(msg_font, m, mw)
                    total_msg_h += len(lines) * line_height
                total_msg_h += (len(chat_messages) - 1) * 5
                visible_h = chat_box_h - inner_height - inner_padding - 5
                chat_max_scroll_val = max(0, total_msg_h - visible_h)
                vertical_rect_x = chat_box_x - small_square_size - 5
                vertical_rect_y = chat_box_y + small_square_size + gap
                vertical_rect_h = chat_box_h - small_square_size - gap
                track_height = vertical_rect_h
                thumb_height = chat_scrollbar_rect.height
                usable_track = max(1, track_height - thumb_height)
                scroll_position = event.pos[1] - vertical_rect_y - chat_drag_offset
                chat_scroll_target = int(
                    max(0, min(usable_track, scroll_position))
                    / usable_track
                    * max(0, chat_max_scroll_val)
                )

        if event.type == pygame.MOUSEMOTION and mob_gallery_dragging:
            gallery_visible_rows = max(
                1,
                min(
                    GALLERY_MAX_VISIBLE_ROWS,
                    (new_button_panel_target_rect.height - 97) // 42
                )
            )
            gallery_max_scroll = max(
                0,
                len(mob_gallery_names) - gallery_visible_rows
            )
            track_top = mob_gallery_grid_top
            track_height = GALLERY_GRID_WINDOW_HEIGHT
            thumb_height = mob_gallery_scrollbar_rect.height
            usable_track = max(1, track_height - thumb_height)
            scroll_position = event.pos[1] - track_top
            mob_gallery_scroll_target = int(
                max(0, min(usable_track, scroll_position))
                / usable_track
                * gallery_max_scroll
            )

        if event.type == pygame.MOUSEMOTION and mob_gallery_x_dragging:
            gallery_visible_columns = max(1, (280 - 40) // 42)
            gallery_max_horizontal_scroll = max(
                0,
                len(RARITIES) - gallery_visible_columns
            )
            track_left = new_button_panel_rect.x + 10
            track_width = 280 - 40
            thumb_width = mob_gallery_horizontal_scrollbar_rect.width
            usable_track = max(1, track_width - thumb_width)
            scroll_position = event.pos[0] - track_left
            mob_gallery_horizontal_scroll_target = int(
                max(0, min(usable_track, scroll_position))
                / usable_track
                * gallery_max_horizontal_scroll
            )

        if event.type == pygame.MOUSEWHEEL:

            if (
                cmd_panel_open
                and cmd_panel_rect.collidepoint(
                    pygame.mouse.get_pos()
                )
            ):
                cmd_panel_scroll -= event.y * 32

            if inventory_open:

                inventory_scroll -= event.y

                if inventory_scroll < 0:
                    inventory_scroll = 0

                inventory_scroll = min(
                    inventory_scroll,
                    max(
                        0,
                        get_inventory_total_rows()
                        - get_inventory_max_rows()
                    )
                )

    if game_state == "login":

        if login_error_timer > 0:

            login_error_timer -= 1

            if login_error_timer <= 0:

                login_error = ""

        draw_login_screen()

        shown_password = "•" * len(password_text)

        password_surface = login_font.render(
            shown_password,
            True,
            (0,0,0)
        )

        screen.blit(
            password_surface,
            (
                password_box.x + 10,
                password_box.y + 8
            )
        )


        name_surface = login_font.render(
            acc_name_text,
            True,
            (0,0,0)
        )

        screen.blit(
            name_surface,
            (
                acc_name_box.x + 10,
                acc_name_box.y + 8
            )
        )


    elif game_state == "welcome":

        # Smoothly interpolate the grid color toward the selected biome.
        # This makes the grid colors change slowly instead of instantly.
        if welcome_grid_color != welcome_target_grid_color:
            welcome_grid_color = tuple(
                int(
                    welcome_grid_color[i]
                    + (
                        welcome_target_grid_color[i]
                        - welcome_grid_color[i]
                    )
                    * 0.04
                )
                for i in range(3)
            )

        # advance the scrolling grid (right and a little down)
        welcome_scroll_x += 1.5
        welcome_scroll_y += 0.35

        screen.fill(welcome_grid_color)

        # draw the grid tiles with the same size as the real in-game grass,
        # shifted by the scroll offset so they move right and a little down,
        # and clipped to the screen
        gsize = GRASS_SIZE

        off_x = welcome_scroll_x % gsize
        off_y = welcome_scroll_y % gsize

        grid_border_color = tuple(
            max(0, c - 10)
            for c in welcome_grid_color
        )

        for gx in range(-1, WIDTH // gsize + 2):
            for gy in range(-1, HEIGHT // gsize + 2):

                x = int(gx * gsize - off_x)
                y = int(gy * gsize - off_y)

                pygame.draw.rect(
                    screen,
                    welcome_grid_color,
                    (x, y, gsize, gsize)
                )
                pygame.draw.rect(
                    screen,
                    grid_border_color,
                    (x, y, gsize, gsize),
                    1
                )

        # remove the petals that flew offscreen
        welcome_petals = [
            p for p in welcome_petals
            if p["x"] - p["size"] * 2 <= WIDTH + 40
        ]

        # reload: after a random lull, spawn a whole batch of petals at the
        # left edge together, then wait again
        welcome_petal_reload -= 1

        if welcome_petal_reload <= 0:

            welcome_petal_reload = random.randint(50, 110)

            for _ in range(random.randint(4, 9)):

                welcome_petals.append({
                    "x": -random.randint(10, 120),
                    "y": random.uniform(0, HEIGHT),
                    "speed": random.uniform(1.0, 3.0),
                    "size": random.uniform(8, 22),
                    "wobble": random.uniform(0.0, 360.0),
                    "spin": random.uniform(0.0, 360.0),
                    "spin_speed": random.uniform(-6.0, 6.0),
                    "name": random.choice(WELCOME_PETAL_NAMES),
                    "surf": None,
                })

        # move the petals right, spin them, and redraw their real petal
        # pictures behind the panel, clipped to the screen
        for petal in welcome_petals:

            petal["x"] += petal["speed"]
            petal["wobble"] += 2.0
            petal["spin"] += petal["spin_speed"]

            px = petal["x"]
            py = (
                petal["y"]
                + math.sin(math.radians(petal["wobble"])) * 10
            )
            s = petal["size"]

            # skip fully offscreen petals (clipping)
            if px + s < 0 or px > WIDTH:
                continue
            if py + s < 0 or py > HEIGHT:
                continue

            # render the real petal picture once, then reuse/rotate it
            if petal["surf"] is None:
                petal["surf"] = make_petal_surface(
                    petal["name"],
                    0,
                    0,
                    "Common",
                    size_scale=petal["size"] / 12.0
                )

            petal_surf = pygame.transform.rotate(
                petal["surf"],
                petal["spin"] % 360
            )

            screen.blit(
                petal_surf,
                petal_surf.get_rect(
                    center=(int(px), int(py))
                )
            )

        # 80% black transparent rectangle with rounded corners drawn in the
        # middle
        welcome_panel_w = int(WIDTH * 0.26)
        welcome_panel_h = int(HEIGHT * 0.20)

        panel_surf = pygame.Surface(
            (welcome_panel_w, welcome_panel_h),
            pygame.SRCALPHA
        )
        pygame.draw.rect(
            panel_surf,
            (0, 0, 0, 204),
            panel_surf.get_rect(),
            border_radius=30
        )

        screen.blit(
            panel_surf,
            (
                WIDTH // 2 - welcome_panel_w // 2,
                HEIGHT // 2 - welcome_panel_h // 2
            )
        )

        # "Velora.io" title above the panel, white text with a black outline,
        # drawn in front of the petals
        velora_title = pygame.font.SysFont("arialnarrow", 56)
        velora_white_text = velora_title.render(
            "Velora.io", True, (255, 255, 255)
        )
        velora_black_text = velora_title.render(
            "Velora.io", True, (0, 0, 0)
        )
        for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            screen.blit(
                velora_black_text,
                (
                    WIDTH // 2 - velora_black_text.get_width() // 2 + ox,
                    HEIGHT // 2 - welcome_panel_h // 2 - 95 + oy
                )
            )
        screen.blit(
            velora_white_text,
            (
                WIDTH // 2 - velora_white_text.get_width() // 2,
                HEIGHT // 2 - welcome_panel_h // 2 - 95
            )
        )

        # green "garden" button near the top-left corner of the panel,
        # with its own darker outline and white text with a black outline
        panel_topleft = (
            WIDTH // 2 - welcome_panel_w // 2,
            HEIGHT // 2 - welcome_panel_h // 2
        )
        garden_btn_w = 120
        garden_btn_h = 48
        garden_btn = pygame.Rect(
            panel_topleft[0] + 16,
            panel_topleft[1] + 12,
            garden_btn_w,
            garden_btn_h
        )
        pygame.draw.rect(
            screen,
            (80, 200, 90),
            garden_btn,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (40, 130, 55),
            garden_btn,
            3,
            border_radius=8
        )

        thinner_label = pygame.font.SysFont("arialnarrow", 24)
        garden_white = pygame.font.SysFont(
            "arialnarrow", 25
        ).render("garden", True, (255, 255, 255))
        garden_black = thinner_label.render(
            "garden", True, (0, 0, 0)
        )
        screen.blit(
            garden_white,
            (
                garden_btn.centerx - garden_white.get_width() // 2,
                garden_btn.centery - garden_white.get_height() // 2
            )
        )
        screen.blit(
            garden_black,
            (
                garden_btn.centerx - garden_black.get_width() // 2,
                garden_btn.centery - garden_black.get_height() // 2
            )
        )

        # white "(new)Eagle Land" button under the garden button
        eagle_btn_w = 180
        eagle_btn_h = 48
        eagle_btn = pygame.Rect(
            garden_btn.left,
            garden_btn.bottom + 12,
            eagle_btn_w,
            eagle_btn_h
        )
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            eagle_btn,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (140, 140, 140),
            eagle_btn,
            3,
            border_radius=8
        )

        eagle_label = pygame.font.SysFont("arialnarrow", 24)
        eagle_white = pygame.font.SysFont(
            "arialnarrow", 25
        ).render("(new)Eagle Land", True, (255, 255, 255))
        eagle_black = eagle_label.render(
            "(new)Eagle Land", True, (0, 0, 0)
        )
        screen.blit(
            eagle_white,
            (
                eagle_btn.centerx - eagle_white.get_width() // 2,
                eagle_btn.centery - eagle_white.get_height() // 2
            )
        )
        screen.blit(
            eagle_black,
            (
                eagle_btn.centerx - eagle_black.get_width() // 2,
                eagle_btn.centery - eagle_black.get_height() // 2
            )
        )

        # dark-green "(new)Farm" button to the right of the eagle button,
        # same y position as the eagle button
        farm_btn_h = 48
        farm_btn_x = eagle_btn.right + 16
        farm_btn_max_right = panel_topleft[0] + welcome_panel_w - 16
        farm_btn_w = max(60, farm_btn_max_right - farm_btn_x)
        farm_btn = pygame.Rect(
            farm_btn_x,
            eagle_btn.top,
            farm_btn_w,
            farm_btn_h
        )
        pygame.draw.rect(
            screen,
            (50, 140, 65),
            farm_btn,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (25, 90, 40),
            farm_btn,
            3,
            border_radius=8
        )

        farm_label = pygame.font.SysFont("arialnarrow", 24)
        farm_white = pygame.font.SysFont(
            "arialnarrow", 25
        ).render("(new)Farm", True, (255, 255, 255))
        farm_black = farm_label.render(
            "(new)Farm", True, (0, 0, 0)
        )
        screen.blit(
            farm_white,
            (
                farm_btn.centerx - farm_white.get_width() // 2,
                farm_btn.centery - farm_white.get_height() // 2
            )
        )
        screen.blit(
            farm_black,
            (
                farm_btn.centerx - farm_black.get_width() // 2,
                farm_btn.centery - farm_black.get_height() // 2
            )
        )

        # sand "desert" button copied to the right of the garden button
        desert_btn_w = 120
        desert_btn_h = 48
        desert_btn = pygame.Rect(
            garden_btn.right + 16,
            garden_btn.top,
            desert_btn_w,
            desert_btn_h
        )
        pygame.draw.rect(
            screen,
            (222, 204, 150),
            desert_btn,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (150, 130, 85),
            desert_btn,
            3,
            border_radius=8
        )

        desert_label = pygame.font.SysFont("arialnarrow", 24)
        desert_white = pygame.font.SysFont(
            "arialnarrow", 25
        ).render("desert", True, (255, 255, 255))
        desert_black = desert_label.render(
            "desert", True, (0, 0, 0)
        )
        screen.blit(
            desert_white,
            (
                desert_btn.centerx - desert_white.get_width() // 2,
                desert_btn.centery - desert_white.get_height() // 2
            )
        )
        screen.blit(
            desert_black,
            (
                desert_btn.centerx - desert_black.get_width() // 2,
                desert_btn.centery - desert_black.get_height() // 2
            )
        )

        # ocean "ocean" button to the right of the desert button, shortened
        # so it stays inside the panel's right edge
        ocean_btn_h = 48
        ocean_btn_x = desert_btn.right + 16
        ocean_btn_max_right = panel_topleft[0] + welcome_panel_w - 16
        ocean_btn_w = max(60, ocean_btn_max_right - ocean_btn_x)
        ocean_btn = pygame.Rect(
            ocean_btn_x,
            garden_btn.top,
            ocean_btn_w,
            ocean_btn_h
        )
        pygame.draw.rect(
            screen,
            (70, 150, 235),
            ocean_btn,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (20, 90, 175),
            ocean_btn,
            3,
            border_radius=8
        )

        ocean_label = pygame.font.SysFont("arialnarrow", 24)
        ocean_white = pygame.font.SysFont(
            "arialnarrow", 25
        ).render("ocean", True, (255, 255, 255))
        ocean_black = ocean_label.render(
            "ocean", True, (0, 0, 0)
        )
        screen.blit(
            ocean_white,
            (
                ocean_btn.centerx - ocean_white.get_width() // 2,
                ocean_btn.centery - ocean_white.get_height() // 2
            )
        )
        screen.blit(
            ocean_black,
            (
                ocean_btn.centerx - ocean_black.get_width() // 2,
                ocean_btn.centery - ocean_black.get_height() // 2
            )
        )

        # detect biome button clicks (garden/desert/ocean/eagle/farm)
        if welcome_click_pending:
            welcome_click_pending = False
            mx, my = pygame.mouse.get_pos()
            biome_rects = [
                ("garden", garden_btn),
                ("desert", desert_btn),
                ("ocean", ocean_btn),
                ("eagle", eagle_btn),
                ("farm", farm_btn),
            ]
            for biome_name, btn in biome_rects:
                if btn.collidepoint(mx, my):
                    if welcome_selected_biome == biome_name:
                        welcome_selected_biome = None
                        selected_biome = None
                    else:
                        welcome_selected_biome = biome_name
                        selected_biome = biome_name
                        # Set the target grid color for smooth transition
                        welcome_target_grid_color = BIOME_COLORS[biome_name]

                # start the iris wipe when the (green) play button is clicked:
            # only works once a biome has been selected, and never restarts
            # a wipe that is already running
            if (
                not welcome_transition_active
                and welcome_selected_biome is not None
                and play_btn.collidepoint(mx, my)
            ):
                welcome_transition_active = True
                welcome_transition_phase = "close"
                welcome_transition_progress = 0.0
                welcome_play_pressed = True

        # draw a white glow overlay on the currently selected biome button
        if welcome_selected_biome is not None:
            biome_rects = [
                ("garden", garden_btn),
                ("desert", desert_btn),
                ("ocean", ocean_btn),
                ("eagle", eagle_btn),
                ("farm", farm_btn),
            ]
            for biome_name, btn in biome_rects:
                if biome_name == welcome_selected_biome:
                    glow_rect = btn.inflate(8, 8)
                    glow_surf = pygame.Surface(
                        (glow_rect.w, glow_rect.h), pygame.SRCALPHA
                    )
                    glow_surf.fill((255, 255, 255, 60))
                    pygame.draw.rect(
                        glow_surf,
                        (255, 255, 255, 120),
                        glow_surf.get_rect(),
                        3,
                        border_radius=10
                    )
                    screen.blit(glow_surf, glow_rect.topleft)

        # play button below the panel: red when no biome selected, green
        # once a biome is selected, with a matching label color
        play_btn_w = 200
        play_btn_h = 60
        play_btn = pygame.Rect(
            WIDTH // 2 - play_btn_w // 2,
            HEIGHT // 2 + welcome_panel_h // 2 + 30,
            play_btn_w,
            play_btn_h
        )
        if welcome_selected_biome is None:
            play_btn_fill = (210, 70, 70)
            play_btn_outline = (140, 35, 35)
            play_btn_text_color = (255, 255, 255)
        else:
            play_btn_fill = (80, 200, 90)
            play_btn_outline = (40, 130, 55)
            play_btn_text_color = (20, 80, 40)
        pygame.draw.rect(
            screen,
            play_btn_fill,
            play_btn,
            border_radius=10
        )
        pygame.draw.rect(
            screen,
            play_btn_outline,
            play_btn,
            3,
            border_radius=10
        )

        play_btn_font = pygame.font.SysFont("arialnarrow", 30)
        play_btn_play_text = play_btn_font.render(
            "Play", True, play_btn_text_color
        )
        screen.blit(
            play_btn_play_text,
            (
                play_btn.centerx - play_btn_play_text.get_width() // 2,
                play_btn.centery - play_btn_play_text.get_height() // 2
            )
        )

        # the logged-in account name as plain white text under the panel
        welcome_name_font = pygame.font.SysFont("arialnarrow", 26)
        welcome_name_text = welcome_name_font.render(
            acc_name_text, True, (255, 255, 255)
        )
        screen.blit(
            welcome_name_text,
            (
                WIDTH // 2 - welcome_name_text.get_width() // 2,
                HEIGHT // 2 + welcome_panel_h // 2 - 41
            )
        )

    elif game_state == "game":

        dt = clock.tick(FPS)

        # Smoothly interpolate the game grid color toward the selected biome.
        if game_grid_color != game_target_grid_color:
            game_grid_color = tuple(
                int(
                    game_grid_color[i]
                    + (
                        game_target_grid_color[i]
                        - game_grid_color[i]
                    )
                    * 0.04
                )
                for i in range(3)
            )

        # ---------------- INVENTORY PANEL SLIDE (acceleration) ----------------
        # Damped-spring slide: it accelerates toward the resting x position
        # when open and settles with no oscillation (no wiggling).

        INV_SPRING = 0.10
        INV_DAMP = 0.37

        target = (
            inv_panel_target_x
            if inventory_open
            else -inventory_panel_rect.width
        )

        inv_panel_vx += (target - inv_panel_x) * INV_SPRING
        inv_panel_vx *= INV_DAMP
        inv_panel_x += inv_panel_vx

        if (
            abs(target - inv_panel_x) < 1.0
            and abs(inv_panel_vx) < 2.0
        ):
            inv_panel_x = float(target)
            inv_panel_vx = 0.0

        inventory_panel_rect.x = int(round(inv_panel_x))

        if craft_animation_active:
            craft_animation_timer -= 1
            if craft_animation_timer <= 0:
                batch_safety_limit = 0
                while craft_animation_active and batch_safety_limit < 10000:
                    finish_craft(save_after=False)
                    batch_safety_limit += 1
                save_player()

        rose_heal_timer -= 1

        if rose_heal_timer <= 0:

            defending = True  # replace this with your real defend check

            if defending:

                for i in range(PETAL_SLOTS):

                    if petal_alive[i]:

                        if i < len(petal_slots) and petal_slots[i]["petal"] == "Rose":

                            player_hp += 10

                            if player_hp > PLAYER_MAX_HP:
                                player_hp = PLAYER_MAX_HP

                            rose_heal_timer = 60  # 1 second
                            break

        leaf_heal_timer -= 1

        if leaf_heal_timer <= 0:

            for i in range(PETAL_SLOTS):

                if petal_alive[i]:

                    if i < len(petal_slots) and petal_slots[i]["petal"] == "Leaf":

                        rarity = petal_slots[i]["rarity"]

                        heal_amount = LEAF_HEAL.get(
                            rarity,
                            1
                        )

                        player_hp += heal_amount / 5

                        if player_hp > PLAYER_MAX_HP:
                            player_hp = PLAYER_MAX_HP

                        leaf_heal_timer = 1
                        break

        # -------- INPUT --------
        new_rarity_gradient += 0.01
        infino_gradient_timer += 1

        # slowly move toward target direction
        if infino_gradient_angle < infino_gradient_target_angle:
            infino_gradient_angle += 0.02

        elif infino_gradient_angle > infino_gradient_target_angle:
            infino_gradient_angle -= 0.02


        infino_gradient_offset += 0.04


        # change direction every few seconds
        if infino_gradient_timer >= 180:

            infino_gradient_timer = 0

            import random

            infino_gradient_target_angle = random.choice([
                0,              # horizontal
                math.pi / 2,    # vertical
                math.pi / 4,    # diagonal
                -math.pi / 4,   # diagonal other way
                math.pi
            ])
        keys = pygame.key.get_pressed()

        # movement direction (normalized input)
        move_x = 0
        move_y = 0

        if keys[pygame.K_UP]:
            move_y -= 1
        if keys[pygame.K_DOWN]:
            move_y += 1
        if keys[pygame.K_LEFT]:
            move_x -= 1
        if keys[pygame.K_RIGHT]:
            move_x += 1

        if player_spawn_cooldown > 0:
            player_spawn_cooldown -= 1

        # prevent diagonal speed boost
        if move_x != 0 and move_y != 0:
            normalize = 1 / math.sqrt(2)
            move_x *= normalize
            move_y *= normalize

        # -------- DEATH / BOUNCE --------

        if player_dead:

            # bounce away from the enemy with friction
            player_bounce_x *= 0.94
            player_bounce_y *= 0.94

            # move in small sub-steps so the dead flower never tunnels
            # through a wall, and bounce off the wall it actually hits
            steps = max(
                1,
                int(math.ceil(
                    max(abs(player_bounce_x), abs(player_bounce_y)) / 2.0
                ))
            )
            sx = player_bounce_x / steps
            sy = player_bounce_y / steps

            for _ in range(steps):

                prev_x = player_x
                prev_y = player_y

                player_x += sx
                player_y += sy

                frect = pygame.Rect(
                    player_x - PLAYER_RADIUS,
                    player_y - PLAYER_RADIUS,
                    PLAYER_RADIUS * 2,
                    PLAYER_RADIUS * 2
                )

                wall_hit = False

                for wall in walls:

                    if frect.colliderect(wall.rect):

                        # reflect on each axis independently, based on which
                        # face the flower actually crossed. this keeps a
                        # flower sliding along a wall's edge from being flung
                        # to the wall's left/right ends.
                        if (
                            prev_x + PLAYER_RADIUS <= wall.rect.left
                            and player_x + PLAYER_RADIUS > wall.rect.left
                        ):
                            player_x = wall.rect.left - PLAYER_RADIUS
                            player_bounce_x = -abs(player_bounce_x) * 0.6
                        elif (
                            prev_x - PLAYER_RADIUS >= wall.rect.right
                            and player_x - PLAYER_RADIUS < wall.rect.right
                        ):
                            player_x = wall.rect.right + PLAYER_RADIUS
                            player_bounce_x = abs(player_bounce_x) * 0.6

                        if (
                            prev_y + PLAYER_RADIUS <= wall.rect.top
                            and player_y + PLAYER_RADIUS > wall.rect.top
                        ):
                            player_y = wall.rect.top - PLAYER_RADIUS
                            player_bounce_y = -abs(player_bounce_y) * 0.6
                        elif (
                            prev_y - PLAYER_RADIUS >= wall.rect.bottom
                            and player_y - PLAYER_RADIUS < wall.rect.bottom
                        ):
                            player_y = wall.rect.bottom + PLAYER_RADIUS
                            player_bounce_y = abs(player_bounce_y) * 0.6

                        # safety net: if still overlapping (e.g. shoved inside
                        # a wall by an enemy), push out along the nearest face
                        if frect.colliderect(wall.rect):

                            overlap_left = (
                                (player_x + PLAYER_RADIUS) - wall.rect.left
                            )
                            overlap_right = (
                                wall.rect.right - (player_x - PLAYER_RADIUS)
                            )
                            overlap_top = (
                                (player_y + PLAYER_RADIUS) - wall.rect.top
                            )
                            overlap_bottom = (
                                wall.rect.bottom - (player_y - PLAYER_RADIUS)
                            )

                            min_overlap = min(
                                overlap_left,
                                overlap_right,
                                overlap_top,
                                overlap_bottom
                            )

                            if min_overlap == overlap_left:
                                player_x = wall.rect.left - PLAYER_RADIUS
                                player_bounce_x = -abs(player_bounce_x) * 0.6
                            elif min_overlap == overlap_right:
                                player_x = wall.rect.right + PLAYER_RADIUS
                                player_bounce_x = abs(player_bounce_x) * 0.6
                            elif min_overlap == overlap_top:
                                player_y = wall.rect.top - PLAYER_RADIUS
                                player_bounce_y = -abs(player_bounce_y) * 0.6
                            else:
                                player_y = wall.rect.bottom + PLAYER_RADIUS
                                player_bounce_y = abs(player_bounce_y) * 0.6

                        wall_hit = True
                        break

                if wall_hit:
                    # stop moving this frame after a wall hit
                    break

                # if the bouncing flower hits any other enemy, just stop it there
                # (no bounce-back so the enemy doesn't look like it got pushed
                # by the flower)
                enemy_hit = False
                flower_speed = math.hypot(player_bounce_x, player_bounce_y)

                for group in (
                    ladybugs,
                    bees,
                    spiders,
                    rocks,
                    hornets,
                    baby_ants,
                    soldier_ants,
                    worker_ants,
                    queen_ants,
                    ant_eggs
                ):
                    for e in group:
                        e_radius = getattr(e, "radius", 0)
                        if e_radius <= 0:
                            continue
                        dx = player_x - e.x
                        dy = player_y - e.y
                        dist = math.hypot(dx, dy)
                        if dist > 0 and dist < PLAYER_RADIUS + e_radius:
                            # push the flower just out of the enemy
                            nx = dx / dist
                            ny = dy / dist
                            player_x = e.x + nx * (PLAYER_RADIUS + e_radius)
                            player_y = e.y + ny * (PLAYER_RADIUS + e_radius)
                            # stop the bounce so the flower doesn't fly
                            # back into the enemy
                            player_bounce_x = 0
                            player_bounce_y = 0
                            enemy_hit = True
                            break
                    if enemy_hit:
                        break

                if enemy_hit:
                    break

            # clamp the bounce speed so the flower can never get flung
            max_bounce = 9
            bspeed = math.hypot(player_bounce_x, player_bounce_y)

            if bspeed > max_bounce:
                scale = max_bounce / bspeed
                player_bounce_x *= scale
                player_bounce_y *= scale

            # spin the player, ending the spin via acceleration (friction)
            player_rot_angle += player_rot_vel
            player_rot_vel *= 0.96

            if abs(player_rot_vel) < 0.05:
                player_rot_vel = 0

        # -------- DIRECT MOVEMENT (no acceleration) --------

        if not player_dead:

            # Sticky spider king webs slow the flower down; the
            # slowdown depends on the spider king's rarity.
            move_speed = PLAYER_SPEED * player_speed_mult
            if player_in_web:
                move_speed *= player_in_web_slowdown

            player_x += move_x * move_speed
            player_y += move_y * move_speed

            if player_trail != "none" and (move_x != 0 or move_y != 0):
                # Spawn trail particles behind the flower with lifetime based on player_trail_last_sec
                trail_life_frames = max(3, int(player_trail_last_sec * FPS))
                for _ in range(2):
                    offset_angle = random.uniform(0, 2 * math.pi)
                    offset_dist = random.uniform(0, PLAYER_RADIUS * 0.7)
                    px = player_x + math.cos(offset_angle) * offset_dist
                    py = player_y + math.sin(offset_angle) * offset_dist
                    if player_trail == "rainbow":
                        colors = [
                            (255, 75, 75),   # Red
                            (255, 160, 40),  # Orange
                            (255, 235, 50),  # Yellow
                            (75, 225, 90),   # Green
                            (50, 180, 255),  # Cyan
                            (120, 100, 255), # Blue/Purple
                            (230, 90, 230),  # Magenta
                        ]
                        col = random.choice(colors)
                        player_trail_particles.append({
                            "x": px, "y": py,
                            "vx": random.uniform(-0.6, 0.6) - move_x * 0.4,
                            "vy": random.uniform(-0.6, 0.6) - move_y * 0.4,
                            "life": trail_life_frames, "max_life": trail_life_frames,
                            "size": random.uniform(PLAYER_RADIUS * 0.35, PLAYER_RADIUS * 0.6) * player_trail_size_mult,
                            "color": col,
                            "type": "circle"
                        })
                    elif player_trail == "fire":
                        fire_cols = [(255, 60, 20), (255, 140, 20), (255, 220, 40), (255, 255, 180)]
                        player_trail_particles.append({
                            "x": px, "y": py,
                            "vx": random.uniform(-0.8, 0.8) - move_x * 0.5,
                            "vy": random.uniform(-0.8, 0.8) - move_y * 0.5 - random.uniform(0.5, 1.5),
                            "life": trail_life_frames, "max_life": trail_life_frames,
                            "size": random.uniform(PLAYER_RADIUS * 0.35, PLAYER_RADIUS * 0.65) * player_trail_size_mult,
                            "color": random.choice(fire_cols),
                            "type": "flame"
                        })
                    elif player_trail == "sparkle":
                        sparkle_cols = [(255, 255, 255), (255, 250, 160), (200, 240, 255), (255, 220, 255)]
                        player_trail_particles.append({
                            "x": px, "y": py,
                            "vx": random.uniform(-1.2, 1.2),
                            "vy": random.uniform(-1.2, 1.2),
                            "life": trail_life_frames, "max_life": trail_life_frames,
                            "size": random.uniform(PLAYER_RADIUS * 0.25, PLAYER_RADIUS * 0.5) * player_trail_size_mult,
                            "color": random.choice(sparkle_cols),
                            "type": "star",
                            "rot": random.uniform(0, 360),
                            "vrot": random.uniform(-8, 8)
                        })

            # small knockback from enemy hits decays with friction so the
            # flower gets pushed a little and then recovers
            player_bounce_x *= 0.90
            player_bounce_y *= 0.90
            player_x += player_bounce_x
            player_y += player_bounce_y

        # -------- WALL COLLISION --------

        player_rect = pygame.Rect(
            player_x - PLAYER_RADIUS,
            player_y - PLAYER_RADIUS,
            PLAYER_RADIUS * 2,
            PLAYER_RADIUS * 2
        )

        for wall in walls:

            if player_rect.colliderect(wall.rect):

                # push the player out along the smallest overlap so that
                # sliding along a wall (even with diagonal input) doesn't
                # fling the player to the wall's left/right ends
                overlap_left = (player_x + PLAYER_RADIUS) - wall.rect.left
                overlap_right = wall.rect.right - (player_x - PLAYER_RADIUS)
                overlap_top = (player_y + PLAYER_RADIUS) - wall.rect.top
                overlap_bottom = wall.rect.bottom - (player_y - PLAYER_RADIUS)

                min_overlap = min(
                    overlap_left,
                    overlap_right,
                    overlap_top,
                    overlap_bottom
                )

                if min_overlap == overlap_left:
                    player_x = wall.rect.left - PLAYER_RADIUS
                elif min_overlap == overlap_right:
                    player_x = wall.rect.right + PLAYER_RADIUS
                elif min_overlap == overlap_top:
                    player_y = wall.rect.top - PLAYER_RADIUS
                else:
                    player_y = wall.rect.bottom + PLAYER_RADIUS

                break

        if player_godmode:
            player_hp = PLAYER_MAX_HP

        # keep player inside map

        player_x = max(
            PLAYER_RADIUS,
            min(player_x, WORLD_WIDTH - PLAYER_RADIUS)
        )

        player_y = max(
            PLAYER_RADIUS,
            min(player_y, WORLD_HEIGHT - PLAYER_RADIUS)
        )

        # -------- PICKUPS -------- (loot boxes)
        pickup_dt = dt / 1000.0
        pickup_pulse_phase += pickup_dt * 3.5
        pickup_half = PICKUP_SIZE // 2
        for pickup in PICKUP_LIST[:]:

            pickup["timer"] -= pickup_dt

            # If magnet is enabled, continuously pull active pickups within magnet range toward the player
            if player_magnet and not player_dead and pickup.get("collecting") is None:
                mag_dx = player_x - pickup["x"]
                mag_dy = player_y - pickup["y"]
                mag_dist = math.hypot(mag_dx, mag_dy)
                if player_magnet_range is None or mag_dist <= player_magnet_range:
                    if mag_dist > 5:
                        mag_speed = min(mag_dist, 700.0 * pickup_dt + (mag_dist * 4.0 * pickup_dt))
                        pickup["x"] += (mag_dx / mag_dist) * mag_speed
                        pickup["y"] += (mag_dy / mag_dist) * mag_speed

            # A collected pickup shrinks away quickly instead of vanishing
            # instantly.
            if pickup.get("collecting") is not None:

                pickup["collecting"] += pickup_dt

                if pickup["collecting"] >= PICKUP_SHRINK_TIME:

                    PICKUP_LIST.remove(pickup)

                continue

            if pickup["timer"] <= 0:
                PICKUP_LIST.remove(pickup)
                continue

            pickup_box = pygame.Rect(
                pickup["x"] - pickup_half,
                pickup["y"] - pickup_half,
                PICKUP_SIZE,
                PICKUP_SIZE
            )
            closest_x = max(
                pickup_box.left,
                min(player_x, pickup_box.right)
            )
            closest_y = max(
                pickup_box.top,
                min(player_y, pickup_box.bottom)
            )
            pickup_dx = player_x - closest_x
            pickup_dy = player_y - closest_y

            if (
                pickup_dx * pickup_dx + pickup_dy * pickup_dy
                < PLAYER_RADIUS * PLAYER_RADIUS
            ):
                if pickup.get("petal"):
                    add_inventory_petal(
                        pickup["petal"],
                        pickup["rarity"],
                        1
                    )
                pickup["collecting"] = 0.0

        spin_speed = 2

        for i in range(PETAL_SLOTS):

            if i < len(petal_slots) and petal_slots[i]["petal"] == "Faster":

                rarity = petal_slots[i]["rarity"]

                spin_amount = PETAL_ROT_SPEED_MUL.get(
                    rarity,
                    1
                )

                spin_speed += spin_amount

        petal_angle += spin_speed * petal_rot_speed_mult
        petal_self_spin_angle += 0.45 * petal_rot_speed_mult

        mouse = pygame.mouse.get_pressed()

        petal_attack = get_third_eye_range(petal_slots)
        if mouse[0]:
            petal_target = petal_attack
            petal_face_target = PETAL_ATTACK
        elif mouse[2]:
            petal_target = PETAL_DEFEND

        else:
            petal_target = PETAL_NORMAL

        if petal_distance < petal_target:
            petal_distance += 10
            if petal_distance > petal_target:
                petal_distance = petal_target

        elif petal_distance > petal_target:
            petal_distance -= 10
            if petal_distance < petal_target:
                petal_distance = petal_target

        # -------- CAMERA --------

        camera_x = player_x - WIDTH // 2
        camera_y = player_y - HEIGHT // 2

        # -------- WHIRLPOOLS UPDATE & PHYSICS --------
        all_enemies_pool = (
            ladybugs
            + hole_ladybugs
            + hole_bees
            + hole_spiders
            + hole_rocks
            + hole_hornets
            + hole_baby_ants
            + hole_soldier_ants
            + hole_worker_ants
            + hole_queen_ants
            + bees
            + spiders
            + rocks
            + hornets
            + baby_ants
            + soldier_ants
            + worker_ants
            + queen_ants
            + ant_eggs
        )
        wp_dt = dt / 1000.0
        for wp in active_whirlpools[:]:
            wp["duration"] -= wp_dt
            if wp["duration"] <= 0:
                active_whirlpools.remove(wp)
                continue
            wp["angle"] = (wp["angle"] + 240 * wp_dt) % 360
            wp["damage_timer"] += wp_dt
            dps_tick = False
            if wp["damage_timer"] >= 1.0:
                wp["damage_timer"] -= 1.0
                dps_tick = True

            for enemy in all_enemies_pool:
                if not enemy.alive or getattr(enemy, "dying", False):
                    continue
                w_dx = wp["x"] - enemy.x
                w_dy = wp["y"] - enemy.y
                w_dist = math.hypot(w_dx, w_dy)
                if w_dist <= wp["radius"] + enemy.radius:
                    # Trapped inside whirlpool!
                    # Initial damage on first entry
                    enemy_id = id(enemy)
                    if enemy_id not in wp["hit_enemies"]:
                        wp["hit_enemies"].add(enemy_id)
                        if wp["initial_damage"] > 0:
                            enemy.take_damage(wp["initial_damage"])

                    # Periodic DPS or continuous infinity spam attack
                    if wp["dps"] == "infinity":
                        # Spam attack every single frame with heavy damage
                        enemy.take_damage(999999)
                    elif dps_tick and isinstance(wp["dps"], (int, float)) and wp["dps"] > 0:
                        enemy.take_damage(wp["dps"])

                    # Strong gravitational pull towards whirlpool center (cannot escape)
                    if w_dist > 4:
                        pull_speed = min(w_dist, max(180.0, (wp["radius"] - w_dist) * 2.0 + 260.0) * wp_dt)
                        enemy.x += (w_dx / w_dist) * pull_speed
                        enemy.y += (w_dy / w_dist) * pull_speed

                        # Swirling vortex tangential movement
                        tangent_x = -w_dy / w_dist
                        tangent_y = w_dx / w_dist
                        swirl_speed = 140.0 * wp_dt
                        enemy.x += tangent_x * swirl_speed
                        enemy.y += tangent_y * swirl_speed
                    else:
                        enemy.x = wp["x"]
                        enemy.y = wp["y"]

                    # Cancel normal enemy knockback velocity while trapped
                    enemy.knockback_x = 0
                    enemy.knockback_y = 0

        # -------- BLACK HOLES UPDATE & PHYSICS --------
        for bh in active_blackholes[:]:
            bh["duration"] -= wp_dt
            if bh["duration"] <= 0:
                active_blackholes.remove(bh)
                continue
            bh["angle"] = (bh["angle"] + 180 * wp_dt) % 360

            # Pull enemies
            for enemy in all_enemies_pool:
                if not enemy.alive or getattr(enemy, "dying", False):
                    continue
                bh_dx = bh["x"] - enemy.x
                bh_dy = bh["y"] - enemy.y
                bh_dist = math.hypot(bh_dx, bh_dy)
                if bh_dist <= bh["radius"] + enemy.radius:
                    # Event horizon / center check: when reaching the very center, the mob instantly disappears
                    horizon_thresh = max(10.0, bh["radius"] * 0.22)
                    if bh_dist <= horizon_thresh:
                        enemy.alive = False
                        enemy.dying = False
                        cleanup_king(enemy)
                        continue

                    pull_mag = min(bh_dist, (bh["pull_speed"] + (bh["radius"] - bh_dist) * 1.5) * wp_dt)
                    enemy.x += (bh_dx / bh_dist) * pull_mag
                    enemy.y += (bh_dy / bh_dist) * pull_mag
                    # Spiral inward
                    t_x = -bh_dy / bh_dist
                    t_y = bh_dx / bh_dist
                    enemy.x += t_x * (bh["pull_speed"] * 0.4 * wp_dt)
                    enemy.y += t_y * (bh["pull_speed"] * 0.4 * wp_dt)
                    enemy.knockback_x = 0
                    enemy.knockback_y = 0

            # Pull petal pickups (loot boxes)
            for pickup in PICKUP_LIST:
                if pickup.get("collecting") is not None:
                    continue
                p_dx = bh["x"] - pickup["x"]
                p_dy = bh["y"] - pickup["y"]
                p_dist = math.hypot(p_dx, p_dy)
                if p_dist <= bh["radius"]:
                    if p_dist > 5:
                        p_speed = min(p_dist, (bh["pull_speed"] * 1.2) * wp_dt)
                        pickup["x"] += (p_dx / p_dist) * p_speed
                        pickup["y"] += (p_dy / p_dist) * p_speed

            # Pull player flower
            if not player_dead:
                pbh_dx = bh["x"] - player_x
                pbh_dy = bh["y"] - player_y
                pbh_dist = math.hypot(pbh_dx, pbh_dy)
                if pbh_dist <= bh["radius"] + PLAYER_RADIUS:
                    # Check center event horizon: teleports the player into "hole land"
                    p_horizon = max(10.0, bh["radius"] * 0.22)
                    if pbh_dist <= p_horizon:
                        if current_dimension != "hole_land":
                            pre_hole_land_x = bh["x"]
                            pre_hole_land_y = bh["y"]
                            pre_hole_land_grid_color = game_target_grid_color if game_target_grid_color != (0, 0, 0) else (60, 180, 75)
                            current_dimension = "hole_land"
                            game_grid_color = (0, 0, 0)
                            game_target_grid_color = (0, 0, 0)
                            player_x = WORLD_WIDTH // 2
                            player_y = WORLD_HEIGHT // 2
                            player_vel_x = 0
                            player_vel_y = 0
                            player_bounce_x = 0
                            player_bounce_y = 0
                            hole_land_banner_timer = 180
                            hole_land_banner_alpha = 255
                            show_error("Entering Hole Land...")
                    else:
                        p_pull = min(pbh_dist, (bh["pull_speed"] + (bh["radius"] - pbh_dist) * 1.5) * wp_dt)
                        player_x += (pbh_dx / pbh_dist) * p_pull
                        player_y += (pbh_dy / pbh_dist) * p_pull
                        # Spiral inward
                        p_tx = -pbh_dy / pbh_dist
                        p_ty = pbh_dx / pbh_dist
                        player_x += p_tx * (bh["pull_speed"] * 0.35 * wp_dt)
                        player_y += p_ty * (bh["pull_speed"] * 0.35 * wp_dt)
                        player_bounce_x = 0
                        player_bounce_y = 0

        # -------- SHIELD DOMES UPDATE & PHYSICS --------
        all_enemy_projectiles = (
            king_stinger_projectiles
            + king_rose_projectiles
            + rock_projectiles
            + soldier_wing_projectiles
            + hole_ladybug_projectiles
        )
        for sd in active_shield_domes[:]:
            sd["duration"] -= wp_dt
            if sd["duration"] <= 0:
                active_shield_domes.remove(sd)
                continue
            sd["pulse"] = (sd["pulse"] + 4.0 * wp_dt)

            # Repel enemies from inside the dome
            for enemy in all_enemies_pool:
                if not enemy.alive or getattr(enemy, "dying", False):
                    continue
                sd_dx = enemy.x - sd["x"]
                sd_dy = enemy.y - sd["y"]
                sd_dist = math.hypot(sd_dx, sd_dy)
                min_dist = sd["radius"] + enemy.radius
                if sd_dist < min_dist:
                    if sd_dist > 0.01:
                        push_mag = (min_dist - sd_dist) + 120.0 * wp_dt
                        enemy.x += (sd_dx / sd_dist) * push_mag
                        enemy.y += (sd_dy / sd_dist) * push_mag
                    else:
                        enemy.x += min_dist

            # Deflect / destroy enemy projectiles that hit the dome perimeter
            for proj in all_enemy_projectiles:
                if not getattr(proj, "alive", True):
                    continue
                # Determine projectile coords
                p_x = getattr(proj, "x", None)
                p_y = getattr(proj, "y", None)
                if p_x is None and isinstance(proj, dict):
                    p_x = proj.get("x")
                    p_y = proj.get("y")
                if p_x is not None and p_y is not None:
                    p_dist = math.hypot(p_x - sd["x"], p_y - sd["y"])
                    if p_dist <= sd["radius"] + 15:
                        # Deflect projectile away or destroy it
                        if hasattr(proj, "alive"):
                            proj.alive = False
                        if hasattr(proj, "vx"):
                            proj.vx = -proj.vx * 1.5
                            proj.vy = -proj.vy * 1.5
                        elif isinstance(proj, dict):
                            proj["alive"] = False


        for ladybug in ladybugs:

            move_with_collision(
                ladybug,
                ladybug.knockback_x,
                ladybug.knockback_y
            )

            ladybug.knockback_x *= 0.85
            ladybug.knockback_y *= 0.85


            # normal AI movement
            old_x = ladybug.x
            old_y = ladybug.y

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                if player_ghost or game_peaceful_mode:
                    # Ghost mode: the enemy can't see the
                    # player, so hide the player far away
                    # while its AI thinks, then restore.
                    ghost_px, ghost_py = player_x, player_y
                    player_x = -1000000
                    player_y = -1000000
                    ladybug.update()
                    player_x, player_y = ghost_px, ghost_py
                else:
                    ladybug.update()

            if ladybug.attack_cooldown > 0:
                ladybug.attack_cooldown -= 1

            if ladybug.petal_attack_cooldown > 0:
                ladybug.petal_attack_cooldown -= 1

            if ladybug.flash_timer > 0:
                ladybug.flash_timer -= 1

        for hlb in hole_ladybugs:
            move_with_collision(
                hlb,
                hlb.knockback_x,
                hlb.knockback_y
            )
            hlb.knockback_x *= 0.85
            hlb.knockback_y *= 0.85

            if player_spawn_cooldown <= 0 and enemies_frozen_timer <= 0:
                if player_ghost or game_peaceful_mode:
                    fake_player_x = hlb.x + 99999
                    fake_player_y = hlb.y + 99999
                    real_px, real_py = player_x, player_y
                    player_x, player_y = fake_player_x, fake_player_y
                    try:
                        hlb.update()
                    finally:
                        player_x, player_y = real_px, real_py
                else:
                    hlb.update()

            if hlb.attack_cooldown > 0:
                hlb.attack_cooldown -= 1

            if hlb.petal_attack_cooldown > 0:
                hlb.petal_attack_cooldown -= 1

            if hlb.flash_timer > 0:
                hlb.flash_timer -= 1

        for hb in hole_bees:
            move_with_collision(
                hb,
                hb.knockback_x,
                hb.knockback_y
            )
            hb.knockback_x *= 0.85
            hb.knockback_y *= 0.85

            if player_spawn_cooldown <= 0 and enemies_frozen_timer <= 0:
                if player_ghost or game_peaceful_mode:
                    fake_player_x = hb.x + 99999
                    fake_player_y = hb.y + 99999
                    real_px, real_py = player_x, player_y
                    player_x, player_y = fake_player_x, fake_player_y
                    try:
                        hb.update()
                    finally:
                        player_x, player_y = real_px, real_py
                else:
                    hb.update()

            if hb.attack_cooldown > 0:
                hb.attack_cooldown -= 1

            if hb.petal_attack_cooldown > 0:
                hb.petal_attack_cooldown -= 1

            if hb.flash_timer > 0:
                hb.flash_timer -= 1


        for bee in bees:

            move_with_collision(
                bee,
                bee.knockback_x,
                bee.knockback_y
            )

            bee.knockback_x *= 0.85
            bee.knockback_y *= 0.85


            old_x = bee.x
            old_y = bee.y

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                if player_ghost or game_peaceful_mode:
                    # Ghost mode: the enemy can't see the
                    # player, so hide the player far away
                    # while its AI thinks, then restore.
                    ghost_px, ghost_py = player_x, player_y
                    player_x = -1000000
                    player_y = -1000000
                    bee.update()
                    player_x, player_y = ghost_px, ghost_py
                else:
                    bee.update()

            if bee.attack_cooldown > 0:
                bee.attack_cooldown -= 1

            if bee.petal_attack_cooldown > 0:
                bee.petal_attack_cooldown -= 1

            if bee.flash_timer > 0:
                bee.flash_timer -= 1


        for hs in hole_spiders:
            move_with_collision(
                hs,
                hs.knockback_x,
                hs.knockback_y
            )
            hs.knockback_x *= 0.85
            hs.knockback_y *= 0.85

            if player_spawn_cooldown <= 0 and enemies_frozen_timer <= 0:
                if player_ghost or game_peaceful_mode:
                    fake_player_x = hs.x + 99999
                    fake_player_y = hs.y + 99999
                    real_px, real_py = player_x, player_y
                    player_x, player_y = fake_player_x, fake_player_y
                    try:
                        hs.update()
                    finally:
                        player_x, player_y = real_px, real_py
                else:
                    hs.update()

            if hs.attack_cooldown > 0:
                hs.attack_cooldown -= 1

            if hs.petal_attack_cooldown > 0:
                hs.petal_attack_cooldown -= 1

            if hs.flash_timer > 0:
                hs.flash_timer -= 1

        for spider in spiders:

            move_with_collision(
                spider,
                spider.knockback_x,
                spider.knockback_y
            )

            spider.knockback_x *= 0.85
            spider.knockback_y *= 0.85


            old_x = spider.x
            old_y = spider.y

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                if player_ghost or game_peaceful_mode:
                    # Ghost mode: the enemy can't see the
                    # player, so hide the player far away
                    # while its AI thinks, then restore.
                    ghost_px, ghost_py = player_x, player_y
                    player_x = -1000000
                    player_y = -1000000
                    spider.update()
                    player_x, player_y = ghost_px, ghost_py
                else:
                    spider.update()

            if spider.attack_cooldown > 0:
                spider.attack_cooldown -= 1

            if spider.petal_attack_cooldown > 0:
                spider.petal_attack_cooldown -= 1

            if spider.flash_timer > 0:
                spider.flash_timer -= 1


        for hr in hole_rocks:
            move_with_collision(
                hr,
                hr.knockback_x,
                hr.knockback_y
            )
            hr.knockback_x *= 0.85
            hr.knockback_y *= 0.85

            if player_spawn_cooldown <= 0 and enemies_frozen_timer <= 0:
                if player_ghost or game_peaceful_mode:
                    fake_player_x = hr.x + 99999
                    fake_player_y = hr.y + 99999
                    real_px, real_py = player_x, player_y
                    player_x, player_y = fake_player_x, fake_player_y
                    try:
                        hr.update()
                    finally:
                        player_x, player_y = real_px, real_py
                else:
                    hr.update()

            if hr.attack_cooldown > 0:
                hr.attack_cooldown -= 1

            if hr.petal_attack_cooldown > 0:
                hr.petal_attack_cooldown -= 1

            if hr.flash_timer > 0:
                hr.flash_timer -= 1

        for rock in rocks:

            move_with_collision(
                rock,
                rock.knockback_x,
                rock.knockback_y
            )

            rock.knockback_x *= 0.85
            rock.knockback_y *= 0.85


            old_x = rock.x
            old_y = rock.y

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                if player_ghost or game_peaceful_mode:
                    # Ghost mode: the enemy can't see the
                    # player, so hide the player far away
                    # while its AI thinks, then restore.
                    ghost_px, ghost_py = player_x, player_y
                    player_x = -1000000
                    player_y = -1000000
                    rock.update()
                    player_x, player_y = ghost_px, ghost_py
                else:
                    rock.update()

            if rock.attack_cooldown > 0:
                rock.attack_cooldown -= 1

            if rock.petal_attack_cooldown > 0:
                rock.petal_attack_cooldown -= 1

            if rock.flash_timer > 0:
                rock.flash_timer -= 1


        for hh in hole_hornets:
            move_with_collision(
                hh,
                hh.knockback_x,
                hh.knockback_y
            )
            hh.knockback_x *= 0.85
            hh.knockback_y *= 0.85

            if player_spawn_cooldown <= 0 and enemies_frozen_timer <= 0:
                if player_ghost or game_peaceful_mode:
                    fake_player_x = hh.x + 99999
                    fake_player_y = hh.y + 99999
                    real_px, real_py = player_x, player_y
                    player_x, player_y = fake_player_x, fake_player_y
                    try:
                        hh.update()
                    finally:
                        player_x, player_y = real_px, real_py
                else:
                    hh.update()

            if hh.attack_cooldown > 0:
                hh.attack_cooldown -= 1

            if hh.petal_attack_cooldown > 0:
                hh.petal_attack_cooldown -= 1

            if hh.flash_timer > 0:
                hh.flash_timer -= 1

        for hornet in hornets:

            move_with_collision(
                hornet,
                hornet.knockback_x,
                hornet.knockback_y
            )

            hornet.knockback_x *= 0.85
            hornet.knockback_y *= 0.85


            old_x = hornet.x
            old_y = hornet.y

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                if player_ghost or game_peaceful_mode:
                    # Ghost mode: the enemy can't see the
                    # player, so hide the player far away
                    # while its AI thinks, then restore.
                    ghost_px, ghost_py = player_x, player_y
                    player_x = -1000000
                    player_y = -1000000
                    hornet.update()
                    player_x, player_y = ghost_px, ghost_py
                else:
                    hornet.update()

            if hornet.attack_cooldown > 0:
                hornet.attack_cooldown -= 1

            if hornet.petal_attack_cooldown > 0:
                hornet.petal_attack_cooldown -= 1

            if hornet.flash_timer > 0:
                hornet.flash_timer -= 1

        for hba in hole_baby_ants:
            move_with_collision(
                hba,
                hba.knockback_x,
                hba.knockback_y
            )
            hba.knockback_x *= 0.85
            hba.knockback_y *= 0.85

            if player_spawn_cooldown <= 0 and enemies_frozen_timer <= 0:
                if player_ghost or game_peaceful_mode:
                    fake_player_x = hba.x + 99999
                    fake_player_y = hba.y + 99999
                    real_px, real_py = player_x, player_y
                    player_x, player_y = fake_player_x, fake_player_y
                    try:
                        hba.update()
                    finally:
                        player_x, player_y = real_px, real_py
                else:
                    hba.update()

            if hba.attack_cooldown > 0:
                hba.attack_cooldown -= 1

            if hba.petal_attack_cooldown > 0:
                hba.petal_attack_cooldown -= 1

            if hba.flash_timer > 0:
                hba.flash_timer -= 1

        for ant in baby_ants:

            move_with_collision(
                ant,
                ant.knockback_x,
                ant.knockback_y
            )

            ant.knockback_x *= 0.85
            ant.knockback_y *= 0.85


            old_x = ant.x
            old_y = ant.y

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                if player_ghost or game_peaceful_mode:
                    # Ghost mode: the enemy can't see the
                    # player, so hide the player far away
                    # while its AI thinks, then restore.
                    ghost_px, ghost_py = player_x, player_y
                    player_x = -1000000
                    player_y = -1000000
                    ant.update()
                    player_x, player_y = ghost_px, ghost_py
                else:
                    ant.update()

            if ant.attack_cooldown > 0:
                ant.attack_cooldown -= 1

            if ant.petal_attack_cooldown > 0:
                ant.petal_attack_cooldown -= 1

            if ant.flash_timer > 0:
                ant.flash_timer -= 1

        for hsa in hole_soldier_ants:
            move_with_collision(
                hsa,
                hsa.knockback_x,
                hsa.knockback_y
            )
            hsa.knockback_x *= 0.85
            hsa.knockback_y *= 0.85

            if player_spawn_cooldown <= 0 and enemies_frozen_timer <= 0:
                if player_ghost or game_peaceful_mode:
                    fake_player_x = hsa.x + 99999
                    fake_player_y = hsa.y + 99999
                    real_px, real_py = player_x, player_y
                    player_x, player_y = fake_player_x, fake_player_y
                    try:
                        hsa.update()
                    finally:
                        player_x, player_y = real_px, real_py
                else:
                    hsa.update()

            if hsa.attack_cooldown > 0:
                hsa.attack_cooldown -= 1

            if hsa.petal_attack_cooldown > 0:
                hsa.petal_attack_cooldown -= 1

            if hsa.flash_timer > 0:
                hsa.flash_timer -= 1

        for soldier_ant in soldier_ants:

            move_with_collision(
                soldier_ant,
                soldier_ant.knockback_x,
                soldier_ant.knockback_y
            )

            soldier_ant.knockback_x *= 0.85
            soldier_ant.knockback_y *= 0.85


            old_x = soldier_ant.x
            old_y = soldier_ant.y

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                if player_ghost or game_peaceful_mode:
                    # Ghost mode: the enemy can't see the
                    # player, so hide the player far away
                    # while its AI thinks, then restore.
                    ghost_px, ghost_py = player_x, player_y
                    player_x = -1000000
                    player_y = -1000000
                    soldier_ant.update()
                    player_x, player_y = ghost_px, ghost_py
                else:
                    soldier_ant.update()

            if soldier_ant.attack_cooldown > 0:
                soldier_ant.attack_cooldown -= 1

            if soldier_ant.petal_attack_cooldown > 0:
                soldier_ant.petal_attack_cooldown -= 1

            if soldier_ant.flash_timer > 0:
                soldier_ant.flash_timer -= 1

        for hwa in hole_worker_ants:
            move_with_collision(
                hwa,
                hwa.knockback_x,
                hwa.knockback_y
            )
            hwa.knockback_x *= 0.85
            hwa.knockback_y *= 0.85

            if player_spawn_cooldown <= 0 and enemies_frozen_timer <= 0:
                if player_ghost or game_peaceful_mode:
                    fake_player_x = hwa.x + 99999
                    fake_player_y = hwa.y + 99999
                    real_px, real_py = player_x, player_y
                    player_x, player_y = fake_player_x, fake_player_y
                    try:
                        hwa.update()
                    finally:
                        player_x, player_y = real_px, real_py
                else:
                    hwa.update()

            if hwa.attack_cooldown > 0:
                hwa.attack_cooldown -= 1

            if hwa.petal_attack_cooldown > 0:
                hwa.petal_attack_cooldown -= 1

            if hwa.flash_timer > 0:
                hwa.flash_timer -= 1

        for worker_ant in worker_ants:

            old_x = worker_ant.x
            old_y = worker_ant.y

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                if player_ghost or game_peaceful_mode:
                    # Ghost mode: the enemy can't see the
                    # player, so hide the player far away
                    # while its AI thinks, then restore.
                    ghost_px, ghost_py = player_x, player_y
                    player_x = -1000000
                    player_y = -1000000
                    worker_ant.update()
                    player_x, player_y = ghost_px, ghost_py
                else:
                    worker_ant.update()

            if worker_ant.attack_cooldown > 0:
                worker_ant.attack_cooldown -= 1

            if worker_ant.petal_attack_cooldown > 0:
                worker_ant.petal_attack_cooldown -= 1

            if worker_ant.flash_timer > 0:
                worker_ant.flash_timer -= 1

        for hqa in hole_queen_ants:
            old_x = hqa.x
            old_y = hqa.y

            if player_spawn_cooldown <= 0 and enemies_frozen_timer <= 0:
                if player_ghost or game_peaceful_mode:
                    fake_player_x = hqa.x + 99999
                    fake_player_y = hqa.y + 99999
                    real_px, real_py = player_x, player_y
                    player_x, player_y = fake_player_x, fake_player_y
                    try:
                        hqa.update()
                    finally:
                        player_x, player_y = real_px, real_py
                else:
                    hqa.update()

            if hqa.attack_cooldown > 0:
                hqa.attack_cooldown -= 1

            if hqa.petal_attack_cooldown > 0:
                hqa.petal_attack_cooldown -= 1

            if hqa.flash_timer > 0:
                hqa.flash_timer -= 1

        for queen_ant in queen_ants:

            old_x = queen_ant.x
            old_y = queen_ant.y

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                if player_ghost or game_peaceful_mode:
                    # Ghost mode: the queen can't see the
                    # player, so hide the player far away
                    # while her AI thinks, then restore.
                    ghost_px, ghost_py = player_x, player_y
                    player_x = -1000000
                    player_y = -1000000
                    queen_ant.update()
                    player_x, player_y = ghost_px, ghost_py
                else:
                    queen_ant.update()

            if queen_ant.attack_cooldown > 0:
                queen_ant.attack_cooldown -= 1

            if queen_ant.petal_attack_cooldown > 0:
                queen_ant.petal_attack_cooldown -= 1

            if queen_ant.flash_timer > 0:
                queen_ant.flash_timer -= 1

        for ant_egg in ant_eggs:

            if (
                player_spawn_cooldown <= 0
                and enemies_frozen_timer <= 0
            ):
                ant_egg.update()

            if ant_egg.attack_cooldown > 0:
                ant_egg.attack_cooldown -= 1

            if ant_egg.petal_attack_cooldown > 0:
                ant_egg.petal_attack_cooldown -= 1

            if ant_egg.flash_timer > 0:
                ant_egg.flash_timer -= 1

        update_queen_eggs()

        # ---------------- ENEMY BUMP SEPARATION ----------------

        # All enemy types push each other apart when they bump
        # into each other.
        bump_list = [
            e
            for e in all_enemies
            if e.alive and not getattr(e, "dying", False)
        ]
        for a_index in range(len(bump_list)):
            enemy_a = bump_list[a_index]
            circles_a = entity_hit_circles(enemy_a)
            for b_index in range(a_index + 1, len(bump_list)):
                enemy_b = bump_list[b_index]
                circles_b = entity_hit_circles(enemy_b)
                # Find the deepest overlapping circle pair.
                hit = None
                for ca_x, ca_y, ca_r in circles_a:
                    for cb_x, cb_y, cb_r in circles_b:
                        d = distance(ca_x, ca_y, cb_x, cb_y)
                        min_dist = ca_r + cb_r
                        if 0 < d < min_dist:
                            overlap = min_dist - d
                            if hit is None or overlap > hit[0]:
                                hit = (
                                    overlap,
                                    ca_x,
                                    ca_y,
                                    cb_x,
                                    cb_y
                                )
                if hit is not None:
                    overlap, ca_x, ca_y, cb_x, cb_y = hit
                    d = distance(ca_x, ca_y, cb_x, cb_y)
                    push_x = (ca_x - cb_x) / d
                    push_y = (ca_y - cb_y) / d
                    immobile_a = type(enemy_a).__name__ in ("Rock", "AntEgg")
                    immobile_b = type(enemy_b).__name__ in ("Rock", "AntEgg")
                    if immobile_a and immobile_b:
                        pass
                    elif immobile_a:
                        enemy_b.x -= push_x * overlap
                        enemy_b.y -= push_y * overlap
                    elif immobile_b:
                        enemy_a.x += push_x * overlap
                        enemy_a.y += push_y * overlap
                    else:
                        enemy_a.x += push_x * overlap / 2
                        enemy_a.y += push_y * overlap / 2
                        enemy_b.x -= push_x * overlap / 2
                        enemy_b.y -= push_y * overlap / 2

        # Keep all enemies (regular mobs, mob kings, mob minions) inside map boundaries
        for enemy in all_enemies:
            rad = getattr(enemy, "radius", 0)
            enemy.x = max(rad, min(enemy.x, WORLD_WIDTH - rad))
            enemy.y = max(rad, min(enemy.y, WORLD_HEIGHT - rad))

        # The queen ant is solid: push the flower out of every
        # body-part circle.
        if not player_dead:
            for hqa in hole_queen_ants:
                for c_x, c_y, c_r in hqa.hitbox_circles():
                    d = distance(player_x, player_y, c_x, c_y)
                    min_dist = PLAYER_RADIUS + c_r
                    if 0 < d < min_dist:
                        player_x = c_x + ((player_x - c_x) / d * min_dist)
                        player_y = c_y + ((player_y - c_y) / d * min_dist)
            for queen_ant in queen_ants:
                for c_x, c_y, c_r in queen_ant.hitbox_circles():
                    d = distance(
                        player_x,
                        player_y,
                        c_x,
                        c_y
                    )
                    min_dist = PLAYER_RADIUS + c_r
                    if 0 < d < min_dist:
                        player_x = c_x + (
                            (player_x - c_x) / d * min_dist
                        )
                        player_y = c_y + (
                            (player_y - c_y) / d * min_dist
                        )

        update_boss_hp()
        # ---------------- PETAL RESPAWN ----------------

        for i in range(PETAL_SLOTS):

            # Respawning petals slide out from the flower.
            if petal_alive[i] and petal_deploy[i] < 1.0:
                petal_deploy[i] = min(
                    1.0,
                    petal_deploy[i] + 0.08
                )

            if (
                not petal_alive[i]
                and not player_dead
                and petal_slots[i]["filled"]
            ):

                if petal_respawn_timer[i] > 0:

                    petal_respawn_timer[i] -= 1

                else:

                    petal_alive[i] = True
                    petal_hp[i] = petal_max_hp[i]
                    petal_deploy[i] = 0.0

                    if i < len(petal_slots) and petal_slots[i]["petal"] == "Light":
                        light_count = get_petal_count("Light", petal_slots[i]["rarity"])
                        light_hp[i] = [petal_max_hp[i]] * light_count
                        light_cooldowns[i] = [0] * light_count
                        light_alive[i] = [True] * light_count

                    save_player()

            if petal_flash_timers[i] > 0:
                petal_flash_timers[i] -= 1

        if player_flash_timer > 0:
            player_flash_timer -= 1

        # ---------------- PETAL REGEN ----------------

        for i in range(PETAL_SLOTS):

            if petal_alive[i]:

                if i < len(petal_slots) and petal_slots[i]["petal"] == "Light":
                    for li in range(len(light_hp[i])):
                        if light_alive[i][li] and light_hp[i][li] < petal_max_hp[i]:
                            light_hp[i][li] += 0.05
                            if light_hp[i][li] > petal_max_hp[i]:
                                light_hp[i][li] = petal_max_hp[i]
                elif petal_hp[i] < petal_max_hp[i]:
                    petal_hp[i] += 0.05

                    if petal_hp[i] > petal_max_hp[i]:
                        petal_hp[i] = petal_max_hp[i]


        # enemy touching player
        for hlb in hole_ladybugs:
            if hlb.alive:
                d = distance(player_x, player_y, hlb.x, hlb.y)
                if d < PLAYER_RADIUS + hlb.radius and not player_dead:
                    if player_spawn_cooldown <= 0:
                        if (
                            hlb.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):
                            player_hp -= get_enemy_attack_damage(hlb)
                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4
                            push_player_from(hlb, 6.0)

                            if player_hp == 0:
                                kill_player(hlb)

                            hlb.attack_cooldown = 2

        for hb in hole_bees:
            if hb.alive:
                d = distance(player_x, player_y, hb.x, hb.y)
                if d < PLAYER_RADIUS + hb.radius and not player_dead:
                    if player_spawn_cooldown <= 0:
                        if (
                            hb.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):
                            player_hp -= get_enemy_attack_damage(hb)
                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4
                            push_player_from(hb, 6.0)

                            if player_hp == 0:
                                kill_player(hb)

                            hb.attack_cooldown = 2

        # enemy touching player
        for ladybug in ladybugs:

            if ladybug.alive:

                d = distance(
                    player_x,
                    player_y,
                    ladybug.x,
                    ladybug.y
                )

                if d < PLAYER_RADIUS + ladybug.radius and not player_dead:

                    if player_spawn_cooldown <= 0:

                        if (
                            ladybug.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):

                            player_hp -= get_enemy_attack_damage(ladybug)

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(ladybug)

                            if player_hp == 0:
                                kill_player(ladybug)

                            ladybug.attack_cooldown = 2



        for bee in bees:

            if bee.alive:
                d = distance(
                    player_x,
                    player_y,
                    bee.x,
                    bee.y
                )

                if d < PLAYER_RADIUS + bee.radius and not player_dead:

                    if player_spawn_cooldown <= 0:

                        if (
                            bee.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):

                            player_hp -= get_enemy_attack_damage(bee)

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(bee)

                            if player_hp == 0:
                                kill_player(bee)

                            bee.attack_cooldown = 2




        for hs in hole_spiders:
            if hs.alive:
                d = distance(player_x, player_y, hs.x, hs.y)
                if d < PLAYER_RADIUS + hs.radius and not player_dead:
                    if player_spawn_cooldown <= 0:
                        if (
                            hs.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):
                            player_hp -= get_enemy_attack_damage(hs)
                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4
                            push_player_from(hs, 6.0)

                            if player_hp == 0:
                                kill_player(hs)

                            hs.attack_cooldown = 2

        for spider in spiders:

            if spider.alive:
                d = distance(
                    player_x,
                    player_y,
                    spider.x,
                    spider.y
                )

                if d < PLAYER_RADIUS + spider.radius and not player_dead:

                    if player_spawn_cooldown <= 0:

                        if (
                            spider.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):

                            player_hp -= get_enemy_attack_damage(spider)

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(spider)

                            if player_hp == 0:
                                kill_player(spider)

                            spider.attack_cooldown = 2




        for hr in hole_rocks:
            if hr.alive:
                d = distance(player_x, player_y, hr.x, hr.y)
                if d < PLAYER_RADIUS + hr.radius and not player_dead:
                    if player_spawn_cooldown <= 0:
                        if (
                            hr.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):
                            player_hp -= get_enemy_attack_damage(hr)
                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4
                            push_player_from(hr, 6.0)

                            if player_hp == 0:
                                kill_player(hr)

                            hr.attack_cooldown = 2

        for rock in rocks:

            if rock.alive:
                d = distance(
                    player_x,
                    player_y,
                    rock.x,
                    rock.y
                )

                if d < PLAYER_RADIUS + rock.radius and not player_dead:

                    if player_spawn_cooldown <= 0:

                        if (
                            rock.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):

                            player_hp -= get_enemy_attack_damage(rock)

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(rock)

                            if player_hp == 0:
                                kill_player(rock)

                            rock.attack_cooldown = 2




        for hh in hole_hornets:
            if hh.alive:
                d = distance(player_x, player_y, hh.x, hh.y)
                if d < PLAYER_RADIUS + hh.radius and not player_dead:
                    if player_spawn_cooldown <= 0:
                        if (
                            hh.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):
                            player_hp -= get_enemy_attack_damage(hh)
                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4
                            push_player_from(hh, 6.0)

                            if player_hp == 0:
                                kill_player(hh)

                            hh.attack_cooldown = 2

        for hornet in hornets:

            if hornet.alive:
                d = distance(
                    player_x,
                    player_y,
                    hornet.x,
                    hornet.y
                )

                if d < PLAYER_RADIUS + hornet.radius and not player_dead:

                    if player_spawn_cooldown <= 0:

                        if (
                            hornet.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):

                            player_hp -= get_enemy_attack_damage(hornet)

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(hornet)

                            if player_hp == 0:
                                kill_player(hornet)

                            hornet.attack_cooldown = 2


        for hba in hole_baby_ants:
            if hba.alive:
                d = distance(player_x, player_y, hba.x, hba.y)
                if d < PLAYER_RADIUS + hba.radius and not player_dead:
                    if player_spawn_cooldown <= 0:
                        if (
                            hba.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):
                            player_hp -= get_enemy_attack_damage(hba)
                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4
                            push_player_from(hba, 6.0)

                            if player_hp == 0:
                                kill_player(hba)

                            hba.attack_cooldown = 2

        for ant in baby_ants:

            if ant.alive:

                d = distance(
                    player_x,
                    player_y,
                    ant.x,
                    ant.y
                )

                if d < PLAYER_RADIUS + ant.radius and not player_dead:

                    if player_spawn_cooldown <= 0:

                        if (
                            ant.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):

                            player_hp -= get_enemy_attack_damage(ant)

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(ant)

                            if player_hp == 0:
                                kill_player(ant)

                            ant.attack_cooldown = 2


        for hsa in hole_soldier_ants:
            if hsa.alive:
                d = distance(player_x, player_y, hsa.x, hsa.y)
                if d < PLAYER_RADIUS + hsa.radius and not player_dead:
                    if player_spawn_cooldown <= 0:
                        if (
                            hsa.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):
                            player_hp -= get_enemy_attack_damage(hsa)
                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4
                            push_player_from(hsa, 7.0)

                            if player_hp == 0:
                                kill_player(hsa)

                            hsa.attack_cooldown = 2

        for soldier_ant in soldier_ants:

            if soldier_ant.alive:

                d = distance(
                    player_x,
                    player_y,
                    soldier_ant.x,
                    soldier_ant.y
                )

                if d < PLAYER_RADIUS + soldier_ant.radius and not player_dead:

                    if player_spawn_cooldown <= 0:

                        if (
                            soldier_ant.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):

                            player_hp -= get_enemy_attack_damage(soldier_ant)

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(soldier_ant)

                            if player_hp == 0:
                                kill_player(soldier_ant)

                            soldier_ant.attack_cooldown = 2

        for hwa in hole_worker_ants:
            if hwa.alive and not player_dead:
                d = distance(player_x, player_y, hwa.x, hwa.y)
                if (
                    d < PLAYER_RADIUS + hwa.radius
                    and player_spawn_cooldown <= 0
                    and hwa.attack_cooldown == 0
                    and not player_ghost
                    and not game_peaceful_mode
                ):
                    player_hp -= get_enemy_attack_damage(hwa)
                    if player_hp < 0:
                        player_hp = 0

                    player_flash_timer = 4
                    push_player_from(hwa, 6.0)

                    if player_hp == 0:
                        kill_player(hwa)

                    hwa.attack_cooldown = 2

        for worker_ant in worker_ants:

            # All worker ants damage and push the flower on
            # contact (like the other ants).
            if worker_ant.alive and not player_dead:

                d = distance(
                    player_x,
                    player_y,
                    worker_ant.x,
                    worker_ant.y
                )
                if (
                    d < PLAYER_RADIUS + worker_ant.radius
                    and player_spawn_cooldown <= 0
                    and worker_ant.attack_cooldown == 0
                    and not player_ghost
                    and not game_peaceful_mode
                ):
                    player_hp -= get_enemy_attack_damage(worker_ant)

                    if player_hp < 0:
                        player_hp = 0

                    player_flash_timer = 4

                    push_player_from(worker_ant)

                    if player_hp == 0:
                        kill_player(worker_ant)

                    worker_ant.attack_cooldown = 2

        for hqa in hole_queen_ants:
            if hqa.alive and not player_dead:
                for c_x, c_y, c_r in hqa.hitbox_circles():
                    d = distance(player_x, player_y, c_x, c_y)
                    if not (
                        0 < d < PLAYER_RADIUS + c_r
                        and player_spawn_cooldown <= 0
                        and hqa.attack_cooldown == 0
                        and not player_ghost
                        and not game_peaceful_mode
                    ):
                        continue

                    player_hp -= get_enemy_attack_damage(hqa)
                    if player_hp < 0:
                        player_hp = 0

                    player_flash_timer = 4

                    knock_x = player_x - c_x
                    knock_y = player_y - c_y
                    knock_len = math.sqrt(knock_x * knock_x + knock_y * knock_y)
                    if knock_len > 0:
                        knock_x /= knock_len
                        knock_y /= knock_len
                        player_x += knock_x * 8.0
                        player_y += knock_y * 8.0

                    if player_hp == 0:
                        kill_player(hqa)

                    hqa.attack_cooldown = 2

        for queen_ant in queen_ants:

            # Queen ants damage the flower on contact with any of
            # her three body-part circles, and knock it away from
            # the body part it touched.
            if queen_ant.alive and not player_dead:

                for c_x, c_y, c_r in queen_ant.hitbox_circles():
                    d = distance(
                        player_x,
                        player_y,
                        c_x,
                        c_y
                    )
                    if not (
                        0 < d < PLAYER_RADIUS + c_r
                        and player_spawn_cooldown <= 0
                        and queen_ant.attack_cooldown == 0
                        and not player_ghost
                        and not game_peaceful_mode
                    ):
                        continue

                    player_hp -= get_enemy_attack_damage(queen_ant)

                    if player_hp < 0:
                        player_hp = 0

                    player_flash_timer = 4

                    # Knockback away from the touched body part.
                    knock_x = player_x - c_x
                    knock_y = player_y - c_y
                    knock_len = math.sqrt(
                        knock_x * knock_x + knock_y * knock_y
                    )
                    if knock_len == 0:
                        knock_x = 1
                        knock_y = 0
                        knock_len = 1
                    player_bounce_x = (
                        knock_x / knock_len * 6.0
                    )
                    player_bounce_y = (
                        knock_y / knock_len * 6.0
                    )

                    if player_hp == 0:
                        kill_player(queen_ant)

                    queen_ant.attack_cooldown = 2
                    break

        for ant_egg in ant_eggs:

            if ant_egg.alive and not player_dead:
                d = distance(
                    player_x,
                    player_y,
                    ant_egg.x,
                    ant_egg.y
                )

                if d < PLAYER_RADIUS + ant_egg.radius:

                    if player_spawn_cooldown <= 0:

                        if (
                            ant_egg.attack_cooldown == 0
                            and not player_ghost
                            and not game_peaceful_mode
                        ):

                            player_hp -= get_enemy_attack_damage(ant_egg)

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(ant_egg)

                            if player_hp == 0:
                                kill_player(ant_egg)

                            ant_egg.attack_cooldown = 2

        # -------- DRAW --------

        screen.fill(game_grid_color)

        # Compute grass colors based on current game grid color
        if current_dimension == "hole_land":
            grass_color = (0, 0, 0)
            grass_border = (20, 20, 25)
        else:
            grass_color = game_grid_color
            grass_border = tuple(max(0, c - 10) for c in game_grid_color)

        # Draw grass tiles
        start_x = int(camera_x // GRASS_SIZE) - 1
        end_x = start_x + WIDTH // GRASS_SIZE + 3

        start_y = int(camera_y // GRASS_SIZE) - 1
        end_y = start_y + HEIGHT // GRASS_SIZE + 3

        for gx in range(start_x, end_x):
            for gy in range(start_y, end_y):

                world_x = gx * GRASS_SIZE
                world_y = gy * GRASS_SIZE

                screen_x = world_x - camera_x
                screen_y = world_y - camera_y

                color = grass_color

                pygame.draw.rect(
                    screen,
                    color,
                    (screen_x, screen_y, GRASS_SIZE, GRASS_SIZE)
                )

                pygame.draw.rect(
                    screen,
                    grass_border,
                    (screen_x, screen_y, GRASS_SIZE, GRASS_SIZE),
                    1
                )

                if game_theme == "night":
                    # Deterministic little starry twinkles on tiles
                    star_hash = (gx * 73856093 ^ gy * 19349663) & 0xFFFFFFFF
                    if star_hash % 7 == 0:
                        star_ox = (star_hash >> 4) % (GRASS_SIZE - 8) + 4
                        star_oy = (star_hash >> 8) % (GRASS_SIZE - 8) + 4
                        star_bright = 160 + (star_hash % 95)
                        pygame.draw.circle(
                            screen,
                            (star_bright, star_bright, min(255, star_bright + 30)),
                            (int(screen_x + star_ox), int(screen_y + star_oy)),
                            1 if star_hash % 2 == 0 else 2
                        )

        # ---------------- KING WEBS ----------------
        # Transparent spider webs drawn under the mobs.

        for web in king_webs:

            web_x = web["x"] - camera_x
            web_y = web["y"] - camera_y

            if (
                -web["radius"] * 2 <= web_x <= WIDTH + web["radius"] * 2
                and -web["radius"] * 2 <= web_y <= HEIGHT + web["radius"] * 2
            ):
                # Fade out during the last second of life.
                alpha = 255
                if web["timer"] < 60:
                    alpha = int(255 * web["timer"] / 60)
                web_surf = web["surface"].copy()
                web_surf.set_alpha(alpha)
                if web["radius"] < web["target_radius"]:
                    scale = web["radius"] / web["target_radius"]
                    new_size = (
                        max(2, int(web_surf.get_width() * scale)),
                        max(2, int(web_surf.get_height() * scale))
                    )
                    web_surf = pygame.transform.scale(
                        web_surf,
                        new_size
                    )
                rotated = pygame.transform.rotate(
                    web_surf,
                    web["spin"]
                )
                screen.blit(
                    rotated,
                    rotated.get_rect(
                        center=(int(web_x), int(web_y))
                    )
                )

        # -------- DRAW WHIRLPOOLS --------
        for wp in active_whirlpools:
            sx = int(wp["x"] - camera_x)
            sy = int(wp["y"] - camera_y)
            r = int(wp["radius"])
            # Only draw if on screen
            if -r * 2 <= sx <= WIDTH + r * 2 and -r * 2 <= sy <= HEIGHT + r * 2:
                # Semi-transparent vortex surface
                v_surf = pygame.Surface((r * 2 + 8, r * 2 + 8), pygame.SRCALPHA)
                center_pt = (r + 4, r + 4)
                # Outer fade water ring
                pygame.draw.circle(v_surf, (0, 160, 230, 70), center_pt, r)
                # Concentric swirling vortex arms
                num_rings = max(3, int(r // 20))
                for ri in range(1, num_rings + 1):
                    ring_r = int(r * (ri / num_rings))
                    ring_alpha = int(90 + (1.0 - ri / num_rings) * 110)
                    pygame.draw.circle(v_surf, (40, 200, 255, ring_alpha), center_pt, ring_r, max(2, int(r * 0.03)))
                # Spiral swirling arms
                base_a = math.radians(wp["angle"])
                for arm in range(4):
                    arm_offset = arm * (math.pi / 2)
                    pts = []
                    for step in range(12):
                        step_t = step / 11.0
                        step_r = r * step_t
                        step_a = base_a + arm_offset + (step_t * 3.5)
                        pt_x = center_pt[0] + math.cos(step_a) * step_r
                        pt_y = center_pt[1] + math.sin(step_a) * step_r
                        pts.append((int(pt_x), int(pt_y)))
                    if len(pts) >= 2:
                        pygame.draw.lines(v_surf, (180, 240, 255, 170), False, pts, max(2, int(r * 0.04)))
                # Deep center eye of the whirlpool
                pygame.draw.circle(v_surf, (10, 60, 140, 220), center_pt, max(6, int(r * 0.22)))
                pygame.draw.circle(v_surf, (0, 20, 60, 240), center_pt, max(3, int(r * 0.12)))
                screen.blit(v_surf, (sx - r - 4, sy - r - 4))

        # -------- DRAW BLACK HOLES --------
        for bh in active_blackholes:
            sx = int(bh["x"] - camera_x)
            sy = int(bh["y"] - camera_y)
            r = int(bh["radius"])
            if -r * 2 <= sx <= WIDTH + r * 2 and -r * 2 <= sy <= HEIGHT + r * 2:
                bh_surf = pygame.Surface((r * 2 + 10, r * 2 + 10), pygame.SRCALPHA)
                center_pt = (r + 5, r + 5)
                # Outer purple gravitational lens glow
                pygame.draw.circle(bh_surf, (80, 20, 140, 50), center_pt, r)
                pygame.draw.circle(bh_surf, (140, 40, 220, 90), center_pt, int(r * 0.75))
                # Swirling accretion disk spiral rings
                bh_angle = math.radians(bh["angle"])
                for arm in range(3):
                    arm_offset = arm * (2 * math.pi / 3)
                    pts = []
                    for step in range(14):
                        step_t = step / 13.0
                        step_r = r * 0.2 + (r * 0.75) * step_t
                        step_a = bh_angle + arm_offset + (step_t * 4.0)
                        pts.append((int(center_pt[0] + math.cos(step_a) * step_r), int(center_pt[1] + math.sin(step_a) * step_r)))
                    if len(pts) >= 2:
                        pygame.draw.lines(bh_surf, (220, 130, 255, 180), False, pts, max(2, int(r * 0.04)))
                # Inner event horizon (pure abyss black with sharp violet border)
                horizon_r = max(8, int(r * 0.32))
                pygame.draw.circle(bh_surf, (180, 60, 255, 220), center_pt, horizon_r + 3)
                pygame.draw.circle(bh_surf, (5, 0, 15, 255), center_pt, horizon_r)
                screen.blit(bh_surf, (sx - r - 5, sy - r - 5))

        # -------- DRAW SHIELD DOMES --------
        for sd in active_shield_domes:
            sx = int(sd["x"] - camera_x)
            sy = int(sd["y"] - camera_y)
            r = int(sd["radius"])
            if -r * 2 <= sx <= WIDTH + r * 2 and -r * 2 <= sy <= HEIGHT + r * 2:
                sd_surf = pygame.Surface((r * 2 + 10, r * 2 + 10), pygame.SRCALPHA)
                center_pt = (r + 5, r + 5)
                # Shimmering energetic hexagonal/dome forcefield
                pulse_wave = math.sin(sd["pulse"]) * 15
                fill_alpha = int(45 + pulse_wave)
                pygame.draw.circle(sd_surf, (0, 210, 255, fill_alpha), center_pt, r)
                # Electric perimeter rings
                pygame.draw.circle(sd_surf, (120, 240, 255, 210), center_pt, r, max(3, int(r * 0.035)))
                pygame.draw.circle(sd_surf, (220, 255, 255, 140), center_pt, max(1, r - 3), 2)
                # Hexagonal force lines
                for angle_deg in range(0, 360, 60):
                    a_rad = math.radians(angle_deg + sd["pulse"] * 10)
                    px = center_pt[0] + math.cos(a_rad) * r
                    py = center_pt[1] + math.sin(a_rad) * r
                    pygame.draw.line(sd_surf, (100, 230, 255, 100), center_pt, (int(px), int(py)), 2)
                screen.blit(sd_surf, (sx - r - 5, sy - r - 5))

        for ladybug in ladybugs:
            ladybug.draw()

        for hlb in hole_ladybugs:
            hlb.draw()

        for hb in hole_bees:
            hb.draw()

        for bee in bees:
            bee.draw()

        for hs in hole_spiders:
            hs.draw()

        for spider in spiders:
            spider.draw()

        for hr in hole_rocks:
            hr.draw()

        for rock in rocks:
            rock.draw()

        for hh in hole_hornets:
            hh.draw()

        for hornet in hornets:
            hornet.draw()

        for hba in hole_baby_ants:
            hba.draw()

        for ant in baby_ants:
            ant.draw()

        for hsa in hole_soldier_ants:
            hsa.draw()

        for soldier_ant in soldier_ants:

            soldier_ant.draw()

        for hwa in hole_worker_ants:
            hwa.draw()

        for worker_ant in worker_ants:

            worker_ant.draw()

        # ---------------- QUEEN ANT EGGS ----------------

        # Eggs are drawn before the queens so they sit on the
        # back layer, underneath the queen's body.
        for egg in queen_eggs:

            egg_x = int(egg["x"] - camera_x)
            egg_y = int(egg["y"] - camera_y)
            egg_r = egg["radius"]
            wobble = (
                math.sin(
                    time.time() * 8 + egg["wobble"]
                ) * 1.5
            )
            if egg.get("is_void_egg", False):
                pygame.draw.circle(
                    screen,
                    (28, 8, 42),
                    (egg_x, int(egg_y + wobble)),
                    egg_r
                )
                pygame.draw.circle(
                    screen,
                    (0, 240, 255),
                    (egg_x, int(egg_y + wobble)),
                    egg_r,
                    3
                )
                pygame.draw.circle(
                    screen,
                    (200, 50, 255),
                    (egg_x, int(egg_y + wobble)),
                    max(2, int(egg_r * 0.45))
                )
            else:
                pygame.draw.circle(
                    screen,
                    (250, 240, 180),
                    (egg_x, int(egg_y + wobble)),
                    egg_r
                )
                pygame.draw.circle(
                    screen,
                    (200, 175, 110),
                    (egg_x, int(egg_y + wobble)),
                    egg_r,
                    3
                )

        for hqa in hole_queen_ants:
            hqa.draw()

        for queen_ant in queen_ants:

            queen_ant.draw()

        for ant_egg in ant_eggs:
            ant_egg.draw()

        # ---------------- FLOWER MINIONS ----------------

        for minion in flower_minions:

            minion.draw()

            if getattr(minion, "dying", False):
                continue

            # Small HP bar above the minion.
            m_r = max(1, int(minion.radius))
            hp_ratio = max(0.0, min(1.0, minion.hp / max(1, minion.max_hp)))
            bar_w = max(14, min(32, int(m_r * 1.4)))
            bar_h = 4
            bar_x = int(minion.x - camera_x - bar_w / 2)
            bar_y = int(minion.y - camera_y - m_r - 10)
            pygame.draw.rect(
                screen,
                (60, 60, 60),
                (bar_x, bar_y, bar_w, bar_h),
                border_radius=2
            )
            pygame.draw.rect(
                screen,
                (80, 220, 100),
                (
                    bar_x,
                    bar_y,
                    max(0, int(bar_w * hp_ratio)),
                    bar_h
                ),
                border_radius=2
            )

        # ---------------- FLOWER PROJECTILES (NOT MADE YET) ----------------

        for fp in flower_projectiles:
            if isinstance(fp, dict):
                fp_x = fp.get("x", 0) - camera_x
                fp_y = fp.get("y", 0) - camera_y
                fp_r = fp.get("radius", 8) * fp.get("shrink", 1.0)
                if -50 <= fp_x <= WIDTH + 50 and -50 <= fp_y <= HEIGHT + 50:
                    pygame.draw.circle(
                        screen,
                        fp.get("color", (255, 220, 60)),
                        (int(fp_x), int(fp_y)),
                        max(1, int(fp_r))
                    )
            elif hasattr(fp, "draw"):
                fp.draw()

        # ---------------- HORNET MISSILES ----------------

        for missile in hornet_missiles:

            missile_x = missile["x"] - camera_x
            missile_y = missile["y"] - camera_y

            if (
                -50 <= missile_x <= WIDTH + 50
                and -50 <= missile_y <= HEIGHT + 50
            ):
                missile_rad = math.atan2(
                    missile["dy"],
                    missile["dx"]
                )
                shrink = missile.get("shrink", 1.0)
                owner_radius = missile["owner"].radius * shrink
                missile_len = owner_radius * 0.9
                missile_w = owner_radius * 0.45
                fx = math.cos(missile_rad)
                fy = math.sin(missile_rad)
                side_x = -fy
                side_y = fx
                if missile.get("is_hole_projectile"):
                    # Void Torpedo: Glowing cyan thruster trail, obsidian dart body, neon violet wings
                    flame_fx = -fx * missile_len * 0.7
                    flame_fy = -fy * missile_len * 0.7
                    flame_pts = [
                        (missile_x - fx * missile_len * 0.4 + side_x * missile_w * 0.4, missile_y - fy * missile_len * 0.4 + side_y * missile_w * 0.4),
                        (missile_x + flame_fx, missile_y + flame_fy),
                        (missile_x - fx * missile_len * 0.4 - side_x * missile_w * 0.4, missile_y - fy * missile_len * 0.4 - side_y * missile_w * 0.4),
                    ]
                    pygame.draw.polygon(screen, (0, 240, 255), flame_pts)
                    # Obsidian missile chassis
                    body_pts = [
                        (missile_x + fx * missile_len * 1.15, missile_y + fy * missile_len * 1.15),
                        (missile_x - fx * missile_len * 0.35 + side_x * missile_w * 1.25, missile_y - fy * missile_len * 0.35 + side_y * missile_w * 1.25),
                        (missile_x - fx * missile_len * 0.4, missile_y - fy * missile_len * 0.4),
                        (missile_x - fx * missile_len * 0.35 - side_x * missile_w * 1.25, missile_y - fy * missile_len * 0.35 - side_y * missile_w * 1.25),
                    ]
                    pygame.draw.polygon(screen, (22, 6, 35), body_pts)
                    pygame.draw.polygon(screen, (190, 50, 255), body_pts, 2)
                    # Neon warhead core
                    pygame.draw.circle(screen, (255, 0, 140), (int(missile_x + fx * missile_len * 0.7), int(missile_y + fy * missile_len * 0.7)), max(2, int(missile_w * 0.4)))
                else:
                    pygame.draw.polygon(
                        screen,
                        (0, 0, 0),
                        [
                            (
                                missile_x + fx * missile_len,
                                missile_y + fy * missile_len
                            ),
                            (
                                missile_x - fx * missile_len * 0.4
                                + side_x * missile_w,
                                missile_y - fy * missile_len * 0.4
                                + side_y * missile_w
                            ),
                            (
                                missile_x - fx * missile_len * 0.4
                                - side_x * missile_w,
                                missile_y - fy * missile_len * 0.4
                                - side_y * missile_w
                            )
                        ]
                    )
                draw_projectile_hp_bar(
                    missile_x,
                    missile_y,
                    missile["owner"].radius * 0.5,
                    missile["hp"],
                    missile["max_hp"]
                )
                # Hitbox outline.
                pygame.draw.circle(
                    screen,
                    (255, 60, 60),
                    (int(missile_x), int(missile_y)),
                    int(missile["owner"].radius * 0.5),
                    2
                )

        # ---------------- HOLE LADYBUG YELLOW ORBS ----------------
        for orb in hole_ladybug_projectiles:
            ox = orb["x"] - camera_x
            oy = orb["y"] - camera_y
            if -50 <= ox <= WIDTH + 50 and -50 <= oy <= HEIGHT + 50:
                shrink = orb.get("shrink", 1.0)
                orb_r = max(2, int(orb.get("radius", 10) * shrink))
                # Outer glowing yellow ring
                pygame.draw.circle(screen, (255, 235, 100), (int(ox), int(oy)), orb_r + 2)
                # Vibrant solid yellow circle
                pygame.draw.circle(screen, (255, 215, 0), (int(ox), int(oy)), orb_r)
                # Bright white core
                pygame.draw.circle(screen, (255, 255, 200), (int(ox), int(oy)), max(1, orb_r // 2))

        # ---------------- ROCK PROJECTILES ----------------

        for rock_p in rock_projectiles:

            rock_x = rock_p["x"] - camera_x
            rock_y = rock_p["y"] - camera_y

            if (
                -50 <= rock_x <= WIDTH + 50
                and -50 <= rock_y <= HEIGHT + 50
            ):
                rock_r = rock_p.get("radius", 8) * rock_p.get(
                    "shrink",
                    1.0
                )
                rock_pts = [
                    (
                        rock_x + px * rock_r,
                        rock_y + py * rock_r
                    )
                    for px, py in rock_p.get(
                        "shape",
                        [(0, -1), (-1, 1), (1, 1)]
                    )
                ]
                if rock_p.get("is_hole_projectile"):
                    # Violent 80% spikier void shard: obsidian core, glowing purple outline, electric cyan spike nodes
                    pygame.draw.polygon(screen, (25, 8, 38), rock_pts)
                    pygame.draw.polygon(screen, (190, 50, 255), rock_pts, 2)
                    for pt in rock_pts[1::2]:
                        pygame.draw.circle(screen, (0, 240, 255), (int(pt[0]), int(pt[1])), max(1, int(rock_r * 0.15)))
                else:
                    pygame.draw.polygon(
                        screen,
                        (110, 110, 110),
                        rock_pts
                    )
                    pygame.draw.polygon(
                        screen,
                        (70, 70, 70),
                        rock_pts,
                        2
                    )
                draw_projectile_hp_bar(
                    rock_x,
                    rock_y,
                    rock_p.get("radius", 8),
                    rock_p["hp"],
                    rock_p["max_hp"]
                )
                # Hitbox outline.
                pygame.draw.circle(
                    screen,
                    (255, 60, 60),
                    (int(rock_x), int(rock_y)),
                    int(rock_p.get("radius", 8)),
                    2
                )

        # ---------------- KING STINGERS ----------------

        for stinger in king_stinger_projectiles:

            stinger_x = stinger["x"] - camera_x
            stinger_y = stinger["y"] - camera_y

            if (
                -50 <= stinger_x <= WIDTH + 50
                and -50 <= stinger_y <= HEIGHT + 50
            ):
                # Dark triangle pointing along its flight angle,
                # like a stinger petal.
                stinger_r = stinger.get("radius", 8) * (
                    stinger.get("shrink", 1.0)
                )
                # A chasing stinger faces the direction it flies
                # (toward the flower); others keep their launch angle.
                if stinger.get("has_homed"):
                    stinger_rad = math.atan2(
                        stinger["dy"],
                        stinger["dx"]
                    )
                else:
                    stinger_rad = math.radians(stinger["angle"])
                tip_x = (
                    stinger_x
                    + math.cos(stinger_rad) * stinger_r * 2
                )
                tip_y = (
                    stinger_y
                    + math.sin(stinger_rad) * stinger_r * 2
                )
                side_x = math.cos(stinger_rad + math.pi / 2)
                side_y = math.sin(stinger_rad + math.pi / 2)
                pygame.draw.polygon(
                    screen,
                    (50, 50, 55),
                    [
                        (tip_x, tip_y),
                        (
                            stinger_x + side_x * stinger_r,
                            stinger_y + side_y * stinger_r
                        ),
                        (
                            stinger_x - side_x * stinger_r,
                            stinger_y - side_y * stinger_r
                        )
                    ]
                )
                draw_projectile_hp_bar(
                    stinger_x,
                    stinger_y,
                    stinger.get("radius", 8),
                    stinger["hp"],
                    stinger["max_hp"]
                )
                # Hitbox outline.
                pygame.draw.circle(
                    screen,
                    (255, 60, 60),
                    (int(stinger_x), int(stinger_y)),
                    int(stinger.get("radius", 8)),
                    2
                )

        # ---------------- KING ROSES ----------------

        for rose in king_rose_projectiles:

            rose_x = rose["x"] - camera_x
            rose_y = rose["y"] - camera_y

            if (
                -50 <= rose_x <= WIDTH + 50
                and -50 <= rose_y <= HEIGHT + 50
            ):
                # Small pink rose petal with a darker outline.
                rose_r = rose.get("radius", 8)
                pygame.draw.circle(
                    screen,
                    (255, 105, 180),
                    (int(rose_x), int(rose_y)),
                    rose_r
                )
                pygame.draw.circle(
                    screen,
                    (200, 60, 130),
                    (int(rose_x), int(rose_y)),
                    rose_r,
                    2
                )
                draw_projectile_hp_bar(
                    rose_x,
                    rose_y,
                    rose.get("radius", 8),
                    rose["hp"],
                    rose["max_hp"]
                )
                # Hitbox outline.
                pygame.draw.circle(
                    screen,
                    (255, 60, 60),
                    (int(rose_x), int(rose_y)),
                    int(rose.get("radius", 8)),
                    2
                )

        # ---------------- SOLDIER KING WINGS ----------------

        for wing in soldier_wing_projectiles:

            wing_x = wing["x"] - camera_x
            wing_y = wing["y"] - camera_y

            if (
                -200 <= wing_x <= WIDTH + 200
                and -200 <= wing_y <= HEIGHT + 200
            ):
                wing_r = wing.get("radius", 8) * wing.get(
                    "shrink",
                    1.0
                )
                spin_rad = math.radians(wing.get("spin", 0))
                cos_s = math.cos(spin_rad)
                sin_s = math.sin(spin_rad)
                # Wing shape: start, control and end points of the
                # two bezier curves, scaled up and spun.
                start = (-0.9, 0.5)
                control = (0.9, 1.0)
                end = (0.7, -1.0)

                def spin_point(px, py):
                    return (
                        wing_x
                        + (px * cos_s - py * sin_s) * wing_r,
                        wing_y
                        + (px * sin_s + py * cos_s) * wing_r
                    )

                start_x, start_y = spin_point(*start)
                end_x, end_y = spin_point(*end)
                points = []
                for j in range(31):
                    t = j / 30
                    px = (
                        (1 - t) ** 2 * start_x
                        + 2 * (1 - t) * t * spin_point(*control)[0]
                        + t ** 2 * end_x
                    )
                    py = (
                        (1 - t) ** 2 * start_y
                        + 2 * (1 - t) * t * spin_point(*control)[1]
                        + t ** 2 * end_y
                    )
                    points.append((px, py))
                inner_control = (-0.1, 0.1)
                for j in range(30, -1, -1):
                    t = j / 30
                    px = (
                        (1 - t) ** 2 * start_x
                        + 2 * (1 - t) * t * spin_point(*inner_control)[0]
                        + t ** 2 * end_x
                    )
                    py = (
                        (1 - t) ** 2 * start_y
                        + 2 * (1 - t) * t * spin_point(*inner_control)[1]
                        + t ** 2 * end_y
                    )
                    points.append((px, py))
                pygame.draw.polygon(
                    screen,
                    (255, 255, 255),
                    points
                )
                pygame.draw.lines(
                    screen,
                    (150, 150, 150),
                    True,
                    points,
                    2
                )
                draw_projectile_hp_bar(
                    wing_x,
                    wing_y,
                    wing.get("radius", 8),
                    wing["hp"],
                    wing["max_hp"]
                )
                # Hitbox outline.
                pygame.draw.circle(
                    screen,
                    (255, 60, 60),
                    (int(wing_x), int(wing_y)),
                    int(wing.get("radius", 8) * 0.7),
                    2
                )

        for pickup in PICKUP_LIST:

            collect_t = pickup.get("collecting")
            shrink_scale = 1.0
            if collect_t is not None:
                shrink_scale = max(
                    0.0,
                    1.0 - collect_t / PICKUP_SHRINK_TIME
                )

            px = pickup["x"] - camera_x
            py = pickup["y"] - camera_y
            box_size = max(
                1,
                int(
                    (
                        PICKUP_SIZE
                        + int(
                            (math.sin(pickup_pulse_phase) + 1.0) * 3.0
                        )
                    )
                    * shrink_scale
                )
            )
            half = box_size // 2
            pickup_rect = pygame.Rect(
                px - half,
                py - half,
                box_size,
                box_size
            )
            pickup_box_color = RARITY_COLORS.get(
                pickup["rarity"],
                (140, 140, 140)
            )
            pygame.draw.rect(
                screen,
                lighten_color(
                    pickup_box_color,
                    0.4
                ),
                pickup_rect,
                border_radius=2
            )
            pygame.draw.rect(
                screen,
                pickup_box_color,
                pickup_rect,
                4,
                border_radius=2
            )
            if pickup.get("petal"):
                draw_petal(
                    pickup["petal"],
                    px,
                    py,
                    pickup["rarity"],
                    size_scale=(
                        (PICKUP_SIZE * 0.6)
                        / (PETAL_RADIUS * 2)
                        * shrink_scale
                    )
                )

        # draw the merged wall layer (one shared outline, connected look)
        vx0 = int(camera_x)
        vy0 = int(camera_y)

        if vx0 < 0:
            vx0 = 0
        if vy0 < 0:
            vy0 = 0

        vw = min(WIDTH, WORLD_SIZE - vx0)
        vh = min(HEIGHT, WORLD_SIZE - vy0)

        for wall in walls:
            wall.draw()

        # ---------------- PLAYER MOVEMENT TRAIL ----------------
        if player_trail_particles:
            for pt in player_trail_particles[:]:
                pt["x"] += pt["vx"]
                pt["y"] += pt["vy"]
                pt["life"] -= 1
                if pt.get("type") == "star":
                    pt["rot"] = (pt["rot"] + pt.get("vrot", 0)) % 360
                if pt["life"] <= 0:
                    player_trail_particles.remove(pt)
                    continue

                t = pt["life"] / pt["max_life"]
                curr_size = max(1, int(pt["size"] * t))
                alpha = int(220 * t)
                screen_px = int(pt["x"] - camera_x)
                screen_py = int(pt["y"] - camera_y)

                if -50 <= screen_px <= WIDTH + 50 and -50 <= screen_py <= HEIGHT + 50:
                    surf = pygame.Surface((curr_size * 2 + 4, curr_size * 2 + 4), pygame.SRCALPHA)
                    center = (curr_size + 2, curr_size + 2)
                    r, g, b = pt["color"]

                    if pt.get("type") == "circle":
                        pygame.draw.circle(surf, (r, g, b, alpha), center, curr_size)
                        pygame.draw.circle(surf, (255, 255, 255, min(255, alpha + 30)), center, max(1, curr_size // 2))
                    elif pt.get("type") == "flame":
                        # Inner bright core
                        pygame.draw.circle(surf, (r, g, b, alpha), center, curr_size)
                        pygame.draw.circle(surf, (255, 255, 200, min(255, int(alpha * 1.2))), center, max(1, curr_size // 2))
                    elif pt.get("type") == "star":
                        # 4-point sparkle star
                        star_r = curr_size
                        rot_rad = math.radians(pt.get("rot", 0))
                        cos_r = math.cos(rot_rad)
                        sin_r = math.sin(rot_rad)
                        pts = []
                        for i_sp in range(8):
                            sp_angle = rot_rad + i_sp * (math.pi / 4)
                            sp_rad = star_r if i_sp % 2 == 0 else star_r * 0.3
                            pts.append((center[0] + math.cos(sp_angle) * sp_rad, center[1] + math.sin(sp_angle) * sp_rad))
                        pygame.draw.polygon(surf, (r, g, b, alpha), pts)

                    screen.blit(surf, (screen_px - (curr_size + 2), screen_py - (curr_size + 2)))

            # Draw petals

        # ---------------- DRAW PETAL SLOTS ----------------

        # Ensure petal_slots matches PETAL_SLOTS (defensive)
        while len(petal_slots) < PETAL_SLOTS:
            petal_slots.append({
                "filled": False,
                "petal": "Basic",
                "rarity": "Common"
            })

        # Ensure swap_petal_slots matches PETAL_SLOTS (defensive)
        while len(swap_petal_slots) < PETAL_SLOTS:
            swap_petal_slots.append({
                "filled": False,
                "petal": "Basic",
                "rarity": "Common"
            })

        slots_per_row = PETAL_SLOTS

        total_width = (
            slots_per_row * PETAL_SLOT_SIZE +
            (slots_per_row - 1) * PETAL_SLOT_GAP
        )

        start_x = WIDTH // 2 - total_width // 2

        if show_hud:
                    for i in range(PETAL_SLOTS * 2):

                        # Main slots: indices 0 to PETAL_SLOTS-1
                        # Swap slots: indices PETAL_SLOTS to PETAL_SLOTS*2-1
                        if i < PETAL_SLOTS:
                            # Main equip slot
                            row = i // slots_per_row
                            col = i % slots_per_row
                            slot = petal_slots[i]
                        else:
                            # Swap slot
                            swap_idx = i - PETAL_SLOTS
                            row = (swap_idx // slots_per_row) + 1
                            col = swap_idx % slots_per_row
                            slot = swap_petal_slots[swap_idx]

                        if row < 0 or row >= 2:
                            continue

                        x = start_x + col * (PETAL_SLOT_SIZE + PETAL_SLOT_GAP)

                        y = PETAL_BAR_Y + row * (PETAL_SLOT_SIZE + PETAL_SLOT_GAP)


                        # Slot color

                        slot_color = (90,90,90)
                        border_color = (160,160,160)

                        if slot["filled"]:

                            if slot["rarity"] in RARITY_COLORS:

                                slot_color = RARITY_COLORS[
                                    slot["rarity"]
                                ]

                            border_color = (
                                max(slot_color[0] - 40, 0),
                                max(slot_color[1] - 40, 0),
                                max(slot_color[2] - 40, 0)
                            )

                        # Draw slot background

                        if i < PETAL_SLOTS and slot.get("filled", False):
                            # Main equip slots with a petal filled: show rarity box
                            draw_rarity_slot(
                                x,
                                y,
                                PETAL_SLOT_SIZE,
                                slot.get("rarity", "Common")
                            )
                        else:
                            # Empty slot (swap slots or main slot without a petal): just gray box
                            pygame.draw.rect(
                                screen,
                                (90,90,90),
                                (
                                    x,
                                    y,
                                    PETAL_SLOT_SIZE,
                                    PETAL_SLOT_SIZE
                                ),
                                border_radius=8
                            )

                        # Draw basic petal image only for filled main slots

                        if i < PETAL_SLOTS and slot.get("filled", False):

                            petal_type = slot.get("petal", "Basic")
                            rarity = slot.get("rarity", "Common")

                            slot_sprite = make_petal_surface(
                                petal_type,
                                0,
                                0,
                                rarity,
                                size_scale=1.4
                            )
                            sprite_rect = slot_sprite.get_bounding_rect()
                            if sprite_rect.w > 0 and sprite_rect.h > 0:
                                slot_sprite = slot_sprite.subsurface(sprite_rect)
                            cx = x + PETAL_SLOT_SIZE // 2
                            cy = y + PETAL_SLOT_SIZE // 2
                            screen.blit(
                                slot_sprite,
                                (
                                    cx - slot_sprite.get_width() // 2,
                                    cy - slot_sprite.get_height() // 2
                                )
                            )

                        # ---------------- HP UPGRADE BUTTON --------------

                        # Respawn timer number above slot

                        if i < PETAL_SLOTS:

                            if not petal_alive[i] and petal_respawn_timer[i] > 0:

                                font = respawn_timer_font

                                seconds = math.ceil(
                                    petal_respawn_timer[i] / FPS
                                )

                                text = font.render(
                                    str(seconds),
                                    True,
                                    (255,255,255)
                                )

                                screen.blit(
                                    text,
                                    (
                                        x + PETAL_SLOT_SIZE//2 - text.get_width()//2,
                                        y - 30
                                    )
                                )


        # Compute total visual elements so all petals and lights
        # form one even polygon around the flower.
        total_elements = 0
        for i in range(PETAL_SLOTS):
            if not petal_alive[i]:
                continue
            if petal_slots[i]["petal"] == "Light":
                total_elements += get_petal_count(
                    "Light",
                    petal_slots[i]["rarity"]
                )
            else:
                total_elements += 1

        angle_increment = 360 / total_elements if total_elements > 0 else 72
        element_index = 0

        for i in range(PETAL_SLOTS):
            if not petal_alive[i]:
                continue

            petal_type = petal_slots[i]["petal"]
            rarity = petal_slots[i]["rarity"]

            if petal_type == "Light":
                light_count = get_petal_count("Light", rarity)
                # Draw each light as a separate element
                for li in range(light_count):
                    angle = math.radians(
                        petal_angle + element_index * angle_increment
                    )
                    x = (
                        WIDTH // 2
                        + math.cos(angle)
                        * petal_orbit_distance(i)
                    )
                    y = (
                        HEIGHT // 2
                        + math.sin(angle)
                        * petal_orbit_distance(i)
                    )

                    orbit_angle = petal_angle
                    petal_angle = petal_self_spin_angle
                    draw_petal(
                        "Light",
                        x,
                        y,
                        rarity,
                        flash_timer=petal_flash_timers[i]
                    )
                    petal_angle = orbit_angle

                    element_index += 1
            else:
                # Draw normal petal as single element
                # The giant moon orbits a little farther out so it
                # doesn't crowd the flower.
                moon_extra_orbit = (
                    40
                    if petal_type == "Moon"
                    else 0
                )
                angle = math.radians(
                    petal_angle + element_index * angle_increment
                )
                x = (
                    WIDTH // 2
                    + math.cos(angle)
                    * petal_orbit_distance(i, moon_extra_orbit)
                )
                y = (
                    HEIGHT // 2
                    + math.sin(angle)
                    * petal_orbit_distance(i, moon_extra_orbit)
                )

                orbit_angle = petal_angle
                petal_angle = petal_self_spin_angle
                draw_petal(
                    petal_type,
                    x,
                    y,
                    rarity,
                    size_scale=(
                        4.0
                        if petal_type == "Moon"
                        else 1.0
                    ),
                    flash_timer=petal_flash_timers[i]
                )
                petal_angle = orbit_angle

                element_index += 1


            # ---------------- UPGRADE MENU DRAW ----------------


        # ---------------- RESPAWN TIMER ----------------

        if i < PETAL_SLOTS:

            if not petal_alive[i]:

                seconds = math.ceil(
                    petal_respawn_timer[i] / FPS
                )


                text = font.render(
                    str(seconds),
                    True,
                    (255,255,255)
                )


                text_rect = text.get_rect(
                    center=(
                        x + PETAL_SLOT_SIZE//2,
                        y - 15
                    )
                )


                screen.blit(
                    text,
                    text_rect
                )


            # ---------------- PETAL ATTACK ----------------

# ---------------- PETAL ATTACK ----------------

            # Calculate total elements and increment for attack positions
            total_elements = 0
            for i in range(PETAL_SLOTS):
                if not petal_alive[i]:
                    continue
                if petal_slots[i]["petal"] == "Light":
                    total_elements += get_petal_count(
                        "Light",
                        petal_slots[i]["rarity"]
                    )
                else:
                    total_elements += 1
            angle_increment = 360 / total_elements if total_elements > 0 else 72
            element_index = 0

            for i in range(PETAL_SLOTS):

                # skip dead petals
                if not petal_alive[i]:
                    continue


                angle = math.radians(
                    petal_angle + element_index * angle_increment
                )

                slot_start_index = element_index

                petal_size_scale = (
                    4.0
                    if petal_slots[i]["petal"] == "Moon"
                    else 1.0
                )
                petal_world_x = (
                    player_x
                    + math.cos(angle)
                    * petal_orbit_distance(
                        i,
                        40 if petal_slots[i]["petal"] == "Moon" else 0
                    )
                )
                petal_world_y = (
                    player_y
                    + math.sin(angle)
                    * petal_orbit_distance(
                        i,
                        40 if petal_slots[i]["petal"] == "Moon" else 0
                    )
                )


                petal_type = petal_slots[i]["petal"]
                rarity = petal_slots[i]["rarity"]

                if petal_type == "Light":
                    light_count = get_petal_count(petal_type, rarity)
                    if light_count == 0:
                        light_count = 1

                    # Ensure per-light arrays have enough capacity
                    while len(light_cooldowns[i]) < light_count:
                        light_cooldowns[i].append(0)
                    while len(light_hp[i]) < light_count:
                        light_hp[i].append(petal_max_hp[i])
                    while len(light_alive[i]) < light_count:
                        light_alive[i].append(True)

                    damage = get_petal_damage(petal_type, rarity) / light_count
                    petal_range = int(PETAL_RADIUS * 0.55)

                    all_enemies = (
                        ladybugs +
                        hole_ladybugs +
                        hole_bees +
                        hole_spiders +
                        hole_rocks +
                        hole_hornets +
                        hole_baby_ants +
                        hole_soldier_ants +
                        hole_worker_ants +
                        hole_queen_ants +
                        bees +
                        spiders +
                        rocks +
                        hornets +
                        baby_ants +
                        soldier_ants +
                        worker_ants +
                        queen_ants +
                        ant_eggs
                    )

                    hit = False

                    for li in range(light_count):
                        # Handle cooldown and respawn
                        if light_cooldowns[i][li] > 0:
                            light_cooldowns[i][li] -= 1
                            if light_cooldowns[i][li] <= 0:
                                light_alive[i][li] = True
                                light_hp[i][li] = petal_max_hp[i]
                                petal_deploy[i] = 0.0

                        if not light_alive[i][li]:
                            continue

                        # Calculate light position
                        light_angle = petal_angle + element_index * angle_increment
                        light_x = player_x + math.cos(math.radians(light_angle)) * petal_orbit_distance(i)
                        light_y = player_y + math.sin(math.radians(light_angle)) * petal_orbit_distance(i)

                        if light_cooldowns[i][li] == 0:
                            for enemy in all_enemies:
                                if not enemy.alive:
                                    continue

                                d = distance(light_x, light_y, enemy.x, enemy.y)

                                if d < petal_range + enemy.radius:
                                    if enemy.attack_cooldown == 0:
                                        light_hp[i][li] -= (
                                            enemy.petal_damage
                                            if hasattr(enemy, "petal_damage")
                                            else get_enemy_attack_damage(enemy)
                                        )
                                        if light_hp[i][li] <= 0:
                                            light_alive[i][li] = False
                                            light_cooldowns[i][li] = PETAL_RELOAD["Light"]
                                        enemy.attack_cooldown = 2

                                    enemy.take_damage(damage)
                                    hit = True

                        element_index += 1

                    # Check if all lights dead
                    if not any(light_alive[i]):
                        petal_alive[i] = False
                        petal_respawn_timer[i] = PETAL_RELOAD["Light"]

                else:
                    # Existing non-Light logic
                    # cooldown
                    if petal_cooldowns[i] > 0:
                        petal_cooldowns[i] -= 1

                    # attack only if ready
                    if petal_cooldowns[i] == 0:

                        hit = False

                        all_enemies = (
                            ladybugs +
                            hole_ladybugs +
                            hole_bees +
                            hole_spiders +
                            hole_rocks +
                            hole_hornets +
                            hole_baby_ants +
                            hole_soldier_ants +
                            hole_worker_ants +
                            hole_queen_ants +
                            bees +
                            spiders +
                            rocks +
                            hornets +
                            baby_ants +
                            soldier_ants +
                            worker_ants +
                            queen_ants +
                            ant_eggs
                        )

                        damage = get_petal_damage(
                            petal_type,
                            rarity
                        )

                        for enemy in all_enemies:

                            if not enemy.alive:
                                continue

                            d = distance(
                                petal_world_x,
                                petal_world_y,
                                enemy.x,
                                enemy.y
                            )

                            petal_range = (
                                int(PETAL_RADIUS * petal_size_scale)
                            )

                            if petal_slots[i]["petal"] == "Wing":
                                petal_range = int(PETAL_RADIUS)

                            if d < petal_range + enemy.radius:

                                # enemy damages petal
                                if enemy.attack_cooldown == 0:

                                    # Mobs damage petals, scaled by
                                    # rarity so high-rarity mobs
                                    # one-shot them.
                                    petal_hp[i] -= (
                                        enemy.petal_damage
                                        if hasattr(enemy, "petal_damage")
                                        else get_enemy_attack_damage(enemy)
                                    )
                                    petal_flash_timers[i] = 4

                                    if petal_hp[i] <= 0:

                                        petal_hp[i] = 0
                                        petal_alive[i] = False

                                        petal_respawn_timer[i] = PETAL_RELOAD[
                                            petal_slots[i]["petal"]
                                        ]

                                    enemy.attack_cooldown = 2

                                # petal attacks enemy
                                enemy.take_damage(damage)

                                if petal_type == "Heavy":

                                    dx = enemy.x - player_x
                                    dy = enemy.y - player_y

                                    length = math.sqrt(dx * dx + dy * dy)

                                    if length != 0:

                                        dx /= length
                                        dy /= length

                                        knockback = (
                                            8 *
                                            HEAVY_KNOCKBACK_MULTIPLIER[
                                                rarity
                                            ]
                                        )

                                        weight = (
                                            MOB_WEIGHT.get(type(enemy).__name__, 1.0) *
                                            MOB_WEIGHT_MULTIPLIER.get(enemy.rarity, 1.0)
                                        )

                                        enemy.knockback_x += dx * knockback / weight
                                        enemy.knockback_y += dy * knockback / weight

                                hit = True

                        # Petals can also destroy the king's roses
                        # and the bee king's stingers.
                        for rose in king_rose_projectiles[:]:
                            rose_d = distance(
                                petal_world_x,
                                petal_world_y,
                                rose["x"],
                                rose["y"]
                            )
                            if rose_d < (
                                petal_range
                                + rose.get("radius", 8)
                            ):
                                rose["hp"] -= damage
                                if rose["hp"] <= 0:
                                    king_rose_projectiles.remove(rose)
                                hit = True

                        for stinger in king_stinger_projectiles[:]:
                            stinger_d = distance(
                                petal_world_x,
                                petal_world_y,
                                stinger["x"],
                                stinger["y"]
                            )
                            if stinger_d < (
                                petal_range
                                + stinger.get("radius", 8)
                            ):
                                stinger["hp"] -= damage
                                if stinger["hp"] <= 0:
                                    king_stinger_projectiles.remove(stinger)
                                hit = True

                        for rice in baby_ant_rice[:]:
                            if rice.get("dying") or rice["respawn"] > 0:
                                continue
                            rice_x, rice_y = baby_ant_rice_pos(rice)
                            rice_d = distance(
                                petal_world_x,
                                petal_world_y,
                                rice_x,
                                rice_y
                            )
                            if rice_d < (
                                petal_range
                                + rice.get("radius", 8)
                            ):
                                rice["hp"] -= damage
                                if rice["hp"] <= 0:
                                    rice["dying"] = True
                                    rice["shrink"] = 1.0
                                hit = True

                        for corn in worker_ant_corn[:]:
                            if corn.get("dying") or corn["respawn"] > 0:
                                continue
                            corn_d = distance(
                                petal_world_x,
                                petal_world_y,
                                corn["x"],
                                corn["y"]
                            )
                            if corn_d < (
                                petal_range
                                + corn.get("radius", 10)
                            ):
                                corn["hp"] -= damage
                                if corn["hp"] <= 0:
                                    corn["dying"] = True
                                    corn["shrink"] = 1.0
                                hit = True

                        for wing in soldier_wing_projectiles[:]:
                            if wing.get("dying"):
                                continue
                            wing_d = distance(
                                petal_world_x,
                                petal_world_y,
                                wing["x"],
                                wing["y"]
                            )
                            if wing_d < (
                                petal_range
                                + wing.get("radius", 8)
                            ):
                                wing["hp"] -= damage
                                if wing["hp"] <= 0:
                                    wing["dying"] = True
                                    wing["shrink"] = 1.0
                                hit = True

                        for rock_p in rock_projectiles[:]:
                            rock_d = distance(
                                petal_world_x,
                                petal_world_y,
                                rock_p["x"],
                                rock_p["y"]
                            )
                            if rock_d < (
                                petal_range
                                + rock_p.get("radius", 8)
                            ):
                                rock_p["hp"] -= damage
                                if rock_p["hp"] <= 0:
                                    rock_projectiles.remove(rock_p)
                                hit = True

                        for missile in hornet_missiles[:]:
                            missile_d = distance(
                                petal_world_x,
                                petal_world_y,
                                missile["x"],
                                missile["y"]
                            )
                            if missile_d < (
                                petal_range + 10
                            ):
                                missile["hp"] -= damage
                                if missile["hp"] <= 0:
                                    hornet_missiles.remove(missile)
                                hit = True

                        if hit:
                            if petal_type == "Wing":
                                petal_cooldowns[i] = PETAL_RELOAD["Wing"]
                            else:
                                petal_cooldowns[i] = 0

                    element_index += 1

                # ---------------- PETAL HP BAR ----------------

                if petal_type == "Light":
                    # Draw individual HP bars for each light element
                    for li in range(light_count):
                        if light_hp[i][li] < petal_max_hp[i]:
                            bar_width = 20
                            bar_height = 4
                            hp_percent = max(0.0, min(1.0, light_hp[i][li] / max(1, petal_max_hp[i])))
                            bar_orbit = petal_orbit_distance(
                                i,
                                40 if petal_slots[i]["petal"] == "Moon" else 0
                            )
                            bar_petal_r = PETAL_RADIUS
                            light_angle = math.radians(
                                petal_angle + (slot_start_index + li) * angle_increment
                            )
                            bar_x = int(
                                WIDTH//2 +
                                math.cos(light_angle) * bar_orbit -
                                bar_width/2
                            )
                            bar_y = int(
                                HEIGHT//2 +
                                math.sin(light_angle) * bar_orbit -
                                bar_petal_r -
                                12
                            )
                            pygame.draw.rect(
                                screen,
                                (80,80,80),
                                (bar_x, bar_y, bar_width, bar_height)
                            )
                            pygame.draw.rect(
                                screen,
                                (0,255,0),
                                (bar_x, bar_y, int(bar_width * hp_percent), bar_height)
                            )

                if show_hud and petal_hp[i] < petal_max_hp[i]:

                    bar_width = 35
                    bar_height = 5

                    hp_percent = max(
                        0.0,
                        min(
                            1.0,
                            petal_hp[i] / max(1, petal_max_hp[i])
                        )
                    )

                    bar_orbit = petal_orbit_distance(
                        i,
                        40 if petal_slots[i]["petal"] == "Moon" else 0
                    )
                    bar_petal_r = PETAL_RADIUS

                    pygame.draw.rect(
                        screen,
                        (80,80,80),
                        (
                            int(
                                WIDTH//2 +
                                math.cos(angle) * bar_orbit -
                                bar_width/2
                            ),
                            int(
                                HEIGHT//2 +
                                math.sin(angle) * bar_orbit -
                                bar_petal_r -
                                12
                            ),
                            bar_width,
                            bar_height
                        )
                    )


                    pygame.draw.rect(
                        screen,
                        (0,255,0),
                        (
                            int(
                                WIDTH//2 +
                                math.cos(angle) * bar_orbit -
                                bar_width/2
                            ),
                            int(
                                HEIGHT//2 +
                                math.sin(angle) * bar_orbit -
                                bar_petal_r -
                                12
                            ),
                            int(bar_width * hp_percent),
                            bar_height
                        )
                    )

                # Draw player


                if show_hud and boss_hp > 0:

                    font = large_hud_font

                    boss_text = font.render(
                        boss_rarity + " " + boss_name,
                        True,
                        (255,0,0)
                    )

                    screen.blit(
                        boss_text,
                        (
                            WIDTH//2 - boss_text.get_width()//2,
                            70
                        )
                    )


                    bar_width = 600
                    bar_height = 25

                    hp_percent = max(0.0, min(1.0, boss_hp / max(1, boss_max_hp)))


                    pygame.draw.rect(
                        screen,
                        (60,60,60),
                        (
                            WIDTH//2 - bar_width//2,
                            120,
                            bar_width,
                            bar_height
                        )
                    )


                    pygame.draw.rect(
                        screen,
                        (255,0,0),
                        (
                            WIDTH//2 - bar_width//2,
                            120,
                            int(bar_width * hp_percent),
                            bar_height
                        )
                    )

        # ---- MOON PUSH: continuous push while hitboxes overlap ----

        all_enemies = (
            ladybugs
            + hole_ladybugs
            + hole_bees
            + hole_spiders
            + hole_rocks
            + hole_hornets
            + hole_baby_ants
            + hole_soldier_ants
            + hole_worker_ants
            + hole_queen_ants
            + bees
            + spiders
            + rocks
            + hornets
            + baby_ants
            + soldier_ants
            + worker_ants
            + queen_ants
            + ant_eggs
        )

        # ---------------- ENEMY DEATH SHRINK ----------------
        # D-key deleted enemies shrink until they vanish.

        for enemy in all_enemies:

            if getattr(enemy, "dying", False):

                enemy.shrink_scale -= 0.08

                if enemy.shrink_scale <= 0:

                    enemy.shrink_scale = 0
                    enemy.dying = False
                    enemy.alive = False
                    cleanup_king(enemy)
                else:
                    enemy.radius = (
                        enemy.full_radius * enemy.shrink_scale
                    )

        spawn_king_minions()
        update_flower_minions()
        update_flower_projectiles()
        update_flower_minion_projectile_fight()
        update_king_roses()
        update_king_stingers()
        update_baby_ant_rice()
        update_soldier_wings()
        update_worker_ant_corn()
        update_king_webs()
        update_rock_projectiles()
        update_hornet_missiles()
        update_hole_ladybug_projectiles()

        for i in range(PETAL_SLOTS):

            if (
                not petal_alive[i]
                or petal_slots[i]["petal"] != "Moon"
            ):
                continue

            moon_angle = math.radians(
                petal_angle + i * 72
            )
            moon_x = (
                player_x
                + math.cos(moon_angle)
                * petal_orbit_distance(i, 40)
            )
            moon_y = (
                player_y
                + math.sin(moon_angle)
                * petal_orbit_distance(i, 40)
            )
            moon_hitbox = PETAL_RADIUS * 4

            for enemy in all_enemies:

                if not enemy.alive:
                    continue

                d = distance(
                    moon_x,
                    moon_y,
                    enemy.x,
                    enemy.y
                )

                if d < moon_hitbox + enemy.radius:

                    dx = enemy.x - player_x
                    dy = enemy.y - player_y

                    length = math.sqrt(dx * dx + dy * dy)

                    if length != 0:

                        dx /= length
                        dy /= length

                        rarity_push = (
                            8
                            / MOB_WEIGHT_MULTIPLIER[
                                enemy.rarity
                            ]
                        )

                        enemy.knockback_x += dx * rarity_push
                        enemy.knockback_y += (
                            dy * rarity_push
                        )

        # ---------------- FLOWER LEVEL UI ----------------

        font = flower_info_font


        level_text = font.render(
            "Level: " + str(flower_level),
            True,
            (255,255,255)
        )


        xp_text = font.render(
            "XP: " + format_number(int(flower_xp)) +
            "/" +
            format_number(int(flower_xp_needed)),
            True,
            (255,255,255)
        )


        points_text = font.render(
            "Points: " + format_number(upgrade_points),
            True,
            (255,255,0)
        )



        # ---------------- DRAW PLAYER ----------------

            # Draw player

        player_center_x = WIDTH // 2
        player_center_y = HEIGHT // 2


        # body
        # ---------------- PLAYER HP BAR ----------------

        if show_hud:
            bar_width = 80
            bar_height = 8

            hp_percent = max(
                0,
                min(
                    player_hp / PLAYER_MAX_HP,
                    1
                )
            )

            pygame.draw.rect(
                screen,
                (210, 45, 45),
                (
                    player_center_x - bar_width//2,
                    player_center_y - PLAYER_RADIUS - 25,
                    bar_width,
                    bar_height
                )
            )

            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    player_center_x - bar_width//2,
                    player_center_y - PLAYER_RADIUS - 25,
                    int(bar_width * hp_percent),
                    bar_height
                )
            )
        player_center_x = WIDTH // 2
        player_center_y = HEIGHT // 2

        if player_ghost:

            # Ghost mode: draw the flower semi-transparent.
            ghost_surf = pygame.Surface(
                (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                ghost_surf,
                player_body_color,
                (PLAYER_RADIUS, PLAYER_RADIUS),
                PLAYER_RADIUS
            )
            pygame.draw.circle(
                ghost_surf,
                player_outline_color,
                (PLAYER_RADIUS, PLAYER_RADIUS),
                PLAYER_RADIUS,
                5
            )
            ghost_surf.set_alpha(90)
            screen.blit(
                ghost_surf,
                (
                    int(player_center_x) - PLAYER_RADIUS,
                    int(player_center_y) - PLAYER_RADIUS
                )
            )

        else:

            pygame.draw.circle(
                screen,
                player_body_color,
                (player_center_x, player_center_y),
                PLAYER_RADIUS
            )


            # outline

            pygame.draw.circle(
                screen,
                player_outline_color,
                (player_center_x, player_center_y),
                PLAYER_RADIUS,
                5
            )


        # ---- PLAYER DAMAGE FLASH ----

        if player_flash_timer > 0:
            flash_surf = pygame.Surface(
                (PLAYER_RADIUS * 2, PLAYER_RADIUS * 2),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                flash_surf,
                (255, 0, 0),
                (PLAYER_RADIUS, PLAYER_RADIUS),
                PLAYER_RADIUS
            )
            screen.blit(
                flash_surf,
                (int(player_center_x) - PLAYER_RADIUS,
                 int(player_center_y) - PLAYER_RADIUS),
                special_flags=pygame.BLEND_RGB_ADD
            )


        # ---- HITBOX VISUALIZATION (blue outlines, no gameplay change) ----
        if settings_switch3_on:
            hitbox_color = (0, 100, 255)
            hitbox_width = 2

            # Player hitbox
            pygame.draw.circle(
                screen,
                hitbox_color,
                (int(player_center_x), int(player_center_y)),
                PLAYER_RADIUS,
                hitbox_width
            )

            # Compute total visual elements (same as drawing loop)
            total_elements = 0
            for i in range(PETAL_SLOTS):
                if not petal_alive[i]:
                    continue
                if petal_slots[i]["petal"] == "Light":
                    total_elements += get_petal_count(
                        "Light",
                        petal_slots[i]["rarity"]
                    )
                else:
                    total_elements += 1

            angle_increment = 360 / total_elements if total_elements > 0 else 72
            element_index = 0

            # Petal hitboxes
            for i in range(PETAL_SLOTS):
                if not petal_alive[i]:
                    continue

                petal_type = petal_slots[i]["petal"]
                rarity = petal_slots[i]["rarity"]

                if petal_type == "Light":
                    light_count = get_petal_count("Light", rarity)
                    petal_range_draw = int(PETAL_RADIUS * 0.55)

                    for li in range(light_count):
                        angle = math.radians(
                            petal_angle + element_index * angle_increment
                        )
                        l_x = int(
                            player_center_x + math.cos(angle) * petal_orbit_distance(i)
                        )
                        l_y = int(
                            player_center_y + math.sin(angle) * petal_orbit_distance(i)
                        )
                        pygame.draw.circle(
                            screen,
                            hitbox_color,
                            (l_x, l_y),
                            petal_range_draw,
                            hitbox_width
                        )
                        element_index += 1
                else:
                    petal_size_scale = (
                        4.0
                        if petal_type == "Moon"
                        else 1.0
                    )
                    moon_extra_orbit = (
                        40
                        if petal_type == "Moon"
                        else 0
                    )
                    angle = math.radians(
                        petal_angle + element_index * angle_increment
                    )
                    hp_x = int(
                        player_center_x
                        + math.cos(angle)
                        * petal_orbit_distance(i, moon_extra_orbit)
                    )
                    hp_y = int(
                        player_center_y
                        + math.sin(angle)
                        * petal_orbit_distance(i, moon_extra_orbit)
                    )
                    petal_range_draw = (
                        int(PETAL_RADIUS * petal_size_scale)
                    )

                    if petal_type == "Wing":
                        petal_range_draw = int(PETAL_RADIUS)

                    pygame.draw.circle(
                        screen,
                        hitbox_color,
                        (hp_x, hp_y),
                        petal_range_draw,
                        hitbox_width
                    )
                    element_index += 1

            # Enemy hitboxes
            all_enemy_lists = [
                ladybugs,
                hole_ladybugs,
                hole_bees,
                hole_spiders,
                hole_rocks,
                hole_hornets,
                hole_baby_ants,
                hole_soldier_ants,
                hole_worker_ants,
                hole_queen_ants,
                bees,
                spiders,
                rocks,
                hornets,
                baby_ants,
                soldier_ants,
                worker_ants,
                queen_ants,
                ant_eggs,
            ]
            for enemy_list in all_enemy_lists:
                for enemy in enemy_list:
                    if not enemy.alive:
                        continue
                    if isinstance(enemy, QueenAnt):
                        # Queens show all three body-part circles.
                        for c_x, c_y, c_r in enemy.hitbox_circles():
                            pygame.draw.circle(
                                screen,
                                hitbox_color,
                                (
                                    int(c_x - camera_x),
                                    int(c_y - camera_y),
                                ),
                                int(c_r),
                                hitbox_width
                            )
                    else:
                        pygame.draw.circle(
                            screen,
                            hitbox_color,
                            (
                                int(enemy.x - camera_x),
                                int(enemy.y - camera_y),
                            ),
                            enemy.radius,
                            hitbox_width
                        )

            # Queen egg hitboxes
            for egg in queen_eggs:
                pygame.draw.circle(
                    screen,
                    hitbox_color,
                    (
                        int(egg["x"] - camera_x),
                        int(egg["y"] - camera_y),
                    ),
                    egg["radius"],
                    hitbox_width
                )


        # ---------------- PLAYER FACE (spins while dead) ----------------

        face_surf = pygame.Surface((42, 42), pygame.SRCALPHA)
        fc = 21

        # eyes
        if player_dead:

            # X eyes, each rotated 45 degrees, at the normal eye spots
            half = 4
            for ex, ey in ((fc - 7, fc - 4), (fc + 7, fc - 4)):

                pygame.draw.line(
                    face_surf,
                    player_face_color,
                    (int(ex - half), int(ey - half)),
                    (int(ex + half), int(ey + half)),
                    3
                )
                pygame.draw.line(
                    face_surf,
                    player_face_color,
                    (int(ex - half), int(ey + half)),
                    (int(ex + half), int(ey - half)),
                    3
                )

        else:

            pygame.draw.ellipse(
                face_surf,
                player_face_color,
                (fc - 11, fc - 10, 8, 12)
            )

            pygame.draw.ellipse(
                face_surf,
                player_face_color,
                (fc + 3, fc - 10, 8, 12)
            )

        # mouth
        if player_dead:

            # sad mouth when dead
            pygame.draw.arc(
                face_surf,
                player_face_color,
                (fc - 9, fc + 7, 18, 16),
                math.radians(20),
                math.radians(160),
                2
            )

        else:

            if petal_target == PETAL_NORMAL:

                pygame.draw.arc(
                    face_surf,
                    player_face_color,
                    (fc - 9, fc - 1, 18, 16),
                    math.radians(200),
                    math.radians(340),
                    2
                )

            elif petal_face_target == PETAL_ATTACK:

                # attack angry face: eye cut-outs + frown
                pygame.draw.polygon(
                    face_surf,
                    player_body_color,
                    [
                        (fc - 12, fc - 12),
                        (fc - 4, fc - 8),
                        (fc - 4, fc - 16),
                        (fc - 12, fc - 16)
                    ]
                )

                pygame.draw.polygon(
                    face_surf,
                    player_body_color,
                    [
                        (fc + 4, fc - 8),
                        (fc + 12, fc - 12),
                        (fc + 12, fc - 16),
                        (fc + 4, fc - 16)
                    ]
                )

                pygame.draw.arc(
                    face_surf,
                    player_face_color,
                    (fc - 9, fc + 7, 18, 16),
                    math.radians(20),
                    math.radians(160),
                    2
                )

            elif petal_target == PETAL_DEFEND:

                pygame.draw.arc(
                    face_surf,
                    player_face_color,
                    (fc - 9, fc + 7, 18, 16),
                    math.radians(20),
                    math.radians(160),
                    2
                )

        if player_rot_angle != 0:
            face_surf = pygame.transform.rotate(face_surf, -player_rot_angle)

        # Shrink or grow the face to match the picked flower size.
        if PLAYER_RADIUS != 25:
            face_scale = PLAYER_RADIUS / 25
            face_surf = pygame.transform.smoothscale(
                face_surf,
                (
                    max(1, int(42 * face_scale)),
                    max(1, int(42 * face_scale))
                )
            )

        if player_ghost:
            face_surf.set_alpha(90)

        screen.blit(
            face_surf,
            face_surf.get_rect(center=(int(player_center_x), int(player_center_y)))
        )

        # Show the flower's name / XP / level / points only when alive and show_hud is True.
        if not player_dead and show_hud:

            # Center the flower's name above the flower and HP bar.
            flower_name_text = flower_name_font.render(
                acc_name_text,
                True,
                (255, 255, 255)
            )
            flower_name_rect = flower_name_text.get_rect(
                midbottom=(
                    player_center_x,
                    player_center_y - PLAYER_RADIUS - 30
                )
            )
            screen.blit(flower_name_text, flower_name_rect)

            xp_text = flower_info_font.render(
                "XP: " + format_number(int(flower_xp)) +
                "/" +
                format_number(int(flower_xp_needed)),
                True,
                (255, 255, 255)
            )
            level_text = flower_info_font.render(
                "Level: " + str(flower_level),
                True,
                (255, 255, 255)
            )
            points_text = flower_info_font.render(
                "Points: " + format_number(upgrade_points),
                True,
                (255, 255, 0)
            )

            flower_xp_rect = xp_text.get_rect(
                midtop=(
                    player_center_x,
                    player_center_y + PLAYER_RADIUS + 10
                )
            )
            screen.blit(xp_text, flower_xp_rect)

            flower_level_rect = level_text.get_rect(
                midtop=(
                    player_center_x,
                    flower_xp_rect.bottom + 2
                )
            )
            screen.blit(level_text, flower_level_rect)

            flower_points_rect = points_text.get_rect(
                midtop=(
                    player_center_x,
                    flower_level_rect.bottom + 2
                )
            )
            screen.blit(points_text, flower_points_rect)


        # ---------------- WEATHER EFFECTS ----------------
        if game_weather != "sunny":
            target_count = 140 if game_weather in ("rainy", "snowy", "hail") else 24
            # On first start, distribute particles across the entire height so there is no gap/wave
            if len(weather_particles) == 0:
                for _ in range(target_count):
                    init_y = random.randint(-40, HEIGHT)
                    if game_weather == "rainy":
                        weather_particles.append({
                            "x": random.randint(-50, WIDTH + 50),
                            "y": init_y,
                            "speed_y": random.uniform(14, 20),
                            "speed_x": random.uniform(-3, -1),
                            "len": random.randint(12, 18),
                            "alpha": random.randint(140, 210)
                        })
                    elif game_weather == "snowy":
                        weather_particles.append({
                            "x": random.randint(-50, WIDTH + 50),
                            "y": init_y,
                            "speed_y": random.uniform(1.8, 3.8),
                            "speed_x": random.uniform(-1.5, 0.5),
                            "r": random.randint(2, 4),
                            "wobble": random.uniform(0, 6.28)
                        })
                    elif game_weather == "hail":
                        weather_particles.append({
                            "x": random.randint(-50, WIDTH + 50),
                            "y": init_y,
                            "speed_y": random.uniform(16, 24),
                            "speed_x": random.uniform(-2, 0),
                            "r": random.randint(3, 5),
                            "bounce": 0
                        })
                    elif game_weather == "cloudy":
                        weather_particles.append({
                            "x": random.randint(-150, WIDTH + 150),
                            "y": random.randint(0, HEIGHT),
                            "speed_x": random.uniform(-0.6, -0.3),
                            "r": random.randint(60, 110),
                            "alpha": random.randint(25, 45)
                        })

            # Continuously spawn a few raindrops every single frame for smooth steady rainfall
            if game_weather == "rainy":
                for _ in range(random.randint(4, 7)):
                    weather_particles.append({
                        "x": random.randint(-50, WIDTH + 80),
                        "y": random.randint(-35, -5),
                        "speed_y": random.uniform(14, 20),
                        "speed_x": random.uniform(-3, -1),
                        "len": random.randint(12, 18),
                        "alpha": random.randint(140, 210)
                    })
            else:
                while len(weather_particles) < target_count:
                    if game_weather == "snowy":
                        weather_particles.append({
                            "x": random.randint(-50, WIDTH + 50),
                            "y": random.randint(-30, -5),
                            "speed_y": random.uniform(1.8, 3.8),
                            "speed_x": random.uniform(-1.5, 0.5),
                            "r": random.randint(2, 4),
                            "wobble": random.uniform(0, 6.28)
                        })
                    elif game_weather == "hail":
                        weather_particles.append({
                            "x": random.randint(-50, WIDTH + 50),
                            "y": random.randint(-40, -10),
                            "speed_y": random.uniform(16, 24),
                            "speed_x": random.uniform(-2, 0),
                            "r": random.randint(3, 5),
                            "bounce": 0
                        })
                    elif game_weather == "cloudy":
                        weather_particles.append({
                            "x": random.randint(-150, WIDTH + 150),
                            "y": random.randint(0, HEIGHT),
                            "speed_x": random.uniform(-0.6, -0.3),
                            "r": random.randint(60, 110),
                            "alpha": random.randint(25, 45)
                        })

            # Update and draw weather particles
            for wp in weather_particles[:]:
                if game_weather == "rainy":
                    wp["x"] += wp["speed_x"]
                    wp["y"] += wp["speed_y"]
                    if wp["y"] > HEIGHT + 20:
                        weather_particles.remove(wp)
                    else:
                        rain_surf = pygame.Surface((3, wp["len"]), pygame.SRCALPHA)
                        rain_surf.fill((160, 205, 255, wp["alpha"]))
                        screen.blit(rain_surf, (int(wp["x"]), int(wp["y"])))
                elif game_weather == "snowy":
                    wp["wobble"] += 0.05
                    wp["x"] += wp["speed_x"] + math.sin(wp["wobble"]) * 0.8
                    wp["y"] += wp["speed_y"]
                    if wp["y"] > HEIGHT + 10:
                        weather_particles.remove(wp)
                    else:
                        pygame.draw.circle(
                            screen,
                            (240, 245, 255),
                            (int(wp["x"]), int(wp["y"])),
                            wp["r"]
                        )
                elif game_weather == "hail":
                    wp["x"] += wp["speed_x"]
                    wp["y"] += wp["speed_y"]
                    if wp["y"] > HEIGHT + 15:
                        weather_particles.remove(wp)
                    else:
                        pygame.draw.circle(
                            screen,
                            (215, 235, 250),
                            (int(wp["x"]), int(wp["y"])),
                            wp["r"]
                        )
                        pygame.draw.circle(
                            screen,
                            (255, 255, 255),
                            (int(wp["x"]), int(wp["y"])),
                            max(1, wp["r"] - 2)
                        )
                elif game_weather == "cloudy":
                    wp["x"] += wp["speed_x"]
                    if wp["x"] < -180:
                        wp["x"] = WIDTH + 180
                        wp["y"] = random.randint(0, HEIGHT)
                    cloud_surf = pygame.Surface((wp["r"] * 2, wp["r"] * 2), pygame.SRCALPHA)
                    pygame.draw.circle(
                        cloud_surf,
                        (200, 210, 225, wp["alpha"]),
                        (wp["r"], wp["r"]),
                        wp["r"]
                    )
                    screen.blit(cloud_surf, (int(wp["x"] - wp["r"]), int(wp["y"] - wp["r"])))

        # ---------------- MINIMAP ----------------
        draw_minimap()

        # ---------------- DEATH OVERLAY ----------------
        # Black 80%-transparent overlay covering the game world and minimap,
        # drawn before the HUD/buttons/panels so those stay in front of it.

        if player_dead:

            death_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            death_overlay.fill((0, 0, 0, 204))
            screen.blit(death_overlay, (0, 0))

            # Dead flower picture in the middle of the overlay, with the
            # equipped petals arranged around it. Everything is drawn at
            # fixed angles, so the petals do not spin while dead.

            fcx = WIDTH // 2
            # at the same position as the real (world) flower behind
            # the overlay, since the camera centers on the player
            fcy = HEIGHT // 2

            # flower body + outline
            pygame.draw.circle(
                screen,
                player_body_color,
                (fcx, fcy),
                PLAYER_RADIUS
            )
            pygame.draw.circle(
                screen,
                player_outline_color,
                (fcx, fcy),
                PLAYER_RADIUS,
                5
            )

            # dead face: X eyes + sad mouth, no rotation
            face_surf = pygame.Surface((42, 42), pygame.SRCALPHA)
            fc = 21
            half = 4
            for ex, ey in ((fc - 7, fc - 4), (fc + 7, fc - 4)):

                pygame.draw.line(
                    face_surf,
                    player_face_color,
                    (int(ex - half), int(ey - half)),
                    (int(ex + half), int(ey + half)),
                    3
                )
                pygame.draw.line(
                    face_surf,
                    player_face_color,
                    (int(ex - half), int(ey + half)),
                    (int(ex + half), int(ey - half)),
                    3
                )

            pygame.draw.arc(
                face_surf,
                player_face_color,
                (fc - 9, fc + 7, 18, 16),
                math.radians(20),
                math.radians(160),
                2
            )
            if PLAYER_RADIUS != 25:
                face_scale = PLAYER_RADIUS / 25
                face_surf = pygame.transform.smoothscale(
                    face_surf,
                    (
                        max(1, int(42 * face_scale)),
                        max(1, int(42 * face_scale))
                    )
                )
            screen.blit(
                face_surf,
                face_surf.get_rect(center=(fcx, fcy))
            )

            # equipped petals in a fixed ring around the flower (no spin)
            saved_petal_angle = petal_angle
            try:
                total_elements = 0
                for i in range(PETAL_SLOTS):
                    if not petal_slots[i]["filled"]:
                        continue
                    total_elements += 1
                angle_increment = 360 / total_elements if total_elements > 0 else 72
                element_index = 0
                for i in range(PETAL_SLOTS):

                    if not petal_slots[i]["filled"]:
                        continue

                    ring_pos = element_index * angle_increment
                    angle = math.radians(ring_pos - 90)
                    element_index += 1

                    moon_extra = (
                        40
                        if petal_slots[i]["petal"] == "Moon"
                        else 0
                    )

                    px = fcx + math.cos(angle) * (PETAL_NORMAL + moon_extra)
                    py = fcy + math.sin(angle) * (PETAL_NORMAL + moon_extra)

                    # fixed orientation so the petal tips point outward and
                    # never rotate
                    petal_angle = ring_pos

                    draw_petal(
                        petal_slots[i]["petal"],
                        px,
                        py,
                        petal_slots[i]["rarity"],
                        size_scale=(
                            4.0
                            if petal_slots[i]["petal"] == "Moon"
                            else 1.0
                        )
                    )
            finally:
                petal_angle = saved_petal_angle

            # "You've been destroyed by ..." text, white with a black
            # outline, centered on the fake flower picture
            if killer_name and killer_rarity:

                death_prefix = "You've been destroyed by "
                death_rarity = killer_rarity
                death_suffix = " " + killer_name

                prefix_txt = respawn_timer_font.render(
                    death_prefix, True, (255, 255, 255)
                )
                rarity_color = RARITY_COLORS.get(
                    killer_rarity, (255, 255, 255)
                )
                rarity_txt = respawn_timer_font.render(
                    death_rarity, True, rarity_color
                )
                suffix_txt = respawn_timer_font.render(
                    death_suffix, True, (255, 255, 255)
                )

                total_w = (
                    prefix_txt.get_width()
                    + rarity_txt.get_width()
                    + suffix_txt.get_width()
                )

                start_x = fcx - total_w // 2
                text_y = fcy - 300

                # draw black outlines for each part
                for ox in (-2, 0, 2):
                    for oy in (-2, 0, 2):
                        if ox == 0 and oy == 0:
                            continue

                        for text_str, dx in (
                            (death_prefix, 0),
                            (death_rarity,
                             prefix_txt.get_width()),
                            (death_suffix,
                             prefix_txt.get_width()
                             + rarity_txt.get_width()),
                        ):
                            outline = respawn_timer_font.render(
                                text_str, True, (0, 0, 0)
                            )
                            screen.blit(
                                outline,
                                (start_x + dx + ox, text_y + oy)
                            )

                screen.blit(
                    prefix_txt, (start_x, text_y)
                )
                screen.blit(
                    rarity_txt,
                    (start_x + prefix_txt.get_width(), text_y)
                )
                screen.blit(
                    suffix_txt,
                    (start_x + prefix_txt.get_width()
                     + rarity_txt.get_width(),
                     text_y)
                )

            # Respawn button placed near the bottom edge of the screen.
            btn_rect = respawn_button_rect

            # lighten the button while hovered, back to normal otherwise
            hovered = btn_rect.collidepoint(pygame.mouse.get_pos())
            btn_fill = (90, 170, 255) if hovered else (30, 110, 250)
            btn_outline = (5, 30, 110) if hovered else (10, 50, 140)

            # blue button with an outline
            pygame.draw.rect(
                screen,
                btn_fill,
                btn_rect,
                border_radius=12
            )
            pygame.draw.rect(
                screen,
                btn_outline,
                btn_rect,
                3,
                border_radius=12
            )

            # white "Respawn" text with a black outline
            respawn_txt = large_hud_font.render(
                "Respawn",
                True,
                (255, 255, 255)
            )
            txt_rect = respawn_txt.get_rect(center=btn_rect.center)

            for ox in (-2, 0, 2):
                for oy in (-2, 0, 2):
                    if ox == 0 and oy == 0:
                        continue
                    outline_txt = large_hud_font.render(
                        "Respawn",
                        True,
                        (0, 0, 0)
                    )
                    screen.blit(
                        outline_txt,
                        (txt_rect.x + ox, txt_rect.y + oy)
                    )

            screen.blit(respawn_txt, txt_rect)


        # ---------------- INVENTORY BUTTON ----------------

        # ---------------- SETTINGS BUTTON ----------------
        # Drawn before the panels so any open panel covers it.

        # ---------------- CMD BUTTON ----------------

        pygame.draw.rect(
            screen,
            (128, 0, 196),
            cmd_button_rect,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (70, 0, 110),
            cmd_button_rect,
            3,
            border_radius=8
        )
        cmd_txt = cmd_button_font.render(
            "/cmd",
            True,
            (255, 255, 255)
        )
        cmd_txt_rect = cmd_txt.get_rect(
            center=cmd_button_rect.center
        )
        screen.blit(cmd_txt, cmd_txt_rect)

        # ---------------- SETTINGS BUTTON ----------------
        # Drawn before the panels so any open panel covers it.

        pygame.draw.rect(
            screen,
            (185, 185, 185),
            settings_button_rect,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (95, 95, 95),
            settings_button_rect,
            3,
            border_radius=8
        )

        # Slider icon: three horizontal lines with round knobs.
        # While hovered the knobs slide back and forth along their
        # lines, and ease back to their spots when the mouse leaves.
        if settings_button_rect.collidepoint(pygame.mouse.get_pos()):
            settings_button_knob_phase += 0.14
            settings_button_knob_amplitude = min(
                1.0,
                settings_button_knob_amplitude + 0.08
            )
        else:
            settings_button_knob_amplitude = max(
                0.0,
                settings_button_knob_amplitude - 0.08
            )

        for row_index, knob_base in enumerate((-14, 0, 14)):
            slider_line_y = settings_button_rect.centery + knob_base
            pygame.draw.line(
                screen,
                (60, 60, 60),
                (
                    settings_button_rect.centerx - 18,
                    slider_line_y
                ),
                (
                    settings_button_rect.centerx + 18,
                    slider_line_y
                ),
                4
            )
            # Each knob slides within its own span along the bar, so a
            # circle can never slide past either end of the line.
            slide_t = (
                math.sin(
                    settings_button_knob_phase + row_index * 2.1
                )
                + 1
            ) * 0.5
            if row_index == 0:
                knob_slide_min = -14
                knob_slide_span = 12
            elif row_index == 1:
                knob_slide_min = -7
                knob_slide_span = 14
            else:
                knob_slide_min = 2
                knob_slide_span = 12
            knob_x = (
                settings_button_rect.centerx
                + knob_slide_min
                + int(
                    slide_t
                    * knob_slide_span
                    * settings_button_knob_amplitude
                )
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    knob_x,
                    slider_line_y
                ),
                6
            )
            pygame.draw.circle(
                screen,
                (60, 60, 60),
                (
                    knob_x,
                    slider_line_y
                ),
                6,
                2
            )

        new_panel_target_x = (
            new_button_panel_target_rect.x
            if new_button_panel_open
            else -new_button_panel_rect.width
        )
        # The panel slides with acceleration, easing into place.
        new_button_panel_slide_velocity += (
            new_panel_target_x - new_button_panel_rect.x
        ) * 0.045
        new_button_panel_slide_velocity *= 0.78
        new_button_panel_rect.x += new_button_panel_slide_velocity
        # Once nearly closed, rest exactly offscreen so no outline
        # sliver stays visible.
        if not new_button_panel_open and (
            new_button_panel_rect.x
            <= -new_button_panel_rect.width + 1
        ):
            new_button_panel_rect.x = -new_button_panel_rect.width
            new_button_panel_slide_velocity = 0.0
        if (
            abs(new_panel_target_x - new_button_panel_rect.x) < 0.5
            and abs(new_button_panel_slide_velocity) < 0.5
        ):
            new_button_panel_rect.x = new_panel_target_x
            new_button_panel_slide_velocity = 0.0

        # ---------------- SETTINGS PANEL SLIDE ----------------

        # The panel slides with acceleration: it speeds up while
        # traveling and eases into its resting position.
        settings_target_y = (
            settings_panel_target_rect.y
            if settings_panel_open
            else -settings_panel_rect.height - 20
        )
        settings_panel_slide_velocity += (
            settings_target_y - settings_panel_rect.y
        ) * 0.045
        settings_panel_slide_velocity *= 0.78
        settings_panel_rect.y += settings_panel_slide_velocity
        # Once nearly closed, rest exactly offscreen so no outline
        # sliver stays visible.
        if not settings_panel_open and (
            settings_panel_rect.y
            <= -settings_panel_rect.height + 1
        ):
            settings_panel_rect.y = -settings_panel_rect.height - 20
            settings_panel_slide_velocity = 0.0
        if (
            abs(settings_target_y - settings_panel_rect.y) < 0.5
            and abs(settings_panel_slide_velocity) < 0.5
        ):
            settings_panel_rect.y = settings_target_y
            settings_panel_slide_velocity = 0.0

        # ---------------- CMD PANEL SLIDE ----------------

        # Slides down from offscreen above the top edge and eases into
        # place, mirroring the settings panel behavior.
        cmd_panel_target_y = (
            cmd_panel_target_rect.y
            if cmd_panel_open
            else -cmd_panel_rect.height - 20
        )
        cmd_panel_slide_velocity += (
            cmd_panel_target_y - cmd_panel_rect.y
        ) * 0.045
        cmd_panel_slide_velocity *= 0.78
        cmd_panel_rect.y += cmd_panel_slide_velocity
        # Once nearly closed, rest exactly offscreen so no outline
        # sliver stays visible.
        if not cmd_panel_open and (
            cmd_panel_rect.y
            <= -cmd_panel_rect.height + 1
        ):
            cmd_panel_rect.y = -cmd_panel_rect.height - 20
            cmd_panel_slide_velocity = 0.0
        if (
            abs(cmd_panel_target_y - cmd_panel_rect.y) < 0.5
            and abs(cmd_panel_slide_velocity) < 0.5
        ):
            cmd_panel_rect.y = cmd_panel_target_y
            cmd_panel_slide_velocity = 0.0

        # The switch knob slides between the ends with acceleration.
        switch_target_progress = (
            1.0 if settings_switch_on else 0.0
        )
        settings_switch_slide_velocity += (
            switch_target_progress
            - settings_switch_knob_progress
        ) * 0.045
        settings_switch_slide_velocity *= 0.78
        settings_switch_knob_progress += (
            settings_switch_slide_velocity
        )
        if (
            abs(
                switch_target_progress
                - settings_switch_knob_progress
            ) < 0.005
            and abs(settings_switch_slide_velocity) < 0.005
        ):
            settings_switch_knob_progress = switch_target_progress
            settings_switch_slide_velocity = 0.0

        # The second switch knob slides with acceleration too.
        switch2_target_progress = (
            1.0 if settings_switch2_on else 0.0
        )
        settings_switch2_slide_velocity += (
            switch2_target_progress
            - settings_switch2_knob_progress
        ) * 0.045
        settings_switch2_slide_velocity *= 0.78
        settings_switch2_knob_progress += (
            settings_switch2_slide_velocity
        )
        if (
            abs(
                switch2_target_progress
                - settings_switch2_knob_progress
            ) < 0.005
            and abs(settings_switch2_slide_velocity) < 0.005
        ):
            settings_switch2_knob_progress = (
                switch2_target_progress
            )
            settings_switch2_slide_velocity = 0.0

        # The third switch knob slides with acceleration too.
        switch3_target_progress = (
            1.0 if settings_switch3_on else 0.0
        )
        settings_switch3_slide_velocity += (
            switch3_target_progress
            - settings_switch3_knob_progress
        ) * 0.045
        settings_switch3_slide_velocity *= 0.78
        settings_switch3_knob_progress += (
            settings_switch3_slide_velocity
        )
        if (
            abs(
                switch3_target_progress
                - settings_switch3_knob_progress
            ) < 0.005
            and abs(settings_switch3_slide_velocity) < 0.005
        ):
            settings_switch3_knob_progress = (
                switch3_target_progress
            )
            settings_switch3_slide_velocity = 0.0

        if cmd_panel_rect.y > -cmd_panel_rect.height:
            pygame.draw.rect(
                screen,
                (128, 0, 196),
                cmd_panel_rect,
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                (70, 0, 110),
                cmd_panel_rect,
                4,
                border_radius=10
            )
            cmd_title_txt = cmd_button_font.render(
                "Commands:",
                True,
                (255, 255, 255)
            )
            screen.blit(
                cmd_title_txt,
                (
                    cmd_panel_rect.x + 16,
                    cmd_panel_rect.y + 12
                )
            )
            cmd_list_font = pygame.font.Font(None, 20)
            cmd_lines = [
                "/spawn_enemy [rarity] [mob] [mob damage] [mob health] [mob xp]",
                "/spawn_enemy [rarity] [mob type] [amount]",
                "/equip [rarity] [petal] [petal slot]",
                "/all_equip [rarity] [petal]",
                "/empty [petal slot]",
                "/empty_all",
                "/ban [user]",
                "/mute [user]",
                "/unmute [user]",
                "/gift [user] [rarity] [petal] [amount]",
                "/take [rarity] [petal] [amount] from.[user]",
                "/kick [user]",
                "/give_points [user] [amount]",
                "/tp [user]",
                "/announce [message]",
                "/self_heal [amount]",
                "/heal_user [user] [amount]",
                "/full_heal_user [user]",
                "/king",
                "/me [action]",
                "/stats",
                "/whisper [user] [message]",
                "/freez_enemies [seconds]",
                "/unfreeze",
                "/godmode [state]",
                "/reload_petals",
                "/spawn_whirlpool [damage] [damage each second] [whirlpool last seconds] [whirlpool size]",
                "/delete_whirlpools [amount]",
                "/delete_whirlpools",
                "/spawn_blackhole [pull speed] [duration] [size]",
                "/delete_blackholes [amount]",
                "/delete_blackholes",
                "/spawn_shield_dome [radius] [duration]",
                "/delete_shield_domes [amount]",
                "/delete_shield_domes",
                "/magnet_petal_drops [state] [size]",
                "/magnet_petal_drops [state]",
                "/trail_size [size]",
                "/hud [state]",
                "/speed [multiplier]",
                "/tp_pos [x] [y]",
                "/clear_chat",
                "/clean_drops",
                "/spawn_minion [rarity] [mob] [damage] [health] [speed] [size] [view range] [amount]",
                "/spawn_minion [rarity] [mob] [amount]",
                "/p.flower [color] or [hex]",
                "/p.trail [none or rainbow or fire or sparkle] [last seconds]",
                "/p.trail [none or rainbow or fire or sparkle]",
                "/p.petal_speed [slow or normal or fast]",
                "/p.theme [day or night]",
                "/p.weather [sunny or rainy or cloudy or snowy or hail]",
                "/p.ghost [y or n]",
                "/p.size [small or big]",
                "/p.mode [peaceful or normal]",
                "/delete_minion [amount]",
                "/delete_minion",
                "/kill_all_enemies",
                "/despawn_mobs",
                "/revive_user [user]",
                "/rarity_to [rarity]",
                "/s.enemy_increase [amount]",
                "/s.enemy_decrease [amount]"
            ]
            # Color the bracketed argument words in the list.
            cmd_word_colors = {
                "[rarity]": (255, 255, 0),
                "[mob]": (0, 230, 255),
                "[mob": (0, 255, 0),
                "type]": (0, 255, 0),
                "[damage]": (255, 65, 65),
                "damage]": (255, 65, 65),
                "[health]": (50, 255, 90),
                "health]": (50, 255, 90),
                "[xp]": (255, 110, 200),
                "xp]": (255, 110, 200),
                "[amount]": (0, 128, 255),
                "[petal]": (255, 0, 0),
                "[petal": (255, 0, 0),
                "slot]": (255, 165, 0),
                "[user]": (128, 255, 0),
                "[message]": (0, 255, 255),
                "[speed]": (60, 235, 220),
                "[size]": (170, 120, 255),
                "[view": (255, 185, 30),
                "range]": (255, 185, 30),
                "[action]": (255, 0, 255),
                "[seconds]": (0, 255, 128),
                "[last": (0, 255, 128),
                "seconds]": (0, 255, 128),
                "[state]": (255, 185, 30),
                "[whirlpool": (0, 210, 255),
                "[radius]": (100, 220, 255),
                "[duration]": (255, 200, 80),
                "[multiplier]": (60, 235, 220),
                "[color]": (255, 150, 200),
                "[hex]": (120, 220, 255),
                "[x]": (190, 120, 255),
                "[y]": (255, 130, 220),
                "from.[user]": (128, 255, 0),
            }
            cmd_max_width = cmd_panel_rect.width - 48
            # Clamp scroll so the list can't scroll past its ends.
            # First measure total content height, then clamp, then draw.
            cmd_list_top = cmd_panel_rect.y + 44
            cmd_list_bottom = cmd_panel_rect.bottom - 10
            cmd_total_height = 0
            for cmd_line in cmd_lines:
                words = cmd_line.split()
                cmd_line_x = cmd_panel_rect.x + 16
                cmd_total_height += 32
                for word in words:
                    prefix_txt = cmd_list_font.render(
                        "0. " + word, True, (0, 0, 0)
                    )
                    if (
                        cmd_line_x
                        + prefix_txt.get_width()
                        > cmd_panel_rect.right - 32
                    ):
                        cmd_line_x = cmd_panel_rect.x + 40
                        cmd_total_height += 24
                    cmd_line_x += prefix_txt.get_width() + 6
            cmd_max_scroll = max(0, cmd_total_height - (cmd_list_bottom - cmd_list_top))
            cmd_panel_scroll = max(0, min(cmd_panel_scroll, cmd_max_scroll))
            cmd_scroll_off = cmd_panel_scroll
            # Clip the list so lines scroll under the panel edges.
            cmd_clip = screen.get_clip()
            screen.set_clip(
                pygame.Rect(
                    cmd_panel_rect.x + 4,
                    cmd_panel_rect.y + 36,
                    cmd_panel_rect.width - 8,
                    cmd_panel_rect.height - 44
                )
            )
            cmd_line_y = cmd_panel_rect.y + 44 - cmd_scroll_off
            for cmd_number, cmd_line in enumerate(cmd_lines, start=1):
                words = cmd_line.split()
                cmd_line_x = cmd_panel_rect.x + 16
                first_line = True
                for word_index, word in enumerate(words):
                    # A bracketed [petal that is followed by slot]
                    # belongs to [petal slot] (orange), not [petal].
                    word_color = cmd_word_colors.get(
                        word, (255, 255, 255)
                    )
                    if (
                        word == "[petal"
                        and word_index + 1 < len(words)
                        and words[word_index + 1] == "slot]"
                    ):
                        word_color = (255, 165, 0)
                    elif word == "[pull" and word_index + 1 < len(words) and words[word_index + 1] == "speed]":
                        word_color = (255, 140, 60)
                    elif word == "speed]" and "[pull" in words:
                        word_color = (255, 140, 60)
                    elif word == "[damage" and word_index + 1 < len(words) and words[word_index + 1] == "each":
                        word_color = (255, 100, 100)
                    elif word in ("each", "second]") and "[damage" in words and "second]" in words:
                        word_color = (255, 100, 100)
                    elif word in ("[whirlpool", "last", "seconds]") and "[whirlpool" in words and "seconds]" in words:
                        word_color = (0, 220, 255)
                    elif word in ("[whirlpool", "size]") and "[whirlpool" in words and "size]" in words:
                        word_color = (170, 120, 255)
                    elif word == "[mob" and word_index + 1 < len(words):
                        next_w = words[word_index + 1]
                        if next_w == "damage]":
                            word_color = (255, 65, 65)
                        elif next_w == "health]":
                            word_color = (50, 255, 90)
                        elif next_w == "xp]":
                            word_color = (255, 110, 200)
                        elif next_w == "type]":
                            word_color = (0, 255, 0)
                    # Pick phrases like [y or n] and [small or big]
                    # must only color the bracket words, not the command name!
                    if word in ("[y", "or", "n]") and "[y" in words and "n]" in words:
                        word_color = (0, 255, 128)
                    elif word in ("[small", "or", "big]") and "[small" in words and "big]" in words:
                        word_color = (170, 120, 255)
                    elif word in ("[peaceful", "or", "normal]") and "[peaceful" in words and "normal]" in words:
                        word_color = (100, 240, 180)
                    elif word in ("[slow", "or", "normal", "fast]") and "[slow" in words and "fast]" in words:
                        word_color = (255, 140, 0)
                    elif word in ("[day", "or", "night]") and "[day" in words and "night]" in words:
                        word_color = (80, 200, 255)
                    elif word in ("[sunny", "or", "rainy", "cloudy", "snowy", "hail]") and "[sunny" in words and "hail]" in words:
                        word_color = (130, 220, 255)
                    elif word in ("[none", "or", "rainbow", "fire", "sparkle]") and "[none" in words and "sparkle]" in words:
                        word_color = (255, 120, 200)
                    elif word == "or" and "[color]" in words and "[hex]" in words:
                        word_color = (200, 200, 200)
                    prefix = (
                        f"{cmd_number}. "
                        if first_line
                        else ""
                    )
                    word_txt = cmd_list_font.render(
                        prefix + word,
                        True,
                        word_color
                    )
                    space_width = (
                        cmd_list_font.size(" ")[0]
                        if first_line
                        else cmd_list_font.size("  ")[0]
                    )
                    # Wrap when the word would pass the panel edge.
                    if (
                        cmd_line_x
                        + word_txt.get_width()
                        > cmd_panel_rect.right - 32
                    ):
                        cmd_line_x = cmd_panel_rect.x + 40
                        cmd_line_y += 24
                        first_line = False
                        word_txt = cmd_list_font.render(
                            word,
                            True,
                            word_color
                        )
                        space_width = cmd_list_font.size(" ")[0]
                    screen.blit(word_txt, (cmd_line_x, cmd_line_y))
                    cmd_line_x += word_txt.get_width() + space_width
                    first_line = False
                cmd_line_y += 24
                cmd_line_y += 8
            screen.set_clip(cmd_clip)
            # Scrollbar on the right edge of the panel.
            if cmd_max_scroll > 0:
                track_rect = pygame.Rect(
                    cmd_panel_rect.right - 8,
                    cmd_list_top,
                    6,
                    cmd_list_bottom - cmd_list_top
                )
                pygame.draw.rect(
                    screen,
                    (70, 0, 110),
                    track_rect,
                    border_radius=3
                )
                track_height = track_rect.height
                visible_ratio = (cmd_list_bottom - cmd_list_top) / (
                    cmd_total_height
                )
                thumb_height = max(
                    20, int(track_height * visible_ratio)
                )
                thumb_y = track_rect.y + int(
                    (track_height - thumb_height)
                    * (cmd_panel_scroll / cmd_max_scroll)
                )
                pygame.draw.rect(
                    screen,
                    (200, 120, 255),
                    (
                        track_rect.x,
                        thumb_y,
                        track_rect.width,
                        thumb_height
                    ),
                    border_radius=3
                )

        if settings_panel_rect.y > -settings_panel_rect.height:
            pygame.draw.rect(
                screen,
                (185, 185, 185),
                settings_panel_rect,
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                (95, 95, 95),
                settings_panel_rect,
                4,
                border_radius=10
            )

            # Mob hp bar size slider: a dark grey bar running from
            # the panel's top left corner to its top right corner,
            # with a white knob circle on it.  Both have outlines.
            settings_hp_bar_track_rect = pygame.Rect(
                settings_panel_rect.x + 16,
                settings_panel_rect.y + 38,
                settings_panel_rect.width - 32,
                14
            )
            pygame.draw.rect(
                screen,
                (80, 80, 80),
                settings_hp_bar_track_rect,
                border_radius=7
            )
            pygame.draw.rect(
                screen,
                (45, 45, 45),
                settings_hp_bar_track_rect,
                2,
                border_radius=7
            )
            settings_hp_bar_knob_x = int(
                settings_hp_bar_track_rect.left
                + 12
                + settings_hp_bar_knob_progress
                * (settings_hp_bar_track_rect.width - 24)
            )
            settings_hp_bar_knob_y = (
                settings_hp_bar_track_rect.centery
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (settings_hp_bar_knob_x, settings_hp_bar_knob_y),
                12
            )
            pygame.draw.circle(
                screen,
                (140, 140, 140),
                (settings_hp_bar_knob_x, settings_hp_bar_knob_y),
                12,
                2
            )

            # Percent readout above the slider: the left end of the
            # bar is 1% and the right end is 100%.  White text with
            # a black outline.
            settings_hp_bar_percent = int(
                round(1 + settings_hp_bar_knob_progress * 99)
            )
            settings_percent_text = (
                str(settings_hp_bar_percent) + "%"
            )
            settings_percent_surface = (
                settings_label_font.render(
                    settings_percent_text,
                    True,
                    (255, 255, 255)
                )
            )
            settings_percent_outline_surface = (
                settings_label_font.render(
                    settings_percent_text,
                    True,
                    (0, 0, 0)
                )
            )
            settings_percent_rect = settings_percent_surface.get_rect(
                centerx=(
                    settings_hp_bar_track_rect.left
                    + settings_hp_bar_track_rect.width // 2
                ),
                bottom=settings_hp_bar_track_rect.top - 4
            )
            for outline_offset_x in (-2, 0, 2):
                for outline_offset_y in (-2, 0, 2):
                    if outline_offset_x or outline_offset_y:
                        screen.blit(
                            settings_percent_outline_surface,
                            (
                                settings_percent_rect.x
                                + outline_offset_x,
                                settings_percent_rect.y
                                + outline_offset_y
                            )
                        )
            screen.blit(
                settings_percent_surface,
                settings_percent_rect
            )

            # Label under the slider: white text with a black
            # outline, centered on the bar.
            settings_label_text = "mob health bar size"
            settings_label_surface = (
                settings_label_font.render(
                    settings_label_text,
                    True,
                    (255, 255, 255)
                )
            )
            settings_label_outline_surface = (
                settings_label_font.render(
                    settings_label_text,
                    True,
                    (0, 0, 0)
                )
            )
            settings_label_rect = settings_label_surface.get_rect(
                centerx=(
                    settings_hp_bar_track_rect.left
                    + settings_hp_bar_track_rect.width // 2
                ),
                top=settings_hp_bar_track_rect.bottom + 6
            )
            for outline_offset_x in (-2, 0, 2):
                for outline_offset_y in (-2, 0, 2):
                    if outline_offset_x or outline_offset_y:
                        screen.blit(
                            settings_label_outline_surface,
                            (
                                settings_label_rect.x
                                + outline_offset_x,
                                settings_label_rect.y
                                + outline_offset_y
                            )
                        )
            screen.blit(
                settings_label_surface,
                settings_label_rect
            )

            # Toggle switch below the label: a short dark grey bar
            # aligned with the slider's left end, with a white knob
            # circle on its left edge.  Both have outlines.
            settings_switch_rect = pygame.Rect(
                settings_hp_bar_track_rect.x,
                settings_label_rect.bottom + 20,
                60,
                18
            )
            pygame.draw.rect(
                screen,
                (80, 80, 80),
                settings_switch_rect,
                border_radius=9
            )
            pygame.draw.rect(
                screen,
                (45, 45, 45),
                settings_switch_rect,
                2,
                border_radius=9
            )
            settings_switch_knob_x = int(
                settings_switch_rect.x
                + 9
                + settings_switch_knob_progress
                * (settings_switch_rect.width - 18)
            )
            settings_switch_knob_y = (
                settings_switch_rect.centery
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (settings_switch_knob_x, settings_switch_knob_y),
                9
            )
            pygame.draw.circle(
                screen,
                (140, 140, 140),
                (settings_switch_knob_x, settings_switch_knob_y),
                9,
                2
            )

            # Label to the right of the switch: white text with a
            # black outline, vertically centered on it.
            settings_switch_label = "auto squad"
            settings_switch_surface = (
                settings_label_font.render(
                    settings_switch_label,
                    True,
                    (255, 255, 255)
                )
            )
            settings_switch_outline_surface = (
                settings_label_font.render(
                    settings_switch_label,
                    True,
                    (0, 0, 0)
                )
            )
            settings_switch_label_rect = (
                settings_switch_surface.get_rect(
                    left=settings_switch_rect.right + 10,
                    centery=settings_switch_rect.centery
                )
            )
            for outline_offset_x in (-2, 0, 2):
                for outline_offset_y in (-2, 0, 2):
                    if outline_offset_x or outline_offset_y:
                        screen.blit(
                            settings_switch_outline_surface,
                            (
                                settings_switch_label_rect.x
                                + outline_offset_x,
                                settings_switch_label_rect.y
                                + outline_offset_y
                            )
                        )
            screen.blit(
                settings_switch_surface,
                settings_switch_label_rect
            )

            # Second toggle switch below the first one, same style,
            # just lower.  Label sits to its right.
            settings_switch2_rect = pygame.Rect(
                settings_hp_bar_track_rect.x,
                settings_switch_rect.bottom + 12,
                60,
                18
            )
            pygame.draw.rect(
                screen,
                (80, 80, 80),
                settings_switch2_rect,
                border_radius=9
            )
            pygame.draw.rect(
                screen,
                (45, 45, 45),
                settings_switch2_rect,
                2,
                border_radius=9
            )
            settings_switch2_knob_x = int(
                settings_switch2_rect.x
                + 9
                + settings_switch2_knob_progress
                * (settings_switch2_rect.width - 18)
            )
            settings_switch2_knob_y = (
                settings_switch2_rect.centery
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    settings_switch2_knob_x,
                    settings_switch2_knob_y
                ),
                9
            )
            pygame.draw.circle(
                screen,
                (140, 140, 140),
                (
                    settings_switch2_knob_x,
                    settings_switch2_knob_y
                ),
                9,
                2
            )

            # Label to the right of the second switch.
            settings_switch2_label = "equip collected petals"
            settings_switch2_surface = (
                settings_label_font.render(
                    settings_switch2_label,
                    True,
                    (255, 255, 255)
                )
            )
            settings_switch2_outline_surface = (
                settings_label_font.render(
                    settings_switch2_label,
                    True,
                    (0, 0, 0)
                )
            )
            settings_switch2_label_rect = (
                settings_switch2_surface.get_rect(
                    left=settings_switch2_rect.right + 10,
                    centery=settings_switch2_rect.centery
                )
            )
            for outline_offset_x in (-2, 0, 2):
                for outline_offset_y in (-2, 0, 2):
                    if outline_offset_x or outline_offset_y:
                        screen.blit(
                            settings_switch2_outline_surface,
                            (
                                settings_switch2_label_rect.x
                                + outline_offset_x,
                                settings_switch2_label_rect.y
                                + outline_offset_y
                            )
                        )
            screen.blit(
                settings_switch2_surface,
                settings_switch2_label_rect
            )

            # Third toggle switch below the second one.
            settings_switch3_rect = pygame.Rect(
                settings_hp_bar_track_rect.x,
                settings_switch2_rect.bottom + 12,
                60,
                18
            )
            pygame.draw.rect(
                screen,
                (80, 80, 80),
                settings_switch3_rect,
                border_radius=9
            )
            pygame.draw.rect(
                screen,
                (45, 45, 45),
                settings_switch3_rect,
                2,
                border_radius=9
            )
            settings_switch3_knob_x = int(
                settings_switch3_rect.x
                + 9
                + settings_switch3_knob_progress
                * (settings_switch3_rect.width - 18)
            )
            settings_switch3_knob_y = (
                settings_switch3_rect.centery
            )
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (
                    settings_switch3_knob_x,
                    settings_switch3_knob_y
                ),
                9
            )
            pygame.draw.circle(
                screen,
                (140, 140, 140),
                (
                    settings_switch3_knob_x,
                    settings_switch3_knob_y
                ),
                9,
                2
            )

            # Label to the right of the third switch.
            settings_switch3_label = "Show hitbox"
            settings_switch3_surface = (
                settings_label_font.render(
                    settings_switch3_label,
                    True,
                    (255, 255, 255)
                )
            )
            settings_switch3_outline_surface = (
                settings_label_font.render(
                    settings_switch3_label,
                    True,
                    (0, 0, 0)
                )
            )
            settings_switch3_label_rect = (
                settings_switch3_surface.get_rect(
                    left=settings_switch3_rect.right + 10,
                    centery=settings_switch3_rect.centery
                )
            )
            for outline_offset_x in (-2, 0, 2):
                for outline_offset_y in (-2, 0, 2):
                    if outline_offset_x or outline_offset_y:
                        screen.blit(
                            settings_switch3_outline_surface,
                            (
                                settings_switch3_label_rect.x
                                + outline_offset_x,
                                settings_switch3_label_rect.y
                                + outline_offset_y
                            )
                        )
            screen.blit(
                settings_switch3_surface,
                settings_switch3_label_rect
            )

        if new_button_panel_rect.x > -new_button_panel_rect.width:
            pygame.draw.rect(
                screen,
                (250, 205, 45),
                new_button_panel_rect,
                border_radius=10
            )
            pygame.draw.rect(
                screen,
                (175, 105, 20),
                new_button_panel_rect,
                4,
                border_radius=10
            )

            gallery_cell_size = GALLERY_CELL_SIZE
            gallery_grid_rect = pygame.Rect(
                new_button_panel_rect.x + 10,
                mob_gallery_grid_top,
                new_button_panel_rect.width - 40,
                GALLERY_GRID_WINDOW_HEIGHT
            )
            gallery_visible_rows = max(
                1,
                min(
                    GALLERY_MAX_VISIBLE_ROWS,
                    gallery_grid_rect.height // gallery_cell_size
                )
            )
            gallery_visible_columns = max(
                1,
                gallery_grid_rect.width // gallery_cell_size
            )
            gallery_max_scroll = max(
                0,
                len(mob_gallery_names) - gallery_visible_rows
            )
            gallery_max_horizontal_scroll = max(
                0,
                len(RARITIES) - gallery_visible_columns
            )
            mob_gallery_scroll_target = max(
                0,
                min(mob_gallery_scroll_target, gallery_max_scroll)
            )
            mob_gallery_horizontal_scroll_target = max(
                0,
                min(
                    mob_gallery_horizontal_scroll_target,
                    gallery_max_horizontal_scroll
                )
            )
            mob_gallery_scroll_position += (
                mob_gallery_scroll_target - mob_gallery_scroll_position
            ) * 0.22
            mob_gallery_horizontal_scroll_position += (
                mob_gallery_horizontal_scroll_target
                - mob_gallery_horizontal_scroll_position
            ) * 0.22

            previous_gallery_clip = screen.get_clip()
            screen.set_clip(gallery_grid_rect)
            first_gallery_row = int(mob_gallery_scroll_position)
            first_gallery_column = int(
                mob_gallery_horizontal_scroll_position
            )
            gallery_start_x = (
                gallery_grid_rect.x
                - (
                    mob_gallery_horizontal_scroll_position
                    - first_gallery_column
                ) * gallery_cell_size
            )
            gallery_start_y = (
                gallery_grid_rect.y
                - (
                    mob_gallery_scroll_position
                    - first_gallery_row
                ) * gallery_cell_size
            )
            gallery_grid_surface = pygame.Surface(
                gallery_grid_rect.size,
                pygame.SRCALPHA
            )

            # Hover check: find which gallery cell the cursor is over
            # before drawing so the hovered icon can spin this frame.
            mouse_x, mouse_y = pygame.mouse.get_pos()
            hover_column = None
            hover_row = None
            if gallery_grid_rect.collidepoint(mouse_x, mouse_y):
                candidate_column = first_gallery_column + int(
                    (mouse_x - gallery_start_x) // gallery_cell_size
                )
                candidate_row = first_gallery_row + int(
                    (mouse_y - gallery_start_y) // gallery_cell_size
                )
                if (
                    0 <= candidate_column < len(RARITIES)
                    and 0 <= candidate_row < len(mob_gallery_names)
                ):
                    hover_column = candidate_column
                    hover_row = candidate_row

            gallery_hover_unlocked = False
            if hover_row is not None:
                hover_key_name = (
                    f"{mob_gallery_names[hover_row]}|"
                    f"{RARITIES[hover_column]}"
                )
                gallery_hover_unlocked = (
                    int(mob_gallery_unlocks.get(hover_key_name, 0)) > 0
                )

            if gallery_hover_unlocked:
                current_hover_key = (hover_row, hover_column)
                if current_hover_key != mob_gallery_hover_key:
                    mob_gallery_hover_key = current_hover_key
                    mob_gallery_hover_spin = 0.0
                # Keep turning 15 degrees per step while hovered.
                mob_gallery_hover_spin = (
                    mob_gallery_hover_spin + 2.5
                ) % 360
            else:
                # Not hovering an unlocked cell: reset to the original
                # direction.
                mob_gallery_hover_key = None
                mob_gallery_hover_spin = 0.0

            for row in range(first_gallery_row, len(mob_gallery_names)):
                for column in range(
                    first_gallery_column,
                    len(RARITIES)
                ):
                    gallery_cell = pygame.Rect(
                        int(
                            gallery_start_x
                            + (column - first_gallery_column)
                            * gallery_cell_size
                        ),
                        int(
                            gallery_start_y
                            + (row - first_gallery_row)
                            * gallery_cell_size
                        ),
                        gallery_cell_size - 3,
                        gallery_cell_size - 3
                    )
                    gallery_cell.move_ip(
                        -gallery_grid_rect.x,
                        -gallery_grid_rect.y
                    )
                    # Transparent grid: only the outline is drawn, so the
                    # panel remains visible through the grey cell fill.
                    pygame.draw.rect(
                        gallery_grid_surface,
                        (90, 90, 90, 75),
                        gallery_cell,
                        border_radius=4
                    )
                    pygame.draw.rect(
                        gallery_grid_surface,
                        (55, 55, 55, 210),
                        gallery_cell,
                        2,
                        border_radius=4
                    )
                    gallery_key = (
                        f"{mob_gallery_names[row]}|{RARITIES[column]}"
                    )
                    gallery_count = int(
                        mob_gallery_unlocks.get(gallery_key, 0)
                    )
                    if gallery_count > 0:
                        rarity_color = RARITY_COLORS.get(
                            RARITIES[column],
                            (180, 180, 180)
                        )
                        pygame.draw.rect(
                            gallery_grid_surface,
                            (*rarity_color, 150),
                            gallery_cell,
                            border_radius=4
                        )
                        pygame.draw.rect(
                            gallery_grid_surface,
                            (*rarity_color, 255),
                            gallery_cell,
                            2,
                            border_radius=4
                        )
                        # Clip icon drawing to its own cell so parts like
                        # legs or wings cannot spill into neighbors.
                        gallery_grid_surface.set_clip(gallery_cell)
                        if (
                            row,
                            column
                        ) == mob_gallery_hover_key and (
                            mob_gallery_hover_spin % 360
                        ):
                            # Hovered: draw the icon flat, rotate it by
                            # the current spin, then blit it centered.
                            icon_surface = pygame.Surface(
                                gallery_cell.size,
                                pygame.SRCALPHA
                            )
                            draw_gallery_enemy_icon(
                                icon_surface,
                                mob_gallery_names[row],
                                icon_surface.get_rect().center,
                                RARITIES[column]
                            )
                            icon_surface = pygame.transform.rotate(
                                icon_surface,
                                mob_gallery_hover_spin
                            )
                            gallery_grid_surface.blit(
                                icon_surface,
                                icon_surface.get_rect(
                                    center=gallery_cell.center
                                )
                            )
                        else:
                            draw_gallery_enemy_icon(
                                gallery_grid_surface,
                                mob_gallery_names[row],
                                gallery_cell.center,
                                RARITIES[column]
                            )
                        gallery_grid_surface.set_clip(None)
                        count_surface = gallery_count_font.render(
                            str(gallery_count),
                            True,
                            (255, 255, 255)
                        )
                        gallery_grid_surface.blit(
                            count_surface,
                            (
                                gallery_cell.right
                                - count_surface.get_width() - 2,
                                gallery_cell.top + 1
                            )
                        )

            screen.blit(gallery_grid_surface, gallery_grid_rect)
            screen.set_clip(previous_gallery_clip)

            # Hovering an unlocked gallery cell shows a translucent
            # rectangle in the free space above the grid.
            if gallery_hover_unlocked:
                space_top = new_button_panel_rect.y + 12
                space_bottom = gallery_grid_rect.y - 12
                hover_box_rect = pygame.Rect(
                    new_button_panel_rect.x + 10,
                    space_top,
                    new_button_panel_rect.width - 40,
                    max(
                        40,
                        space_bottom - space_top
                    )
                )
                hover_box_surface = pygame.Surface(
                    hover_box_rect.size,
                    pygame.SRCALPHA
                )
                pygame.draw.rect(
                    hover_box_surface,
                    (0, 0, 0, 89),
                    hover_box_surface.get_rect(),
                    border_radius=8
                )
                # Show the hovered mob's name in the top-left corner.
                hover_name_surface = gallery_hover_name_font.render(
                    mob_gallery_names[hover_row],
                    True,
                    (255, 255, 255)
                )
                hover_box_surface.blit(
                    hover_name_surface,
                    (
                        6,
                        4
                    )
                )
                # Rarity label sits right next to the name.
                hover_rarity_name = RARITIES[hover_column]
                hover_rarity_surface = gallery_hover_name_font.render(
                    hover_rarity_name,
                    True,
                    RARITY_COLORS.get(
                        hover_rarity_name,
                        (255, 255, 255)
                    )
                )
                hover_box_surface.blit(
                    hover_rarity_surface,
                    (
                        6 + hover_name_surface.get_width() + 8,
                        4
                    )
                )
                # Total HP of this mob at this rarity, shown below the
                # name.  Gallery icons are built at Common, so their
                # max_hp is the base value: scale it by the rarity.
                hover_enemy = gallery_enemy_icon_cache.get(
                    (
                        mob_gallery_names[hover_row],
                        RARITIES[hover_column]
                    )
                )
                drop_info = None
                if hover_enemy is not None:
                    hover_hp_text = (
                        "mob hp: "
                        f"{format_number(int(hover_enemy.max_hp * MOB_HP_MULTIPLIER[RARITIES[hover_column]]))}"
                    )
                    hover_hp_surface = gallery_hover_name_font.render(
                        hover_hp_text,
                        True,
                        (255, 255, 255)
                    )
                    hover_box_surface.blit(
                        hover_hp_surface,
                        (
                            6,
                            4 + hover_name_surface.get_height()
                        )
                    )
                    hover_damage_text = (
                        "mob damage: "
                        f"{format_number(int(hover_enemy.damage * MOB_DAMAGE_MULTIPLIER[RARITIES[hover_column]]))}"
                    )
                    hover_damage_surface = gallery_hover_name_font.render(
                        hover_damage_text,
                        True,
                        (255, 255, 255)
                    )
                    hover_box_surface.blit(
                        hover_damage_surface,
                        (
                            6,
                            4 + hover_name_surface.get_height()
                            + hover_hp_surface.get_height()
                        )
                    )
                    hover_description = GALLERY_MOB_DESCRIPTIONS.get(
                        mob_gallery_names[hover_row]
                    )
                    if hover_description:
                        # The description wraps onto new lines below the stat
                        # texts. Every line starts from the same left edge.
                        desc_y = (
                            4
                            + hover_name_surface.get_height()
                            + hover_hp_surface.get_height()
                            + hover_damage_surface.get_height()
                        )
                        desc_max_width = (
                            hover_box_surface.get_width() - 12
                        )
                        current_line = ""
                        for word in hover_description.split():
                            test_line = (
                                current_line + " " + word
                                if current_line
                                else word
                            )
                            if gallery_hover_desc_font.size(
                                test_line
                            )[0] <= desc_max_width:
                                current_line = test_line
                            else:
                                desc_line_surface = (
                                    gallery_hover_desc_font.render(
                                        current_line,
                                        True,
                                        (230, 230, 230)
                                    )
                                )
                                hover_box_surface.blit(
                                    desc_line_surface,
                                    (6, desc_y)
                                )
                                desc_y += (
                                    desc_line_surface.get_height() + 2
                                )
                                current_line = word
                        if current_line:
                            desc_line_surface = (
                                gallery_hover_desc_font.render(
                                    current_line,
                                    True,
                                    (230, 230, 230)
                                )
                            )
                            hover_box_surface.blit(
                                desc_line_surface,
                                (6, desc_y)
                            )
                    drop_table = MOB_DROP_INFO.get(
                        (
                            mob_gallery_names[hover_row],
                            RARITIES[hover_column]
                        )
                    )
                    if drop_table:
                        drop_box_size = 36
                        drop_box_x = 6
                        drop_box_y = desc_y + 30
                        drop_text_y = drop_box_y + drop_box_size + 5
                        drop_pct_font_height = (
                            gallery_hover_name_font.get_height()
                        )
                        drops_by_petal = {}
                        for drop_petal, drop_rarity, drop_chance in drop_table:
                            drops_by_petal.setdefault(
                                drop_petal,
                                []
                            ).append((drop_rarity, drop_chance))
                        drop_row_height = (
                            drop_box_size
                            + 5
                            + drop_pct_font_height
                            + 8
                        )
                        drop_boxes = []
                        for row_index, drop_petal in enumerate(
                            drops_by_petal
                        ):
                            for col_index, (
                                drop_rarity,
                                drop_chance
                            ) in enumerate(
                                drops_by_petal[drop_petal]
                            ):
                                drop_boxes.append({
                                    "x": (
                                        drop_box_x
                                        + col_index
                                        * (drop_box_size + 8)
                                    ),
                                    "y": (
                                        drop_box_y
                                        + row_index * drop_row_height
                                    ),
                                    "rarity": drop_rarity,
                                    "petal": drop_petal,
                                    "pct": f"{drop_chance}%"
                                })
                        drop_box_centers = []
                        for drop_box in drop_boxes:
                            box_x = drop_box["x"]
                            box_y = drop_box["y"]
                            box_rarity_color = RARITY_COLORS.get(
                                drop_box["rarity"],
                                (0, 255, 0)
                            )
                            pygame.draw.rect(
                                hover_box_surface,
                                lighten_color(
                                    box_rarity_color,
                                    0.4
                                ),
                                (
                                    box_x,
                                    box_y,
                                    drop_box_size,
                                    drop_box_size
                                ),
                                border_radius=4
                            )
                            pygame.draw.rect(
                                hover_box_surface,
                                box_rarity_color,
                                (
                                    box_x,
                                    box_y,
                                    drop_box_size,
                                    drop_box_size
                                ),
                                4,
                                border_radius=4
                            )
                            drop_box_centers.append((
                                hover_box_rect.x
                                + box_x
                                + drop_box_size // 2,
                                hover_box_rect.y
                                + box_y
                                + drop_box_size // 2
                            ))
                            drop_pct_white = (
                                gallery_hover_name_font.render(
                                    drop_box["pct"],
                                    True,
                                    (255, 255, 255)
                                )
                            )
                            drop_pct_black = (
                                gallery_hover_name_font.render(
                                    drop_box["pct"],
                                    True,
                                    (0, 0, 0)
                                )
                            )
                            box_text_y = box_y + drop_box_size + 5
                            for outline_x in (-1, 0, 1):
                                for outline_y in (-1, 0, 1):
                                    if outline_x or outline_y:
                                        hover_box_surface.blit(
                                            drop_pct_black,
                                            (
                                                box_x + outline_x,
                                                box_text_y + outline_y
                                            )
                                        )
                            hover_box_surface.blit(
                                drop_pct_white,
                                (box_x + 1, box_text_y + 1)
                            )
                screen.blit(
                    hover_box_surface,
                    hover_box_rect
                )
                if drop_table:
                    for drop_center, drop_box in zip(
                        drop_box_centers,
                        drop_boxes
                    ):
                        draw_petal(
                            drop_box["petal"],
                            drop_center[0],
                            drop_center[1],
                            drop_box["rarity"],
                            size_scale=(
                                drop_box_size * 0.6
                            ) / (PETAL_RADIUS * 2)
                        )

            gallery_track_top = gallery_grid_rect.y
            gallery_track_height = gallery_grid_rect.height
            pygame.draw.rect(
                screen,
                (150, 95, 20),
                (
                    new_button_panel_rect.right - 18,
                    gallery_track_top,
                    10,
                    gallery_track_height
                ),
                border_radius=4
            )
            gallery_thumb_height = max(
                28,
                int(
                    gallery_track_height
                    * gallery_visible_rows
                    / max(1, len(mob_gallery_names))
                )
            )
            gallery_usable_track = max(
                1,
                gallery_track_height - gallery_thumb_height
            )
            gallery_thumb_y = gallery_track_top
            if gallery_max_scroll:
                gallery_thumb_y += int(
                    gallery_usable_track
                    * mob_gallery_scroll_position
                    / gallery_max_scroll
                )
            mob_gallery_scrollbar_rect = pygame.Rect(
                new_button_panel_rect.right - 18,
                gallery_thumb_y,
                10,
                gallery_thumb_height
            )
            pygame.draw.rect(
                screen,
                (255, 225, 110),
                mob_gallery_scrollbar_rect,
                border_radius=4
            )

            gallery_track_left = gallery_grid_rect.x
            gallery_track_top = (
                mob_gallery_grid_top
                + GALLERY_GRID_WINDOW_HEIGHT
                + 4
            )
            gallery_track_width = gallery_grid_rect.width
            pygame.draw.rect(
                screen,
                (150, 95, 20),
                (
                    gallery_track_left,
                    gallery_track_top,
                    gallery_track_width,
                    10
                ),
                border_radius=4
            )
            gallery_thumb_width = max(
                28,
                int(
                    gallery_track_width
                    * gallery_visible_columns
                    / max(1, len(RARITIES))
                )
            )
            gallery_usable_track = max(
                1,
                gallery_track_width - gallery_thumb_width
            )
            gallery_thumb_x = gallery_track_left
            if gallery_max_horizontal_scroll:
                gallery_thumb_x += int(
                    gallery_usable_track
                    * mob_gallery_horizontal_scroll_position
                    / gallery_max_horizontal_scroll
                )
            mob_gallery_horizontal_scrollbar_rect = pygame.Rect(
                gallery_thumb_x,
                gallery_track_top,
                gallery_thumb_width,
                10
            )
            pygame.draw.rect(
                screen,
                (255, 225, 110),
                mob_gallery_horizontal_scrollbar_rect,
                border_radius=4
            )

        craft_panel_target_y = (
            craft_panel_target_rect.y
            if craft_open
            else HEIGHT + 20
        )
        # The panel slides with acceleration, easing into place.
        craft_panel_slide_velocity += (
            craft_panel_target_y - craft_panel_rect.y
        ) * 0.045
        craft_panel_slide_velocity *= 0.78
        craft_panel_rect.y += craft_panel_slide_velocity
        # Once nearly closed, rest exactly offscreen so no outline
        # sliver stays visible.
        if not craft_open and (
            craft_panel_rect.y >= HEIGHT + 19
        ):
            craft_panel_rect.y = HEIGHT + 20
            craft_panel_slide_velocity = 0.0
        if (
            abs(craft_panel_target_y - craft_panel_rect.y) < 0.5
            and abs(craft_panel_slide_velocity) < 0.5
        ):
            craft_panel_rect.y = craft_panel_target_y
            craft_panel_slide_velocity = 0.0

        if craft_panel_rect.y < HEIGHT + 20:
            pygame.draw.rect(
                screen,
                (215, 165, 75),
                craft_panel_rect,
                border_radius=8
            )
            pygame.draw.rect(
                screen,
                (120, 75, 30),
                craft_panel_rect,
                3,
                border_radius=8
            )

        pygame.draw.rect(
            screen,
            (215, 165, 75),
            above_inventory_button_rect,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (120, 75, 30),
            above_inventory_button_rect,
            3,
            border_radius=8
        )
        # The white circle splits into two full circles that spin
        # around the middle while hovered, and merges back when the
        # mouse leaves.  Each circle keeps its own dark outline.
        if above_inventory_button_rect.collidepoint(
            pygame.mouse.get_pos()
        ):
            craft_button_split_amount = min(
                1.0,
                craft_button_split_amount + 0.08
            )
            craft_button_spin_angle = (
                craft_button_spin_angle + 3.5
            ) % 360
        else:
            craft_button_split_amount = max(
                0.0,
                craft_button_split_amount - 0.08
            )

        craft_center_x, craft_center_y = (
            above_inventory_button_rect.center
        )
        craft_split_distance = 10 * craft_button_split_amount
        craft_split_rad = math.radians(craft_button_spin_angle)
        craft_offset_x = math.cos(craft_split_rad) * craft_split_distance
        craft_offset_y = math.sin(craft_split_rad) * craft_split_distance

        pygame.draw.circle(
            screen,
            (120, 75, 30),
            (
                int(craft_center_x + craft_offset_x),
                int(craft_center_y + craft_offset_y)
            ),
            10
        )
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                int(craft_center_x + craft_offset_x),
                int(craft_center_y + craft_offset_y)
            ),
            8
        )
        pygame.draw.circle(
            screen,
            (120, 75, 30),
            (
                int(craft_center_x - craft_offset_x),
                int(craft_center_y - craft_offset_y)
            ),
            10
        )
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                int(craft_center_x - craft_offset_x),
                int(craft_center_y - craft_offset_y)
            ),
            8
        )

        # Solid mixed orange/yellow fill, with no gradient or separated
        # color sections.
        pygame.draw.rect(
            screen,
            (250, 205, 45),
            above_craft_button_rect,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (175, 105, 20),
            above_craft_button_rect,
            3,
            border_radius=8
        )

        # White smooth-pointed square (diamond) in its center.  It
        # spins while the button is hovered and eases back upright
        # when the mouse leaves.
        if above_craft_button_rect.collidepoint(pygame.mouse.get_pos()):
            gallery_button_diamond_angle = (
                gallery_button_diamond_angle + 4.0
            ) % 360
        else:
            settle_target = (
                round(gallery_button_diamond_angle / 90) * 90
            )
            gallery_button_diamond_angle += (
                settle_target - gallery_button_diamond_angle
            ) * 0.15

        diamond_x, diamond_y = above_craft_button_rect.center
        diamond_size = 13
        diamond_points = []
        for diamond_point_index in range(4):
            diamond_point_angle = math.radians(
                -90
                + diamond_point_index * 90
                + gallery_button_diamond_angle
            )
            diamond_points.append(
                (
                    diamond_x + math.cos(diamond_point_angle) * diamond_size,
                    diamond_y + math.sin(diamond_point_angle) * diamond_size
                )
            )
        pygame.draw.polygon(
            screen,
            (255, 255, 255),
            diamond_points
        )
        pygame.draw.lines(
            screen,
            (235, 235, 235),
            True,
            diamond_points,
            2
        )

        pygame.draw.rect(
            screen,
            (40,120,255),
            inventory_button_rect,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (10, 45, 150),
            inventory_button_rect,
            3,
            border_radius=8
        )


        # ---------------- BAG ICON ----------------

        bag_width = 26
        bag_height = 25

        bag_x = (
            inventory_button_rect.centerx
            - bag_width // 2
        )

        bag_y = (
            inventory_button_rect.centery
            - bag_height // 2
        )


        # bag body

        pygame.draw.rect(
            screen,
            (20,50,150),
            (
                bag_x,
                bag_y,
                bag_width,
                bag_height
            ),
            border_radius=5
        )


        # bag handle

        pygame.draw.arc(
            screen,
            (20,50,150),
            (
                bag_x + 5,
                bag_y - 10,
                bag_width - 10,
                15
            ),
            math.radians(180),
            math.radians(360),
            4
        )

        # ---------------- INVENTORY MENU ----------------
        # Drawn while open AND while sliding back offscreen on close, so the
        # close animation is visible too.

        if (
            inventory_open
            or inv_panel_x > -inventory_panel_rect.width + 1
        ):


            pygame.draw.rect(
                screen,
                (30,120,255),
                inventory_panel_rect,
                border_radius=15
            )

            pygame.draw.rect(
                screen,
                (10,40,120),
                inventory_panel_rect,
                4,
                border_radius=15
            )


            # inventory grid settings

            inventory_cols = INVENTORY_COLS
            slot_size = INVENTORY_SLOT_SIZE
            slot_gap = INVENTORY_SLOT_GAP

            max_rows = get_inventory_max_rows()


            # how many rows fit inside the panel

            top_padding = 40
            bottom_padding = 20

            max_rows = (
                inventory_panel_rect.height
                - top_padding
                - bottom_padding
            ) // (slot_size + slot_gap)


            # center inventory grid

            grid_width = (
                inventory_cols * slot_size +
                (inventory_cols - 1) * slot_gap
            )

            start_x = (
                inventory_panel_rect.centerx -
                grid_width // 2
            )

            start_y = (
                inventory_panel_rect.y + top_padding
            )

            inventory_previous_clip = screen.get_clip()
            screen.set_clip(
                pygame.Rect(
                    inventory_panel_rect.x + 4,
                    inventory_panel_rect.y + top_padding,
                    inventory_panel_rect.width - 8,
                    inventory_panel_rect.height
                    - top_padding
                    - bottom_padding
                )
            )

            inventory_display_rows = build_inventory_display_rows()

            for display_index, display_row in enumerate(
                inventory_display_rows
            ):

                row = display_index - inventory_scroll

                if row < 0 or row >= max_rows:
                    continue

                y = start_y + row * (slot_size + slot_gap)

                if display_row["type"] == "divider":

                    divider_rarity_color = RARITY_COLORS.get(
                        display_row["rarity"],
                        (80, 80, 80)
                    )
                    divider_color = darken_color(
                        divider_rarity_color,
                        0.78
                    )
                    divider_outline_color = darken_color(
                        divider_rarity_color,
                        0.4
                    )

                    divider_surface = flower_name_font.render(
                        display_row["rarity"],
                        True,
                        divider_color
                    )
                    divider_outline_surface = flower_name_font.render(
                        display_row["rarity"],
                        True,
                        divider_outline_color
                    )
                    divider_center_x = inventory_panel_rect.centerx
                    divider_text_x = (
                        divider_center_x
                        - divider_surface.get_width() // 2
                    )
                    divider_text_y = (
                        y
                        + (slot_size - divider_surface.get_height()) // 2
                    )
                    line_y = (
                        divider_text_y
                        + divider_surface.get_height() // 2
                    )
                    line_gap = 8
                    edge_margin = 12

                    for outline_x in (-1, 0, 1):
                        for outline_y in (-1, 0, 1):
                            if outline_x or outline_y:
                                screen.blit(
                                    divider_outline_surface,
                                    (
                                        divider_text_x + outline_x * 2,
                                        divider_text_y + outline_y * 2
                                    )
                                )

                    pygame.draw.line(
                        screen,
                        divider_color,
                        (
                            inventory_panel_rect.x + edge_margin,
                            line_y
                        ),
                        (
                            divider_text_x - line_gap,
                            line_y
                        ),
                        2
                    )
                    pygame.draw.line(
                        screen,
                        divider_color,
                        (
                            divider_text_x
                            + divider_surface.get_width()
                            + line_gap,
                            line_y
                        ),
                        (
                            inventory_panel_rect.right - edge_margin,
                            line_y
                        ),
                        2
                    )

                    screen.blit(
                        divider_surface,
                        (divider_text_x, divider_text_y)
                    )

                    continue

                for col, item in enumerate(display_row["items"]):

                    x = start_x + col * (slot_size + slot_gap)

                    rarity = item["rarity"]
                    amount = item.get(
                        "amount",
                        1
                    )

                    if rarity == "Omnient":

                        draw_omnient_slot(
                            screen,
                            x,
                            y,
                            slot_size
                        )


                    elif rarity == "Celestial":

                        draw_celestial_slot(
                            screen,
                            x,
                            y,
                            slot_size
                        )


                    elif rarity == "Infino":

                        draw_infino_slot(
                            screen,
                            x,
                            y,
                            slot_size
                        )


                    else:

                        rarity_color = RARITY_COLORS.get(
                            rarity,
                            (80,80,80)
                        )

                        pygame.draw.rect(
                            screen,
                            rarity_color,
                            (
                                x,
                                y,
                                slot_size,
                                slot_size
                            ),
                            border_radius=8
                        )

                    # draw petal

                    draw_petal(
                        item["petal"],
                        x + slot_size // 2,
                        y + slot_size // 2,
                        item["rarity"]
                    )

                    if amount > 1:

                        count_font = craft_count_font

                        count_text = count_font.render(
                            str(format_number(int(amount))),
                            True,
                            (255, 255, 255)
                        )

                        screen.blit(
                            count_text,
                            (
                                x + slot_size - count_text.get_width() - 5,
                                y + 3
                            )
                        )

            screen.set_clip(inventory_previous_clip)

        if hp_menu_open:


            # background square

            menu = pygame.Rect(
                WIDTH//2 - 150,
                HEIGHT//2 - 150,
                300,
                250
            )


            pygame.draw.rect(
                screen,
                (40,40,40),
                menu,
                border_radius=10
            )


            pygame.draw.rect(
                screen,
                (180,180,180),
                menu,
                3,
                border_radius=10
            )


            font = hud_font


            hp_text = font.render(
                "MAX HP: " + format_number(PLAYER_MAX_HP),
                True,
                (255,255,255)
            )


            cost_text = font.render(
                "Cost: " + format_number(hp_upgrade_cost),
                True,
                (255,255,0)
            )


            screen.blit(
                hp_text,
                (
                    menu.x + 20,
                    menu.y + 30
                )
            )


            screen.blit(
                cost_text,
                (
                    menu.x + 20,
                    menu.y + 70
                )
            )

            # upgrade button

            pygame.draw.rect(
                screen,
                (0,180,0),
                hp_upgrade_rect,
                border_radius=8
            )
            pygame.draw.rect(
                screen,
                (0, 85, 0),
                hp_upgrade_rect,
                3,
                border_radius=8
            )


            upgrade_text = font.render(
                "Upgrade HP",
                True,
                (255,255,255)
            )


            screen.blit(
                upgrade_text,
                (
                    hp_upgrade_rect.centerx - upgrade_text.get_width()/2,
                    hp_upgrade_rect.centery - upgrade_text.get_height()/2
                )
            )

            pygame.draw.rect(
            screen,
            (180,50,50),
            close_button_rect,
            border_radius=8
        )
            pygame.draw.rect(
                screen,
                (110, 20, 20),
                close_button_rect,
                3,
                border_radius=8
            )


            close_text = font.render(
                "X",
                True,
                (255,255,255)
            )


            screen.blit(
                close_text,
                (
                    close_button_rect.centerx - close_text.get_width()/2,
                    close_button_rect.centery - close_text.get_height()/2
                )
            )


        pygame.draw.rect(
            screen,
            (50,50,50),
            hp_button_rect,
            border_radius=8
        )
        pygame.draw.rect(
            screen,
            (15, 15, 15),
            hp_button_rect,
            3,
            border_radius=8
        )

        hp_font = game_hp_font

        hp_button_text = hp_font.render(
            "HP",
            True,
            (255,255,255)
        )

        screen.blit(
            hp_button_text,
            (
                hp_button_rect.centerx - hp_button_text.get_width()//2,
                hp_button_rect.centery - hp_button_text.get_height()//2
            )
        )

        # Draw the craft panel last so it stays in front of the HP controls.
        if craft_panel_rect.y < HEIGHT + 20:
            pygame.draw.rect(
                screen,
                (215, 165, 75),
                craft_panel_rect,
                border_radius=8
            )
            pygame.draw.rect(
                screen,
                (120, 75, 30),
                craft_panel_rect,
                3,
                border_radius=8
            )

            # Five crafting slots arranged at the points of the former
            # pentagon, without drawing the pentagon itself.
            craft_slot_size = 38
            craft_center_x = craft_panel_rect.centerx - 55
            craft_center_y = craft_panel_rect.y + 95
            craft_radius = 55
            craft_slot_points = [
                (
                    int(
                        craft_center_x
                        + math.cos(-math.pi / 2 + i * 2 * math.pi / 5)
                        * craft_radius
                    ),
                    int(
                        craft_center_y
                        + math.sin(-math.pi / 2 + i * 2 * math.pi / 5)
                        * craft_radius
                    )
                )
                for i in range(5)
            ]
            craft_draw_slot_points = craft_slot_points
            if craft_animation_active:
                animation_progress = min(
                    1.0,
                    max(
                        0.0,
                        1
                        - craft_animation_timer
                        / max(1, craft_animation_duration)
                    )
                )
                # Spin quickly at first, then decelerate smoothly.
                move_angle = (
                    2 * animation_progress
                    - animation_progress ** 2
                ) * math.pi * 4
                # Keep the five input slots stationary while crafting. The
                # crafted result is shown separately in the center slot.
                slide_progress = 0.0
                slide_progress = (
                    slide_progress ** 2
                    * (3 - 2 * slide_progress)
                )
                radius_scale = 1 - slide_progress
                craft_draw_slot_points = []
                for point_x, point_y in craft_slot_points:
                    offset_x = (point_x - craft_center_x) * radius_scale
                    offset_y = (point_y - craft_center_y) * radius_scale
                    craft_draw_slot_points.append(
                        (
                            int(
                                craft_center_x
                                + offset_x * math.cos(move_angle)
                                - offset_y * math.sin(move_angle)
                            ),
                            int(
                                craft_center_y
                                + offset_x * math.sin(move_angle)
                                + offset_y * math.cos(move_angle)
                            )
                        )
                    )

            for point_x, point_y in craft_draw_slot_points:
                craft_slot_rect = pygame.Rect(
                    point_x - craft_slot_size // 2,
                    point_y - craft_slot_size // 2,
                    craft_slot_size,
                    craft_slot_size
                )
                pygame.draw.rect(
                    screen,
                    (185, 135, 60),
                    craft_slot_rect,
                    border_radius=6
                )
                pygame.draw.rect(
                    screen,
                    (105, 85, 60),
                    craft_slot_rect,
                    2,
                    border_radius=6
                )

            # Sixth slot: a permanent empty result slot in the center of the
            # five input slots. A crafted petal is drawn into this slot when
            # a craft succeeds.
            center_slot_rect = pygame.Rect(
                craft_center_x - craft_slot_size // 2,
                craft_center_y - craft_slot_size // 2,
                craft_slot_size,
                craft_slot_size
            )
            pygame.draw.rect(
                screen,
                (185, 135, 60),
                center_slot_rect,
                border_radius=6
            )
            pygame.draw.rect(
                screen,
                (105, 85, 60),
                center_slot_rect,
                2,
                border_radius=6
            )

            if (
                craft_result_item is not None
                and not craft_animation_active
                and not craft_post_result_items
            ):
                for point_x, point_y in craft_draw_slot_points:
                    result_input_slot_rect = pygame.Rect(
                        point_x - craft_slot_size // 2,
                        point_y - craft_slot_size // 2,
                        craft_slot_size,
                        craft_slot_size
                    )
                    pygame.draw.rect(
                        screen,
                        (185, 135, 60),
                        result_input_slot_rect,
                        border_radius=6
                    )
                    pygame.draw.rect(
                        screen,
                        (105, 85, 60),
                        result_input_slot_rect,
                        2,
                        border_radius=6
                    )
                draw_rarity_slot(
                    craft_center_x - 19,
                    craft_center_y - 19,
                    38,
                    craft_result_item["rarity"]
                )
                draw_petal(
                    craft_result_item["petal"],
                    craft_center_x,
                    craft_center_y,
                    craft_result_item["rarity"],
                    0.60
                )
                if craft_result_item.get("amount", 1) > 1:
                    result_count_font = craft_count_font
                    result_count_text = result_count_font.render(
                        str(format_number(craft_result_item["amount"])),
                        True,
                        (255, 255, 255)
                    )
                    screen.blit(
                        result_count_text,
                        (
                            craft_center_x + craft_slot_size // 2
                            - result_count_text.get_width() - 3,
                            craft_center_y - craft_slot_size // 2 + 2
                        )
                    )

            craft_button_rect = pygame.Rect(
                craft_panel_rect.right - 82,
                craft_center_y - 19,
                70,
                38
            )
            pygame.draw.rect(
                screen,
                (215, 165, 75),
                craft_button_rect,
                border_radius=7
            )
            pygame.draw.rect(
                screen,
                (120, 75, 30),
                craft_button_rect,
                2,
                border_radius=7
            )
            craft_button_text = craft_button_font.render(
                "Craft",
                True,
                (255, 255, 255)
            )
            screen.blit(
                craft_button_text,
                (
                    craft_button_rect.centerx
                    - craft_button_text.get_width() // 2,
                    craft_button_rect.centery
                    - craft_button_text.get_height() // 2
                )
            )

            # Combine matching inventory petals and rarities for the grid.
            current_inventory_signature = tuple(
                (
                    item.get("petal"),
                    item.get("rarity"),
                    int(item.get("amount", 1))
                )
                for item in inventory
            )
            if current_inventory_signature != craft_inventory_signature:
                craft_inventory_signature = current_inventory_signature
                craft_slot_items_cache = []
                craft_slot_lookup_cache = {}
                for inventory_item in inventory:
                    item_key = (
                        inventory_item.get("petal"),
                        inventory_item.get("rarity")
                    )
                    if item_key in craft_slot_lookup_cache:
                        craft_slot_items_cache[
                            craft_slot_lookup_cache[item_key]
                        ]["amount"] += inventory_item.get("amount", 1)
                    else:
                        craft_slot_lookup_cache[item_key] = len(
                            craft_slot_items_cache
                        )
                        craft_slot_items_cache.append({
                            "petal": item_key[0],
                            "rarity": item_key[1],
                            "amount": inventory_item.get("amount", 1)
                        })

            craft_slot_items = craft_slot_items_cache
            craft_slot_lookup = craft_slot_lookup_cache

            if craft_result_item is not None and not craft_animation_active:
                craft_display_items = []
            else:
                craft_display_items = (
                    craft_selected_items
                    if craft_selected_items
                    else craft_post_result_items
                )
            for slot_index, craft_item in enumerate(craft_display_items):
                point_x, point_y = craft_draw_slot_points[slot_index]
                display_petal = craft_item["petal"]
                display_rarity = craft_item["rarity"]
                draw_x = point_x
                draw_y = point_y
                draw_rarity_slot(
                    point_x - craft_slot_size // 2,
                    point_y - craft_slot_size // 2,
                    craft_slot_size,
                    display_rarity
                )
                draw_petal(
                    display_petal,
                    draw_x,
                    draw_y,
                    display_rarity,
                    0.60
                )
                displayed_slot_amount = craft_item["amount"]
                if displayed_slot_amount > 1:
                    count_text = craft_count_font.render(
                        str(format_number(int(displayed_slot_amount))),
                        True,
                        (255, 255, 255)
                    )
                    screen.blit(
                        count_text,
                        (
                            point_x + craft_slot_size // 2
                            - count_text.get_width() - 3,
                            point_y - craft_slot_size // 2 + 2
                        )
                    )

            if craft_animation_active:
                success_text_value = "Crafting..."
            elif craft_result_text:
                success_text_value = craft_result_text
            elif craft_selected_items:
                selected_rarity = craft_selected_items[0]["rarity"]
                rarity_level = (
                    RARITIES.index(selected_rarity)
                    if selected_rarity in RARITIES
                    else 0
                )
                success_percent = min(
                    100,
                    256 / (2 ** rarity_level)
                )
                success_percent_text = (
                    f"{success_percent:.4f}".rstrip("0").rstrip(".")
                )
                success_text_value = (
                    f"Success: {success_percent_text}%"
                )
            else:
                success_text_value = "Success: --"

            success_font = craft_success_font
            success_text = success_font.render(
                success_text_value,
                True,
                (255, 255, 255)
            )
            screen.blit(
                success_text,
                (
                    craft_button_rect.centerx
                    - success_text.get_width() // 2,
                    craft_button_rect.bottom + 6
                )
            )

            if craft_animation_active and craft_animation_duration > 0:
                craft_progress = min(
                    1.0,
                    max(
                        0.0,
                        1
                        - craft_animation_timer
                        / craft_animation_duration
                    )
                )
                progress_text = success_font.render(
                    f"{int(craft_progress * 100)}%",
                    True,
                    (255, 255, 255)
                )
                progress_text_y = success_text.get_rect(
                    center=(
                        craft_button_rect.centerx,
                        craft_button_rect.bottom + 30
                    )
                )
                screen.blit(progress_text, progress_text_y)
                progress_bar_rect = pygame.Rect(
                    craft_button_rect.centerx - 48,
                    craft_button_rect.bottom + 42,
                    96,
                    7
                )
                pygame.draw.rect(
                    screen,
                    (80, 55, 30),
                    progress_bar_rect,
                    border_radius=4
                )
                pygame.draw.rect(
                    screen,
                    (255, 220, 90),
                    (
                        progress_bar_rect.x,
                        progress_bar_rect.y,
                        int(progress_bar_rect.width * craft_progress),
                        progress_bar_rect.height
                    ),
                    border_radius=4
                )

            craft_petals = craft_petals_cache
            craft_rarities = craft_rarities_cache
            craft_row_height = 42
            craft_cell_width = 42
            craft_grid_x = craft_panel_rect.x + 10
            craft_grid_y = craft_panel_rect.bottom - 350
            craft_visible_rows = math.ceil(
                325 / craft_row_height
            )
            craft_visible_columns = max(
                1,
                    math.ceil(
                        (craft_panel_rect.width - 40) / craft_cell_width
                    )
            )
            craft_max_scroll = max(
                0,
                len(craft_petals) - craft_visible_rows
            )
            craft_max_horizontal_scroll = max(
                0,
                len(craft_rarities) - craft_visible_columns
            )
            craft_scroll_target = max(
                0,
                min(craft_scroll_target, craft_max_scroll)
            )
            craft_horizontal_scroll_target = max(
                0,
                min(craft_horizontal_scroll_target, craft_max_horizontal_scroll)
            )

            # Smoothly ease both scroll positions toward their targets.
            craft_scroll_position += (
                craft_scroll_target - craft_scroll_position
            ) * 0.22
            craft_horizontal_scroll_position += (
                craft_horizontal_scroll_target
                - craft_horizontal_scroll_position
            ) * 0.22
            craft_scroll = int(craft_scroll_position)
            craft_horizontal_scroll = int(craft_horizontal_scroll_position)

            # Crafting grid: petal rows by rarity columns.
            craft_first_row = int(craft_scroll_position)
            craft_first_column = int(craft_horizontal_scroll_position)
            craft_grid_y -= (
                craft_scroll_position - craft_first_row
            ) * craft_row_height
            craft_grid_x -= (
                craft_horizontal_scroll_position - craft_first_column
            ) * craft_cell_width

            previous_clip = screen.get_clip()
            craft_grid_clip = pygame.Rect(
                craft_panel_rect.x + 10,
                craft_panel_rect.bottom - 350,
                craft_panel_rect.width - 40,
                325
            )
            screen.set_clip(craft_grid_clip)

            for row in range(craft_visible_rows + 1):
                petal_index = row + craft_first_row
                if petal_index >= len(craft_petals):
                    break

                for col in range(craft_visible_columns + 1):
                    rarity_index = col + craft_first_column
                    if rarity_index >= len(craft_rarities):
                        break
                    rarity = craft_rarities[rarity_index]
                    full_cell = pygame.Rect(
                        craft_grid_x + col * craft_cell_width,
                        craft_grid_y + row * craft_row_height,
                        craft_cell_width - 2,
                        craft_row_height - 2
                    )
                    cell = full_cell.clip(craft_grid_clip)
                    if cell.width <= 0 or cell.height <= 0:
                        continue
                    pygame.draw.rect(screen, (185, 135, 60), cell)
                    pygame.draw.rect(screen, (105, 85, 60), cell, 1)

                    grid_item_index = craft_slot_lookup.get(
                        (craft_petals[petal_index], rarity)
                    )
                    if grid_item_index is not None:
                        grid_item = craft_slot_items[grid_item_index]
                        grid_amount = grid_item["amount"]
                        if any(
                            remaining_item["petal"] == grid_item["petal"]
                            and remaining_item["rarity"] == grid_item["rarity"]
                            for remaining_item in craft_post_result_items
                        ):
                            grid_amount = 0
                        if (
                            craft_selected_items
                            and craft_selected_items[0]["petal"]
                            == grid_item["petal"]
                            and craft_selected_items[0]["rarity"]
                            == grid_item["rarity"]
                        ):
                            grid_amount -= sum(
                                item["amount"]
                                for item in craft_selected_items
                            )

                        if grid_amount > 0:
                            if grid_item["rarity"] == "Infino":
                                pygame.draw.rect(
                                    screen,
                                    (130, 130, 130),
                                    full_cell,
                                    border_radius=8
                                )
                                pygame.draw.rect(
                                    screen,
                                    (65, 65, 65),
                                    full_cell,
                                    2,
                                    border_radius=8
                                )
                            else:
                                draw_rarity_slot(
                                    full_cell.x,
                                    full_cell.y,
                                    full_cell.width,
                                    grid_item["rarity"]
                                )
                            draw_petal(
                                grid_item["petal"],
                                full_cell.centerx,
                                full_cell.centery,
                                grid_item["rarity"],
                                0.60
                            )

                        if grid_amount > 1:
                            grid_count_font = craft_grid_count_font
                            grid_count_text = grid_count_font.render(
                                str(format_number(int(grid_amount))),
                                True,
                                (255, 255, 255)
                            )
                            screen.blit(
                                grid_count_text,
                                (
                                    full_cell.right
                                    - grid_count_text.get_width() - 2,
                                    full_cell.top + 1
                                )
                            )

            screen.set_clip(previous_clip)

            # Draggable scrollbar.
            track_top = craft_panel_rect.bottom - 350
            track_height = 325
            pygame.draw.rect(
                screen,
                (80, 55, 30),
                (
                    craft_panel_rect.right - 18,
                    track_top,
                    12,
                    track_height
                ),
                border_radius=5
            )
            thumb_height = max(
                30,
                int(
                    track_height
                    * craft_visible_rows
                    / max(1, len(craft_petals))
                )
            )
            usable_track = max(1, track_height - thumb_height)
            thumb_y = track_top
            if craft_max_scroll:
                thumb_y += int(
                    usable_track
                    * craft_scroll_position
                    / craft_max_scroll
                )
            craft_scrollbar_rect = pygame.Rect(
                craft_panel_rect.right - 18,
                thumb_y,
                12,
                thumb_height
            )
            pygame.draw.rect(
                screen,
                (235, 200, 120),
                craft_scrollbar_rect,
                border_radius=5
            )
            pygame.draw.rect(
                screen,
                (120, 75, 30),
                craft_scrollbar_rect,
                2,
                border_radius=5
            )

            horizontal_track_left = craft_panel_rect.x + 10
            horizontal_track_top = craft_panel_rect.bottom - 18
            horizontal_track_width = craft_panel_rect.width - 40
            pygame.draw.rect(
                screen,
                (80, 55, 30),
                (
                    horizontal_track_left,
                    horizontal_track_top,
                    horizontal_track_width,
                    12
                ),
                border_radius=5
            )
            horizontal_thumb_width = max(
                30,
                int(
                    horizontal_track_width
                    * craft_visible_columns
                    / max(1, len(craft_rarities))
                )
            )
            horizontal_usable_track = max(
                1,
                horizontal_track_width - horizontal_thumb_width
            )
            horizontal_thumb_x = horizontal_track_left
            if craft_max_horizontal_scroll:
                horizontal_thumb_x += int(
                    horizontal_usable_track
                    * craft_horizontal_scroll_position
                    / craft_max_horizontal_scroll
                )
            craft_horizontal_scrollbar_rect = pygame.Rect(
                horizontal_thumb_x,
                horizontal_track_top,
                horizontal_thumb_width,
                12
            )
            pygame.draw.rect(
                screen,
                (235, 200, 120),
                craft_horizontal_scrollbar_rect,
                border_radius=5
            )
            pygame.draw.rect(
                screen,
                (120, 75, 30),
                craft_horizontal_scrollbar_rect,
                2,
                border_radius=5
            )

        # ---------------- HOLE LAND BANNER ----------------
        if hole_land_banner_timer > 0:
            hole_land_banner_timer -= 2
            if hole_land_banner_timer < 60:
                hole_land_banner_alpha = int(255 * (hole_land_banner_timer / 60.0))
            banner_surf = pygame.Surface((WIDTH, 80), pygame.SRCALPHA)
            banner_surf.fill((0, 0, 0, int(hole_land_banner_alpha * 0.85)))
            hl_title_font = pygame.font.Font(None, 44)
            hl_title = hl_title_font.render("H O L E   L A N D", True, (190, 80, 255))
            hl_title.set_alpha(hole_land_banner_alpha)
            banner_surf.blit(hl_title, (WIDTH // 2 - hl_title.get_width() // 2, 22))
            screen.blit(banner_surf, (0, 100))

        # ---------------- SPAWN MESSAGE ----------------

        if spawn_message_timer > 0:

            spawn_message_timer -= 3

            # fade during the last 60 frames
            if spawn_message_timer < 60:
                spawn_message_alpha = int(
                    255 * (spawn_message_timer / 60)
                )

            font = spawn_message_font

            text = font.render(
                spawn_message,
                True,
                (255, 0, 0)
            )

            text.set_alpha(spawn_message_alpha)

            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    20
                )
            )

        # ---------------- ERROR MESSAGE ----------------

        if error_message_timer > 0:
            error_message_timer -= 3

            if error_message_timer < 60:
                error_message_alpha = int(
                    255 * (error_message_timer / 60)
                )

            error_font = pygame.font.Font(None, 24)
            # Wrap the message so long text doesn't overflow the screen;
            # the box grows taller as more lines wrap.
            error_lines = wrap_text(
                error_font,
                error_message,
                400
            )
            error_text_surfs = [
                error_font.render(line, True, (255, 255, 255))
                for line in error_lines
            ]
            for error_text in error_text_surfs:
                error_text.set_alpha(error_message_alpha)

            # Calculate rectangle alpha (max 128 for the rectangle's alpha channel)
            rect_alpha = int(128 * (error_message_alpha / 255))

            # Centered at top, very close to the top edge
            error_box_width = max(
                surf.get_width() for surf in error_text_surfs
            ) + 20
            error_box_height = (
                sum(surf.get_height() for surf in error_text_surfs)
                + 10
                + (len(error_text_surfs) - 1) * 10
            )
            error_box_rect = pygame.Rect(
                WIDTH//2 - error_box_width//2,
                10,
                error_box_width,
                error_box_height
            )

            # Create a transparent surface for the error box background
            error_box_surf = pygame.Surface((error_box_width, error_box_height), pygame.SRCALPHA)
            pygame.draw.rect(
                error_box_surf,
                (0, 0, 0, rect_alpha),
                error_box_surf.get_rect(),
                border_radius=5
            )

            # Blit the error box surface to screen
            screen.blit(error_box_surf, error_box_rect.topleft)

            # Blit the text lines on top
            error_text_y = error_box_rect.y + 5
            for error_text in error_text_surfs:
                screen.blit(
                    error_text,
                    (
                        error_box_rect.x + 10,
                        error_text_y
                    )
                )
                error_text_y += error_text.get_height() + 10

        # ---------------- UPDATE SCREEN ----------------

    # ---------------- IRIS WIPE TRANSITION ----------------
    if welcome_transition_active:

        if welcome_transition_phase == "close":

            p = welcome_transition_progress / WELCOME_TRANSITION_LENGTH
            radius = WELCOME_IRIS_START_RADIUS * (1.0 - p)
            draw_iris_wipe(int(radius))

            welcome_transition_progress += 1.0

            if welcome_transition_progress >= WELCOME_TRANSITION_LENGTH:

                # hole fully closed; reveal the game under a fresh black
                # screen and start expanding the hole back out again
                game_state = "game"
                welcome_transition_phase = "open"
                welcome_transition_progress = 1.0
                # Set the game grid color to match the current welcome grid color
                game_grid_color = welcome_grid_color
                game_target_grid_color = welcome_target_grid_color

        else:  # "open"

            p = welcome_transition_progress / WELCOME_TRANSITION_LENGTH
            radius = WELCOME_IRIS_END_RADIUS + (
                WELCOME_IRIS_START_RADIUS - WELCOME_IRIS_END_RADIUS
            ) * p
            draw_iris_wipe(int(radius))

            welcome_transition_progress += 1.0

            if welcome_transition_progress >= WELCOME_TRANSITION_LENGTH:

                welcome_transition_active = False

# ---------------- CHAT BOX ----------------
    # Only visible during gameplay after clicking the green Play button.
    if welcome_play_pressed:
        chat_box_w = 260
        chat_margin = 20
        border_radius = 12
        # Arrow button and vertical rectangle stay at fixed positions
        arrow_y = HEIGHT - chat_margin - 120
        # Chat box bottom stays fixed; grows upward when taller
        if chat_arrow_up:
            chat_box_h = 200
            box_y = arrow_y - 80
        else:
            chat_box_h = 120
            box_y = arrow_y
        box_x = WIDTH - chat_margin - chat_box_w

        chat_surf = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            chat_surf,
            (30, 30, 30, 200),
            (box_x, box_y, chat_box_w, chat_box_h),
            border_radius=border_radius
        )

        # Smaller 80% transparent square on the left of the big rect (fixed position)
        small_square_size = 40
        pygame.draw.rect(
            chat_surf,
            (30, 30, 30, 204),  # 80% transparent
            (box_x - small_square_size - 5, arrow_y, small_square_size, small_square_size),
            border_radius=6
        )
        # White 80% transparent arrow in the center of the square
        triangle_size = 20
        triangle_height = triangle_size * 0.866
        square_x = box_x - small_square_size - 5
        square_y = arrow_y
        cx = square_x + small_square_size // 2
        cy = square_y + small_square_size // 2
        if chat_arrow_up:
            points = [
                (cx - triangle_size // 2, cy + triangle_height // 3),
                (cx + triangle_size // 2, cy + triangle_height // 3),
                (cx, cy - triangle_height * 2 // 3)
            ]
        else:
            points = [
                (cx - triangle_size // 2, cy - triangle_height // 3),
                (cx + triangle_size // 2, cy - triangle_height // 3),
                (cx, cy + triangle_height * 2 // 3)
            ]
        pygame.draw.polygon(chat_surf, (255, 255, 255, 204), points)

        # Vertical rectangle below the arrow square (fixed position)
        small_square_bottom = arrow_y + small_square_size
        gap = 5
        pygame.draw.rect(
            chat_surf,
            (30, 30, 30, 204),  # 80% transparent
            (box_x - small_square_size - 5, small_square_bottom + gap, small_square_size, 120 - small_square_size - gap),
            border_radius=6
        )

        # Inner rectangle near the bottom
        inner_padding = 10
        inner_height = 30
        inner_rect_x = box_x + inner_padding
        inner_rect_y = box_y + chat_box_h - inner_height - inner_padding
        inner_rect_w = chat_box_w - 2 * inner_padding

        pygame.draw.rect(
            chat_surf,
            (40, 40, 40, 180),  # Slightly lighter and more transparent
            (inner_rect_x, inner_rect_y, inner_rect_w, inner_height),
            border_radius=8
        )

        # Display chat messages above the input box
        if chat_messages:
            msg_font = pygame.font.SysFont("arial", 14, bold=True)
            line_height = 16
            # Pre-calculate wrapped lines and heights for ALL messages for pixel scrolling
            all_wrapped = []
            for username, msg, ts in chat_messages:
                is_dev = username.lower() == "devguard"
                is_king = username.startswith("King ")
                name_surf = msg_font.render(
                    f"[{username}]",
                    True,
                    (
                        (255, 0, 0)
                        if is_dev or is_king
                        else (255, 255, 0)
                    )
                )
                elapsed = format_elapsed(time.time() - ts)
                elapsed_sec = time.time() - ts
                if elapsed_sec < 300:
                    time_color = (0, 255, 0)
                elif elapsed_sec < 600:
                    time_color = (255, 255, 0)
                elif elapsed_sec < 1800:
                    time_color = (255, 0, 0)
                else:
                    time_color = (64, 64, 64)
                if is_dev:
                    time_color = (255, 0, 0)
                time_surf = msg_font.render(f" [{elapsed}]: ", True, time_color)
                prefix_w = name_surf.get_width() + time_surf.get_width()
                max_msg_width = inner_rect_w - 10 - prefix_w
                lines = wrap_text(msg_font, msg, max_msg_width)
                all_wrapped.append((username, ts, name_surf, time_surf, lines))

            if all_wrapped:
                total_msg_height = sum(len(lines) * line_height for _, _, _, _, lines in all_wrapped) + (len(all_wrapped) - 1) * 5
                visible_area_height = inner_rect_y - 5 - box_y
                chat_max_scroll = max(0, total_msg_height - visible_area_height)
                chat_scroll_target = max(0, min(chat_max_scroll, chat_scroll_target))
                chat_scroll_position += (chat_scroll_target - chat_scroll_position) * 0.1
                scroll_pix = int(chat_scroll_position)

                running_y = inner_rect_y - 5
                positions = []
                for msg_data in reversed(all_wrapped):
                    username, ts, name_surf, time_surf, lines = msg_data
                    h = len(lines) * line_height
                    running_y -= h
                    positions.append((name_surf, time_surf, lines, running_y + scroll_pix))
                    running_y -= 5
                chat_box_surf = chat_surf.subsurface(pygame.Rect(box_x, box_y, chat_box_w, chat_box_h))
                chat_box_surf.set_clip(pygame.Rect(0, 0, chat_box_w, inner_rect_y - box_y - 5))
                for name_surf, time_surf, lines, msg_y in positions:
                    chat_box_surf.blit(name_surf, (inner_rect_x + 5 - box_x, msg_y - box_y))
                    chat_box_surf.blit(time_surf, (inner_rect_x + 5 + name_surf.get_width() - box_x, msg_y - box_y))
                    msg_x = inner_rect_x + 5 + name_surf.get_width() + time_surf.get_width() - box_x
                    for j, line in enumerate(lines):
                        line_y = msg_y + j * line_height
                        line_surf = msg_font.render(
                            line,
                            True,
                            (
                                (255, 0, 0)
                                if username.lower() == "devguard"
                                else (255, 255, 255)
                            )
                        )
                        chat_box_surf.blit(
                            line_surf,
                            (msg_x, line_y - box_y)
                        )

        # Chat scrollbar (drawn after message computation so variables are available)
        if len(chat_messages) > 4 and 'total_msg_height' in locals() and 'visible_area_height' in locals() and total_msg_height > visible_area_height:
            # Use arrow_y (fixed) instead of box_y for scroll track position
            arrow_y = HEIGHT - chat_margin - 120
            small_square_bottom = arrow_y + small_square_size
            gap = 5
            vertical_rect_y = small_square_bottom + gap
            vertical_rect_h = 120 - small_square_size - gap
            thumb_padding = 2
            thumb_width = small_square_size - 12
            thumb_height = max(15, int(vertical_rect_h * visible_area_height / total_msg_height))
            usable_track = max(1, vertical_rect_h - 2 * thumb_padding - thumb_height)
            scroll_fraction = min(1.0, max(0.0, chat_scroll_position / chat_max_scroll)) if chat_max_scroll > 0 else 0
            thumb_y = vertical_rect_y + thumb_padding + int(usable_track * scroll_fraction)
            chat_scrollbar_rect = pygame.Rect(
                box_x - small_square_size - 5 + (small_square_size - thumb_width) // 2, thumb_y,
                thumb_width, thumb_height
            )
            pygame.draw.rect(
                chat_surf,
                (150, 150, 150, 180),
                chat_scrollbar_rect,
                border_radius=4
            )

        # Text in the center of the inner rectangle
        if chat_text_visible:
            font = pygame.font.SysFont("arial", 16)
            text = "Press Enter or Click on Me to Chat"
            text_surf = font.render(text, True, (200, 200, 200))  # Light gray
            # Make text 80% transparent (20% opacity)
            text_surf.set_alpha(51)
            text_rect = text_surf.get_rect()
            text_rect.center = (inner_rect_x + inner_rect_w // 2, inner_rect_y + inner_height // 2)
            chat_surf.blit(text_surf, text_rect)
        else:
            # Render typed text with white outline (per-letter, tight spacing)
            font = pygame.font.SysFont("arial", 16)
            outline_color = (255, 255, 255)
            text_color = (255, 255, 255)

            # Text wrapping parameters
            padding_x = 10
            spacing = 4
            max_width = inner_rect_w - padding_x * 2
            line_height = 15
            max_visible_lines = 1  # Show only current line

            # Split text into lines that fit the width (account for per-character spacing)
            lines = []
            current_line = ""

            for char in chat_input_text:
                test_line = current_line + char
                test_width = font.render(test_line, True, text_color).get_width() + len(test_line) * spacing

                if test_width <= max_width:
                    current_line = test_line
                else:
                    if current_line:  # Add the current line if it's not empty
                        lines.append(current_line)
                    current_line = char

            # Add the last line
            if current_line:
                lines.append(current_line)

            # Show only the last N lines so the cursor is always visible (scroll up)
            if len(lines) > max_visible_lines:
                visible_lines = lines[-max_visible_lines:]
            else:
                visible_lines = lines

            # Render visible lines, aligned to top of inner rectangle
            for line_idx, line in enumerate(visible_lines):
                line_y = inner_rect_y + 4 + line_idx * line_height
                start_x = inner_rect_x + padding_x
                char_x = start_x

                for ch in line:
                    # Get character width
                    char_w = font.render(ch, True, text_color).get_width()
                    # Render outline (2 directions, 1px offset - smaller)
                    for dx, dy in [(-1, 0), (1, 0)]:
                        outline_surf = font.render(ch, True, outline_color)
                        chat_surf.blit(outline_surf, (char_x + dx, line_y + dy))
                    # Render main text
                    text_surf = font.render(ch, True, text_color)
                    chat_surf.blit(text_surf, (char_x, line_y))
                    # Move to next letter position (tight spacing, 2px gap between outlines)
                    char_x += char_w + 4

                # Update cursor position for this line
                if line_idx == len(visible_lines) - 1:
                    cursor_x = char_x + 2
                    cursor_y = line_y
                    cursor_h = line_height - 2

            # Blinking white cursor line (in front of last letter)
            chat_cursor_frame += 1
            if chat_cursor_frame % 40 < 20:  # Blink every 20 frames
                # Only show cursor if we have at least one line or are typing
                if len(lines) > 0 or len(chat_input_text) > 0:
                    # Ensure cursor variables are set (from the rendering loop above)
                    # If no lines were rendered (empty string), position at start
                    if len(visible_lines) == 0:
                        cursor_x = inner_rect_x + padding_x + 2
                        cursor_y = inner_rect_y + 4
                        cursor_h = line_height - 2
                    pygame.draw.line(
                        chat_surf,
                        (255, 255, 255),
                        (cursor_x, cursor_y),
                        (cursor_x, cursor_y + cursor_h),
                        2
                    )

        screen.blit(chat_surf, (0, 0))

    pygame.display.flip()

save_player()

pygame.quit()
sys.exit()
