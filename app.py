from fastapi import FastAPI, Query, HTTPException
import json
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/data")
def read_data(skip: int = 0, limit: int = 10):
    with open('rows.json') as f:
        data = json.load(f)

    total = len(data)
    if skip >= total:
        raise HTTPException(status_code=404, detail="Offset too large")

    return JSONResponse(content={
        "total": total,
        "items": data[skip:skip + limit]
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
