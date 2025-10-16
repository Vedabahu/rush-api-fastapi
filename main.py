from datetime import datetime, timezone
import logging
from random import choice
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.middleware import RequestLoggingMiddleware, BlockOn404Middleware

KEY = "36e56929863eb09971a059416f0d68a10f1264bc3abda51fb50f3fc4ab7e35302b894fa97b7fe9818031cacbd601d72ff9634c0a16d3a1862724844833880b16"

# app = FastAPI(docs_url="doc", redoc_url=None, openapi_url=None)
app = FastAPI()

# CORS configuration: allow everything
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(BlockOn404Middleware)


died_404_messages = [
    {
        "message": "You tried to tickle the balls of a tiger... You died. Now wait 10s before you can continue."
    },
    {
        "message": "You talked in Hindi to a Bangalore auto rikshaw person. He was not ammused. You died. Now wait 10s before you can continue."
    },
    {
        "message": "You are waiting for Michael Jackson... on the world trade center on 9/11... You died. Now wait 10s before you can continue."
    },
    {
        "message": "You ate the paneer from the mess... Turns out, it was not paneer... You died. Now wait 10s before you can continue."
    },
    {
        "message": "You ate the jeera rice from the mess. You got a protein overdose. You died. Now wait 10s before you can continue."
    },
    {
        "message": "You applied for Shrek live action role but you got rejected because you were too ugly... You died from emotional damage. Now wait 10s before you can continue."
    },
    {
        "message": "You tried to race Lightning McQueen... You got hit by Chick Hicks and died. Now wait 10s before you can continue."
    },
    {
        "message": "You got bitten by a dog because you were eating Croissant... You died. Now wait 10s before you can continue."
    },
    {
        "message": "You got blown up by a creeper... You died. Now wait 10s before you can continue."
    },
    {
        "message": "A snake bit you, you bit it back... both of you died. Now wait 10s before you can continue."
    },
]


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # Return the image on 404
        return JSONResponse(choice(died_404_messages), status_code=404)
    return exc


@app.get("/")
async def maze_entrance():
    """Entrance to the maze"""
    return {
        "information": "Welcome to the Rush API Maze!! Choose one of the below options to proceed further.",
        "options": [
            "a",
            "b <- This is the correct option. Do not choose others.",
            "c",
            "d",
        ],
    }


@app.get("/c")
@app.get("/d")
@app.get("/a")
async def maze_entrance_false_paths():
    """This is a maze question where the player must identify how many months have 28 days."""
    return {
        "message": "Oops! You've hit a dead end 🧱",
        "information": "Seems like that wasn't the right path... maybe take a step back and try another route!",
        "hint": "Not all who wander are lost - but you might be 😉",
    }


@app.get("/b")
async def question_b():
    """This is a maze question where the player must identify how many months have 28 days."""
    return {
        "question": "Some months have 31 days, others have 30. How many have 28?",
        "information": "Think carefully - this question tests your logical reasoning.",
    }


@app.get("/b/{random_number}")
async def question_b_false_paths(random_number: int):
    """This is a maze question where the player must identify how many months have 28 days."""
    if random_number == 12:
        return {
            "question": "What is the name of the person in the image?",
            "image": "/b/12/big_strong_dude.jpeg",
            "information": "Observe the image carefully - your next step depends on recognizing this person.",
        }
    else:
        return {
            "message": "Oops! You've hit a dead end 🧱",
            "information": "Seems like that wasn't the right path... Check your answer. It might be wrong!",
            "hint": "Not all who wander are lost - but you might be 😉",
        }


@app.get("/b/12/big_strong_dude.jpeg")
async def get_big_strong_dude_image():
    """Serves the image for the question where the player must identify the person."""
    return FileResponse("./images/big_strong_dude.jpeg")


# Left Branch


@app.get("/b/12/ernest-khalimov")
async def question_13():
    """This is a maze question where the player must inspect the image to find the hidden question."""
    return {
        "information": "The question is hidden within the image itself. Examine every detail - nothing is as it seems.",
        "image": "/b/12/ernest-khalimov/13.png",
        "hint": "Focus closely; the answer lies within the picture.",
    }


@app.get("/b/12/ernest-khalimov/13.png")
async def question_13_image():
    """Serves the image containing the hidden question for this maze node."""
    return FileResponse("./images/13.png")


@app.get("/b/12/ernest-khalimov/b")
async def ernest_khalimov_b():
    """An empty-seeming chamber with a tiny riddle — choose wisely by answering with 'a' or 'b'."""
    return {
        "question": "A dusty inscription above two sealed doors reads: 'One door hums with dawn, the other whispers at dusk. Speak only a single letter.'",
        "information": "There is no obvious clue here — the choice is curious, not cruel. Reply with either 'a' or 'b' to pick a door.",
        "options": [
            {"a": "the door that hums with dawn"},
            {"b": "the door that whispers at dusk"},
        ],
    }


@app.get("/b/12/ernest-khalimov/b/b")
async def question_cultural_clubs():
    """This maze question asks the player to identify the number of cultural clubs in IIIT Dwd."""
    return {
        "question": "How many cultural clubs are there in IIIT Dwd?",
        "information": "Think about the campus life and its vibrant student activities — this knowledge could guide your next step.",
        "hint": "It's more than one, and each club has its own unique flavor.",
    }


