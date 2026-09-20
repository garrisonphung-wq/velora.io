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

for i in range(5):
    petal_cooldowns.append(0)

# Per-light cooldowns for Light petal (each light has its own cooldown)
light_cooldowns = []
for i in range(5):
    light_cooldowns.append([])

# Per-light HP for Light petal
light_hp = []
for i in range(5):
    light_hp.append([])

# Per-light alive state for Light petal
light_alive = []
for i in range(5):
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

for i in range(5):
    petal_respawn_timer.append(0)
    petal_flash_timers.append(0)
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

    if petal_type == "Light":
        light_count = get_petal_count(petal_type, petal_slots[i]["rarity"])
        if light_count > 0:
            hp /= light_count

    petal_max_hp.append(hp)
    petal_hp.append(hp)

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
# Set to True when the player clicks the green Play button
welcome_play_pressed = False
# Chat text visibility flag
chat_text_visible = True
# Chat input text
chat_input_text = ""
# Frame counter for chat cursor blinking
chat_cursor_frame = 0
# Arrow smooth rotation state (degrees, 0=up, 180=down)
chat_arrow_up = True
chat_arrow_angle = 0.0
chat_arrow_angular_vel = 0.0
chat_arrow_target = 0
# Chat message history (list of (username, message) tuples)
chat_messages = []
# Chat scroll state
chat_scroll = 0
chat_scroll_target = 0
chat_scroll_position = 0.0
chat_dragging = False
chat_drag_offset = 0
chat_scrollbar_rect = pygame.Rect(0, 0, 12, 30)

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
    "Bee",
    "Spider",
    "Rock",
    "Hornet",
    "Baby Ant",
    "Soldier Ant"
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

    new_button_panel_open = panel_name == "gallery"
    settings_panel_open = panel_name == "settings"
    craft_open = panel_name == "craft"
    inventory_open = panel_name == "inventory"
    hp_menu_open = panel_name == "hp"


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
        self.attack_cooldown = 2
        self.petal_attack_cooldown = 2   # <-- add this

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

        if self.hp <= 0:

            self.alive = False
            register_mob_kill(self)
            drop_mob_loot(self)

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    10 * MOB_XP_MULTIPLIER[self.rarity]
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

            hp_percent = self.hp / self.max_hp


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



        # red body

        pygame.draw.circle(
            body_surface,
            flash_color((220,30,30), self.flash_timer),
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

        # Dark outline around the red body.
        pygame.draw.circle(
            body_surface,
            flash_color((105, 25, 25), self.flash_timer),
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

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
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

            self.alive = False
            register_mob_kill(self)
            drop_mob_loot(self)

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    10 * MOB_XP_MULTIPLIER[self.rarity]
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



            hp_percent = self.hp / self.max_hp



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

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
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

            self.alive = False
            register_mob_kill(self)
            drop_mob_loot(self)

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    10 * MOB_XP_MULTIPLIER[self.rarity]
                )
            )

    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return

        self.timer += 1


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

            hp_percent = self.hp / self.max_hp

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

        pygame.draw.circle(
            screen,
            flash_color((18, 18, 18), self.flash_timer),
            (
                int(sx),
                int(sy)
            ),
            self.radius + 2
        )

        pygame.draw.circle(
            screen,
            flash_color((40,40,40), self.flash_timer),
            (
                int(sx),
                int(sy)
            ),
            self.radius
        )


        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
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

    def take_damage(self, amount):

        self.hp -= int(amount)
        self.flash_timer = 4

        if self.hp <= 0:

            self.alive = False
            register_mob_kill(self)
            drop_mob_loot(self)

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    10 * MOB_XP_MULTIPLIER[self.rarity]
                )
            )


    def push(self, dx, dy):

        if not self.alive:
            return

        self.x += dx
        self.y += dy


    def update(self):

        if not self.alive:
            return

        pass


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

            hp_percent = self.hp / self.max_hp

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

        rock_points = [
            (
                int(sx + point_x * self.radius),
                int(sy + point_y * self.radius)
            )
            for point_x, point_y in self.shape_points
        ]

        pygame.draw.polygon(
            screen,
            flash_color((120,120,120), self.flash_timer),
            rock_points
        )


        # rock outline

        pygame.draw.polygon(
            screen,
            flash_color((75,75,75), self.flash_timer),
            rock_points,
            max(2, int(self.radius * 0.12))
        )


        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
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


    def take_damage(self, amount):

        if not self.alive:
            return

        self.hp -= int(amount)
        self.flash_timer = 4

        if self.hp <= 0:

            self.alive = False
            register_mob_kill(self)
            drop_mob_loot(self)

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    10 * MOB_XP_MULTIPLIER[self.rarity]
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

            hp_percent = self.hp / self.max_hp


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

            self.alive = False
            register_mob_kill(self)
            drop_mob_loot(self)

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    10 * MOB_XP_MULTIPLIER[self.rarity]
                )
            )


    def update(self):

        if not self.alive:
            return

        if dead_flower_ai(self):
            return


        self.timer += 1



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

        if self.hp < self.max_hp:

            bar_width = max(1, int(30 * settings_hp_bar_scale))
            bar_height = max(
                1,
                int(5 * settings_hp_bar_scale)
            )

            hp_percent = self.hp / self.max_hp



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

        head_x = sx
        head_y = sy

        pygame.draw.circle(
            screen,
            flash_color((48, 48, 48), self.flash_timer),
            (
                int(head_x),
                int(head_y)
            ),
            int(self.radius)
        )

        # Soft gray center highlight like the reference image.
        pygame.draw.circle(
            screen,
            flash_color((78, 78, 78), self.flash_timer),
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




    def take_damage(self, amount):

        if not self.alive:
            return


        self.hp -= int(amount)


        if self.hp <= 0:

            self.alive = False
            register_mob_kill(self)
            drop_mob_loot(self)

            if self.rarity in ("Celestial", "Omnient"):

                show_defeat_message(
                    self.rarity,
                    type(self).__name__
                )

            give_xp(
                int(
                    10 * MOB_XP_MULTIPLIER[self.rarity]
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


        pygame.draw.ellipse(
            body_surface,
            flash_color((62, 62, 62), self.flash_timer),
            (
                0,
                0,
                int(body_width * 2),
                int(body_height * 2)
            )
        )
        pygame.draw.ellipse(
            body_surface,
            flash_color((22, 22, 22), self.flash_timer),
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
            flash_color((48, 48, 48), self.flash_timer),
            (
                int(head_x),
                int(head_y)
            ),
            int(head_size)
        )

        # Soft gray center highlight like the reference image.
        pygame.draw.circle(
            screen,
            flash_color((78, 78, 78), self.flash_timer),
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



        draw_clean_line(
            screen,
            flash_color((40,40,40), self.flash_timer),
            (
                mouth_start_x + side_x * (5 + right_jaw_motion),
                mouth_start_y + side_y * (5 + right_jaw_motion)
            ),
            (
                mouth_end_x + side_x * (8 + right_jaw_motion),
                mouth_end_y + side_y * (8 + right_jaw_motion)
            ),
            3
        )



        draw_clean_line(
            screen,
            flash_color((40,40,40), self.flash_timer),
            (
                mouth_start_x - side_x * (5 + left_jaw_motion),
                mouth_start_y - side_y * (5 + left_jaw_motion)
            ),
            (
                mouth_end_x - side_x * (8 + left_jaw_motion),
                mouth_end_y - side_y * (8 + left_jaw_motion)
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

            hp_percent = self.hp / self.max_hp


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

        # ---------------- RARITY TEXT ----------------

        if not getattr(self, "hide_rarity_label", False):

            draw_mob_rarity_label(
                self,
                int(sx),
                int(sy + self.radius + 15)
            )

# ----- DIF SECTION -----

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
        "flower_level": flower_level,
        "flower_xp": flower_xp,
        "upgrade_points": upgrade_points,
        "hp_level": PLAYER_HP_LEVEL,
        "hp_upgrade_cost": hp_upgrade_cost,
        "mob_gallery_unlocks": mob_gallery_unlocks

    }

    with open("players.json", "w") as file:

        json.dump(
            player_data,
            file,
            indent=4
        )

def load_player():

    global petal_slots
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

    global flower_level
    global flower_xp
    global flower_xp_needed
    global upgrade_points

    global PLAYER_HP_LEVEL
    global PLAYER_MAX_HP
    global hp_upgrade_cost
    global player_hp


    if acc_name_text not in player_data:
        # The account can exist in accounts.json without a saved player
        # record yet.  Initialize its normal five-slot starting loadout.
        create_account()
        return


    data = player_data[acc_name_text]


    # ---------------- PETALS ----------------

    # Older saves may contain fewer than PETAL_SLOTS entries.  Keep the
    # runtime arrays the same length as the game expects.
    saved_petals = data.get("petals", [])
    petal_slots = list(saved_petals[:PETAL_SLOTS])
    while len(petal_slots) < PETAL_SLOTS:
        petal_slots.append({
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

    for i in range(5):

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
        "Soldier Ant": (SoldierAnt, soldier_ants)
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

    enemy.x = player_x + random.randint(-300, 300)
    enemy.y = player_y + random.randint(-300, 300)

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
    if mob_name == "BabyAnt":
        mob_name = "Baby Ant"
    elif mob_name == "SoldierAnt":
        mob_name = "Soldier Ant"

    key = f"{mob_name}|{enemy.rarity}"
    previous_count = int(mob_gallery_unlocks.get(key, 0))
    mob_gallery_unlocks[key] = previous_count + 1

    # Save a newly discovered entry immediately; repeat kills remain cheap
    # and are saved by the normal player-save flow.
    if previous_count == 0:
        save_player()

def spawn_pickup(x, y, petal, rarity):

    PICKUP_LIST.append(
        {
            "x": x,
            "y": y,
            "petal": petal,
            "rarity": rarity,
            "timer": PICKUP_LIFETIME
        }
    )

def drop_mob_loot(enemy):

    mob_name = type(enemy).__name__
    if mob_name == "BabyAnt":
        mob_name = "Baby Ant"
    elif mob_name == "SoldierAnt":
        mob_name = "Soldier Ant"

    drop_table = MOB_DROP_INFO.get((mob_name, enemy.rarity))
    if not drop_table:
        return

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

            if chosen_chance < 5:
                # Rare drop: single roll
                if random.random() * 100 < chosen_chance:
                    drops.append((petal, chosen_rarity))
            else:
                # Normal drop: retry up to 10 times
                for _ in range(10):
                    if random.random() * 100 < chosen_chance:
                        drops.append((petal, chosen_rarity))
                        break
    else:
        # For Common mobs, single roll per row (or none)
        for petal, petal_rarity, drop_chance in drop_table:
            if random.random() * 100 < drop_chance:
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
    "Bee": 9,
    "Spider": 11,
    "Rock": 11,
    "Hornet": 11,
    "Baby Ant": 8,
    "Soldier Ant": 10
}

# Short lore text shown in the gallery hover rectangle.
GALLERY_MOB_DESCRIPTIONS = {
    "Ladybug": (
        "A calm red circle thing that wanders the grass. It never "
        "starts fights, but it will bite back when bothered."
    ),
    "Bee": (
        "A striped pollen lover that flies in soft waves. Bees "
        "run from trouble, yet an angry one chases fast."
    ),
    "Spider": (
        "A dark eight legged hunter. It hides quietly until prey "
        "comes near, then lunges with surprising speed."
    ),
    "Rock": (
        "A silent gray boulder. It cannot move or attack, but "
        "cracking one open takes many patient hits."
    ),
    "Hornet": (
        "An angry wild cousin of the bee. Hornets guard their "
        "zone and dive at any flower that comes close."
    ),
    "Baby Ant": (
        "A tiny ant that is mostly head and hunger. It scurries "
        "nonstop and can barely defend itself."
    ),
    "Soldier Ant": (
        "The nest guardian. Heavy jaws and fast legs make this "
        "armored ant a real threat up close."
    )
}

# Petal drop tables.  Each (mob name, mob rarity) entry lists possible
# drops as (petal name, petal rarity, chance percentage).  Every entry
# is rolled independently when the mob dies, so a kill can give several
# petals or nothing at all.
MOB_DROP_INFO = {
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
        "Bee": Bee,
        "Spider": Spider,
        "Rock": Rock,
        "Hornet": Hornet,
        "Baby Ant": BabyAnt,
        "Soldier Ant": SoldierAnt
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
                "wing_phase"
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
        bees +
        spiders +
        rocks +
        hornets +
        baby_ants +
        soldier_ants
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

    # baby ants do not play with the dead flower
    if enemy.__class__.__name__ == "BabyAnt":
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
bees = []
spiders = []
rocks = []
hornets = []
baby_ants = []
soldier_ants = []

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
        + bees
        + spiders
        + rocks
        + hornets
        + baby_ants
        + soldier_ants
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
                chat_box_h = 120
                chat_margin = 20
                inner_padding = 10
                inner_height = 30
                chat_box_x = WIDTH - chat_margin - chat_box_w
                chat_box_y = HEIGHT - chat_margin - chat_box_h
                inner_rect_x = chat_box_x + inner_padding
                inner_rect_y = chat_box_y + chat_box_h - inner_height - inner_padding
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
                square_y = chat_box_y
                square_rect = pygame.Rect(square_x, square_y, small_square_size, small_square_size)
                if square_rect.collidepoint(mouse_x, mouse_y):
                    if chat_arrow_target == 0:
                        chat_arrow_target = 180
                    else:
                        chat_arrow_target = 0

                # Arrow smooth rotation with spring-damper acceleration (per-frame)
                arrow_diff = chat_arrow_target - chat_arrow_angle
                while arrow_diff > 180:
                    arrow_diff -= 360
                while arrow_diff < -180:
                    arrow_diff += 360
                chat_arrow_angular_vel = (chat_arrow_angular_vel + arrow_diff * 0.15) * 0.85
                chat_arrow_angle += chat_arrow_angular_vel
                if abs(chat_arrow_angle - chat_arrow_target) < 0.5:
                    chat_arrow_angle = float(chat_arrow_target)
                    chat_arrow_angular_vel = 0.0

                # Chat scrollbar drag handling
                if len(chat_messages) > 4:
                    vertical_rect_x = chat_box_x - small_square_size - 5
                    vertical_rect_y = chat_box_y + small_square_size + 5
                    vertical_rect = pygame.Rect(
                        vertical_rect_x, vertical_rect_y, small_square_size, chat_box_h - small_square_size - 5
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

                    if (
                        acc_name_text == "DevGuard"
                        and not player_data.get(
                            acc_name_text,
                            {}
                        ).get("inventory")
                    ):

                        inventory = []

                        flower_level = 250
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
                            chat_messages.append((acc_name_text, chat_input_text, time.time()))
                        chat_input_text = ""
                        chat_text_visible = True
                elif event.key == pygame.K_BACKSPACE and not chat_text_visible:
                    chat_input_text = chat_input_text[:-1]
                elif event.unicode and not chat_text_visible:
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

                                enemy.alive = False

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
            if not craft_open:
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
            if len(chat_messages) > 4:
                chat_box_w = 260
                chat_box_h = 120
                chat_margin = 20
                small_square_size = 40
                gap = 5
                chat_box_x = WIDTH - chat_margin - chat_box_w
                chat_box_y = HEIGHT - chat_margin - chat_box_h
                inner_padding = 10
                inner_height = 30
                line_height = 16
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

        # advance the scrolling green grid (right and a little down)
        welcome_scroll_x += 1.5
        welcome_scroll_y += 0.35

        screen.fill((80, 200, 90))

        # draw the grid tiles with the same size as the real in-game grass,
        # shifted by the scroll offset so they move right and a little down,
        # and clipped to the screen
        gsize = GRASS_SIZE

        off_x = welcome_scroll_x % gsize
        off_y = welcome_scroll_y % gsize

        for gx in range(-1, WIDTH // gsize + 2):
            for gy in range(-1, HEIGHT // gsize + 2):

                x = int(gx * gsize - off_x)
                y = int(gy * gsize - off_y)

                pygame.draw.rect(
                    screen,
                    (80, 200, 90),
                    (x, y, gsize, gsize)
                )
                pygame.draw.rect(
                    screen,
                    (70, 180, 80),
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
                    else:
                        welcome_selected_biome = biome_name

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

                        if petal_slots[i]["petal"] == "Rose":

                            player_hp += 10

                            if player_hp > PLAYER_MAX_HP:
                                player_hp = PLAYER_MAX_HP

                            rose_heal_timer = 60  # 1 second
                            break

        leaf_heal_timer -= 1

        if leaf_heal_timer <= 0:

            for i in range(PETAL_SLOTS):

                if petal_alive[i]:

                    if petal_slots[i]["petal"] == "Leaf":

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
        if keys[pygame.K_SPACE]:
            spawn_random_mob()

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
                    soldier_ants
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

            player_x += move_x * PLAYER_SPEED
            player_y += move_y * PLAYER_SPEED

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

            if petal_slots[i]["petal"] == "Faster":

                rarity = petal_slots[i]["rarity"]

                spin_amount = PETAL_ROT_SPEED_MUL.get(
                    rarity,
                    1
                )

                spin_speed += spin_amount

        petal_angle += spin_speed
        petal_self_spin_angle += 0.45

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

            if player_spawn_cooldown <= 0:
                ladybug.update()

            if ladybug.attack_cooldown > 0:
                ladybug.attack_cooldown -= 1

            if ladybug.petal_attack_cooldown > 0:
                ladybug.petal_attack_cooldown -= 1

            if ladybug.flash_timer > 0:
                ladybug.flash_timer -= 1


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

            if player_spawn_cooldown <= 0:
                bee.update()

            if bee.attack_cooldown > 0:
                bee.attack_cooldown -= 1

            if bee.petal_attack_cooldown > 0:
                bee.petal_attack_cooldown -= 1

            if bee.flash_timer > 0:
                bee.flash_timer -= 1


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

            if player_spawn_cooldown <= 0:
                spider.update()

            if spider.attack_cooldown > 0:
                spider.attack_cooldown -= 1

            if spider.petal_attack_cooldown > 0:
                spider.petal_attack_cooldown -= 1

            if spider.flash_timer > 0:
                spider.flash_timer -= 1


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

            if player_spawn_cooldown <= 0:
                rock.update()

            if rock.attack_cooldown > 0:
                rock.attack_cooldown -= 1

            if rock.petal_attack_cooldown > 0:
                rock.petal_attack_cooldown -= 1

            if rock.flash_timer > 0:
                rock.flash_timer -= 1


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

            if player_spawn_cooldown <= 0:
                hornet.update()

            if hornet.attack_cooldown > 0:
                hornet.attack_cooldown -= 1

            if hornet.petal_attack_cooldown > 0:
                hornet.petal_attack_cooldown -= 1

            if hornet.flash_timer > 0:
                hornet.flash_timer -= 1

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

            if player_spawn_cooldown <= 0:
                ant.update()

            if ant.attack_cooldown > 0:
                ant.attack_cooldown -= 1

            if ant.petal_attack_cooldown > 0:
                ant.petal_attack_cooldown -= 1

            if ant.flash_timer > 0:
                ant.flash_timer -= 1

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

            if player_spawn_cooldown <= 0:
                soldier_ant.update()

            if soldier_ant.attack_cooldown > 0:
                soldier_ant.attack_cooldown -= 1

            if soldier_ant.petal_attack_cooldown > 0:
                soldier_ant.petal_attack_cooldown -= 1

            if soldier_ant.flash_timer > 0:
                soldier_ant.flash_timer -= 1

        update_boss_hp()
        # ---------------- PETAL RESPAWN ----------------

        for i in range(PETAL_SLOTS):

            if not petal_alive[i] and not player_dead:

                if petal_respawn_timer[i] > 0:

                    petal_respawn_timer[i] -= 1

                else:

                    petal_alive[i] = True
                    petal_hp[i] = petal_max_hp[i]

                    if petal_slots[i]["petal"] == "Light":
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

                if petal_slots[i]["petal"] == "Light":
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

                        if ladybug.attack_cooldown == 0:

                            player_hp -= (
                                ladybug.damage *
                                MOB_DAMAGE_MULTIPLIER[ladybug.rarity]
                            )

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

                        if bee.attack_cooldown == 0:

                            player_hp -= (
                                bee.damage *
                                MOB_DAMAGE_MULTIPLIER[bee.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(bee)

                            if player_hp == 0:
                                kill_player(bee)

                            bee.attack_cooldown = 2




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

                        if spider.attack_cooldown == 0:

                            player_hp -= (
                                spider.damage *
                                MOB_DAMAGE_MULTIPLIER[spider.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(spider)

                            if player_hp == 0:
                                kill_player(spider)

                            spider.attack_cooldown = 2




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

                        if rock.attack_cooldown == 0:

                            player_hp -= (
                                rock.damage *
                                MOB_DAMAGE_MULTIPLIER[rock.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(rock)

                            if player_hp == 0:
                                kill_player(rock)

                            rock.attack_cooldown = 2




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

                        if hornet.attack_cooldown == 0:

                            player_hp -= (
                                hornet.damage *
                                MOB_DAMAGE_MULTIPLIER[hornet.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(hornet)

                            if player_hp == 0:
                                kill_player(hornet)

                            hornet.attack_cooldown = 2


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

                        if ant.attack_cooldown == 0:

                            player_hp -= (
                                ant.damage *
                                MOB_DAMAGE_MULTIPLIER[ant.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(ant)

                            if player_hp == 0:
                                kill_player(ant)

                            ant.attack_cooldown = 2


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

                        if soldier_ant.attack_cooldown == 0:

                            player_hp -= (
                                soldier_ant.damage *
                                MOB_DAMAGE_MULTIPLIER[soldier_ant.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            player_flash_timer = 4

                            push_player_from(soldier_ant)

                            if player_hp == 0:
                                kill_player(soldier_ant)

                            soldier_ant.attack_cooldown = 2

        # -------- DRAW --------

        screen.fill((60, 180, 75))

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

                color = (80, 200, 90)

                pygame.draw.rect(
                    screen,
                    color,
                    (screen_x, screen_y, GRASS_SIZE, GRASS_SIZE)
                )

                pygame.draw.rect(
                    screen,
                    (70, 180, 80),
                    (screen_x, screen_y, GRASS_SIZE, GRASS_SIZE),
                    1
                )

        for ladybug in ladybugs:
            ladybug.draw()

        for bee in bees:
            bee.draw()

        for spider in spiders:
            spider.draw()

        for rock in rocks:
            rock.draw()

        for hornet in hornets:
            hornet.draw()

        for ant in baby_ants:
            ant.draw()

        for soldier_ant in soldier_ants:

            soldier_ant.draw()

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

            # Draw petals

        # ---------------- DRAW PETAL SLOTS ----------------

        slots_per_row = 5

        total_width = (
            slots_per_row * PETAL_SLOT_SIZE +
            (slots_per_row - 1) * PETAL_SLOT_GAP
        )

        start_x = WIDTH // 2 - total_width // 2


        for i in range(PETAL_SLOT_COUNT):

            row = i // 5
            col = i % 5

            if row < 0 or row >= 5:
                continue

            x = start_x + col * (PETAL_SLOT_SIZE + PETAL_SLOT_GAP)

            y = PETAL_BAR_Y + row * (PETAL_SLOT_SIZE + PETAL_SLOT_GAP)


            # Slot color

            slot_color = (90,90,90)
            border_color = (160,160,160)

            if i < PETAL_SLOTS and petal_slots[i]["filled"]:

                if petal_slots[i]["rarity"] in RARITY_COLORS:

                    slot_color = RARITY_COLORS[
                        petal_slots[i]["rarity"]
                    ]

                border_color = (
                    max(slot_color[0] - 40, 0),
                    max(slot_color[1] - 40, 0),
                    max(slot_color[2] - 40, 0)
                )

            if i < PETAL_SLOTS and petal_slots[i]["filled"]:

                draw_rarity_slot(
                    x,
                    y,
                    PETAL_SLOT_SIZE,
                    petal_slots[i]["rarity"]
                )

            else:

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

            # ---------------- HP UPGRADE BUTTON --------------

            # Draw equipped basic petal

            if i < PETAL_SLOTS:

                if petal_slots[i]["filled"]:

                    slot_sprite = make_petal_surface(
                        petal_slots[i]["petal"],
                        0,
                        0,
                        petal_slots[i]["rarity"],
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
                        + math.cos(angle) * petal_distance
                    )
                    y = (
                        HEIGHT // 2
                        + math.sin(angle) * petal_distance
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
                    * (petal_distance + moon_extra_orbit)
                )
                y = (
                    HEIGHT // 2
                    + math.sin(angle)
                    * (petal_distance + moon_extra_orbit)
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

            petal_world_x = player_x + math.cos(angle) * petal_distance
            petal_world_y = player_y + math.sin(angle) * petal_distance

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
                    * (
                        petal_distance
                        + (40 if petal_slots[i]["petal"] == "Moon" else 0)
                    )
                )
                petal_world_y = (
                    player_y
                    + math.sin(angle)
                    * (
                        petal_distance
                        + (40 if petal_slots[i]["petal"] == "Moon" else 0)
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
                        bees +
                        spiders +
                        rocks +
                        hornets +
                        baby_ants +
                        soldier_ants
                    )

                    hit = False

                    for li in range(light_count):
                        # Handle cooldown and respawn
                        if light_cooldowns[i][li] > 0:
                            light_cooldowns[i][li] -= 1
                            if light_cooldowns[i][li] <= 0:
                                light_alive[i][li] = True
                                light_hp[i][li] = petal_max_hp[i]

                        if not light_alive[i][li]:
                            continue

                        # Calculate light position
                        light_angle = petal_angle + element_index * angle_increment
                        light_x = player_x + math.cos(math.radians(light_angle)) * petal_distance
                        light_y = player_y + math.sin(math.radians(light_angle)) * petal_distance

                        if light_cooldowns[i][li] == 0:
                            for enemy in all_enemies:
                                if not enemy.alive:
                                    continue

                                d = distance(light_x, light_y, enemy.x, enemy.y)

                                if d < petal_range + enemy.radius:
                                    if enemy.attack_cooldown == 0:
                                        light_hp[i][li] -= enemy.damage
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
                            bees +
                            spiders +
                            rocks +
                            hornets +
                            baby_ants +
                            soldier_ants
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

                                    petal_hp[i] -= enemy.damage
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
                                            MOB_WEIGHT[type(enemy).__name__] *
                                            MOB_WEIGHT_MULTIPLIER[enemy.rarity]
                                        )

                                        enemy.knockback_x += dx * knockback / weight
                                        enemy.knockback_y += dy * knockback / weight

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
                            hp_percent = light_hp[i][li] / petal_max_hp[i]
                            bar_orbit = petal_distance
                            bar_petal_r = PETAL_RADIUS
                            if petal_slots[i]["petal"] == "Moon":
                                bar_orbit += 40
                                bar_petal_r = int(PETAL_RADIUS * 4)
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

                if petal_hp[i] < petal_max_hp[i]:

                    bar_width = 35
                    bar_height = 5

                    hp_percent = (
                        petal_hp[i] /
                        petal_max_hp[i]
                    )

                    bar_orbit = petal_distance
                    bar_petal_r = PETAL_RADIUS

                    if petal_slots[i]["petal"] == "Moon":
                        bar_orbit += 40
                        bar_petal_r = int(PETAL_RADIUS * 4)

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

                if boss_hp > 0:

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

                    hp_percent = boss_hp / boss_max_hp


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
            + bees
            + spiders
            + rocks
            + hornets
            + baby_ants
            + soldier_ants
        )

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
                * (petal_distance + 40)
            )
            moon_y = (
                player_y
                + math.sin(moon_angle)
                * (petal_distance + 40)
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

        pygame.draw.circle(
            screen,
            (225,225,0),
            (player_center_x, player_center_y),
            PLAYER_RADIUS
        )


        # outline

        pygame.draw.circle(
            screen,
            (230,200,40),
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
                            player_center_x + math.cos(angle) * petal_distance
                        )
                        l_y = int(
                            player_center_y + math.sin(angle) * petal_distance
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
                        * (petal_distance + moon_extra_orbit)
                    )
                    hp_y = int(
                        player_center_y
                        + math.sin(angle)
                        * (petal_distance + moon_extra_orbit)
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
                bees,
                spiders,
                rocks,
                hornets,
                baby_ants,
                soldier_ants,
            ]
            for enemy_list in all_enemy_lists:
                for enemy in enemy_list:
                    if not enemy.alive:
                        continue
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
                    (0, 0, 0),
                    (int(ex - half), int(ey - half)),
                    (int(ex + half), int(ey + half)),
                    3
                )
                pygame.draw.line(
                    face_surf,
                    (0, 0, 0),
                    (int(ex - half), int(ey + half)),
                    (int(ex + half), int(ey - half)),
                    3
                )

        else:

            pygame.draw.ellipse(
                face_surf,
                (0, 0, 0),
                (fc - 11, fc - 10, 8, 12)
            )

            pygame.draw.ellipse(
                face_surf,
                (0, 0, 0),
                (fc + 3, fc - 10, 8, 12)
            )

        # mouth
        if player_dead:

            # sad mouth when dead
            pygame.draw.arc(
                face_surf,
                (0, 0, 0),
                (fc - 9, fc + 7, 18, 16),
                math.radians(20),
                math.radians(160),
                2
            )

        else:

            if petal_target == PETAL_NORMAL:

                pygame.draw.arc(
                    face_surf,
                    (0, 0, 0),
                    (fc - 9, fc - 1, 18, 16),
                    math.radians(200),
                    math.radians(340),
                    2
                )

            elif petal_face_target == PETAL_ATTACK:

                # attack angry face: eye cut-outs + frown
                pygame.draw.polygon(
                    face_surf,
                    (225, 225, 0),
                    [
                        (fc - 12, fc - 12),
                        (fc - 4, fc - 8),
                        (fc - 4, fc - 16),
                        (fc - 12, fc - 16)
                    ]
                )

                pygame.draw.polygon(
                    face_surf,
                    (225, 225, 0),
                    [
                        (fc + 4, fc - 8),
                        (fc + 12, fc - 12),
                        (fc + 12, fc - 16),
                        (fc + 4, fc - 16)
                    ]
                )

                pygame.draw.arc(
                    face_surf,
                    (0, 0, 0),
                    (fc - 9, fc + 7, 18, 16),
                    math.radians(20),
                    math.radians(160),
                    2
                )

            elif petal_target == PETAL_DEFEND:

                pygame.draw.arc(
                    face_surf,
                    (0, 0, 0),
                    (fc - 9, fc + 7, 18, 16),
                    math.radians(20),
                    math.radians(160),
                    2
                )

        if player_rot_angle != 0:
            face_surf = pygame.transform.rotate(face_surf, -player_rot_angle)

        screen.blit(
            face_surf,
            face_surf.get_rect(center=(int(player_center_x), int(player_center_y)))
        )

        # Show the flower's name / XP / level / points only when alive.
        if not player_dead:

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
            # shifted down so the real (world) flower behind the overlay
            # stays visible above and is not covered by this picture
            fcy = HEIGHT // 2 + 100

            # flower body + outline
            pygame.draw.circle(
                screen,
                (225, 225, 0),
                (fcx, fcy),
                PLAYER_RADIUS
            )
            pygame.draw.circle(
                screen,
                (230, 200, 40),
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
                    (0, 0, 0),
                    (int(ex - half), int(ey - half)),
                    (int(ex + half), int(ey + half)),
                    3
                )
                pygame.draw.line(
                    face_surf,
                    (0, 0, 0),
                    (int(ex - half), int(ey + half)),
                    (int(ex + half), int(ey - half)),
                    3
                )

            pygame.draw.arc(
                face_surf,
                (0, 0, 0),
                (fc - 9, fc + 7, 18, 16),
                math.radians(20),
                math.radians(160),
                2
            )
            screen.blit(
                face_surf,
                face_surf.get_rect(center=(fcx, fcy))
            )

            # equipped petals in a fixed ring around the flower (no spin)
            saved_petal_angle = petal_angle
            try:
                for i in range(PETAL_SLOTS):

                    if not petal_slots[i]["filled"]:
                        continue

                    ring_pos = i * (360 / PETAL_SLOTS)
                    angle = math.radians(ring_pos - 90)

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
        chat_box_h = 120
        chat_margin = 20
        border_radius = 12

        box_x = WIDTH - chat_margin - chat_box_w
        box_y = HEIGHT - chat_margin - chat_box_h

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

        # Smaller 80% transparent square on the left of the big rect
        small_square_size = 40
        pygame.draw.rect(
            chat_surf,
            (30, 30, 30, 204),  # 80% transparent
            (box_x - small_square_size - 5, box_y, small_square_size, small_square_size),
            border_radius=6
        )
# Smoothly rotating arrow in the center of the square
        triangle_size = 20
        triangle_height = triangle_size * 0.866
        square_x = box_x - small_square_size - 5
        square_y = box_y
        cx = square_x + small_square_size // 2
        cy = square_y + small_square_size // 2
        angle_rad = math.radians(chat_arrow_angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        half_w = triangle_size / 2
        base_pts = [
            (-half_w, triangle_height / 3),
            (half_w, triangle_height / 3),
            (0, -triangle_height * 2 / 3),
        ]
        points = [(cx + x * cos_a - y * sin_a, cy + x * sin_a + y * cos_a) for x, y in base_pts]
        pygame.draw.polygon(chat_surf, (255, 255, 255, 204), points)

        # Vertical rectangle below the arrow square
        small_square_bottom = box_y + small_square_size
        gap = 5
        pygame.draw.rect(
            chat_surf,
            (30, 30, 30, 204),  # 80% transparent
            (box_x - small_square_size - 5, small_square_bottom + gap, small_square_size, chat_box_h - small_square_size - gap),
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
                name_surf = msg_font.render(f"[{username}]", True, (255, 255, 0))
                elapsed = format_elapsed(time.time() - ts)
                elapsed_sec = time.time() - ts
                if elapsed_sec < 300:
                    time_color = (0, 255, 0)
                elif elapsed_sec < 600:
                    time_color = (255, 255, 0)
                else:
                    time_color = (255, 0, 0)
                time_surf = msg_font.render(f" [{elapsed}]: ", True, time_color)
                prefix_w = name_surf.get_width() + time_surf.get_width()
                max_msg_width = inner_rect_w - 10 - prefix_w
                lines = wrap_text(msg_font, msg, max_msg_width)
                all_wrapped.append((name_surf, time_surf, lines))

            if all_wrapped:
                total_msg_height = sum(len(lines) * line_height for _, _, lines in all_wrapped) + (len(all_wrapped) - 1) * 5
                visible_area_height = inner_rect_y - 5 - box_y
                chat_max_scroll = max(0, total_msg_height - visible_area_height)
                chat_scroll_target = max(0, min(chat_max_scroll, chat_scroll_target))
                chat_scroll_position += (chat_scroll_target - chat_scroll_position) * 0.1
                scroll_pix = int(chat_scroll_position)

                running_y = inner_rect_y - 5
                positions = []
                for msg_data in reversed(all_wrapped):
                    name_surf, time_surf, lines = msg_data
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
                        line_surf = msg_font.render(line, True, (255, 255, 255))
                        chat_box_surf.blit(
                            line_surf,
                            (msg_x, line_y - box_y)
                        )

        # Chat scrollbar (drawn after message computation so variables are available)
        if len(chat_messages) > 4 and 'total_msg_height' in locals() and 'visible_area_height' in locals() and total_msg_height > visible_area_height:
            vertical_rect_y = small_square_bottom + gap
            vertical_rect_h = chat_box_h - small_square_size - gap
            thumb_height = max(20, int(vertical_rect_h * visible_area_height / total_msg_height))
            usable_track = max(1, vertical_rect_h - thumb_height)
            scroll_fraction = chat_scroll_position / chat_max_scroll if chat_max_scroll > 0 else 0
            thumb_y = vertical_rect_y + int(usable_track * scroll_fraction)
            chat_scrollbar_rect = pygame.Rect(
                box_x - small_square_size - 5 + 2, thumb_y,
                small_square_size - 4, thumb_height
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
