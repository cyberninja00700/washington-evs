from fastapi import FastAPI, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000)

DEFAULT_PAGE_SIZE = 50


@app.get("/data")
def read_data(page: int = 1, page_size: int = Query(DEFAULT_PAGE_SIZE, gt=0)):
    try:
        # Otwórz i załaduj plik JSON
        with open('rows.json') as f:
            content = json.load(f)

        # Wyodrębnij dane z sekcji "data"
        data = content.get("data", [])

        # Sprawdź, czy dane są listą
        if not isinstance(data, list):
            raise HTTPException(status_code=500, detail="Data is not a list")

        total = len(data)
        skip = (page - 1) * page_size

        # Logowanie wartości skip i limit
        print(f"Total items: {total}, page: {page}, page_size: {page_size}, skip: {skip}")

        # Sprawdź zakres skip
        if skip >= total:
            raise HTTPException(status_code=404, detail="Page out of range")

        # Zwróć dane w zakresie
        return JSONResponse(content={
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": data[skip:skip + page_size]
        })
    except Exception as e:
        # Szczegółowy błąd
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
