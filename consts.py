# THESE ARE THE PARTS YOU HAVE TO CHANGE
# See Readme.md for instructions on getting your tokens/ids
CHANNEL = u'CHANNEL'
SLACK_TOKEN = 'SLACK_TOKEN'
BOT_USER = 'BOT_TOKEN'

HOUSES = ["Ravenclaw", "Hufflepuff", "Gryffindor", "Slytherin"]
IMAGE_PATH = "house_points.png"
MODE = "hogwarts"
# only prefects can add and remove multiple points
# filling this in is optional
PREFECTS = ["your_slack_id_here", "someone_elses_here"]
# Announcers will be able to make the bot print the current standing
ANNOUNCERS = PREFECTS
POINTS_FILE = 'points.pkl'

if MODE == "alice":
    HOUSES = [':clubs:', ':diamonds:', ':spades:', ':hearts:']
    IMAGE_PATH = "cards"
    CARD_VALUES = { '2': 2,
                    '3': 3,
                     '4': 4,
                     '5': 5,
                     '6': 6,
                     '7': 7,
                     '8': 8,
                     '9': 9,
                     '10': 10,
                     'A': 1,
                     'J': 11,
                     'K': 13,
                     'Q': 12}