from fastapi import FastAPI

from ziweipan.router import router as ziweipan_router

app = FastAPI()


@app.get("/")
async def welcome() -> list[str]:
    return [ 
        "messageHello World"
    ]

app.include_router(ziweipan_router)