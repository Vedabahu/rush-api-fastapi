from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.middleware import RequestLoggingMiddleware

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


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # Return the image on 404
        return FileResponse(
            "images/404_not_found.png", media_type="image/png", status_code=404
        )
    return exc


@app.get("/")
async def maze_entrance():
    """Entrance to the maze"""
    return {
        "information": "Welcome to the Rush API Maze!! Choose one of the below options to proceed further.",
        "options": ["a", "b", "c", "d"],
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


# 34 to key node by shhadowpdf
@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar"
)
async def decipher():
    return {
        "question": """Can you decipher this? 
        7 18 11 4  19 3  4 18 15  13 11 26 19 4 11 22  25 16  16 2 11 24 13 15 
        Z = 10, O = 25""",
        "hint": "The alphabet threw a party, and everyone came 10 spots late. Decode their hangover.",
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris"
)
async def love_city():
    return {
        "question": "If in a certain language 'NIL' is written as 'MOHJKM' then how will 'COMB' be written in that language?"
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/"
)
async def branch_node_on_the_left_side():
    return {
        "information": "You've stumbled upon three skulls, each grinning wickedly in the flickering torchlight... Only one hides the path forward — the others whisper doom.",
        "hint": "Choose wisely, traveler. The wrong touch might awaken what sleeps beneath.",
        "options": {"a": "Lion Skull 🦁", "b": "Wolf Skull 🐺", "c": "Human Skull 💀"},
    }


# BRANCHNODE KINDLY CHECK THIS PART
@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/a"
)
async def unknown():
    return {
            "question": "How many clocks are there at the entrance of PI block in the college?"
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/a/4"
)
async def pi_block():
    return {
        "question": "You walk into a room with only one match. Inside the room is an oil lamp, a candle, and a fireplace. Which do you light first?",
        "hint": "So eager to light the world aflame… yet blind to what must perish first. Tell me, what must die before anything else can live?",
    }


@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/a/4/match"
)
async def match():
    return {
        "question": "Best club of IIIT Dharwad 😉😉",
        "information": "If u get this wrong u should be out of this room..... 😐",
    }


# end of 34 to key node


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


# 23 and 22 by shhadowpdf
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
async def called():
    return {
        "question": "If 'cages' are called 'rockets', 'rockets' are called 'traps', 'traps' are called 'planets', 'planets' are called 'aeroplanes', 'aeroplanes' are called 'cycles' and cycles' are called 'cars', what is Earth",
        "options": ["Cycles", "Rockets", "Planet", "Aeroplanes", "Cars"],
    }


# end of 23 and 22


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


@app.post(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/63/time"
)
async def unlock_treasure(request: Request):
    """Handles unlocking of the treasure chest if the correct key is provided."""
    data = await request.json()
    key = data.get("key")

    if key == KEY:
        return {
            "message": "The key fits perfectly! 🔑 The chest creaks open... and inside you find something truly legendary.",
            "treasure": "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/a/vedabahu/63/time/linus-vp-the-brave.webm",
            "information": "Behold! You’ve unlocked the ultimate treasure - get ready, this is going to be *epic*! 🎉",
        }
    else:
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
        "options": [
            {"a": "Holiday"},
            {"b": "Game day"},
            {"c": "Workday"}
        ]
    }

@app.get("/b/12/ernest-khalimov/b/a/c")
async def ernest_khalimov_b_a_c():
    """A seasonal challenge room where the traveler must identify the current season from the scene."""
    return {
        "question": "What season is it?",
        "image": "/images/realcityfr.jpg",
        "information": "Observe the environment carefully — the scenery might reveal the answer.",
        "options": [
            {"a": "Summer"},
            {"b": "Fall"},
            {"c": "Spring"},
            {"d": "Winter"}
        ]
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
            {"d": "Tsunami"}
        ]
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
            {"d": "Tourism"}
        ]
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
        "hint": "Go back to the last branching node to find the path onward."
    }

#### "b/12/ernest-khalimov/b/b/7/haven/venus" gate:

