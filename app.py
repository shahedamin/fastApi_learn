from fastapi import FastAPI

app = FastAPI()

@app.post("api/v1/users")
async def register_user()