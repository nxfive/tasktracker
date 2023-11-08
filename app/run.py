from os import environ
import uvicorn

if __name__ == "__main__":
    environ["env_state"] = "dev"
    from app.main import app

    uvicorn.run(app, host="0.0.0.0", port=8000)
