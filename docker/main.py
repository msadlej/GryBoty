from src.app.services.validation.bot_validation import BotValidationManager
from src.app.services.run_game.bot_runner import BotRunner
import json
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from typing import Optional

app = FastAPI()


def preprocess_file(file: bytes):
    return file.decode().replace("\\n", "\n")[2:-1]


@app.post("/run-match")
async def run_match(
    game: str = Form(...),
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
):
    try:

        filename1 = file1.filename
        filename2 = file2.filename  # test for the same names TODO

        # bot_1_str = preprocess_file(file1) # TODO think if its needed
        # bot_2_str = preprocess_file(file2)

        bot_1_str = file1.file.read().decode()  # TODO think if its needed
        bot_2_str = file2.file.read().decode()

        runner = BotRunner(game, bot_1_str, bot_2_str, filename1, filename2)
        winner, states = runner.run_game()

        result_json = json.dumps(states)
        return {"winner": winner, "states": result_json}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/validate")
async def validate(game: str = Form(...), file: UploadFile = File(...)):
    try:
        bot_str = file.file.read().decode()
        validator = BotValidationManager(bot_str, game)
        validator.validate()
        return {"success": True, "message": "Validation passed."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