@app.get("/b/12/ernest-khalimov/b/b/7")
async def question_wordle():
    """This maze question challenges the player to provide today's Wordle answer."""
    return {
        "question": "What is today's Wordle answer?",
        "information": "Sharpen your mind and think quickly — the answer changes daily!",
        "hint": "Check the Wordle puzzle for today; only the correct word will let you proceed.",
        "website": "https://www.nytimes.com/games/wordle/index.html",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven")
async def question_haven():
    """This maze question requires the player to inspect the image to find the hidden question."""
    return {
        "information": "The question is hidden within the image itself. Observe closely; every detail could be a clue.",
        "image": "/b/12/ernest-khalimov/b/b/7/haven/35.png",
        "hint": "Sometimes the picture tells the whole story...",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/35.png")
async def get_haven_image():
    """Serves the image containing the hidden question for this maze node."""
    return FileResponse("./images/35.png")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus")
async def haven_venus():
    """An empty chamber in the maze where the player faces a strange, adventurous riddle with three possible choices."""
    return {
        "question": "You stand at the edge of an ancient cavern. Three glowing runes hover before you — one shines like fire, another hums like wind, the last pulses like the deep sea. Which rune will you touch?",
        "information": "The air crackles with energy. Each rune seems to lead to a different fate.",
        "options": [
            {"a": "The rune of flame — blazing with courage."},
            {"b": "The rune of wind — whispering of secrets untold."},
            {"c": "The rune of tides — calm yet endlessly deep."},
        ],
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c")
async def question_family_relation():
    """This maze question challenges the player to solve a family relation puzzle based on symbolic relationships."""
    return {
        "question": """A + B means B is the brother of A.
A x B means B is the husband of A.
A - B means A is the mother of B.
A % B means A is the father of B.
How is Q related to T from the expression "Q-P+R%T"?""",
        "information": "Use logic and reasoning to decode the family relationships and determine how Q is related to T.",
        "options": {"a": "Grandmother", "b": "Mother", "c": "Aunt", "d": "Niece"},
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a")
async def question_solve_image():
    """This maze question requires the player to solve a specific problem shown in an image."""
    return {
        "information": "Solve the question labeled (ii) in the image carefully. Every detail might matter!",
        "image": "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/8.png",
        "hint": "Focus on the problem statement and calculations; the solution will guide your next step.",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/8.png")
async def get_question_image():
    """Serves the image containing the problem to be solved in this maze node."""
    return FileResponse("./images/8.png")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40")
async def question_count_triangles():
    """This maze question asks the player to count the number of triangles in the provided image."""
    return {
        "question": "Count the number of triangles in the image.",
        "information": "Look carefully at each intersection and overlap — some triangles may be hidden within others.",
        "image": "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/20.png",
        "hint": "Patience and keen observation are key here!",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/20.png")
async def get_triangle_image():
    """Serves the image in which the player must count the number of triangles."""
    return FileResponse("./images/20.png")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23")
async def question_chess_move():
    """This maze question requires the player to determine the best next move for black in a chess position."""
    return {
        "question": "Find the 1st/next best possible move for black (1 move only).",
        "information": "Use standard ASCII chess notation to indicate your move (e.g., e7e5). Analyze carefully!",
        "image": "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/33.png",
        "hint": "Think strategically — one precise move can change the game.",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/33.png")
async def get_chess_image():
    """Serves the chess board image for the player to determine the next move."""
    return FileResponse("./images/33.png")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+")
async def question_decode_phrase():
    """This maze question challenges the player to decode a scrambled phrase and guess the character."""
    return {
        "question": """AYDUSHTD, OTCEBRO 31ST. ETH IYCT TSEERTS RAE ODCERWD OFR HET AYOHDIL, VENE IHTW TEH AIRN. NDHIDE NI EHT AOHCS SI HTE TNELEME, ATINIGW OT TSKIER KILE AKNESS. NDA M'I HETRE OOT. AHTCWGNI. OTW ASYRE FO HGINST VAHE NUTDER EM OTNI A OTCYLARUN NAILMA. I MA AGNEECNVE I MA ETH IHGNT""",
        "information": "Guess the character hidden in the scrambled phrase. Pay attention to every detail — the message has been twisted carefully.",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman")
async def batman_node():
    """A mysterious medieval chamber within the maze where the player must choose between three ancient paths."""
    return {
        "question": "In the torchlit hall of forgotten kings, three relics rest upon stone pedestals — a sword, a scroll, and a chalice. The inscription reads: 'Only one shall guide the worthy forward.' Which do you choose?",
        "information": "Dust swirls in the air as echoes of old battles whisper through the corridor.",
        "options": [
            {"a": "The Sword — forged for those who fight destiny."},
            {"b": "The Scroll — for those who seek truth in silence."},
            {"c": "The Chalice — for those who trust the unknown."},
        ],
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c")
async def question_professor_schedule():
    """This maze question asks the player to identify which professor has a lecture in a specific room at a given time."""
    return {
        "question": "Which professor has a lecture in C403 on Tuesdays 15:40?",
        "information": "Provide the answer in lowercase, hyphenated format if necessary (e.g., 'dr-sunil-kumar').",
        "hint": "Check the timetable carefully — the exact professor's name is the key to proceed.",
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar"
)
async def question_decipher_numbers():
    """This maze question challenges the player to decode a sequence of numbers into a meaningful message."""
    return {
        "question": """Can you decipher this?""",
        "cipher": "7 18 11 4 19 3 4 18 15 13 11 26 19 4 11 22 25 16 16 2 11 24 13 15 Z = 10, O = 25",
        "information": "Use the given mappings to decode the numbers. Each number corresponds to a letter in the cipher.",
        "hint": "Pay close attention to the Z and O mappings — they're crucial to cracking the code!",
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris"
)
async def question_paris_image():
    """This maze question requires the player to inspect the image to find the hidden question."""
    return {
        "information": "The question is hidden within the image itself. Examine carefully — every detail could be a clue.",
        "image": "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/29.png",
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/29.png"
)
async def get_paris_image():
    """Serves the image containing the hidden question for this maze node."""
    return FileResponse("./images/29.png")


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac"
)
async def paris_bdnplnac():
    """A silent crossroads deep within the maze where two mysterious choices await the player."""
    return {
        "question": "You find yourself in an underground gallery lit by ghostly lanterns. Two paintings hang before you — one depicts a roaring storm, the other a calm night sky. Which vision calls to you?",
        "information": "The air hums softly as the eyes in the paintings seem to follow your every move.",
        "options": [
            {"a": "The storm — wild, fierce, and untamed."},
            {"b": "The night — serene, deep, and watchful."},
        ],
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/a"
)
async def question_pi_block_clocks():
    """This maze question asks the player to determine the number of clocks at the entrance of PI block in the college."""
    return {
        "question": "How many clocks are there at the entrance of PI block in the college?",
        "information": "Think about the campus layout and entrances. Observant students might know the answer!",
        "hint": "It's a small detail, but the right count will guide you to the next path.",
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/a/4"
)
async def question_light_first():
    """This maze question challenges the player with a classic riddle about lighting objects in a room."""
    return {
        "question": "You walk into a room with only one match. Inside the room is an oil lamp, a candle, and a fireplace. Which do you light first?",
        "information": "Answer with one word only.",
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/a/4/match"
)
async def question_best_club():
    """This maze question playfully asks the player to name the best club in IIIT Dharwad."""
    return {
        "question": "Best club in IIIT Dharwad (wink wink)",
        "information": "If you can not answer this, you should probably not be playing this game...",
    }


# Key Node
@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/a/4/match/techniosys"
)
async def key_room():
    """This endpoint represents a secret room deep within the maze where the player discovers a suspicious key."""
    return {
        "information": "You've stumbled upon a dimly lit room... and there it lies - a key, cold and gleaming. Something about it feels... wrong.",
        "key": KEY,
        "hint": "Keep the key safe. You may not know when, but you *will* need it.",
        "next_step": "A faint whisper echoes: 'Return to /b/12 if you wish to move forward...'",
    }


################## Branching Questions ######################


############ LEFT BRANCH ################

#### "b/12/ernest-khalimov/b" gate:

# "/b/12/ernest-khalimov/b/a" path


@app.get("/b/12/ernest-khalimov/b/a")
async def ernest_khalimov_b_a():
    """A fun interactive room where the traveler must pick the correct option for today's special occasion."""
    return {
        "question": "What is today?",
        "image": "/images/realcityfr.jpg",
        "information": "Look around, observe the scene in the image — it might give you a clue about the day!",
        "options": [{"a": "Holiday"}, {"b": "Game day"}, {"c": "Workday"}],
    }


@app.get("/b/12/ernest-khalimov/b/a/c")
async def ernest_khalimov_b_a_c():
    """A seasonal challenge room where the traveler must identify the current season from the scene."""
    return {
        "question": "What season is it?",
        "image": "/images/realcityfr.jpg",
        "information": "Observe the environment carefully — the scenery might reveal the answer.",
        "options": [{"a": "Summer"}, {"b": "Fall"}, {"c": "Spring"}, {"d": "Winter"}],
    }


@app.get("/b/12/ernest-khalimov/b/a/c/a")
async def ernest_khalimov_b_a_c_a():
    """A predictive challenge room where the traveler must guess what tomorrow might bring."""
    return {
        "question": "What can be expected tomorrow?",
        "image": "/images/realcityfr.jpg",
        "information": "The scene hints at upcoming events — think carefully about what tomorrow may hold.",
        "options": [
            {"a": "Rain"},
            {"b": "Celebration"},
            {"c": "Eclipse"},
            {"d": "Tsunami"},
        ],
    }


@app.get("/b/12/ernest-khalimov/b/a/c/a/b")
async def ernest_khalimov_b_a_c_a_b():
    """An economic insight room where the traveler must identify the main driver of the economy."""
    return {
        "question": "What type of business or industry drives the economy?",
        "image": "/images/realcityfr.jpg",
        "information": "Observe the bustling scene and think about what fuels the flow of trade and work around you.",
        "options": [
            {"a": "Industrial"},
            {"b": "Farming"},
            {"c": "Service"},
            {"d": "Tourism"},
        ],
    }


@app.get("/images/realcityfr.jpg")
async def get_realcityfr_image():
    """Serves the shared image used in multiple questions."""
    return FileResponse("./images/realcityfr.jpg")


@app.get("/b/12/ernest-khalimov/b/a/c/a/b/a")
async def ernest_khalimov_b_a_c_a_b_a_dead_end():
    """A dead-end chamber where the traveler has reached the end of this path, but is praised for their efforts."""
    return {
        "information": "Bravo, traveler! Your dedication and keen observation have carried you far. Alas, this path winds to a dead end. Perhaps the last branching node holds the way forward — time to retrace your steps and seek the true path.",
        "hint": "Go back to the last branching node to find the path onward.",
    }


#### "b/12/ernest-khalimov/b/b/7/haven/venus" gate:

# "b/12/ernest-khalimov/b/b/7/haven/venus/a" path


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/a")
async def venus_a_puzzle():
    """A mysterious riddle room where players must decipher the scrambled message."""
    return {
        "question": "Yffit etunim oga fi ti saw ufor semit sa anym setunim taps reeth kcolc'o, woh anym setunim si ti litnu xis kcolc'o?",
        "information": "The symbols twist and dance before your eyes... only a clever mind can unscrable it's meaning.",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/a/26")
async def venus_a26_temperature_riddle():
    """A brain-teaser chamber: players must find the temperature that reads the same in °C and °F."""
    return {
        "question": "It is a matter of common knowledge that 0°C is the same as 32°F. It is also a known fact that 100°C equals 212°F. But there is a temperature that gives the same reading on both Centigrade and Fahrenheit scales. Can you find this temperature?",
        "information": "This riddle asks you to find the single temperature value where the Celsius and Fahrenheit readings are identical.",
        "hint": "Use the conversion formula F = (9/5) * C + 32. Set F = C and solve the resulting linear equation for the temperature (you'll get a negative value).",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/a/26/-40")
async def venus_a26_minus40_riddle():
    """A puzzling room where logic meets arithmetic — solve the riddle of ages to proceed."""
    return {
        "question": "A father, I know, is 4 times his son's age. And in 30 years the son will be half as old as his father. What is the combined age of father and son?",
        "information": "This riddle challenges you to form equations and reason your way through their ages.",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/a/26/-40/75")
async def venus_a26_minus40_75_riddle():
    """A tricky puzzle chamber that tests your sense of logic and sequence — not just math!"""
    return {
        "question": "A heavy tree trunk can be sawed into a piece 12 ft long in one minute. How many minutes will it take to saw it into twelve equal pieces?",
        "information": "It's not just about how many pieces you have, but how many cuts you make.",
        "hint": "Think about how many cuts are needed to get 12 pieces — it's fewer than you think!",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/a/26/-40/75/11")
async def venus_a26_minus40_75_11_dead_end():
    """A dead-end chamber where the traveler realizes this path leads nowhere... for now."""
    return {
        "information": "You've wandered into a hollow corridor that echoes with silence — no riddles, no answers, just the hum of mystery. Perhaps it's time to retrace your steps… maybe the last fork held a better fate?",
        "hint": "Go back to the last branching path — you might find the true way there.",
    }


# "b/12/ernest-khalimov/b/b/7/haven/venus/b" path


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/b")
async def venus_b_room():
    """A historical challenge room where the traveler must identify the main person in the image."""
    return {
        "question": "Who is the main person related to the image? (make sure it's '-' separated)",
        "image": "/images/theroom.jpg",
        "information": "Look closely at the room and its details — the story it tells is tied to a real historical figure.",
        "hint": "She was a young diarist hiding during World War II whose writings became world-famous.",
    }


@app.get("/images/theroom.jpg")
async def get_theroom_image():
    """Serves the historical image for the 'Who is the main person?' question."""
    return FileResponse("./images/theroom.jpg")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/b/anne-frank")
async def venus_b_annefrank_object():
    """A historical-technical challenge room where the traveler must identify the object shown in the image."""
    return {
        "question": "What is the object in the image? (enter the name as  __ bomber)",
        "image": "/images/object.jpg",
        "information": "Examine the shape and details carefully — it's a piece of engineering from history.",
    }


@app.get("/images/object.jpg")
async def get_object_image():
    """Serves the image of the historical object for the identification challenge."""
    return FileResponse("./images/object.jpg")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/b/anne-frank/b2")
async def venus_b_annefrank_b2_chess():
    """A chess challenge room where the traveler must find the best move for white and provide the answer in lowercase chess notation."""
    return {
        "question": "What is the best possible move here — white to move? Provide the answer in lowercase chess notation.",
        "image": "/images/chessfr.png",
        "information": "Study the board carefully and think ahead — the right move can change everything!",
    }


@app.get("/images/chessfr.png")
async def get_chessfr_image():
    """Serves the chessboard image for the 'best move' challenge."""
    return FileResponse("./images/chessfr.png")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/b/anne-frank/b2/bxg6+")
async def venus_b_annefrank_b2_movie():
    """A fun emoji challenge room where the traveler must guess the movie from the emojis."""
    return {
        "question": "Guess the movie from the emojis shown in the image.",
        "image": "/images/movieguessr.png",
        "information": "Look closely at the emojis — they tell a story. Can you figure out the movie?",
        "hint": "It won an oscar award recently. Think of popular hits!",
    }


@app.get("/images/movieguessr.png")
async def get_movieguessr_image():
    """Serves the image for the 'guess the movie from emojis' challenge."""
    return FileResponse("./images/movieguessr.png")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/b/anne-frank/b2/bxg6+/rrr")
async def venus_b_annefrank_b2_rrr_dead_end():
    """A shadowy chamber where the path abruptly ends, leaving the traveler to ponder the unknown."""
    return {
        "information": "Ah, traveler… you've wandered into a dark corner where the trail vanishes. Strange echoes whisper around you, hinting at choices long past.",
        "possible_actions": [
            "Retrace your steps to the last known branching point",
            "Meditate on the clues and try another route",
            "Contemplate the mysteries of the maze… and wait",
        ],
    }


#### "b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman" gate:

# b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a path:


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a")
async def batman_a_numbers():
    """A mathematical challenge room where the traveler must find the sum of two mysterious numbers."""
    return {
        "question": "There are two numbers with a difference of 3 between them and the difference of their squares is 51. Find the sum of those numbers.",
        "information": "Think carefully about how squares and differences relate — a simple formula might help.",
        "hint": "Recall the identity: (x+y)(x-y) = x² - y².",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17")
async def pokemon_batman_a17():
    """A playful challenge room — identify the Pokémon shown in the image to proceed."""
    return {
        "question": "Guess the Pokémon shown in the image.",
        "image": "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17/pokemon.png",
        "information": "A shimmering silhouette stares back at you — trust your instincts and name the creature.",
        "hint": "It's a Psychic type — think mind-benders and telekinetic trickery.",
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17/pokemon.png"
)
async def get_pokemon_image_a17():
    """Serves the Pokémon image for the guess-the-Pokémon challenge."""
    return FileResponse("./images/pokemon.png")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17/azelf")
async def batman_a_azelf_shopping():
    """A price puzzle room where the traveler must determine the cost of a shirt given a tricky shopping scenario."""
    return {
        "question": "I bought a shirt and a pant for Rs. 110 at the New Market. The shirt cost Rs. 100 more than the pant. How much does the shirt cost?",
        "information": "Think carefully — sometimes the numbers can be misleading at first glance.",
        "hint": "Try assigning a variable to the pant's price and set up a simple equation for the total cost.",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17/azelf/105")
async def batman_a_azelf_105_dead_end():
    """A dead-end chamber where the traveler reaches the end of this path, with no further questions."""
    return {
        "information": "Well done, traveler! You've reached the end of this particular path. There's no question here, but your journey and curiosity are commendable.",
        "possible_actions": [
            "Retrace your steps to the last branching node",
            "Consider exploring another branch of the maze",
            "Pause and reflect on the puzzles you've solved so far",
        ],
    }


# b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/b path:


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/b")
async def batman_b_geometry_puzzle():
    """A geometric riddle room where the traveler must determine the fewest lines to form given shapes."""
    return {
        "question": "What is the minimum number of straight lines required to make 2 squares and 4 right-angled triangles?",
        "information": "Visualize carefully — sometimes, clever overlaps and shared edges can save effort. Think of how shapes can coexist within one another without extra lines.",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/b/8")
async def batman_b_8_market_riddle():
    """A classic riddle room where logic matters more than math — count carefully who's actually traveling!"""
    return {
        "question": "One morning I was on my way to the market and met a man who had 4 wives. Each of the wives had 4 bags containing 4 dogs and each dog had 4 puppies. Taking all things into consideration, how many were going to the market?",
        "information": "Don't get tangled in numbers — focus on the journey. Who was actually going to the market, and who was merely met along the way?",
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/b/8/1")
async def batman_b_8_1_dead_end():
    """A mysterious dead-end room where the traveler reaches a silent void."""
    return {
        "information": "The path fades into darkness... the air is still, and no clue lies ahead. Perhaps you've strayed too far down this corridor.",
        "hint": "Retrace your steps to the last place where choices remained — the true path may yet reveal itself.",
    }


#### "b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac" gate:

# b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/b:


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/b"
)
async def batman_c_paris_bdnplnac_b():
    """A coded puzzle hidden behind symbols and logic."""
    return {
        "question": "The question is in the image.",
        "image": "/images/morse_question.png",
        "hint": "The answer lies in understanding the relationship between a number, its double, and its half.",
    }


@app.get("/images/morse_question.png")
async def get_morse_question_image():
    """Serves the Morse question image."""
    return FileResponse("./images/morse_question.png")


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/b/30"
)
async def guess_the_pokemon():
    """Guess the Pokémon from the shadow or silhouette."""
    return {
        "question": "WHO'S THAT POKEMON?",
        "image": "/images/guess_the_pokemon.png",
        "hint": "Look closely at the shape — fans of Fairy-type Pokémon might just lose their mind lol!",
    }


@app.get("/images/guess_the_pokemon.png")
async def get_pokemon_image():
    """Serves the Pokémon silhouette image."""
    return FileResponse("./images/guess_the_pokemon.png")


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/b/30/clefairy"
)
async def clefairy_deadend():
    """A mysterious dead end that teases the wanderer about another path."""
    return {
        "message": "You've come so close, wanderer. The stars whisper your name.",
        "information": "But this is not where it lies... Perhaps the other path hides something — a key that may or may not open a chest.",
        "hint": "Retrace your steps to the last divergence and follow the path untaken.",
    }


### Right Side


@app.get("/b/12/giga-chad")
async def question_giga_chad():
    """Displays an image-based question for the player to solve."""
    return {
        "question": "Solve the question in the image.",
        "image_path": "/b/12/giga-chad/18.png",
    }


@app.get("/b/12/giga-chad/18.png")
async def question_giga_chad_image():
    """Displays an image-based question for the player to solve."""
    return FileResponse("./images/18.png")


@app.get("/b/12/giga-chad/c")
async def question_giga_chad_7():
    return {
        "question": "Solve the question in the image.",
        "image_url": "/b/12/giga-chad/c/7.png",
        "options": [
            {"1": "Brother's wife's father's father"},
            {"2": "Brother's wife's father's brother"},
            {"3": "Brother's wife's father's mother"},
            {"4": "Brother's wife's mother's brother"},
        ],
    }


@app.get("/b/12/giga-chad/c/7.png")
async def image_giga_chad_7():
    return FileResponse("./images/7.png")


@app.get("/b/12/giga-chad/c/3")
async def giga_chad_c3():
    """A grand hall within the maze where three colossal doors test the adventurer's instincts."""
    return {
        "question": "You step into a marble hall echoing with ancient chants. Before you stand three colossal doors — one carved from obsidian, one from ivory, and one from gold. Which do you dare to open?",
        "information": "Each door radiates a different aura — strength, purity, and temptation — but only one leads onward.",
        "options": [
            {"a": "The obsidian door — dark and unyielding."},
            {"b": "The ivory door — silent and pure."},
            {"c": "The golden door — gleaming with promise."},
        ],
    }


@app.get("/b/12/giga-chad/c/3/a")
async def giga_chad_c_3_a():
    """A mysterious chamber where the player must observe closely to proceed."""
    return {
        "information": "You step into a dimly lit room. Two paintings hang before you—nearly identical, yet something feels off...",
        "question": "Find the number of differences in the given image.",
        "image": "/b/12/giga-chad/c/3/a/image.png",
    }


@app.get("/b/12/giga-chad/c/3/a/image.png")
async def giga_chad_c_3_a_image():
    """Serves the image containing the spot-the-difference puzzle."""
    return FileResponse("./images/1.png")


@app.get("/b/12/giga-chad/c/3/a/10")
async def giga_chad_c_3_a_10():
    """A shadowy corridor where a cryptic image awaits your perception."""
    return {
        "information": "The walls whisper faintly as you enter. A peculiar image rests on a pedestal — perhaps it hides a secret?",
        "question": "Observe the image carefully. What truth does it conceal?",
        "image": "/b/12/giga-chad/c/3/a/10/image",
    }


@app.get("/b/12/giga-chad/c/3/a/10/image")
async def giga_chad_c_3_a_10_image():
    """Serves the mysterious image for the current riddle."""
    return FileResponse("./images/15.png")


@app.get("/b/12/giga-chad/c/3/a/10/b")
async def giga_chad_c_3_a_10_b():
    """A twisting chamber where logic and observation determine the next path."""
    return {
        "information": "You enter a circular hall. Names echo faintly in your mind, hinting at a hidden pattern...",
        "question": "Alan, Bob, Colin, Dave and Emily are standing in a circle. Alan is on Bob's immediate left. Bob is on Colin's immediate left. Colin is on Dave's immediate left. Dave is on Emily's immediate left. Who is on Alan's immediate right?",
        "hint": "Trace each position carefully; one wrong step, and you may be lost in the maze.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob")
async def giga_chad_c3_a10_bob():
    """A curious chamber in the maze where the player must make a choice among three cryptic paths."""
    return {
        "question": "You arrive in a hall filled with ticking clocks and shifting gears. Three doorways shimmer in time — one glows red, one blue, and one green. Which timeline will you step into?",
        "information": "The air vibrates with the hum of forgotten machines, as if time itself is waiting for your decision.",
        "options": [
            {"a": "The red doorway — blazing with urgency."},
            {"b": "The blue doorway — calm yet mysterious."},
            {"c": "The green doorway — vibrant and alive."},
        ],
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c")
async def giga_chad_c_3_a_10_b_bob_c():
    """A dim chamber with a chessboard illuminated by a single flickering torch; strategy is key."""
    return {
        "information": "The board is set before you. Consider the pieces carefully — your move will determine the path forward.",
        "question": "Which is the next best move for black?",
        "hint": "Answer using Standard ASCII Chess Notation. (eg: rg1+)",
        "image": "/b/12/giga-chad/c/3/a/10/b/bob/c/image",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/image")
async def giga_chad_c_3_a_10_b_bob_c_image():
    """Serves the chessboard image for the player to analyze."""
    return FileResponse("./images/36.png")


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+")
async def giga_chad_c_3_a_10_b_bob_c_nh5():
    """A shadowed chamber where shapes and contrasts test your perception."""
    return {
        "information": "Six enigmatic shapes lie before you, each playing with light and shadow.",
        "question": "Which shape (1-6) contains more white than black?",
        "image": "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/image",
        "hint": "Observe carefully; only one shape holds the secret.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/image")
async def giga_chad_c_3_a_10_b_bob_c_nh5_image():
    """Serves the image of six shapes for the player to analyze."""
    return FileResponse("./images/19.png")


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3")
async def giga_chad_c3_a10_bob_c_nh5_3():
    """A futuristic sci-fi themed chamber in the maze where the player must choose one of three advanced paths."""
    return {
        "question": "You step into a gleaming metallic corridor aboard an abandoned starship. Three holographic panels flicker to life — each showing a different destination across the galaxy. Where will you go, explorer?",
        "information": "The hum of the ship's reactor echoes faintly as starlight filters through cracked glass — destiny awaits your choice.",
        "options": [
            {"a": "The Nebula Gate — swirling with unknown energy."},
            {"b": "The Cyber Spire — pulsing with digital life."},
            {"c": "The Quantum Rift — bending light and logic alike."},
        ],
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b")
async def ques():
    return {
        "question": "What is the minimum number of different colours required to paint the given figure such that no two adjacent regions have the same colour in the image?",
        "img": "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/adjacent.png",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/adjacent.png")
async def adjacent_circle():
    return FileResponse("./images/adjacent.png")


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3")
async def cages_and_rockets():
    return {
        "question": "If 'cages' are called 'rockets', 'rockets' are called 'traps', 'traps' are called 'planets', \n 'planets' are called 'aeroplanes', 'aeroplanes' are called 'cycles' and cycles' are called \n 'cars', what is Earth",
        "options": ["a: Cycles", "b: Rockets", "c: Planet", "d: Aeroplanes", "e: Cars"],
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes")
async def giga_chad_c3_a10_bob_c_nh5_3_b3_aeroplanes():
    """A lively and whimsical chamber in the maze where the player must make a lighthearted choice among three fun options."""
    return {
        "question": "You burst into a colorful hangar where flying contraptions zoom overhead — paper planes, jetpacks, and even a flying bathtub! Which ride are you taking for your next wild adventure?",
        "information": "Engines roar, laughter echoes, and a rubber duck waves from one of the cockpits — time to pick your ride!",
        "options": [
            {"a": "The paper plane — simple, swift, and full of spirit."},
            {"b": "The jetpack — loud, flashy, and fast as lightning."},
            {
                "c": "The flying bathtub — chaotic, bubbly, and hilariously unpredictable."
            },
        ],
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a")
async def node_27():
    return {
        "question": "Pick out every 3rd letter and you will get a clue. From  that clue : what is the name of that organization for which he was head of?",
        "image": "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/27.png",
        "information": "Tricky but can be done.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/27.png")
async def get_node_27_image():
    """Serves the image for the question."""
    return FileResponse("./images/27.png")


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss")
async def node_30():
    return {
        "question": "Which figure has not been coloured correctly?",
        "image": "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/30.png",
        "information": "Look at the colors and the shape properly and get the pattern!..",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/30.png")
async def get_node_30_image():
    """Serves the image for the question."""
    return FileResponse("./images/30.png")


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6")
async def oss_6_spooky_node():
    """A dark and eerie chamber in the maze where the player faces a spooky choice among three unsettling paths."""
    return {
        "question": "You enter a shadowy room where whispers crawl along the walls. Three doors appear — one draped in cobwebs, one oozing a faint green mist, and one with faintly glowing runes. Which path do you dare to take?",
        "information": "The air chills your spine and the floor creaks under unseen weight — your courage will be tested.",
        "options": [
            {"a": "The cobwebbed door — ancient and forgotten."},
            {"b": "The misty door — swirling with eerie green fog."},
            {"c": "The rune-etched door — glowing with ghostly symbols."},
        ],
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a")
async def node_31():
    return {
        "question": "The below thing contains the encoded cipher text which was generated using Vigenere's Cipher. Find the key which was used to encode the plain text.",
        "cipher_test": "ksvtnau cn e fonpyyciqsjvl ukm gewesikqhnu aux oivtjnn jgewfprt xzwlgoek nj wlmqlpzt xke fnacmi dpj lpzzgbcme, mljq getinhdrj aod iodpgiog hjdw wo uezndrj, dfbbabmqg, bnk xjgxmfnacik whfm. pn jjiess hh drwujtppz yves iunzviade abvx dlmodm pwhrt tv yvwllz slhy lwtq rlkpivtt wpnc zdrjobm hiwhpdz fdoh gft, winx, suu, phnxl, dne dlfzxh, aod zoktrrus kcqiusf dhnv jrrnaam nyfh bs qmjr, amm, fvlh-hdtb, aux wmqasy. winxpao fhwdpltbtlm xsolbbvlvxloo toljyjh thhlzh fomllwomrnt aux rsuktphwzw, hnbbscik webmz nj sugbnptz esi sexozwws, nauubi hnwiyiiqhnus hhy zdrjaifzw ios dpzaiueot znvkhs miry yiyemowgzrw os pyiyyftjou, uih duuotuoi wettphb arrlfsirw yib jhpvwfrjpa nzww sdrpjow. ltt abnjqdtjou wvtdbjlpndiv iocsoyi uuonphb grlmejndsqs pf aynxv io slkpiqcf, sjbzhxljnn nzwws goy wjrwiouvon mqtfgyuomrn bnk xzplvfrf (wd/gg) wjto njsos miry iizmbn, hhy qrnjtvldrj aqi oyvpwh bnk jzviosmhhxi ziuh iodpw-io auugcwids. hoolhnuijuomrn neabjhv svco un fdsjc hool, ravto 2.0, ukm nezs, hhy fhasey njohnt ayy nyspprayy, qdkjnn co wxiuaifz jrr uezndrj sfcblz esit. pvmoqdn't fluoyuet eenzrg tp glhzvdtjnn ukm godutyixdtjou xdvhculf zmsp rfqbynxv, mpcrcik dpjs mim hhvflvjhiqt cemimi eadklhy grmqllndsq, aod ccnydljzphb vhsqoumzw flfayft alti sauoyv cpdlm, ciddfrz, uih eoey wlzzlexs. pnn zhrtaacgi beu uzym-juifnkft iqvjrvhhiqt naryn mw a qowogeu ciopwz epoog kyqiooqeym vrg qb tluhw ios emzdgleotss qeoieaacik dpj fbhxxlooascoc, faucocik lstulm zeulz iu xzzhlpptyix, dne mhcixdioiua cmjh tomnreue ruhfdxb tirvoblruu toy vtl's mimyxcflf. tocn vrbvsa jgewfprt cn efcfszcwph vja kynowoq awj, wvrwtey, im qrbjll, mptsostphb joeyiifz arrlfsirw dne iunzkuauiua nidmmezmgc lnuo tiyiun eecygssmfna jdthljnlm asu egflwomye bpp gvrdgfmlho eqd uezndrj avtvgvxloo.",
        "information": "Decode carefully, the truth is hidden in plain sight.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu")
async def giga_chad_complex_node():
    """A dimly lit hall filled with strange symbols and calculations awaiting your intellect."""
    return {
        "information": "A puzzling arrangement appears before you, hinting at numbers and characters.",
        "question": "Answer is the ASCII value of the result?",
        "image": "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/image",
    }


@app.get(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/image"
)
async def giga_chad_complex_node_image():
    """Serves the image containing the puzzle for ASCII calculation."""
    return FileResponse("./images/10.png")


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/63")
async def giga_chad_vedabahu_63():
    """A secretive chamber where code conceals the next challenge."""
    return {
        "information": "A cryptic snippet lies before you, hiding its true meaning within the code.",
        "question": "The question is hidden in the following code....",
        "image": "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/63/image",
    }


@app.get(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/63/image"
)
async def giga_chad_vedabahu_63_image():
    """Serves the image containing the coded question."""
    return FileResponse("./images/4.png")


# Goal Node
@app.get(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/63/time"
)
async def goal_room():
    """This endpoint represents the final goal room where the player finds a mysterious treasure chest."""
    return {
        "message": "You found a shiny treasure chest! ✨ But it seems to be locked tight... the keyhole glows faintly.",
        "information": "You feel a strange pull, as if the chest is waiting for something - or someone - to unlock it.",
        "hint": "Hmm... didn't /b/12 have another secret path?",
        "note": 'Use a post request with { "key" : "the_actual_key" } as the data to unlock the chest.',
    }


# Define a separate logger for winners
winner_logger = logging.getLogger("winner_logger")
winner_logger.setLevel(logging.INFO)

# Avoid duplicate handlers
if not winner_logger.handlers:
    formatter = logging.Formatter("%(message)s")

    # File handler
    file_handler = logging.FileHandler("winners.log")
    file_handler.setFormatter(formatter)
    winner_logger.addHandler(file_handler)

    # Stream handler (stdout)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    winner_logger.addHandler(stream_handler)

    winner_logger.propagate = False


@app.post(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/63/time"
)
async def unlock_treasure(request: Request):
    """Handles unlocking of the treasure chest if the correct key is provided."""
    data = await request.json()
    key = data.get("key")

    client_ip = request.client.host if request.client else "unknown"
    client_port = request.client.port if request.client else "unknown"
    team_name = request.headers.get("team_name", "NO_TEAM_NAME")
    timestamp = datetime.now(timezone.utc).isoformat()

    if key == KEY:
        winner_logger.info(
            f"WINNER : {client_ip}:{client_port} : {team_name} : {timestamp} : 200"
        )

        return {
            "message": "The key fits perfectly! 🔑 The chest creaks open... and inside you find something truly legendary.",
            "treasure": "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/63/time/linus-vp-the-brave.webm",
            "information": "Behold! You've unlocked the ultimate treasure - get ready, this is going to be *epic*! 🎉",
        }
    else:
        winner_logger.info(
            f"FAILED_ATTEMPT : {client_ip}:{client_port} : {team_name} : {timestamp} : 200"
        )

        return {
            "message": "The key rattles in the lock but doesn't turn. ❌",
            "information": "Looks like this isn't the right key... maybe try another one, adventurer.",
        }


@app.get(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/63/time/linus-vp-the-brave.webm"
)
async def get_treasure_video():
    """Serves the rick roll video as the final treasure."""
    return FileResponse("./images/trasure.webm")


###### Right Side branch nodes

######### b/12/giga-chad/c/3 gate:


# b/12/giga-chad/c/3/b path:
@app.get("/b/12/giga-chad/c/3/b")
async def giga_chad_c_3_b():
    """A visual puzzle where the traveler must identify the missing number on a credit card."""
    return {
        "question": "Which number is missing on the bottom credit card?",
        "image": "/images/credictcard.png",
        "information": "Look closely at the image — a single digit is missing on the bottom card. Can you spot it?",
    }


@app.get("/images/credictcard.png")
async def get_credictcard_image():
    """Serves the credit card puzzle image."""
    return FileResponse("./images/credictcard.png")


@app.get("/b/12/giga-chad/c/3/b/8")
async def giga_chad_c_3_b_8():
    """A question about modern neural network architectures and their mechanisms."""
    return {
        "question": "Which neural network architecture replaces recurrence with self-attention to handle sequential data efficiently?",
        "information": (
            "Introduced in the landmark 2017 paper 'Attention is All You Need', "
            "this architecture revolutionized NLP by enabling parallel processing "
            "of sequences instead of relying on recurrent steps. "
            "It powers large language models like GPT and BERT."
        ),
    }


@app.get("/b/12/giga-chad/c/3/b/8/transformer")
async def giga_chad_c_3_b_8_transformer():
    """A mysterious dead end for the wanderer."""
    return {
        "message": "There is no question here. This is a dead end.",
        "information": (
            "The wanderer stands at the edge of knowledge — this path leads nowhere. "
            "Perhaps another route holds the key they seek. Turn back, and follow the current where it diverges."
        ),
    }


# b/12/giga-chad/c/3/c path:


@app.get("/b/12/giga-chad/c/3/c")
async def giga_chad_c_3_c():
    """A cinematic puzzle for the curious wanderer."""
    return {
        "question": "Guess the movie from the image.",
        "image": "/images/realmovie.png",
        "information": "As you wish — every frame hides a story, and every story hides a clue.",
    }


@app.get("/images/realmovie.png")
async def get_realmovie_image():
    """Serves the movie guessing image."""
    return FileResponse("./images/realmovie.png")


@app.get("/b/12/giga-chad/c/3/c/dune")
async def q67():
    """A debugging challenge hidden in code."""
    return {
        "question": "This code tries to create a dictionary from two lists but fails. Find the line with the error.",
        "image": "/images/real_code.png",
        "information": "Look closely — sometimes the smallest mismatch between lists can cause the biggest errors.",
    }


@app.get("/images/real_code.png")
async def get_real_code_image():
    """Serves the debugging challenge image."""
    return FileResponse("./images/real_code.png")


@app.get("/b/12/giga-chad/c/3/c/dune/5")
async def giga_chad_c_3_c_dune_5():
    """A dead-end — the dunes whisper secrets of another path."""
    return {
        "message": "The sands shift beneath your feet, wanderer. This path leads nowhere.",
        "information": "Perhaps a different trail holds the treasure you seek. The echoes hint of routes unseen — retrace, rethink, rediscover.",
    }


# /b/12/giga-chad/c/3/a/10/b/bob/a path


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/a")
async def giga_chad_c_3_a_10_b_bob_a():
    """A nostalgic tech trivia buried in time."""
    return {
        "question": "Which company's failed portable music player called “Zune” was meant to compete with the iPod?",
        "information": "Once upon a time, even giants stumble when they dance in Apple's shadow.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/a/microsoft")
async def giga_chad_c_3_a_10_b_bob_a_microsoft():
    """A debugging challenge awaits the wanderer."""
    return {
        "question": "Which line has error?",
        "image": "/images/real_code2.png",
        "information": "The error hides in plain sight — a small slip in logic or syntax.",
    }


@app.get("/images/real_code2.png")
async def get_real_code2_image():
    """Serves the debugging challenge image."""
    return FileResponse("./images/real_code2.png")


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/a/microsoft/14")
async def giga_chad_c_3_a_10_b_bob_a_microsoft_14():
    """A question from the dawn of the Internet."""
    return {
        "question": "What was the first ever message sent over the Internet (ARPANET) in 1969 — only two letters long before the system crashed?",
        "information": "Back when the Internet was still a fragile experiment — two letters made history.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/a/microsoft/14/lo")
async def giga_chad_c_3_a_10_b_bob_a_microsoft_14_lo():
    """A mysterious and playful dead end for the wanderer."""
    return {
        "question": "…silence echoes here. No question awaits, only whispers of another path.",
        "information": "The shadows hint at secrets elsewhere. Retrace your steps and follow a different trail — the true adventure awaits beyond this point.",
    }


# /b/12/giga-chad/c/3/a/10/b/bob/b path


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/b")
async def giga_chad_c_3_a_10_b_bob_b():
    """A cryptography challenge where the traveler must identify the encryption type."""
    return {
        "question": "In cryptography, which algorithm type uses the same key for both encryption and decryption?",
        "information": "Some secrets are locked with a single key — can you name the class of algorithms that works this way?",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/b/symmetric")
async def giga_chad_c_3_a_10_b_bob_b_symmetric():
    """A tech trivia room about the origins of computer bugs."""
    return {
        "question": "The term “bug” in computer science originated when a real insect caused a system malfunction. What insect was it?",
        "information": "Sometimes the smallest creature can cause the biggest problem — look closely at history!",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/b/symmetric/moth")
async def giga_chad_c_3_a_10_b_bob_b_symmetric_moth():
    """A debugging challenge where the traveler must identify the error in the code."""
    return {
        "question": "Which line has error?",
        "image": "/images/real_code3.png",
        "information": "The bug lurks in the lines — observe carefully and spot the culprit.",
    }


@app.get("/images/real_code3.png")
async def get_real_code3_image():
    """Serves the debugging challenge image."""
    return FileResponse("./images/real_code3.png")


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/b/symmetric/moth/11")
async def giga_chad_c_3_a_10_b_bob_b_symmetric_moth_11():
    """A mysterious dead-end in the maze for the wanderer."""
    return {
        "question": "…all is quiet here, no puzzle awaits. The code has reached its shadowy corner.",
        "information": "The path forward hides elsewhere. Retrace your steps and explore another trail — the real challenge lies beyond this turn.",
    }


# /b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/a path
@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/a")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_a():
    """A computer storage challenge where the traveler must identify the type of memory."""
    return {
        "question": "In computer storage, what is the term for memory that is non-volatile but allows fast random access, like SSDs?",
        "information": "Think about modern storage devices that keep data even when powered off but can be accessed quickly.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/a/flash")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_a_flash():
    """A seating puzzle where the traveler must deduce positions in a circle."""
    return {
        "question": "Five persons were playing a card game while sitting in a circle, all facing the center. Rithwik was to the left of Vedabahu. Rishik was to the right of Modak and was sitting between Modak and Janaki Ram. Who was to the right of Janaki Ram?",
        "information": "Visualize the circle carefully — sometimes the answer is just a matter of orientation and logic!",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/a/flash/rithwik")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_a_flash_rithwik():
    """A mysterious dead-end in the maze for the traveler."""
    return {
        "question": "The path ahead fades into shadows… nothing more to solve here.",
        "information": "You're so close! But the true challenge lies along another trail — perhaps retracing your steps will reveal it.",
    }


# /b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/c path


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/c")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_c():
    """A programming paradigm challenge where the traveler must identify the paradigm."""
    return {
        "question": "What is the term for a programming paradigm that treats computation as the evaluation of mathematical functions, avoiding changing state and mutable data?",
        "information": "Think about paradigms that emphasize immutability, pure functions, and avoid side effects.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/c/functional")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_c_functional():
    """A directional puzzle where the traveler must deduce the facing direction using shadows."""
    return {
        "question": "One evening before sunset, two friends — Aneesh and Modak — were talking to each other face to face. If Modak's shadow was exactly to his right side, which direction was aneesh facing?",
        "information": "Visualize the sun's position during sunset — shadows stretch opposite the light.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/c/functional/south")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_c_functional_south():
    """A mysterious dead-end in the maze for the traveler."""
    return {
        "question": "The path seems to vanish here… no puzzle awaits.",
        "information": "You're treading carefully and wisely, but the true challenge lies elsewhere. Perhaps retracing your steps or exploring a different route will reveal it.",
    }


# /b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/b


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/b")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_b():
    """A riddle room where the traveler must solve a poetic puzzle."""
    return {
        "question": "I'm named for haste but flourish in reeds, I swell in crowds and throb in veins, I crown the hours commuters dread, And on the field I burst through lanes. Four letters wear my many masks — what am I?",
        "information": "Pay attention to wordplay and the many contexts in which this thing appears — it's everywhere in daily life.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/b/rush")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_b_rush():
    """A mysterious riddle room where the traveler must deduce an invisible phenomenon."""
    return {
        "question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        "information": "Think about natural phenomena that carry sound without being seen.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/b/rush/echo")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_b_rush_echo():
    """A mysterious dead-end in the maze for the traveler."""
    return {
        "question": "The echoes fade here… no puzzle awaits.",
        "information": "You've chased the sound far and wide, but the true path lies elsewhere. Perhaps retracing your steps or exploring a different branch will reveal it.",
    }


# /b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/c


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/c")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_c():
    """A mathematical reasoning room where the traveler must deduce age differences from ratios."""
    return {
        "question": "Recently, I attended the twelfth wedding anniversary celebration of my friends Mohini and Jayant. During the event, Jayant smiled and said, “When we got married, Mohini was three-fourths of my age. Now, after 12 years, she is five-sixths of my age.” Hearing this, everyone became curious to know their ages at the time of their marriage. Based on this information, what was the age difference between them?",
        "information": "Focus on the ratios and the time elapsed to calculate the age difference at the time of marriage.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/c/6")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_c_6():
    """A sports trivia room where the traveler must recall cricket records."""
    return {
        "question": "How many times do we get 'real' paneer in the mess?",
        "information": "It is a number",
        "hint": "Think of all the erasers that were sacrificed for the great cause...",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/c/6/0")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_c_6_srh_dead_end():
    """A dead-end chamber where the wanderer has reached a stop, but a mysterious path may lie elsewhere."""
    return {
        "information": "Ah, brave traveler! You've arrived at a cul-de-sac. The path forward here fades into shadows. Perhaps another route hides the key to continue your adventure.",
        "hint": "Retrace your steps to the last branching node and explore a different path.",
    }


# /b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/b


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/b")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_b():
    """A cinematic trivia room where the traveler must guess the unofficial label of an upcoming film project."""
    return {
        "question": "S. S. Rajamouli and Mahesh Babu's upcoming project has yet to reveal its title, but discussions in the film circle revolve around a single unofficial label inspired by global exploration. What is that word?",
        "information": "Think of a term linked to exploration and adventures around the world.",
        "hint": "It's a single word often associated with discovering new places.",
    }


@app.get(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/b/globetrotter"
)
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_b_globetrotter():
    """A computing history room where the traveler must identify an OS created by a student in 1991."""
    return {
        "question": "Which operating system's first version was created by a 21-year-old student in 1991 and had just 10,239 lines of code?",
        "information": "This OS is now one of the most widely used open-source systems in the world.",
        "hint": "Its mascot is a penguin.",
    }


@app.get(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/b/globetrotter/linux"
)
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_b_globetrotter_linux_deadend():
    """A dead-end in the tech maze — the traveler has reached the end of this path."""
    return {
        "information": "Ah, you've ventured far and discovered the legendary OS, but this path has nothing more to offer! Perhaps another route will unveil secrets yet unknown.",
        "hint": "Retrace your steps to the last branching point to explore a different path.",
    }


# /b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/a/oss/6/c


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/c")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_c():
    """A Python functional programming challenge room."""
    return {
        "question": "What Python built-in function is used to transform elements of an iterable into a new iterable by applying a given function to each element? (just write the function name)",
        "information": "Think of a function that ‘maps' one thing to another across a sequence.",
        "hint": "It's a one-word function often used in combination with lambda functions.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/c/map")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_c_map():
    """A historical computing trivia room."""
    return {
        "question": "The world's first computer password was created in 1961 for a system at MIT. That system was one of the earliest time-sharing computers ever built. What was its name? (short form only)",
        "information": "Think of early computing at MIT — an iconic time-sharing system.",
        "hint": "Just four letters.",
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/c/map/ctss")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_c_map_ctss_deadend():
    """A mysterious dead-end for the wanderer."""
    return {
        "information": "Ah, traveler… you've reached a silent chamber where no new riddles await. Perhaps a different path holds the secrets you seek. Tread wisely and retrace your steps.",
        "hint": "Go back to the last branching node; a new journey awaits there.",
    }
