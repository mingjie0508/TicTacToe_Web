from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from board2 import Stage

from config import players, scores

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# Home page, 3 by 3 empty board, human goes first
@app.get("/")
def home():
    board_string = players['Empty']*9
    return RedirectResponse(url="/board/"+board_string+"/"+players['Human'])

# Initialize board, if human goes first, the board is empty,
# if bot goes first, bot makes a move
@app.get("/board/{board_string}/{player}")
def init(board_string: str, player: str, request: Request):
    try:
        s = Stage(board_string, player)
    except ValueError:
        return {"error": "length(board_string) not perfect square"}
    if player == players['Bot']:
        s2 = s.next_stage_bot()
        r = s2.get_result()
        board_string = s2.board_string
        if r is not None:
            context = {"request": request, 'result': r, "board": board_string}
            return emplates.TemplateResponse("winner.html", context)

    context = {"request": request, 'board': board_string}
    return templates.TemplateResponse("game.html", context)

# Go to the next stage, human makes a move, then bot makes a move
# Stop early if someone wins or the board is full
@app.get("/board/{board_string}/{player}/played/{row}/{col}")
def play1(board_string: str, player: str, row: int, col: int, request: Request):
    try:
        s = Stage(board_string, player)
    except ValueError:
        return {"error": "length(board_string) not perfect square"}
    s2 = None
    
    if player == players['Human']:
        s2 = s.next_stage_human(row, col)
        r = s2.get_result()
        board_string = s2.board_string
        if r is not None:
            context = {"request": request, 'result': r, 'board': board_string}
            return templates.TemplateResponse("winner.html", context)
        return RedirectResponse(url="/board/"+board_string+"/"+players['Bot']+"/played/0/0")
    
    s2 = s.next_stage_bot()
    r = s2.get_result()
    board_string = s2.board_string
    if r is not None:
        context = {"request": request, 'result': r, 'board': board_string}
        return templates.TemplateResponse("winner.html", context)
    context = {"request": request, 'board': board_string}
    return templates.TemplateResponse("game.html", context)
