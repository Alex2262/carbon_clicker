
import sys
import os

base_path = ""

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable) + "/"
elif __file__:
    base_path = os.path.dirname(__file__) + "/"

# Screen Information
WIDTH = 1100
HEIGHT = 700

SCREEN_SIZE = (WIDTH, HEIGHT)

# Colors
GOLD_COLOR = (255, 206, 46)
MONEY_COLOR = (101, 214, 131)
COUNT_COLOR = (76, 135, 237)
SCREEN_COLOR = (2, 7, 23)

NUM_STARS = 60

# Main Layer component information
LAYER_LEFT_RECT = (0, 0, 300, HEIGHT)
LAYER_MIDDLE_RECT = (LAYER_LEFT_RECT[2], 0, 400, HEIGHT)
LAYER_RIGHT_RECT = (LAYER_MIDDLE_RECT[0] + LAYER_MIDDLE_RECT[2], 0, 400, HEIGHT)

# Information Layers
# Each are written to maximize dependency on each other,
# so if one value is changed, the others will be changed respectively
LAYER_TITLE_RECT = (LAYER_MIDDLE_RECT[0], LAYER_MIDDLE_RECT[1] + 20, LAYER_MIDDLE_RECT[2], 70)

LAYER_POLLUTION_CLEARED_RECT = (LAYER_TITLE_RECT[0], LAYER_TITLE_RECT[1] + LAYER_TITLE_RECT[3], LAYER_TITLE_RECT[2], 40)

