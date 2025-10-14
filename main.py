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
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplnac/{res}"
)
async def unknown(res: str):
    if res == "a":
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


################## Branch Questions ######################

############ LEFT ################

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
        "information": "You’ve wandered into a hollow corridor that echoes with silence — no riddles, no answers, just the hum of mystery. Perhaps it’s time to retrace your steps… maybe the last fork held a better fate?",
        "hint": "Go back to the last branching path — you might find the true way there."
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
    from fastapi.responses import FileResponse
    return FileResponse("./images/pokemon.png")