# "b/12/ernest-khalimov/b/b/7/haven/venus/a" path

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/a")
async def venus_a_puzzle():
    """A mysterious riddle room where players must decipher the scrambled message."""
    return {
        "question": "Yffit etunim oga fi ti saw ufor semit sa anym setunim taps reeth kcolc'o, woh anym setunim si ti litnu xis kcolc'o?",
        "information": "The symbols twist and dance before your eyes... only a clever mind can unscrable it's meaning."
    }

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/a/26")
async def venus_a26_temperature_riddle():
    """A brain-teaser chamber: players must find the temperature that reads the same in °C and °F."""
    return {
        "question": "It is a matter of common knowledge that 0°C is the same as 32°F. It is also a known fact that 100°C equals 212°F. But there is a temperature that gives the same reading on both Centigrade and Fahrenheit scales. Can you find this temperature?",
        "information": "This riddle asks you to find the single temperature value where the Celsius and Fahrenheit readings are identical.",
        "hint": "Use the conversion formula F = (9/5) * C + 32. Set F = C and solve the resulting linear equation for the temperature (you'll get a negative value)."
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
        "hint": "Think about how many cuts are needed to get 12 pieces — it's fewer than you think!"
    }

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/a/26/-40/75/11")
async def venus_a26_minus40_75_11_dead_end():
    """A dead-end chamber where the traveler realizes this path leads nowhere... for now."""
    return {
        "information": "You've wandered into a hollow corridor that echoes with silence — no riddles, no answers, just the hum of mystery. Perhaps it’s time to retrace your steps… maybe the last fork held a better fate?",
        "hint": "Go back to the last branching path — you might find the true way there."
    }

# "b/12/ernest-khalimov/b/b/7/haven/venus/b" path

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/b")
async def venus_b_room():
    """A historical challenge room where the traveler must identify the main person in the image."""
    return {
        "question": "Who is the main person related to the image? (make sure it's '-' separated)",
        "image": "/images/theroom.jpg", 
        "information": "Look closely at the room and its details — the story it tells is tied to a real historical figure.",
        "hint": "She was a young diarist hiding during World War II whose writings became world-famous."
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
        "hint": "It won an oscar award recently. Think of popular hits!"
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
            "Contemplate the mysteries of the maze… and wait"
        ]
    }

#### "b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman" gate:

# b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a path:

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a")
async def batman_a_numbers():
    """A mathematical challenge room where the traveler must find the sum of two mysterious numbers."""
    return {
        "question": "There are two numbers with a difference of 3 between them and the difference of their squares is 51. Find the sum of those numbers.",
        "information": "Think carefully about how squares and differences relate — a simple formula might help.",
        "hint": "Recall the identity: (x+y)(x-y) = x² - y²."
    }


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17")
async def pokemon_batman_a17():
    """A playful challenge room — identify the Pokémon shown in the image to proceed."""
    return {
        "question": "Guess the Pokémon shown in the image.",
        "image": "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17/pokemon.png",
        "information": "A shimmering silhouette stares back at you — trust your instincts and name the creature.",
        "hint": "It's a Psychic type — think mind-benders and telekinetic trickery."
    }

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17/pokemon.png")
async def get_pokemon_image_a17():
    """Serves the Pokémon image for the guess-the-Pokémon challenge."""
    return FileResponse("./images/pokemon.png")


@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17/azelf")
async def batman_a_azelf_shopping():
    """A price puzzle room where the traveler must determine the cost of a shirt given a tricky shopping scenario."""
    return {
        "question": "I bought a shirt and a pant for Rs. 110 at the New Market. The shirt cost Rs. 100 more than the pant. How much does the shirt cost?",
        "information": "Think carefully — sometimes the numbers can be misleading at first glance.",
        "hint": "Try assigning a variable to the pant's price and set up a simple equation for the total cost."
    }

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/a/17/azelf/105")
async def batman_a_azelf_105_dead_end():
    """A dead-end chamber where the traveler reaches the end of this path, with no further questions."""
    return {
        "information": "Well done, traveler! You've reached the end of this particular path. There's no question here, but your journey and curiosity are commendable.",
        "possible_actions": [
            "Retrace your steps to the last branching node",
            "Consider exploring another branch of the maze",
            "Pause and reflect on the puzzles you've solved so far"
        ]
    }

