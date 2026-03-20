from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.post("/sentiment-api", response_class=HTMLResponse)
def sentiment(request: Request, url: str = Form(...)):
    return HTMLResponse(content=f"<div>Result: No Result Yet Just Testing!</div>")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)