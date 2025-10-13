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
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/{response}"
)
async def decipher(response: str):
    if response == "dr-prakash-pawar":
        return{
        "question": """Can you decipher this? 
        7 18 11 4  19 3  4 18 15  13 11 26 19 4 11 22  25 16  16 2 11 24 13 15 
        Z = 10, O = 25""",
        "hint": "The alphabet threw a party, and everyone came 10 spots late. Decode their hangover."
        }
    else:
        return {
            "message": "Oops! You've hit a dead end 🧱",
            "information": "Seems like that wasn't the right path... Check your answer. It might be wrong!",
            "hint": "Not all who wander are lost - but you might be 😉",
        }
@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/{response}"
)
async def love_city(response: str):
    if response == "paris":
        return {
            "question": "If in a certain language 'NIL' is written as 'MOHJKM' then how will 'COMB' be written in that language?"
        }
    else:
        return {
            "message": "Oops! You've hit a dead end 🧱",
            "information": "Seems like that wasn't the right path... Check your answer. It might be wrong!",
            "hint": "Not all who wander are lost - but you might be 😉",
        }

@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplanc/{res}"
)
async def unknown(res: str):
    if res == "a":
        return{
            "question": "How many clocks are there at the entrance of PI block in the college?"
        }
    elif res == "b":
        return{
#confused
        }

@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplanc/a/{res}"
)
async def pi_block(res: int):
    if res == 4:
        return{
            "question": "You walk into a room with only one match. Inside the room is an oil lamp, a candle, and a fireplace. Which do you light first?",
            "hint": "So eager to light the world aflame… yet blind to what must perish first. Tell me, what must die before anything else can live?"
        }
    else:
        return {
            "message": "Oops! You've hit a dead end 🧱",
            "information": "Seems like that wasn't the right path... Check your answer. It might be wrong!",
            "hint": "Not all who wander are lost - but you might be 😉",
        }

@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplanc/a/4/{res}"
)
async def match(res: str):
    if res == "match":
        return{
            "question": "Best club of IIIT Dharwad 😉😉",
            "information": "If u get this wrong u should be out of this room..... 😐"
        }
    else:
        return{
            "message": "Oops! You've hit a dead end 🧱",
            "information": "Seems like that wasn't the right path... Check your answer. It might be wrong!",
            "hint": "Not all who wander are lost - but you might be 😉", 
        }

# Key Node
@app.get(
    "/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/bdnplanc/a/4/match/{res}"
)
async def key_room(res: str):
    """This endpoint represents a secret room deep within the maze where the player discovers a suspicious key."""
    if res == "techniosys":
        return {
        "information": "You've stumbled upon a dimly lit room... and there it lies - a key, cold and gleaming. Something about it feels... wrong.",
        "key": KEY,
        "hint": "Keep the key safe. You may not know when, but you *will* need it.",
        "next_step": "A faint whisper echoes: 'Return to /b/12 if you wish to move forward...'",
        }
    else:
        return{
            "message": "Waiting for someone with *actual taste*.",
            "information": "Try again. 😎"
        }

    
# 23 and 22 by shhadowpdf
@app.get(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/{res}"
)
async def ques(res: str):
    if res == "b":
        return{
            "question": "What is the minimum number of different colours required to paint the given figure such that no two adjacent regions have the same colour in the image?",
            "img": "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/adjacent.png"
        }
    else:
        return{
            "message": "Oops! You've hit a dead end 🧱",
            "information": "Seems like that wasn't the right path... Check your answer. It might be wrong!",
            "hint": "Not all who wander are lost - but you might be 😉", 
        }
    
@app.get(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/adjacent.png"
)
async def adjacent_circle():
    return FileResponse('./images/adjacent.png')

@app.get(
    "/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/{res}"
)
async def called(res: int):
    if res == 3:
        return{
            "question": "If 'cages' are called 'rockets', 'rockets' are called 'traps', 'traps' are called 'planets', \n 'planets' are called 'aeroplanes', 'aeroplanes' are called 'cycles' and cycles' are called \n 'cars', what is Earth",
            "options": [
                {"a": "Cycles"},
                {"b": "Rockets"},
                {"c":"Planet"},
                {"d": "Aeroplanes"},
                {"e": "Cars"} ]
        }
    else:
        return{
            "message": "Oops! You've hit a dead end 🧱",
            "information": "Seems like that wasn't the right path... Check your answer. It might be wrong!",
            "hint": "Not all who wander are lost - but you might be 😉",
        }




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






################################## BRANCH NODES FROM HERE ON  #######################################

########## Left child's Branches ############

