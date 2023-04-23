import uvicorn
from fastapi import FastAPI

from ziweipan.router import router as ziweipan_router

app = FastAPI()


@app.get("/")
async def welcome() -> list[str]:
    return [ 
        "message", "Hello World"
    ]

app.include_router(ziweipan_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)