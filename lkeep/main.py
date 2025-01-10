import uvicorn
from fastapi import FastAPI

app = FastAPI()


def start():
    uvicorn.run(app="lkeep.main:app", reload=True)
