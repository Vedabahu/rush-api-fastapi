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
