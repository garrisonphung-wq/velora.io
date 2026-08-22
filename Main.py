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

class Wall:

    def __init__(self, x, y, width, height):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

    def draw(self):

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
        self.radius = random.randint(20, 35)
        self.attack_cooldown = 0
        self.petal_attack_cooldown = 0   # <-- add this

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
                3
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

        if self.hp <= 0:

            self.alive = False

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

            bar_width = 40
            bar_height = 5

            hp_percent = self.hp / self.max_hp


            pygame.draw.rect(
                screen,
                (80,80,80),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 15),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 15),
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
            (220,30,30),
            center,
            int(self.radius)
        )



        # black spots

        for spot in self.spots:

            pygame.draw.circle(
                body_surface,
                (0,0,0),
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
            (0,0,0),
            (
                int(head_x),
                int(head_y)
            ),
            int(self.radius * 0.45)
        )

        # ---------------- RARITY TEXT ----------------

        font = pygame.font.SysFont(
            None,
            18
        )


        rarity_color = RARITY_COLORS.get(
            self.rarity,
            (255,255,255)
        )


        rarity_text = font.render(
            self.rarity,
            True,
            rarity_color
        )


        text_rect = rarity_text.get_rect(
            center=(
                int(sx),
                int(sy + self.radius + 15)
            )
        )


        screen.blit(
            rarity_text,
            text_rect
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
        self.attack_cooldown = 0
        self.petal_attack_cooldown = 0   # <-- add this
        self.flee = False

        # movement speed
        # smaller bee = faster
        # bigger bee = slower

        self.speed = 2.5

        self.max_speed = 2.5

        if self.max_speed < 0.35:
            self.max_speed = 0.35

        self.acceleration = 0.015

        # direction

        self.base_angle = random.uniform(0,360)
        self.angle = self.base_angle

        # wave movement

        self.wave_offset = random.random() * 100
        self.time = random.random() * 100
        self.player_is_animal = False

        # random direction changing

        self.direction_timer = random.randint(300,600)

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

    def take_damage(self, amount):

        if not self.alive:
            return

        self.angry = True
        self.hp -= int(amount)

        if self.hp <= 0:

            self.alive = False

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

    def decide_player(self):

        player_is_animal = False


        if player_is_animal:

            self.flee = True

        else:

            self.flee = False


    def update(self):

        if not self.alive:
            return


        self.time += 1


        # ---------------- CHECK PLAYER ----------------

        # ---------------- CHECK PLAYER ----------------

        distance_to_player = math.sqrt(
            (player_x - self.x) ** 2 +
            (player_y - self.y) ** 2
        )


        if distance_to_player <= self.view_range:

            self.decide_player()


        self.flee = False


        if distance_to_player <= self.view_range:


            # ---------------- CHECK WHAT PLAYER IS ----------------

            player_is_animal = True


            if player_is_animal:

                self.flee = True



        # ---------------- FLEE ----------------

        if self.flee:


            flee_angle = math.degrees(
                math.atan2(
                    self.y - player_y,
                    self.x - player_x
                )
            )


            self.turn_to(
                flee_angle,
                2
            )



        # ---------------- ANGRY ----------------

        elif self.angry:


            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )


            self.turn_to(
                target_angle,
                2
            )



        # ---------------- NORMAL WANDER ----------------

        else:


            if self.time >= 120:

                self.base_angle = random.uniform(
                    0,
                    360
                )

                self.time = 0



            self.turn_to(
                self.base_angle,
                1
            )



        # ---------------- MOVE ----------------

        rad = math.radians(
            self.angle
        )


        dx = math.cos(rad) * self.speed

        dy = math.sin(rad) * self.speed



        # flying movement

        dy += math.sin(
            pygame.time.get_ticks() / 300 + self.wave
        ) * 0.3



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

            bar_width = 35
            bar_height = 5

            hp_percent = self.hp / self.max_hp


            pygame.draw.rect(
                screen,
                (80,80,80),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 15),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 15),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )



        # ---------------- BODY ----------------

        angle = math.radians(
            self.angle
        )


        fx = math.cos(angle)
        fy = math.sin(angle)

        side_x = -fy
        side_y = fx



        length = self.radius * 3

        width = self.radius * 1.5



        bee = pygame.Surface(
            (
                int(length * 2),
                int(width * 2)
            ),
            pygame.SRCALPHA
        )


        cx = bee.get_width() // 2
        cy = bee.get_height() // 2



        # yellow body

        pygame.draw.ellipse(
            bee,
            (255,220,0),
            (
                cx - length/2,
                cy - width/2,
                length,
                width
            )
        )



        # black stripes

        for offset in [-0.35, 0, 0.35]:

            pygame.draw.line(
                bee,
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



        bee = pygame.transform.rotate(
            bee,
            -self.angle
        )


        rect = bee.get_rect(
            center=(int(sx), int(sy))
        )


        screen.blit(
            bee,
            rect
        )



        # ---------------- WINGS ----------------

        wing_offset = self.radius * 0.8


        for side in [-1, 1]:

            wing_x = (
                sx +
                side_x * side * wing_offset
            )

            wing_y = (
                sy +
                side_y * side * wing_offset
            )


            pygame.draw.ellipse(
                screen,
                (220,220,255),
                (
                    int(wing_x - self.radius),
                    int(wing_y - self.radius * 0.5),
                    int(self.radius * 2),
                    int(self.radius)
                )
            )

        # ---------------- RARITY TEXT ----------------

        font = pygame.font.SysFont(
            None,
            18
        )


        rarity_color = RARITY_COLORS.get(
            self.rarity,
            (255,255,255)
        )


        rarity_text = font.render(
            self.rarity,
            True,
            rarity_color
        )


        text_rect = rarity_text.get_rect(
            center=(
                int(sx),
                int(sy + self.radius + 15)
            )
        )


        screen.blit(
            rarity_text,
            text_rect
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
        self.attack_cooldown = 0
        self.petal_attack_cooldown = 0   # <-- add this
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

        if self.hp <= 0:

            self.alive = False

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


        self.timer += 1


        # ---------------- CHECK PLAYER DISTANCE ----------------

        distance = math.sqrt(
            (player_x - self.x) ** 2 +
            (player_y - self.y) ** 2
        )


        # ---------------- CHASE PLAYER ----------------

        if distance <= self.view_range:


            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )


            self.turn_to(
                target_angle,
                2
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

            bar_width = 40
            bar_height = 5

            hp_percent = self.hp / self.max_hp

            pygame.draw.rect(
                screen,
                (80,80,80),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 15),
                    bar_width,
                    bar_height
                )
            )

            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 15),
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



                pygame.draw.line(
                    screen,
                    (20,20,20),
                    (
                        int(start_x),
                        int(start_y)
                    ),
                    (
                        int(end_x),
                        int(end_y)
                    ),
                    4
                )



        # ---------------- BODY ----------------

        pygame.draw.circle(
            screen,
            (40,40,40),
            (
                int(sx),
                int(sy)
            ),
            self.radius
        )


        # ---------------- RARITY TEXT ----------------

        font = pygame.font.SysFont(
            None,
            18
        )


        rarity_color = RARITY_COLORS.get(
            self.rarity,
            (255,255,255)
        )


        rarity_text = font.render(
            self.rarity,
            True,
            rarity_color
        )


        text_rect = rarity_text.get_rect(
            center=(
                int(sx),
                int(sy + self.radius + 15)
            )
        )


        screen.blit(
            rarity_text,
            text_rect
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
        self.attack_cooldown = 0
        self.petal_attack_cooldown = 0   # <-- add this

        # random size
        self.radius = int(self.max_hp / 4)


    def take_damage(self, amount):

        self.hp -= int(amount)

        if self.hp <= 0:

            self.alive = False

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

            bar_width = 50
            bar_height = 6

            hp_percent = self.hp / self.max_hp

            pygame.draw.rect(
                screen,
                (80,80,80),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 16),
                    bar_width,
                    bar_height
                )
            )

            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 16),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )


        # shadow

        pygame.draw.circle(
            screen,
            (70,70,70),
            (
                int(sx + 5),
                int(sy + 5)
            ),
            self.radius
        )


        # rock body

        pygame.draw.circle(
            screen,
            (120,120,120),
            (
                int(sx),
                int(sy)
            ),
            self.radius
        )


        # rock details

        pygame.draw.circle(
            screen,
            (90,90,90),
            (
                int(sx - self.radius * 0.3),
                int(sy - self.radius * 0.2)
            ),
            int(self.radius * 0.25)
        )

        pygame.draw.circle(
            screen,
            (150,150,150),
            (
                int(sx + self.radius * 0.35),
                int(sy + self.radius * 0.25)
            ),
            int(self.radius * 0.2)
        )


        # ---------------- RARITY TEXT ----------------

        font = pygame.font.SysFont(
            None,
            18
        )


        rarity_color = RARITY_COLORS.get(
            self.rarity,
            (255,255,255)
        )


        rarity_text = font.render(
            self.rarity,
            True,
            rarity_color
        )


        text_rect = rarity_text.get_rect(
            center=(
                int(sx),
                int(sy + self.radius + 15)
            )
        )


        screen.blit(
            rarity_text,
            text_rect
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
        self.attack_cooldown = 0
        self.petal_attack_cooldown = 0   # <-- add this

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

        if self.hp <= 0:

            self.alive = False

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
                2
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

            bar_width = 45
            bar_height = 5

            hp_percent = self.hp / self.max_hp


            pygame.draw.rect(
                screen,
                (80,80,80),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 16),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 16),
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

        font = pygame.font.SysFont(
            None,
            18
        )


        rarity_color = RARITY_COLORS.get(
            self.rarity,
            (255,255,255)
        )


        rarity_text = font.render(
            self.rarity,
            True,
            rarity_color
        )


        text_rect = rarity_text.get_rect(
            center=(
                int(sx),
                int(sy + self.radius + 15)
            )
        )


        screen.blit(
            rarity_text,
            text_rect
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
        self.attack_cooldown = 0
        self.petal_attack_cooldown = 0   # <-- add this

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

        if self.hp <= 0:

            self.alive = False

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

            bar_width = 30
            bar_height = 5

            hp_percent = self.hp / self.max_hp


            pygame.draw.rect(
                screen,
                (80,80,80),
                (
                    int(sx-bar_width/2),
                    int(sy-self.radius-12),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx-bar_width/2),
                    int(sy-self.radius-12),
                    int(bar_width*hp_percent),
                    bar_height
                )
            )



        # ---------------- BODY ----------------

        pygame.draw.circle(
            screen,
            (130,130,130),
            (
                int(sx),
                int(sy)
            ),
            self.radius
        )



        # ---------------- ANTENNAE ----------------

        rad = math.radians(
            self.angle
        )


        fx = math.cos(rad)

        fy = math.sin(rad)


        side_x = -fy

        side_y = fx



        head_x = (
            sx +
            fx * self.radius
        )

        head_y = (
            sy +
            fy * self.radius
        )



        for side in [-1,1]:


            end_x = (
                head_x
                + fx * self.radius * 0.8
                + side_x * side * 5
            )


            end_y = (
                head_y
                + fy * self.radius * 0.8
                + side_y * side * 5
            )



            pygame.draw.line(
                screen,
                (60,60,60),
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

        font = pygame.font.SysFont(
            None,
            18
        )


        rarity_color = RARITY_COLORS.get(
            self.rarity,
            (255,255,255)
        )


        rarity_text = font.render(
            self.rarity,
            True,
            rarity_color
        )


        text_rect = rarity_text.get_rect(
            center=(
                int(sx),
                int(sy + self.radius + 15)
            )
        )


        screen.blit(
            rarity_text,
            text_rect
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

        self.attack_cooldown = 0
        self.petal_attack_cooldown = 0   # <-- add this



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




    def take_damage(self, amount):

        if not self.alive:
            return


        self.hp -= int(amount)


        if self.hp <= 0:

            self.alive = False

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


            target_angle = math.degrees(
                math.atan2(
                    player_y - self.y,
                    player_x - self.x
                )
            )


            self.turn_to(
                target_angle,
                5
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

        head_size = self.radius * 0.85

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
            (90,90,90),
            (
                0,
                0,
                int(body_width * 2),
                int(body_height * 2)
            )
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

        wing_surface = pygame.Surface(
            (
                int(self.radius * 3),
                int(self.radius * 3)
            ),
            pygame.SRCALPHA
        )


        cx = self.radius * 1.5
        cy = self.radius * 1.5



        pygame.draw.ellipse(
            wing_surface,
            (220,220,220),
            (
                cx - self.radius * 0.9,
                cy - self.radius * 1.2,
                self.radius * 0.8,
                self.radius * 1.5
            )
        )



        pygame.draw.ellipse(
            wing_surface,
            (220,220,220),
            (
                cx + self.radius * 0.1,
                cy - self.radius * 1.2,
                self.radius * 0.8,
                self.radius * 1.5
            )
        )



        wing_surface = pygame.transform.rotate(
            wing_surface,
            -self.angle + 90
        )


        wing_rect = wing_surface.get_rect(
            center=(int(sx), int(sy))
        )


        screen.blit(
            wing_surface,
            wing_rect
        )



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
            (130,130,130),
            (
                int(head_x),
                int(head_y)
            ),
            int(head_size)
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



        pygame.draw.line(
            screen,
            (40,40,40),
            (
                int(mouth_start_x + side_x * 5),
                int(mouth_start_y + side_y * 5)
            ),
            (
                int(mouth_end_x + side_x * 8),
                int(mouth_end_y + side_y * 8)
            ),
            3
        )



        pygame.draw.line(
            screen,
            (40,40,40),
            (
                int(mouth_start_x - side_x * 5),
                int(mouth_start_y - side_y * 5)
            ),
            (
                int(mouth_end_x - side_x * 8),
                int(mouth_end_y - side_y * 8)
            ),
            3
        )

        # ---------------- HP BAR ----------------

        if self.hp < self.max_hp:

            bar_width = 45
            bar_height = 5

            hp_percent = self.hp / self.max_hp


            pygame.draw.rect(
                screen,
                (80,80,80),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 18),
                    bar_width,
                    bar_height
                )
            )


            pygame.draw.rect(
                screen,
                (0,255,0),
                (
                    int(sx - bar_width/2),
                    int(sy - self.radius - 18),
                    int(bar_width * hp_percent),
                    bar_height
                )
            )

        # ---------------- RARITY TEXT ----------------

        font = pygame.font.SysFont(
            None,
            18
        )


        rarity_color = RARITY_COLORS.get(
            self.rarity,
            (255,255,255)
        )


        rarity_text = font.render(
            self.rarity,
            True,
            rarity_color
        )


        text_rect = rarity_text.get_rect(
            center=(
                int(sx),
                int(sy + self.radius + 15)
            )
        )


        screen.blit(
            rarity_text,
            text_rect
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
        "petals": petal_slots,
        "flower_level": flower_level,
        "flower_xp": flower_xp,
        "upgrade_points": upgrade_points,
        "hp_level": PLAYER_HP_LEVEL,
        "hp_upgrade_cost": hp_upgrade_cost

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

    global flower_level
    global flower_xp
    global flower_xp_needed
    global upgrade_points

    global PLAYER_HP_LEVEL
    global PLAYER_MAX_HP
    global hp_upgrade_cost


    if acc_name_text not in player_data:
        return


    data = player_data[acc_name_text]


    # ---------------- PETALS ----------------

    petal_slots = data.get(
        "petals",
        []
    )


    # ---------------- INVENTORY ----------------

    inventory = data.get(
        "inventory",
        []
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


    inventory.sort(
        key=lambda item: (
            RARITY_ORDER.index(
                item.get(
                    "rarity",
                    "Common"
                )
            )
            if item.get("rarity", "Common") in RARITY_ORDER
            else 999,

            item.get(
                "petal",
                "Basic"
            )
        )
    )


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
        100 *
        (2 ** (PLAYER_HP_LEVEL - 1))
    )


    # ---------------- PETAL HP RESET ----------------

    petal_hp = []
    petal_max_hp = []
    petal_alive = []


    for slot in petal_slots:

        if slot["filled"]:

            hp = (
                PETAL_HP[slot["petal"]]
                *
                PETAL_HP_MULTIPLIER[slot["rarity"]]
            )


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

player_hp = PLAYER_MAX_HP

def create_map():

    walls.clear()
    global starter_walls
    global common_zone
    global epic_zone
    global unusual_zone
    global mythic_zone
    global ultra_zone
    global super_BabyAnt_zone

    starter_walls = []
    common_zone = []
    epic_zone = []
    unusual_zone = []
    mythic_zone = []
    ultra_zone = []
    super_BabyAnt_zone = []

    X = 0
    Y = 3810
    NEW_X = X
    NEW_Y = Y - 2410
    NEW_WIDTH = 1600
    NEW_HEIGHT = 2500
    LONG_WIDTH = WORLD_SIZE - NEW_X - 200
    BOTTOM_Y = WORLD_SIZE - 100

    # -------- 1# --------

    CA = Wall(
        X,
        Y,
        1000,
        100
    )

    # hole here

    CB = Wall(
        X + 1400,
        Y,
        1000,
        100
    )

    CC = Wall(
        X + 2300,
        Y,
        100,
        500
    )

    # hole here

    CD = Wall(
        X + 2300,
        Y + 800,
        100,
        400
    )

    walls.extend([
        CA,
        CB,
        CC,
        CD
    ])

    common_zone.extend([
        CA,
        CB,
        CC,
        CD
    ])
    # -------- 2# --------

    # top horizontal wall
    EA = Wall(
        NEW_X,
        NEW_Y,
        NEW_WIDTH,
        100
    )

    EB = Wall(
        NEW_X,
        NEW_Y,
        100,
        NEW_HEIGHT
    )

    EC = Wall(
        NEW_X + NEW_WIDTH,
        NEW_Y,
        100,
        NEW_HEIGHT
    )

    walls.extend([
        EA,
        EB,
        EC
    ])

    epic_zone.extend([
        EA,
        EB,
        EC
    ])

    # --- 3# ---

    # left part of top wall
    UA = Wall(
        X + 2300,
        3810,
        500,
        100
    )

    # hole here

    # right part of top wall
    UB = Wall(
        X + 2300 + 900,
        3810,
        NEW_WIDTH - 900,
        100
    )

    walls.extend([
        UA,
        UB
    ])

    unusual_zone.extend([
        UA,
        UB
    ])

    # ------ 4# ------

    MA = Wall(
        X + 2300,
        WORLD_SIZE - 100,
        WORLD_SIZE - (X + 2300),
        100
    )

    MB = Wall(
        WORLD_SIZE - 100,
        WORLD_SIZE - 100 - NEW_HEIGHT,
        100,
        NEW_HEIGHT
    )

    # top wall (same width as bottom wall)
    MC = Wall(
        X + 3900,
        WORLD_SIZE - 100 - NEW_HEIGHT,
        WORLD_SIZE - 100 - (X + 2300) - 1000 - 500,
        100
    )

    MD = Wall(
        X + 3900,
        WORLD_SIZE - 100 - NEW_HEIGHT + 100,
        100,
        NEW_HEIGHT - 1090
    )

    walls.extend([
        MA,
        MB,
        MC,
        MD
    ])

    mythic_zone.extend([
        MA,
        MB,
        MC,
        MD
    ])

    # ----- 5# -----

    walls.append(Wall(
        NEW_X + NEW_WIDTH + 500,
        NEW_Y + 1800,
        1200,
        100
    ))

    walls.append(Wall(
        NEW_X + NEW_WIDTH,
        NEW_Y + 1000,
        1700,
        100
    ))

    walls.append(Wall(
        NEW_X + NEW_WIDTH + 1700,
        NEW_Y + 1000,
        100,
        900
    ))

    # -------- 6# ---------

    walls.append(Wall(
        NEW_X + NEW_WIDTH + 500,
        NEW_Y,
        2500,
        100
    ))

    walls.append(Wall(
        NEW_X + NEW_WIDTH + 500,
        0,
        100,
        NEW_Y
    ))

    # ----- REST -----

    walls.append(Wall(
        0,
        0,
        WORLD_SIZE,
        100
    ))

    walls.append(Wall(
        0,
        0,
        100,
        NEW_Y
    ))

    walls.append(Wall(
        0,
        WORLD_SIZE - 100,
        X + 2300,
        100
    ))

    walls.append(Wall(
        0,
        NEW_Y + NEW_HEIGHT,
        100,
        WORLD_SIZE - 100 - (NEW_Y + NEW_HEIGHT)
    ))

    walls.append(Wall(
        WORLD_SIZE - 100,
        0,
        100,
        WORLD_SIZE - 100 - NEW_HEIGHT
    ))

    # --------- PRINT ---------

    xs = []
    ys = []

    for wall in walls:
        xs.append(wall.rect.x)
        xs.append(wall.rect.right)

        ys.append(wall.rect.y)
        ys.append(wall.rect.bottom)

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

    return damage

def get_mythic_spawn_bounds():

    # Mythic top wall (MC)
    top_wall = mythic_zone[2]


    left = top_wall.rect.x

    right = top_wall.rect.right


    # below the top wall
    top = top_wall.rect.bottom


    # bottom of map
    bottom = WORLD_SIZE - 100


    return (
        left,
        top,
        right,
        bottom
    )

def random_world_position(*zones):

    while True:

        zone_name, zone_walls, bottom_y = random.choice(zones)
        if zone_name == "ultra":

            x, y = random_ultra_position()

            return x, y, "ultra"

        if len(zone_walls) == 0:
            continue

        if zone_name == "mythic":

            left, top, right, bottom = get_mythic_spawn_bounds()

        else:

            left, top, right, bottom = get_zone_bounds_from_top(
                zone_walls,
                bottom_y
            )

        x = random.randint(
            left + 150,
            right - 150
        )

        y = random.randint(
            top + 150,
            bottom - 150
        )


        enemy_rect = pygame.Rect(
            x - 25,
            y - 25,
            50,
            50
        )


        blocked = False

        for wall in zone_walls:

            if enemy_rect.colliderect(wall.rect):
                blocked = True
                break


        if not blocked:

            return x, y, zone_name

def get_zone_bounds_from_top(zone_walls, bottom_y):

    xs = []
    ys = []


    for wall in zone_walls:

        xs.append(
            wall.rect.x
        )

        xs.append(
            wall.rect.right
        )

        ys.append(
            wall.rect.y
        )


    left = min(xs)

    right = max(xs)

    top = min(ys)

    bottom = bottom_y


    return (
        left,
        top,
        right,
        bottom
    )

def get_ultra_spawn_bounds():

    left = 2100
    top = 2500
    right = 3300
    bottom = 3200

    return left, top, right, bottom

def random_ultra_position():

    while True:

        ultra_spaces = [
            (1800, 3300, 3900, 3900)
        ]

        super_baby_ant_spaces = [
            (2400, 2500, 3300, 3200)
        ]

        ultra_part = random.choice(ultra_spaces)

        left, top, right, bottom = ultra_part

        x = random.randint(
            left + 50,
            right - 50
        )

        y = random.randint(
            top + 50,
            bottom - 50
        )

        enemy_rect = pygame.Rect(
            x - 35,
            y - 35,
            70,
            70
        )

        blocked = False

        for wall in walls:

            if enemy_rect.colliderect(wall.rect):
                blocked = True
                break

        if not blocked:
            return x, y

def random_super_baby_ant_position():

    while True:

        super_baby_ant_spaces = [
            (1800, 2500, 3300, 3200)
        ]

        area = random.choice(super_baby_ant_spaces)

        left, top, right, bottom = area

        x = random.randint(left + 50, right - 50)
        y = random.randint(top + 50, bottom - 50)

        return x, y

def random_omnient_position():
    omnient_spaces = [
        (2200, 100, 4900, 1400)
    ]

    area = random.choice(omnient_spaces)

    x1, y1, x2, y2 = area

    x = random.randint(x1, x2)
    y = random.randint(y1, y2)

    return x, y

def get_zone_bounds(zone):

    xs = []
    ys = []

    for wall in zone:

        xs.append(wall.rect.x)
        xs.append(wall.rect.right)

        ys.append(wall.rect.y)
        ys.append(wall.rect.bottom)


    return (
        min(xs),
        min(ys),
        max(xs),
        max(ys)
    )

def random_zone_position(zone):

    left, top, right, bottom = get_zone_bounds(zone)

    if right - left < 300 or bottom - top < 300:
        raise ValueError("Zone is too small to spawn enemies.")

    x = random.randint(
        left + 150,
        right - 150
    )

    y = random.randint(
        top + 150,
        bottom - 150
    )


    return x, y, zone

def random_player_spawn():

    starter_walls = []

    for wall in walls:

        # starter place is near the bottom-left area
        if wall.rect.x < 1000 and wall.rect.y > 3500:

            starter_walls.append(wall)

    xs = []
    ys = []

    for wall in starter_walls:

        xs.append(wall.rect.x)
        xs.append(wall.rect.right)

        ys.append(wall.rect.y)
        ys.append(wall.rect.bottom)


    center_x = (min(xs) + max(xs)) // 2
    center_y = (min(ys) + max(ys)) // 2


    spawn_x = center_x + random.randint(-100,100)
    spawn_y = center_y + random.randint(-100,100)

    return spawn_x, spawn_y

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


            if petal_hp[i] <= 0:

                petal_hp[i] = 0
                petal_alive[i] = False

                petal_respawn_timer[i] = PETAL_RELOAD[
                    petal_slots[i]["petal"]
                ]

                save_player()

def spawn_random_mob():

    enemy_classes = [
        Ladybug,
        Bee,
        Spider,
        Rock,
        Hornet,
        BabyAnt,
        SoldierAnt#,
        #WorkerAnt,
        #QueenAnt,
    ]

    enemy = random.choice(enemy_classes)()

    enemy.rarity = random.choice(ENEMY_RARITIES)

    # Update HP after changing rarity
    enemy.max_hp *= MOB_HP_MULTIPLIER[enemy.rarity]
    enemy.damage *= MOB_DAMAGE_MULTIPLIER[enemy.rarity]
    enemy.radius *= MOB_SIZE_MULTIPLIER[enemy.rarity]
    enemy.hp = enemy.max_hp

    enemy.x = player_x + random.randint(-300, 300)
    enemy.y = player_y + random.randint(-300, 300)

    if isinstance(enemy, Ladybug):
        ladybugs.append(enemy)

    elif isinstance(enemy, Bee):
        bees.append(enemy)

    elif isinstance(enemy, Spider):
        spiders.append(enemy)

    elif isinstance(enemy, Rock):
        rocks.append(enemy)

    elif isinstance(enemy, Hornet):
        hornets.append(enemy)

    elif isinstance(enemy, BabyAnt):
        baby_ants.append(enemy)

    elif isinstance(enemy, SoldierAnt):
        soldier_ants.append(enemy)

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

def get_inventory_max_rows():

    top_padding = 40
    bottom_padding = 20

    return (
        inventory_panel_rect.height
        - top_padding
        - bottom_padding
    ) // (INVENTORY_SLOT_SIZE + INVENTORY_SLOT_GAP)

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

def add_inventory_petal(petal, rarity, amount=1):

    global inventory

    for item in inventory:

        if (
            item["petal"] == petal
            and
            item["rarity"] == rarity
        ):

            item["amount"] += amount
            return

    inventory.append({
        "petal": petal,
        "rarity": rarity,
        "amount": amount
    })

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

def enemy_hit_petals(enemy):

    for i in range(PETAL_SLOTS):

        if not petal_alive[i]:
            continue


        angle = math.radians(petal_angle + i * 72)

        petal_x = player_x + math.cos(angle) * petal_distance
        petal_y = player_y + math.sin(angle) * petal_distance


        d = distance(
            petal_x,
            petal_y,
            enemy.x,
            enemy.y
        )


        petal_range = 35

        if petal_slots[i]["petal"] == "Wing":
            petal_range = 60



        if d < petal_range + enemy.radius:


            if enemy.petal_attack_cooldown == 0:

                # enemy damages petal
                petal_hp[i] -= enemy.damage


                # petal damages enemy
                damage = get_petal_damage(
                    petal_slots[i]["petal"],
                    petal_slots[i]["rarity"]
                )

                enemy.take_damage(damage)


                if type(enemy).__name__ != "BabyAnt" or type(enemy).__name__ != "Hornet" or type(enemy).__name__ != "Spider" or type(enemy).__name__ != "Rock" or type(enemy).__name__ != "Soldier_ant":

                    enemy.angry = True


                if petal_hp[i] <= 0:

                    petal_hp[i] = 0
                    petal_alive[i] = False

                    petal_respawn_timer[i] = PETAL_RELOAD[
                        petal_slots[i]["petal"]
                    ]

                # cooldown for hitting petals
                enemy.petal_attack_cooldown = 0

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

def draw_petal(name, x, y, rarity):

    # ---------------- MOON SPOTS ----------------

    moon_spots = []

    for i in range(random.randint(1, 4)):

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

        count = get_petal_count(
            name,
            rarity
        )

        if count == 1:
            r = PETAL_RADIUS * 0.55
        elif count <= 3:
            r = PETAL_RADIUS * 0.48
        elif count <= 5:
            r = PETAL_RADIUS * 0.42
        elif count <= 7:
            r = PETAL_RADIUS * 0.37
        else:
            r = PETAL_RADIUS * 0.33

        light_color = (255, 255, 255)
        light_outline = (190, 190, 190)

        # One Light
        if count == 1:

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

        # Multiple Lights
        else:

            distance = PETAL_RADIUS * 0.55

            for i in range(count):

                angle = (
                    petal_angle
                    + i * (360 / count)
                )

                angle_rad = math.radians(angle)

                light_x = (
                    x
                    + math.cos(angle_rad) * distance
                )

                light_y = (
                    y
                    + math.sin(angle_rad) * distance
                )

                pygame.draw.circle(
                    screen,
                    light_outline,
                    (
                        int(light_x),
                        int(light_y)
                    ),
                    int(r + 2)
                )

                pygame.draw.circle(
                    screen,
                    light_color,
                    (
                        int(light_x),
                        int(light_y)
                    ),
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

        pygame.draw.circle(
            screen,
            (100,220,255),
            (int(x), int(y)),
            PETAL_RADIUS
        )

        pygame.draw.circle(
            screen,
            (220,255,255),
            (
                int(x-4),
                int(y-5)
            ),
            4
        )

        pygame.draw.circle(
            screen,
            (50,150,220),
            (int(x), int(y)),
            PETAL_RADIUS,
            2
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

        moon_color = (180, 180, 180)
        spot_color = (120, 120, 120)

        # Temporary surface for the moon
        moon_surface = pygame.Surface(
            (int(r * 2.4), int(r * 2.4)),
            pygame.SRCALPHA
        )

        center = int(r * 1.2)

        # ---------------- MOON ----------------

        pygame.draw.circle(
            moon_surface,
            moon_color,
            (center, center),
            int(r)
        )

        # ---------------- DARK SPOTS ----------------

        for spot in moon_spots:

            spot_x = center + int(spot["x"])
            spot_y = center + int(spot["y"])
            spot_radius = int(spot["radius"])

            pygame.draw.circle(
                moon_surface,
                spot_color,
                (spot_x, spot_y),
                spot_radius
            )

        # ---------------- CUT EVERYTHING OUTSIDE MOON ----------------

        mask = pygame.Surface(
            moon_surface.get_size(),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            mask,
            (255, 255, 255, 255),
            (center, center),
            int(r)
        )

        moon_surface.blit(
            mask,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_MULT
        )

        # Draw moon
        screen.blit(
            moon_surface,
            (
                int(x - center),
                int(y - center)
            )
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


    for i in range(PETAL_SLOTS):

        hp = (
            PETAL_HP["Basic"]
            *
            PETAL_HP_MULTIPLIER["Common"]
        )

        petal_max_hp.append(hp)
        petal_hp.append(hp)
        petal_alive.append(True)


    game_state = "game"
    save_player()

def get_enemy_rarity(zone):

    if zone == "common":

        return "Common"


    if zone == "epic":

        roll = random.random()

        if roll < 0.81:
            return "Epic"

        else:
            return "Rare"


    if zone == "unusual":

        roll = random.random()

        if roll < 0.85:
            return "Unusual"

        else:
            return "Rare"


    if zone == "mythic":

        roll = random.random()

        if roll < 0.50:
            return "Mythic"

        elif roll < 0.80:
            return "Legendary"

        else:
            return "Epic"


    if zone == "ultra":

        roll = random.random()

        if roll < 0.50:
            return "Ultra"

        elif roll < 0.80:
            return "Mythic"

        else:
            return "Legendary"

    if zone == "super":

        roll = random.random()

        if roll < 0.90:
            return "Super"

        elif roll < 0.10:
            return "Omega"

        else:
            return "Ultra"

    if zone == "omnient":

        roll = random.random()

        if roll < 0.90:
            return "Ancient"

        elif roll < 0.95:
            return "Radium"

        else:
            return "Omnient"

    return "Common"

create_map()
player_x, player_y = random_player_spawn()
# ---------------- GAME LOOP ----------------

ladybugs = []

for i in range(random.randint(1, 30)):

    ladybug = Ladybug()

    ladybug.x, ladybug.y, zone = random_world_position(
        ("common", common_zone, WORLD_SIZE - 100),
        ("epic", epic_zone, 3810),
        ("unusual", unusual_zone, WORLD_SIZE - 100),
        ("mythic", mythic_zone, WORLD_SIZE - 100),
        ("ultra", ultra_zone, WORLD_SIZE - 100)
    )

    ladybug.rarity = get_enemy_rarity(
        zone
    )

    ladybugs.append(ladybug)

for i in range(20):

    ladybug = Ladybug()

    ladybug.x, ladybug.y = random_omnient_position()

    ladybug.rarity = get_enemy_rarity("omnient")

    ladybugs.append(ladybug)
# ---------------- BEE ----------------

bees = []

for i in range(random.randint(1, 30)):

    bee = Bee()

    bee.x, bee.y, zone = random_world_position(
        ("common", common_zone, WORLD_SIZE - 100),
        ("epic", epic_zone, 3810),
        ("unusual", unusual_zone, WORLD_SIZE - 100),
        ("mythic", mythic_zone, WORLD_SIZE - 100),
        ("ultra", ultra_zone, WORLD_SIZE - 100)
    )

    bee.rarity = get_enemy_rarity(
        zone
    )

    bees.append(bee)

for i in range(20):

    bee = Bee()

    bee.x, bee.y = random_omnient_position()

    bee.rarity = get_enemy_rarity("omnient")

    bees.append(bee)

# ---------------- SPIDER ----------------

spiders = []

for i in range(random.randint(1, 30)):

    spider = Spider()

    spider.x, spider.y, zone = random_world_position(
        ("common", common_zone, WORLD_SIZE - 100),
        ("epic", epic_zone, 3810),
        ("unusual", unusual_zone, WORLD_SIZE - 100),
        ("mythic", mythic_zone, WORLD_SIZE - 100),
        ("ultra", ultra_zone, WORLD_SIZE - 100)
    )

    spider.rarity = get_enemy_rarity(
        zone
    )

    spiders.append(spider)

for i in range(20):

    spider = Spider()

    spider.x, spider.y = random_omnient_position()

    spider.rarity = get_enemy_rarity("omnient")

    spiders.append(spider)

# ---------------- ROCK ----------------

rocks = []

for i in range(random.randint(1, 30)):

    rock = Rock()

    rock.x, rock.y, zone = random_world_position(
        ("common", common_zone, WORLD_SIZE - 100),
        ("epic", epic_zone, 3810),
        ("unusual", unusual_zone, WORLD_SIZE - 100),
        ("mythic", mythic_zone, WORLD_SIZE - 100),
        ("ultra", ultra_zone, WORLD_SIZE - 100)
    )

    rock.rarity = get_enemy_rarity(
        zone
    )

    rocks.append(rock)

for i in range(20):

    rock = Rock()

    rock.x, rock.y = random_omnient_position()

    rock.rarity = get_enemy_rarity("omnient")

    rocks.append(rock)

# ---------------- HORNET ----------------

hornets = []

for i in range(random.randint(1, 30)):

    hornet = Hornet()

    hornet.x, hornet.y, zone = random_world_position(
        ("common", common_zone, WORLD_SIZE - 100),
        ("epic", epic_zone, 3810),
        ("unusual", unusual_zone, WORLD_SIZE - 100),
        ("mythic", mythic_zone, WORLD_SIZE - 100),
        ("ultra", ultra_zone, WORLD_SIZE - 100)
    )

    hornet.rarity = get_enemy_rarity(
        zone
    )

    hornets.append(hornet)

for i in range(20):

    hornet = Hornet()

    hornet.x, hornet.y = random_omnient_position()

    hornet.rarity = get_enemy_rarity("omnient")

    hornets.append(hornet)

# -------------- BABY ANT ---------------------------

baby_ants = []

# ---------------- NORMAL BABY ANTS ----------------

for i in range(random.randint(1, 30)):

    ant = BabyAnt()

    ant.x, ant.y, zone = random_world_position(
        ("common", common_zone, WORLD_SIZE - 100),
        ("epic", epic_zone, 3810),
        ("unusual", unusual_zone, WORLD_SIZE - 100),
        ("mythic", mythic_zone, WORLD_SIZE - 100),
        ("ultra", ultra_zone, WORLD_SIZE - 100)
    )

    ant.rarity = get_enemy_rarity(
        zone
    )

    baby_ants.append(ant)

for i in range(20):

    ant = BabyAnt()

    ant.x, ant.y = random_omnient_position()

    ant.rarity = get_enemy_rarity("omnient")

    baby_ants.append(ant)

# ---------------- SUPER BABY ANTS ----------------

for i in range(random.randint(1, 50)):

    ant = BabyAnt()

    ant.x, ant.y = random_super_baby_ant_position()

    ant.rarity = get_enemy_rarity("super")

    baby_ants.append(ant)

# ---------------- SOLDIER ANT ----------------

soldier_ants = []

for i in range(random.randint(1, 30)):

    soldier_ant = SoldierAnt()

    soldier_ant.x, soldier_ant.y, zone = random_world_position(
        ("common", common_zone, WORLD_SIZE - 100),
        ("epic", epic_zone, 3810),
        ("unusual", unusual_zone, WORLD_SIZE - 100),
        ("mythic", mythic_zone, WORLD_SIZE - 100),
        ("ultra", ultra_zone, WORLD_SIZE - 100)
    )

    soldier_ant.rarity = get_enemy_rarity(
        zone
    )

    soldier_ants.append(soldier_ant)

for i in range(20):

    soldier_ant = SoldierAnt()

    soldier_ant.x, soldier_ant.y = random_omnient_position()

    soldier_ant.rarity = get_enemy_rarity("omnient")

    soldier_ants.append(soldier_ant)

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


                # open menu

            if hp_button_rect.collidepoint(mouse_x, mouse_y):

                hp_menu_open = True



                # close menu

            if hp_menu_open:

                if close_button_rect.collidepoint(mouse_x, mouse_y):

                    hp_menu_open = False



                # buy upgrade

            if hp_menu_open:

                if hp_upgrade_rect.collidepoint(mouse_x, mouse_y):

                    upgrade_player_hp()


            if game_state == "login":

                if password_box.collidepoint(event.pos):

                    active_input = "password"


                elif acc_name_box.collidepoint(event.pos):

                    active_input = "acc_name"


                else:

                    active_input = None

            if login_rect.collidepoint(event.pos):

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

                    if acc_name_text == "DevGuard":

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
                    inventory.sort(
                        key=lambda item: (
                            RARITY_ORDER.index(item["rarity"])
                            if item["rarity"] in RARITY_ORDER
                            else 999,
                            item["petal"]
                        )
                    )

                    game_state = "game"


            if create_acc_button_rect.collidepoint(event.pos):

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

            if inventory_button_rect.collidepoint(event.pos):

                inventory_open = not inventory_open

            if inventory_open:

                if event.button == 4:  # scroll up
                    inventory_scroll -= 1

                if event.button == 5:  # scroll down
                    inventory_scroll += 1


                total_rows = math.ceil(len(inventory) / 5)

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

            if inventory_open:

                inventory_scroll -= event.y

                if inventory_scroll < 0:
                    inventory_scroll = 0


                max_scroll = max(
                    0,
                    len(inventory) - 30
                )


                if inventory_scroll > max_scroll:
                    inventory_scroll = max_scroll

        if event.type == pygame.MOUSEWHEEL:

            if inventory_open:

                inventory_scroll -= event.y

                if inventory_scroll < 0:
                    inventory_scroll = 0

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


    elif game_state == "game":

        dt = clock.tick(FPS)

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

        # movement direction

        move_x = 0
        move_y = 0


        if keys[pygame.K_UP]:
            move_y -= 2

        if keys[pygame.K_DOWN]:
            move_y += 2

        if keys[pygame.K_LEFT]:
            move_x -= 2

        if keys[pygame.K_RIGHT]:
            move_x += 2
        if keys[pygame.K_SPACE]:
            spawn_random_mob()

        if player_spawn_cooldown > 0:
            player_spawn_cooldown -= 1

        # prevent diagonal speed boost
        infino_gradient_offset += 1

        if infino_gradient_offset >= PETAL_SLOT_SIZE * 3:
            infino_gradient_offset = 0
        if move_x != 0 or move_y != 0:

            length = math.sqrt(
                move_x * move_x +
                move_y * move_y
            )

            move_x /= length
            move_y /= length

            player_x += move_x * PLAYER_SPEED
            player_y += move_y * PLAYER_SPEED


            # -------- WALL COLLISION --------

            player_rect = pygame.Rect(
                player_x - PLAYER_RADIUS,
                player_y - PLAYER_RADIUS,
                PLAYER_RADIUS * 2,
                PLAYER_RADIUS * 2
            )

            for wall in walls:

                if player_rect.colliderect(wall.rect):

                    player_x -= move_x * PLAYER_SPEED
                    player_y -= move_y * PLAYER_SPEED

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

        spin_speed = 2

        for i in range(PETAL_SLOTS):

            if petal_alive[i]:

                if petal_slots[i]["petal"] == "Faster":

                    rarity = petal_slots[i]["rarity"]

                    spin_amount = PETAL_ROT_SPEED_MUL.get(
                        rarity,
                        1
                    )

                    spin_speed += spin_amount

        petal_angle += spin_speed

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

        update_boss_hp()
        # ---------------- PETAL RESPAWN ----------------

        for i in range(PETAL_SLOTS):

            if not petal_alive[i]:

                if petal_respawn_timer[i] > 0:

                    petal_respawn_timer[i] -= 1

                else:

                    petal_alive[i] = True
                    petal_hp[i] = petal_max_hp[i]

                    save_player()

        # ---------------- PETAL REGEN ----------------

        for i in range(PETAL_SLOTS):

            if petal_alive[i]:

                if petal_hp[i] < petal_max_hp[i]:

                    petal_hp[i] += 0.05

                    if petal_hp[i] > petal_max_hp[i]:
                        petal_hp[i] = petal_max_hp[i]


        # enemy touching player
        for ladybug in ladybugs:

            if ladybug.alive:
                enemy_hit_petals(ladybug)

                d = distance(
                    player_x,
                    player_y,
                    ladybug.x,
                    ladybug.y
                )

                if d < PLAYER_RADIUS + ladybug.radius:

                    if player_spawn_cooldown <= 0:

                        if ladybug.attack_cooldown == 0:

                            player_hp -= (
                                ladybug.damage *
                                MOB_DAMAGE_MULTIPLIER[ladybug.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            ladybug.attack_cooldown = 0



        for bee in bees:

            if bee.alive:
                enemy_hit_petals(bee)
                d = distance(
                    player_x,
                    player_y,
                    bee.x,
                    bee.y
                )

                if d < PLAYER_RADIUS + bee.radius:

                    if player_spawn_cooldown <= 0:

                        if bee.attack_cooldown == 0:

                            player_hp -= (
                                bee.damage *
                                MOB_DAMAGE_MULTIPLIER[bee.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            bee.attack_cooldown = 0




        for spider in spiders:

            if spider.alive:
                enemy_hit_petals(spider)
                d = distance(
                    player_x,
                    player_y,
                    spider.x,
                    spider.y
                )

                if d < PLAYER_RADIUS + spider.radius:

                    if player_spawn_cooldown <= 0:

                        if spider.attack_cooldown == 0:

                            player_hp -= (
                                spider.damage *
                                MOB_DAMAGE_MULTIPLIER[spider.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            spider.attack_cooldown = 0




        for rock in rocks:

            if rock.alive:
                enemy_hit_petals(rock)
                d = distance(
                    player_x,
                    player_y,
                    rock.x,
                    rock.y
                )

                if d < PLAYER_RADIUS + rock.radius:

                    if player_spawn_cooldown <= 0:

                        if rock.attack_cooldown == 0:

                            player_hp -= (
                                rock.damage *
                                MOB_DAMAGE_MULTIPLIER[rock.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            rock.attack_cooldown = 0




        for hornet in hornets:

            if hornet.alive:
                enemy_hit_petals(hornet)
                d = distance(
                    player_x,
                    player_y,
                    hornet.x,
                    hornet.y
                )

                if d < PLAYER_RADIUS + hornet.radius:

                    if player_spawn_cooldown <= 0:

                        if hornet.attack_cooldown == 0:

                            player_hp -= (
                                hornet.damage *
                                MOB_DAMAGE_MULTIPLIER[hornet.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            hornet.attack_cooldown = 0


        for ant in baby_ants:

            if ant.alive:

                enemy_hit_petals(ant)

                d = distance(
                    player_x,
                    player_y,
                    ant.x,
                    ant.y
                )

                if d < PLAYER_RADIUS + ant.radius:

                    if player_spawn_cooldown <= 0:

                        if ant.attack_cooldown == 0:

                            player_hp -= (
                                ant.damage *
                                MOB_DAMAGE_MULTIPLIER[ant.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            ant.attack_cooldown = 0


        for soldier_ant in soldier_ants:

            if soldier_ant.alive:

                enemy_hit_petals(soldier_ant)

                d = distance(
                    player_x,
                    player_y,
                    soldier_ant.x,
                    soldier_ant.y
                )

                if d < PLAYER_RADIUS + soldier_ant.radius:

                    if player_spawn_cooldown <= 0:

                        if soldier_ant.attack_cooldown == 0:

                            player_hp -= (
                                soldier_ant.damage *
                                MOB_DAMAGE_MULTIPLIER[soldier_ant.rarity]
                            )

                            if player_hp < 0:
                                player_hp = 0

                            soldier_ant.attack_cooldown = 0

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

        for wall in walls:
            wall.draw()

        for wall in walls:
            wall.draw_map()

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

                if petal_slots[i]["filled"] and petal_alive[i]:

                    draw_petal(
                        petal_slots[i]["petal"],
                        x + PETAL_SLOT_SIZE//2,
                        y + PETAL_SLOT_SIZE//2,
                        petal_slots[i]["rarity"]
                    )

            # Respawn timer number above slot

            if i < PETAL_SLOTS:

                if not petal_alive[i] and petal_respawn_timer[i] > 0:

                    font = pygame.font.Font(None, 30)

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


        for i in range(PETAL_SLOTS):

            if not petal_alive[i]:
                continue

            angle = math.radians(petal_angle + i * 72)

            x = WIDTH // 2 + math.cos(angle) * petal_distance
            y = HEIGHT // 2 + math.sin(angle) * petal_distance


            draw_petal(
                petal_slots[i]["petal"],
                x,
                y,
                petal_slots[i]["rarity"]
            )


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

            for i in range(PETAL_SLOTS):

                # skip dead petals
                if not petal_alive[i]:
                    continue


                angle = math.radians(
                    petal_angle + i * 72
                )

                petal_world_x = player_x + math.cos(angle) * petal_distance
                petal_world_y = player_y + math.sin(angle) * petal_distance


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
                        petal_slots[i]["petal"],
                        petal_slots[i]["rarity"]
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


                        petal_range = 35

                        if petal_slots[i]["petal"] == "Wing":
                            petal_range = 60


                        if d < petal_range + enemy.radius:

                            # enemy damages petal first
                            if enemy.attack_cooldown == 0:

                                petal_hp[i] -= enemy.damage

                                if petal_hp[i] <= 0:

                                    petal_hp[i] = 0
                                    petal_alive[i] = False

                                    petal_respawn_timer[i] = PETAL_RELOAD[
                                        petal_slots[i]["petal"]
                                    ]

                                enemy.attack_cooldown = 0


                            # petal attacks enemy
                            enemy.take_damage(damage)


                            if petal_slots[i]["petal"] == "Heavy":

                                dx = enemy.x - player_x
                                dy = enemy.y - player_y

                                length = math.sqrt(dx * dx + dy * dy)

                                if length != 0:

                                    dx /= length
                                    dy /= length

                                    knockback = (
                                        8 *
                                        HEAVY_KNOCKBACK_MULTIPLIER[
                                            petal_slots[i]["rarity"]
                                        ]
                                    )

                                    weight = (
                                        MOB_WEIGHT[type(enemy).__name__] *
                                        MOB_WEIGHT_MULTIPLIER[enemy.rarity]
                                    )

                                    enemy.knockback_x += dx * knockback / weight
                                    enemy.knockback_y += dy * knockback / weight


                            hit = True
                            break



                    if hit:

                        petal_cooldowns[i] = PETAL_RELOAD[
                            petal_slots[i]["petal"]
                        ]



                # ---------------- PETAL HP BAR ----------------

                if petal_hp[i] < petal_max_hp[i]:

                    bar_width = 35
                    bar_height = 5

                    hp_percent = (
                        petal_hp[i] /
                        petal_max_hp[i]
                    )


                    pygame.draw.rect(
                        screen,
                        (80,80,80),
                        (
                            int(
                                WIDTH//2 +
                                math.cos(angle) * petal_distance -
                                bar_width/2
                            ),
                            int(
                                HEIGHT//2 +
                                math.sin(angle) * petal_distance -
                                PETAL_RADIUS -
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
                                math.cos(angle) * petal_distance -
                                bar_width/2
                            ),
                            int(
                                HEIGHT//2 +
                                math.sin(angle) * petal_distance -
                                PETAL_RADIUS -
                                12
                            ),
                            int(bar_width * hp_percent),
                            bar_height
                        )
                    )

                # Draw player

                # ---------------- FLOWER LEVEL UI ----------------

                font = pygame.font.Font(None, 32)


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


                screen.blit(
                    level_text,
                    (20,20)
                )


                screen.blit(
                    xp_text,
                    (20,50)
                )


                screen.blit(
                    points_text,
                    (20,80)
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
                    (80,80,80),
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

                    font = pygame.font.Font(None, 45)

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


        # ---------------- PLAYER FACE ----------------

        # eyes

        pygame.draw.ellipse(
            screen,
            (0,0,0),
            (
                player_center_x - 11,
                player_center_y - 10,
                8,
                12
            )
        )

        pygame.draw.ellipse(
            screen,
            (0,0,0),
            (
                player_center_x + 3,
                player_center_y - 10,
                8,
                12
            )
        )


        # normal smile

        if petal_target == PETAL_NORMAL:

            pygame.draw.arc(
                screen,
                (0,0,0),
                (
                    player_center_x - 9,
                    player_center_y - 1,
                    18,
                    16
                ),
                math.radians(200),
                math.radians(340),
                2
            )


        # attack angry face

    # ---------------- ATTACK ANGRY EYES ----------------

            # left eye cut (top-left -> middle-right)
        elif petal_face_target == PETAL_ATTACK:
            pygame.draw.polygon(
                screen,
                (225,225,0),
                [
                    (
                        player_center_x - 12,
                        player_center_y - 12
                    ),
                    (
                        player_center_x - 4,
                        player_center_y - 8
                    ),
                    (
                        player_center_x - 4,
                        player_center_y - 16
                    ),
                    (
                        player_center_x - 12,
                        player_center_y - 16
                    )
                ]
            )


            # right eye cut (top-right -> middle-left)

            pygame.draw.polygon(
                screen,
                (225,225,0),
                [
                    (
                        player_center_x + 4,
                        player_center_y - 8
                    ),
                    (
                        player_center_x + 12,
                        player_center_y - 12
                    ),
                    (
                        player_center_x + 12,
                        player_center_y - 16
                    ),
                    (
                        player_center_x + 4,
                        player_center_y - 16
                    )
                ]
            )

            pygame.draw.arc(
                screen,
                (0,0,0),
                (
                    player_center_x - 9,
                    player_center_y + 7,
                    18,
                    16
                ),
                math.radians(20),
                math.radians(160),
                2
            )

        elif petal_target == PETAL_DEFEND:

            pygame.draw.arc(
                screen,
                (0,0,0),
                (
                    player_center_x - 9,
                    player_center_y + 7,
                    18,
                    16
                ),
                math.radians(20),
                math.radians(160),
                2
            )

        # ---------------- INVENTORY BUTTON ----------------

        pygame.draw.rect(
            screen,
            (40,120,255),
            inventory_button_rect,
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

        if inventory_open:


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


            for index, item in enumerate(inventory):

                row = index // inventory_cols - inventory_scroll
                col = index % inventory_cols


                # hide rows outside panel

                if row < 0 or row >= max_rows:
                    continue


                x = start_x + col * (slot_size + slot_gap)

                y = start_y + row * (slot_size + slot_gap)


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

                    count_font = pygame.font.Font(None, 24)

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


            font = pygame.font.Font(None,32)


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

        hp_font = pygame.font.Font(None, 28)

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

        # ---------------- SPAWN MESSAGE ----------------

        if spawn_message_timer > 0:

            spawn_message_timer -= 3

            # fade during the last 60 frames
            if spawn_message_timer < 60:
                spawn_message_alpha = int(
                    255 * (spawn_message_timer / 60)
                )

            font = pygame.font.Font(None, 48)

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
        draw_minimap()
    pygame.display.flip()

save_player()

pygame.quit()
sys.exit()
