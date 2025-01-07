from src.app.services.validation.bot_validation import BotValidationManager
from src.app.services.run_game.bot_runner import BotRunner
import json
from fastapi import FastAPI, Form, HTTPException
from typing import Optional


app = FastAPI()


def preprocess_file(file: bytes):
    return file.decode().replace("\\n", "\n")[2:-1]


@app.post("/run-match")
async def run_match(
    game: str = Form(...),
    file1: bytes = Form(...),  # File content as bytes
    file2: bytes = Form(...),  # File content as bytes
    filename1: Optional[str] = Form(None),
    filename2: Optional[str] = Form(None),
):
    try:

        filename1 = filename1 or "file1.py"
        filename2 = filename2 or "file2.py"

        bot_1_str = preprocess_file(file1) # TODO think if its needed
        bot_2_str = preprocess_file(file2)

        runner = BotRunner(game, bot_1_str, bot_2_str, filename1, filename2)
        winner, states = runner.run_game()

        result_json = json.dumps(states)
        return {"winner": winner, "states": result_json}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@app.post("/validate")
async def validate(game: str = Form(...), file: bytes = Form(...)):
    try:
        bot_str = preprocess_file(file)
        validator = BotValidationManager(bot_str, game)
        validator.validate()
        return {"success": True, "message": "Validation passed."}
    except Exception as e:
        return {"success": False, "error": str(e)}
