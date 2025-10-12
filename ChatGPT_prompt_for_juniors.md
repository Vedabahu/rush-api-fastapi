I am creating an API like maze or labyrinth game. The logic is that, people get different questions when they hit an endpoint. The questions can either be in the form of an image (png or jpg) or the question can be in the form of a text. I am using python's FastAPI to create the endpoints. I have the logic and other things setup. I need the code for the endpoint when I ask for it. 

The representations is like that of a tree, where each node is like a room from which you will have doors. Each room has a question, either in the form of an image or as plain text. They are different questions like solve this problem or brain teasers etc. The questions are already ready. The correct answer for the question will be the new endpoint for the next node. For example, if the current endpoint it `/start`, and the question is "When was India freed from the oppression of the British", the solution for it, which is 1947, will be the next appended endpoint, i.e. `/start/1947`.

This pattern goes on and on until they reach the goal nodes. Whenever I ask you to give me the code for the implementation of the current question, I want you to give me only the code that creates the endpoint and nothing else. For example, If my question is the "Start node with 4 options A, B, C, D" and the correct answer as A, your response should be as such.
```py
@app.get("/")
async def start_of_the_maze():
    """This is the start of the maze"""
    return { 
        "information": "This is the start of the maze, you have 4 options, choose any one to proceed.",
        "options" : [
            "A", "B", "C", "D"
        ]
    }
```

Fill the response with a docstring explaining what the function is doing with a proper information. The path of the endpoint will be specified. Do not assume it. Ask for it if I do not mention it. Always use `async` functions. This is for better performance. If there is an image, it will be in the folder `/images/<image.png_jpg_jpeg>`. If the response requires you to send an image, create another endpoint with the same preceeding one as before and add the image to its end by using its name. For example, if the current endpoint is `/` and the image has to be sent, write the json response to have an image field pointing to the image path like `{ "image" : "/image/carbon.png" }`. For this, create another function which return the image when called.

I will now start giving the details. Give me the appropriate fastapi code which is async. 