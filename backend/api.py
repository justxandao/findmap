# backend/api.py
from fastapi import FastAPI
from backend.capture import capture_screen
from backend.identify import identify_map

app = FastAPI()

@app.get("/capture")
def capture():
    screenshot_path = capture_screen()  # Chama a função de captura
    return {"screenshot": screenshot_path}

@app.get("/identify")
def identify():
    result = identify_map()  # Chama a função de identificação
    return {"result": result}
