import pygame
import sys
import math
import random
import json
import os
import Main

player_accounts = {}

if os.path.exists("accounts.json"):

    with open("accounts.json", "r") as file:
        player_accounts = json.load(file)

try:

    with open("players.json", "r") as file:

        player_data = json.load(file)

except:

    player_data = {}

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
MAP_SIZE = 5000
MINIMAP_SIZE = 200
MINIMAP_MARGIN = 20

MINIMAP_SIZE = 150

MINIMAP_X = WIDTH - MINIMAP_SIZE - 65
MINIMAP_Y = 5

minimap_x = WIDTH - MINIMAP_SIZE - 10
minimap_y = HEIGHT - MINIMAP_SIZE - 10

PLAYER_SPEED = 2.5
PLAYER_RADIUS = 25

GRASS_SIZE = 64
petal_respawn_text_timer = []
WORLD_WIDTH = 5000
WORLD_HEIGHT = 5000

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
    "Bee": 0.8,
    "Spider": 1.1,
    "Rock": 1.0,
    "Hornet": 1.0,
    "BabyAnt": 0.7,
    "SoldierAnt": 1.2
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

PETAL_SLOTS = 5

petal_slots = []

# ---------------- PETAL INVENTORY ----------------

PETAL_SLOT_COUNT = 10
PETAL_SLOT_SIZE = 55
PETAL_SLOT_GAP = 5

PETAL_BAR_Y = HEIGHT - 130
# ---------------- WORLD ----------------

WORLD_SIZE = 5000

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

# ---------------- PLAYER HP ----------------

PLAYER_MAX_HP = 100
player_hp = PLAYER_MAX_HP
# ---------------- PLAYER HP UPGRADE ----------------

PLAYER_HP_LEVEL = 0

PLAYER_HP_UPGRADE_AMOUNT = 25

hp_upgrade_cost = 1


petal_cooldowns = []

for i in range(5):
    petal_cooldowns.append(0)
# ---------------- PETAL HP ----------------

PETAL_HP = {

    "Basic": 60,

    "Light": 60,

    "Stinger": 3,

    "Heavy": 400,

    "Rose": 120,

    "Wing": 90,

    "Cactus": 150,

    "Leaf": 110,

    "Pea": 70,

    "Missile": 75,

    "Bone": 130,

    "Web": 100,

    "Rock": 250,

    "Faster": 0.01,

    "Magnet": 100,

    "Bubble": 140,

    "Honey": 120,

    "Poison": 90,

    "Shark": 1,

    "Rice": 1,

    "Corn": 100,

    "Stick": 150,

    "Clover": 110,

    "Glass": 50,

    "Antenna": 1000,

    "Pollen": 0,

    "Soil": 10,

    "Ant Egg": 1,

    "Sand": 10,

    "Lentil": 1,

    "Pincer": 1,

    "Shell": 60,

    "Beetle Egg": 1,

    "Third Eye": 50,

    "Cice": 100,

    "Boubloom": 20,

    "Boulder": 50,

    "Moon": 250,

    "Grape": 70
}

PETAL_ROT_SPEED_MUL = {
    "Common": 1,
    "Unusual": 2,
    "Rare": 3,
    "Epic": 4,
    "Legendary": 5,
    "Mythic": 6,
    "Ultra": 7,
    "Super": 8,
    "Omega": 9,
    "Unique": 10,
    "Eternal": 11,
    "Cosmo": 12,
    "Jeddiful": 13,
    "Tacnic": 14,
    "Radium": 15,
    "Ancient": 16,
    "Omnient": 17,
    "Celestial": 18,
    "Infino": 19
}
PETAL_RADIUS = 12
petal_angle = 0


petal_hp = []
petal_alive = []
petal_max_hp = []

petal_respawn_timer = []

for i in range(5):
    petal_respawn_timer.append(0)
for i in range(5):
    petal_respawn_text_timer.append(0)

for i in range(5):

    if i >= len(petal_slots):
        continue

    petal_type = petal_slots[i]["petal"]

    hp = (
        PETAL_HP[petal_type]
        *
        PETAL_HP_MULTIPLIER[petal_slots[i]["rarity"]]
    )

    petal_max_hp.append(hp)
    petal_hp.append(hp)

    petal_alive.append(True)

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

    "Common": 1.0 * 1.5,
    "Unusual": 9.7 * 1.5,
    "Rare": 30.1 * 1.5,
    "Epic": 65.9 * 1.5,
    "Legendary": 102.9 * 1.5,
    "Mythic": 400.5 * 1.5,
    "Ultra": 1221.9 * 1.5,
    "Super": 3534.4 * 1.5,
    "Omega": 8435.2 * 1.5,
    "Unique": 11320.2 * 1.5,
    "Eternal": 32100.5 * 1.5,
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

    "Basic": 5* 4,
    "Light": 15* 4,
    "Stinger": 85* 4,
    "Heavy": 0.1* 4,
    "Rose": 12* 4,
    "Wing": 8* 4,
    "Cactus": 20* 4,
    "Leaf": 12* 4,
    "Pea": 18* 4,
    "Missile": 35* 4,
    "Bone": 22* 4,
    "Web": 5* 4,
    "Rock": 40* 4,
    "Faster": 7* 4,
    "Magnet": 10* 4,
    "Bubble": 14* 4,
    "Honey": 0.01* 4,
    "Poison": 16* 4,
    "Shark": 55* 4,
    "Rice": 5* 4,
    "Corn": 5* 4,
    "Stick": 25* 4,
    "Clover": 2* 4,
    "Glass": 40* 4,
    "Antenna": 1* 4,
    "Pollen": 30* 4,
    "Soil": 2* 4,
    "Ant Egg": 0.1* 4,
    "Sand": 19* 4,
    "Lentil": 0.1* 4,
    "Pincer": 1* 4,
    "Shell": 0.1* 4,
    "Beetle Egg": 0.1* 4,
    "Third Eye": 0.1* 4,
    "Cice": 5* 4,
    "Boubloom": 52* 4,
    "Boulder": 90* 4,
    "Moon": 0.01 * 4,
    "Grape": 1 * 4
}

# ---------------- PETAL RELOAD ----------------
# lower = faster

PETAL_RELOAD = {

    "Basic": 20,

    "Light": 12,

    "Stinger": 25,

    "Heavy": 15,

    "Rose": 10,

    "Wing": 15,

    "Cactus": 40,

    "Leaf": 22,

    "Pea": 18,

    "Missile": 50,

    "Bone": 30,

    "Web": 60,

    "Rock": 55,

    "Faster": 10,

    "Magnet": 25,

    "Bubble": 5,

    "Honey": 35,

    "Poison": 30,

    "Shark": 70,

    "Rice": 1,

    "Corn": 80,

    "Stick": 20,

    "Clover": 14,

    "Glass": 30,

    "Antenna": 1,

    "Pollen": 15,

    "Soil": 10,

    "Ant Egg": 150,

    "Sand": 10,

    "Lentil": 5,

    "Pincer": 10,

    "Shell": 10,
    
    "Beetle Egg": 60,

    "Third Eye": 10,

    "Cice": 7,

    "Boubloom": 25,

    "Boulder": 150,

    "Moon": 125,

    "Grape": 18
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


inventory_panel_rect = pygame.Rect(
    inventory_button_rect.centerx - 30,
    inventory_button_rect.y - 520,
    250,
    500
)

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