# b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/b path:

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/b")
async def batman_b_geometry_puzzle():
    """A geometric riddle room where the traveler must determine the fewest lines to form given shapes."""
    return {
        "question": "What is the minimum number of straight lines required to make 2 squares and 4 right-angled triangles?",
        "information": "Visualize carefully — sometimes, clever overlaps and shared edges can save effort. Think of how shapes can coexist within one another without extra lines."
    }

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/b/8")
async def batman_b_8_market_riddle():
    """A classic riddle room where logic matters more than math — count carefully who's actually traveling!"""
    return {
        "question": "One morning I was on my way to the market and met a man who had 4 wives. Each of the wives had 4 bags containing 4 dogs and each dog had 4 puppies. Taking all things into consideration, how many were going to the market?",
        "information": "Don't get tangled in numbers — focus on the journey. Who was actually going to the market, and who was merely met along the way?"
    }

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/b/8/1")
async def batman_b_8_1_dead_end():
    """A mysterious dead-end room where the traveler reaches a silent void."""
    return {
        "information": "The path fades into darkness... the air is still, and no clue lies ahead. Perhaps you've strayed too far down this corridor.",
        "hint": "Retrace your steps to the last place where choices remained — the true path may yet reveal itself."
    }

#### "b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac" gate:

# b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/b:

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/b")
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
    

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/b/30")
async def guess_the_pokemon():
    """Guess the Pokémon from the shadow or silhouette."""
    return {
        "question": "WHO'S THAT POKEMON?",
        "image": "/images/guess_the_pokemon.png",
        "hint": "Look closely at the shape — fans of Fairy-type Pokémon might just lose their mind lol!"
    }

@app.get("/images/guess_the_pokemon.png")
async def get_pokemon_image():
    """Serves the Pokémon silhouette image."""
    return FileResponse("./images/guess_the_pokemon.png")

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/b/30/clefairy")
async def clefairy_deadend():
    """A mysterious dead end that teases the wanderer about another path."""
    return {
        "message": "You've come so close, wanderer. The stars whisper your name.",
        "information": "But this is not where it lies... Perhaps the other path hides something — a key that may or may not open a chest.",
        "hint": "Retrace your steps to the last divergence and follow the path untaken."
    }


############ LEFT BRANCH ################

######### b/12/giga-chad/c/3 gate:

# b/12/giga-chad/c/3/b path:
@app.get("/b/12/giga-chad/c/3/b")
async def giga_chad_c_3_b():
    """A visual puzzle where the traveler must identify the missing number on a credit card."""
    return {
        "question": "Which number is missing on the bottom credit card?",
        "image": "/images/credictcard.png",
        "information": "Look closely at the image — a single digit is missing on the bottom card. Can you spot it?"
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
        )
    }

@app.get("/b/12/giga-chad/c/3/b/8/transformer")
async def giga_chad_c_3_b_8_transformer():
    """A mysterious dead end for the wanderer."""
    return {
        "message": "There is no question here. This is a dead end.",
        "information": (
            "The wanderer stands at the edge of knowledge — this path leads nowhere. "
            "Perhaps another route holds the key they seek. Turn back, and follow the current where it diverges."
        )
    }

# b/12/giga-chad/c/3/c path:

@app.get("/b/12/giga-chad/c/3/c")
async def giga_chad_c_3_c():
    """A cinematic puzzle for the curious wanderer."""
    return {
        "question": "Guess the movie from the image.",
        "image": "/images/realmovie.png",
        "information": "As you wish — every frame hides a story, and every story hides a clue."
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
        "information": "Look closely — sometimes the smallest mismatch between lists can cause the biggest errors."
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
        "information": "Perhaps a different trail holds the treasure you seek. The echoes hint of routes unseen — retrace, rethink, rediscover."
    }