LAYER_PPS_RECT = (LAYER_POLLUTION_CLEARED_RECT[0], LAYER_POLLUTION_CLEARED_RECT[1] + LAYER_POLLUTION_CLEARED_RECT[3],
                  LAYER_POLLUTION_CLEARED_RECT[2] // 2, 40)

LAYER_MONEY_RECT = (LAYER_POLLUTION_CLEARED_RECT[0] + LAYER_POLLUTION_CLEARED_RECT[2] // 2,
                    LAYER_POLLUTION_CLEARED_RECT[1] + LAYER_POLLUTION_CLEARED_RECT[3],
                    LAYER_POLLUTION_CLEARED_RECT[2] // 2, 40)

LAYER_ITEMS_RECT = (LAYER_RIGHT_RECT[0], LAYER_RIGHT_RECT[1], LAYER_RIGHT_RECT[2], 100)

LAYER_SCROLL_BAR_RECT = (LAYER_ITEMS_RECT[0]+390, LAYER_ITEMS_RECT[1]+LAYER_ITEMS_RECT[3],
                         10, HEIGHT-LAYER_ITEMS_RECT[3])

LAYER_BOTTOM_RECT = (LAYER_MIDDLE_RECT[0], 180, LAYER_MIDDLE_RECT[2], HEIGHT - 180)

SELL_BUTTON_RECT = (LAYER_MIDDLE_RECT[0] + LAYER_MIDDLE_RECT[2] // 2 - 150 // 2, 600, 150, 70)

LAYER_ACHIEVEMENT_TITLE_RECT = (0, 0, 300, 100)
LAYER_UPGRADE_TITLE_RECT = (0, LAYER_ACHIEVEMENT_TITLE_RECT[3] + 150, 300, 100)

# Clicker Rects
EARTH_CLICKER_RECT = (LAYER_MIDDLE_RECT[0]+50, LAYER_MIDDLE_RECT[1]+270,
                      300, 300)
EARTH_CLICKER_SMALL_RECT = (LAYER_MIDDLE_RECT[0]+60, LAYER_MIDDLE_RECT[1]+280,
                      280, 280)
EARTH_CLICKER_LARGE_RECT = (LAYER_MIDDLE_RECT[0]+45, LAYER_MIDDLE_RECT[1]+265,
                      310, 310)

# Suffixes for numbers for scaling
NUMBER_SUFFIX = [" ", "K", "M", "B", "T", "Qa", "Qu", "Sx"]

# Item information indexed by item type
# Position in array corresponds to type of item
NUM_ITEMS = 9
ITEM_NAMES = ["Volunteer", "Claw", "Tree", "Seabin", "River Trash Fence", "Recycling Facility", "Smog Vacuum",
              "Trash Boat", "Carbon Capturer"]
ITEM_PRICES = [10, 100, 1000, 10000, 100000, 800000, 6000000, 40000000, 300000000]
ITEM_RATES = [0.5, 6, 70, 800, 10000, 100000, 900000, 6300000, 56000000]

# The descriptions for the tower popups
ITEM_INFO = [
    "The Volunteer: by themselves they may be small, but they are the most important in contributing to the"
    " environment. Just like YOU, everyone can make a difference!",

    "Claw: Help pick up some garbage and make the environment cleaner! It will go a long way.",

    "Trees: essential helpers against climate change."
    " They reduce carbon dioxide in the atmosphere while replenishing oxygen."
    "They are also good at removing air pollutants.",

    "The Seabin: filters water and captures oil and trash to help clean the oceans."
    " Get some of these to save the oceans and the environment!",

    "River Trash Fences: placed at a dry river bed."
    " When Flash Floods arrive, the fence will intercept any trash and retain it in place!",

    "Recycling Facilities: help out the environment so much by recycling trash and materials such as plastic"
    " into new and useful material. Instead of throwing your trash in the ocean, help recycle it!",

    "The Smog Vacuum: uses futuristic technology to clean air and remove pollution and smog."
    " Help everyone breathe cleaner!",

    "This Trash Boat: lies in wait for any trash floating down a river, and captures and prevents it from"
    " flowing into oceans!",

    "The Carbon Capturer: captures any unwanted greenhouse gasses from industrial processes,"
    " preventing it from entering the atmosphere and exacerbating climate change."
]


'''
-- UPGRADES --
There are four types of upgrades, and four levels to each. 
    1. Public Transportation for upgrading Volunteers
    2. Garbage Trucks for Recycling Facilities
    3. Activism for Volunteers, Seabin, Trash Fence
    4. Power plants for Smog Vacuum, Trash Boat, Carbon Capture
    
These lists indicate different traits of the upgrades and their four levels.
'''


# This keeps a list of which towers the upgrade rates will affect
UPGRADE_ACTIONS = [
    [0],
    [0, 3, 4],
    [5],
    [6, 7, 8],
]

# A rate for upgrades
# These numbers multiply the rate of the tower
UPGRADE_RATES = [
    [1.2, 1.8, 3, 8],  # Public Transportation for upgrading Volunteers
    [1.2, 1.8, 3, 8],  # Activism for Volunteers, Seabin, Trash Fence
    [1.2, 1.8, 3, 8],  # Garbage Trucks for Recycling Facilities
    [1.2, 1.8, 3, 8],  # Power plants for Smog Vacuum, Trash Boat, Carbon Capture
]

UPGRADE_COSTS = [
    [100, 200, 800, 2000],
    [800000, 2000000, 30000000, 120000000],
    [1000000, 3000000, 90000000, 300000000],
    [1000000000, 5000000000, 20000000000, 100000000000]
]

# The descriptions for the upgrade popups
# Each array contains the descriptions for one type of upgrade
UPGRADE_INFO = [
    [
        "Public Transportation Level 1: Add buses to help volunteers get around.",

        "Public Transportation Level 2: Build railways to improve clean transit for everyone.",

        "Public Transportation Level 3: Electric-powered airplanes dramatically improve the speed and"
        " efficiency of overseas travel.",

        "Public Transportation Level 4: High speed railways become the most popular form of travel,"
        " drastically reducing travel times and traffic emissions."
    ],
    [
        "Robust Garbage Vans: Increase the efficiency of garbage trucks",
        "Fuel-efficient Garbage Trucks: Increase the efficiency of garbage trucks even more",
        "Adventure Garbage Trucks: Garbage Trucks can now traverse all types of terrain",
        "Garbage Planes: Garbage can be collected from far areas and transported at record speeds"
    ],
    [
        "Call to arms: Volunteers are now increasingly motivated."
        " They can now build environmental projects much faster, and better."
        " Increases efficiency of Volunteers, Seabins, and Trash Fences.",

        "Charities: Volunteers have more funds to help the environment,"
        " and can build high quality environmental infrastructure."
        " Increases efficiency of Volunteers, Seabins, and Trash Fences.",

        "Political Influence: Pro-environment politicians are being installed worldwide."
        " Governments how provide assistance to all sorts of projects."
        " Increases efficiency of Volunteers, Seabins, and Trash Fences.",

        "Global Movement: The entire world is on track to help the earth."
        " Across all continents, the spirit of environmental sustainability runs high."
        " Everyone wants to help. Increases efficiency of Volunteers, Seabins, and Trash Fences."
    ],
    [
        "More power plants: There will be more electricity to power Smog Vacuums, Trash Boats, and Carbon Capture.",

        "Better infrastructure: Transporting electricity to the machines is more efficient, with minimal loss."
        " Increases efficiency of Smog Vacuums, Trash Boats, and Carbon Capture.",

        "Advanced Research: Support scientists on their quest to find the best ways to produce power."
        " They are professionals, who constantly produce new methods. Increases efficiency of Smog Vacuums,"
        " Trash Boats, and Carbon Capture.",

        "Full Power: Research has gotten renewable power production to be the most efficient and cheapest,"
        " increasing the efficiency of Smog Vacuums, Trash Boats, and Carbon Capture."
    ]
]

# Sorts the upgrades in ascending order based on cost
UPGRADE_ORDER = []

for i_upgrade in range(len(UPGRADE_COSTS)):
    for j_upgrade in range(len(UPGRADE_COSTS[i_upgrade])):
        UPGRADE_ORDER.append([i_upgrade, j_upgrade])

UPGRADE_ORDER = sorted(UPGRADE_ORDER, key=lambda x: UPGRADE_COSTS[x[0]][x[1]])