@app.get("/b/12/ernest-khalimov/b")
async def ernest_khalimov_b():
    """An empty-seeming chamber with a tiny riddle — choose wisely by answering with 'a' or 'b'."""
    return {
        "question": "A dusty inscription above two sealed doors reads: 'One door hums with dawn, the other whispers at dusk. Speak only a single letter.'",
        "information": "There is no obvious clue here — the choice is curious, not cruel. Reply with either 'a' or 'b' to pick a door.",
        "options": [
            {"a": "the door that hums with dawn"},
            {"b": "the door that whispers at dusk"}
        ]
    }

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus")
async def haven_venus():
    """An empty chamber in the maze where the player faces a strange, adventurous riddle with three possible choices."""
    return {
        "question": "You stand at the edge of an ancient cavern. Three glowing runes hover before you — one shines like fire, another hums like wind, the last pulses like the deep sea. Which rune will you touch?",
        "information": "The air crackles with energy. Each rune seems to lead to a different fate.",
        "options": [
            {"a": "The rune of flame — blazing with courage."},
            {"b": "The rune of wind — whispering of secrets untold."},
            {"c": "The rune of tides — calm yet endlessly deep."}
        ]
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
            {"c": "The Chalice — for those who trust the unknown."}
        ]
    }

@app.get("/b/12/ernest-khalimov/b/b/7/haven/venus/c/a/40/23/re1+/batman/c/dr-prakash-pawar/paris/{res}")
async def paris_bdnplnac(res: str):
    """A silent crossroads deep within the maze where two mysterious choices await the player."""
    if res == "bdnplanc":
        return {
        "question": "You find yourself in an underground gallery lit by ghostly lanterns. Two paintings hang before you — one depicts a roaring storm, the other a calm night sky. Which vision calls to you?",
        "information": "The air hums softly as the eyes in the paintings seem to follow your every move.",
        "options": [
            {"a": "The storm — wild, fierce, and untamed."},
            {"b": "The night — serene, deep, and watchful."}
        ]
    }
    else:
        return {
            "message": "Oops! You've hit a dead end 🧱",
            "information": "Seems like that wasn't the right path... Check your answer. It might be wrong!",
            "hint": "Not all who wander are lost - but you might be 😉",
        }



########## Right child's Branches ############

@app.get("/b/12/giga-chad/c/3")
async def giga_chad_c3():
    """A grand hall within the maze where three colossal doors test the adventurer’s instincts."""
    return {
        "question": "You step into a marble hall echoing with ancient chants. Before you stand three colossal doors — one carved from obsidian, one from ivory, and one from gold. Which do you dare to open?",
        "information": "Each door radiates a different aura — strength, purity, and temptation — but only one leads onward.",
        "options": [
            {"a": "The obsidian door — dark and unyielding."},
            {"b": "The ivory door — silent and pure."},
            {"c": "The golden door — gleaming with promise."}
        ]
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
            {"c": "The green doorway — vibrant and alive."}
        ]
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3")
async def giga_chad_c3_a10_bob_c_nh5_3():
    """A futuristic sci-fi themed chamber in the maze where the player must choose one of three advanced paths."""
    return {
        "question": "You step into a gleaming metallic corridor aboard an abandoned starship. Three holographic panels flicker to life — each showing a different destination across the galaxy. Where will you go, explorer?",
        "information": "The hum of the ship’s reactor echoes faintly as starlight filters through cracked glass — destiny awaits your choice.",
        "options": [
            {"a": "The Nebula Gate — swirling with unknown energy."},
            {"b": "The Cyber Spire — pulsing with digital life."},
            {"c": "The Quantum Rift — bending light and logic alike."}
        ]
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
            {"c": "The flying bathtub — chaotic, bubbly, and hilariously unpredictable."}
        ]
    }

@app.get("/b/12/giga-chad/c/3/a/10/b/bob/c/nh5+/3/b/3/aeroplanes/a/oss/6")
async def oss_6_spooky_node():
    """A dark and eerie chamber in the maze where the player faces a spooky choice among three unsettling paths."""
    return {
        "question": "You enter a shadowy room where whispers crawl along the walls. Three doors appear — one draped in cobwebs, one oozing a faint green mist, and one with faintly glowing runes. Which path do you dare to take?",
        "information": "The air chills your spine and the floor creaks under unseen weight — your courage will be tested.",
        "options": [
            {"a": "The cobwebbed door — ancient and forgotten."},
            {"b": "The misty door — swirling with eerie green fog."},
            {"c": "The rune-etched door — glowing with ghostly symbols."}
        ]
    }
