from fastapi import FastAPI
import json
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/data")
def read_data():
    with open('rows.json') as f:
        data = json.load(f)
    return JSONResponse(content=data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