# /b/12/giga-chad/c/3/a/10/b/bob/a path

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/a")
async def giga_chad_c_3_a_10_b_bob_a():
    """A nostalgic tech trivia buried in time."""
    return {
        "question": "Which company’s failed portable music player called “Zune” was meant to compete with the iPod?",
        "information": "Once upon a time, even giants stumble when they dance in Apple's shadow."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/a/microsoft")
async def giga_chad_c_3_a_10_b_bob_a_microsoft():
    """A debugging challenge awaits the wanderer."""
    return {
        "question": "Which line has error?",
        "image": "/images/real_code2.png",
        "information": "The error hides in plain sight — a small slip in logic or syntax."
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
        "information": "Back when the Internet was still a fragile experiment — two letters made history."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/a/microsoft/14/lo")
async def giga_chad_c_3_a_10_b_bob_a_microsoft_14_lo():
    """A mysterious and playful dead end for the wanderer."""
    return {
        "question": "…silence echoes here. No question awaits, only whispers of another path.",
        "information": "The shadows hint at secrets elsewhere. Retrace your steps and follow a different trail — the true adventure awaits beyond this point."
    }


# /b/12/giga-chad/c/3/a/10/b/bob/b path

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/b")
async def giga_chad_c_3_a_10_b_bob_b():
    """A cryptography challenge where the traveler must identify the encryption type."""
    return {
        "question": "In cryptography, which algorithm type uses the same key for both encryption and decryption?",
        "information": "Some secrets are locked with a single key — can you name the class of algorithms that works this way?"
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/b/symmetric")
async def giga_chad_c_3_a_10_b_bob_b_symmetric():
    """A tech trivia room about the origins of computer bugs."""
    return {
        "question": "The term “bug” in computer science originated when a real insect caused a system malfunction. What insect was it?",
        "information": "Sometimes the smallest creature can cause the biggest problem — look closely at history!"
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/b/symmetric/moth")
async def giga_chad_c_3_a_10_b_bob_b_symmetric_moth():
    """A debugging challenge where the traveler must identify the error in the code."""
    return {
        "question": "Which line has error?",
        "image": "/images/real_code3.png",
        "information": "The bug lurks in the lines — observe carefully and spot the culprit."
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
        "information": "The path forward hides elsewhere. Retrace your steps and explore another trail — the real challenge lies beyond this turn."
    }

# /b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/a path
@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/a")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_a():
    """A computer storage challenge where the traveler must identify the type of memory."""
    return {
        "question": "In computer storage, what is the term for memory that is non-volatile but allows fast random access, like SSDs?",
        "information": "Think about modern storage devices that keep data even when powered off but can be accessed quickly."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/a/flash")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_a_flash():
    """A seating puzzle where the traveler must deduce positions in a circle."""
    return {
        "question": "Five persons were playing a card game while sitting in a circle, all facing the center. Rithwik was to the left of Vedabahu. Rishik was to the right of Modak and was sitting between Modak and Ram. Who was to the right of Ram?",
        "information": "Visualize the circle carefully — sometimes the answer is just a matter of orientation and logic!"
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/a/flash/rithwik")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_a_flash_rithwik():
    """A mysterious dead-end in the maze for the traveler."""
    return {
        "question": "The path ahead fades into shadows… nothing more to solve here.",
        "information": "You're so close! But the true challenge lies along another trail — perhaps retracing your steps will reveal it."
    }

# /b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/c path

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/c")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_c():
    """A programming paradigm challenge where the traveler must identify the paradigm."""
    return {
        "question": "What is the term for a programming paradigm that treats computation as the evaluation of mathematical functions, avoiding changing state and mutable data?",
        "information": "Think about paradigms that emphasize immutability, pure functions, and avoid side effects."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/c/functional")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_c_functional():
    """A directional puzzle where the traveler must deduce the facing direction using shadows."""
    return {
        "question": "One evening before sunset, two friends — Aneesh and Modak — were talking to each other face to face. If Modak’s shadow was exactly to his right side, which direction was aneesh facing?",
        "information": "Visualize the sun’s position during sunset — shadows stretch opposite the light."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/c/functional/south")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_c_functional_south():
    """A mysterious dead-end in the maze for the traveler."""
    return {
        "question": "The path seems to vanish here… no puzzle awaits.",
        "information": "You're treading carefully and wisely, but the true challenge lies elsewhere. Perhaps retracing your steps or exploring a different route will reveal it."
    }

#/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/b

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/b")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_b():
    """A riddle room where the traveler must solve a poetic puzzle."""
    return {
        "question": "I’m named for haste but flourish in reeds, I swell in crowds and throb in veins, I crown the hours commuters dread, And on the field I burst through lanes. Four letters wear my many masks — what am I?",
        "information": "Pay attention to wordplay and the many contexts in which this thing appears — it’s everywhere in daily life."
    }


@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/b/rush")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_b_rush():
    """A mysterious riddle room where the traveler must deduce an invisible phenomenon."""
    return {
        "question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        "information": "Think about natural phenomena that carry sound without being seen."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/b/rush/echo")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_b_rush_echo():
    """A mysterious dead-end in the maze for the traveler."""
    return {
        "question": "The echoes fade here… no puzzle awaits.",
        "information": "You've chased the sound far and wide, but the true path lies elsewhere. Perhaps retracing your steps or exploring a different branch will reveal it."
    }

#/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/c

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/c")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_c():
    """A mathematical reasoning room where the traveler must deduce age differences from ratios."""
    return {
        "question": "Recently, I attended the twelfth wedding anniversary celebration of my friends Mohini and Jayant. During the event, Jayant smiled and said, “When we got married, Mohini was three-fourths of my age. Now, after 12 years, she is five-sixths of my age.” Hearing this, everyone became curious to know their ages at the time of their marriage. Based on this information, what was the age difference between them?",
        "information": "Focus on the ratios and the time elapsed to calculate the age difference at the time of marriage."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/c/6")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_c_6():
    """A sports trivia room where the traveler must recall cricket records."""
    return {
        "question": "Out of the top five highest team totals in IPL history, which team appears four times in the list?",
        "information": "Think IPL teams' short forms for quick reference.",
        "hint": "Use the team's common abbreviation (short form)."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/c/6/srh")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_c_6_srh_dead_end():
    """A dead-end chamber where the wanderer has reached a stop, but a mysterious path may lie elsewhere."""
    return {
        "information": "Ah, brave traveler! You've arrived at a cul-de-sac. The path forward here fades into shadows. Perhaps another route hides the key to continue your adventure.",
        "hint": "Retrace your steps to the last branching node and explore a different path."
    }

#/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/b

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/b")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_b():
    """A cinematic trivia room where the traveler must guess the unofficial label of an upcoming film project."""
    return {
        "question": "S. S. Rajamouli and Mahesh Babu’s upcoming project has yet to reveal its title, but discussions in the film circle revolve around a single unofficial label inspired by global exploration. What is that word?",
        "information": "Think of a term linked to exploration and adventures around the world.",
        "hint": "It's a single word often associated with discovering new places."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/b/globetrotter")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_b_globetrotter():
    """A computing history room where the traveler must identify an OS created by a student in 1991."""
    return {
        "question": "Which operating system’s first version was created by a 21-year-old student in 1991 and had just 10,239 lines of code?",
        "information": "This OS is now one of the most widely used open-source systems in the world.",
        "hint": "Its mascot is a penguin."
    }
@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/b/globetrotter/linux")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_b_globetrotter_linux_deadend():
    """A dead-end in the tech maze — the traveler has reached the end of this path."""
    return {
        "information": "Ah, you’ve ventured far and discovered the legendary OS, but this path has nothing more to offer! Perhaps another route will unveil secrets yet unknown.",
        "hint": "Retrace your steps to the last branching point to explore a different path."
    }

#/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/a/oss/6/c

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/c")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_c():
    """A Python functional programming challenge room."""
    return {
        "question": "What Python built-in function is used to transform elements of an iterable into a new iterable by applying a given function to each element? (just write the function name)",
        "information": "Think of a function that ‘maps’ one thing to another across a sequence.",
        "hint": "It’s a one-word function often used in combination with lambda functions."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/c/map")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_c_map():
    """A historical computing trivia room."""
    return {
        "question": "The world’s first computer password was created in 1961 for a system at MIT. That system was one of the earliest time-sharing computers ever built. What was its name? (short form only)",
        "information": "Think of early computing at MIT — an iconic time-sharing system.",
        "hint": "Just four letters."
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6/c/map/ctss")
async def giga_chad_c_3_a_10_b_bob_c_nh5_3_b_3_aeroplanes_a_oss_6_c_map_ctss_deadend():
    """A mysterious dead-end for the wanderer."""
    return {
        "information": "Ah, traveler… you've reached a silent chamber where no new riddles await. Perhaps a different path holds the secrets you seek. Tread wisely and retrace your steps.",
        "hint": "Go back to the last branching node; a new journey awaits there."
    }


