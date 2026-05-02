from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from dotenv import load_dotenv
from core import orchestrate_pipeline, call_sentiment_endpoint
from utils import authenticate_reddit, get_comments, connect_sentiment

app = FastAPI()
load_dotenv()
reddit = authenticate_reddit()
sentiment_endpoint = connect_sentiment()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/sentiment-stand-alone", response_class=HTMLResponse)
def sentiment_stand_alone(request: Request, text: str = Form(...)):

    payload = {"texts": [{"text": text}]}
    result = call_sentiment_endpoint(payload, sentiment_endpoint)
    if isinstance(result, dict) & ("error" in result):
        return HTMLResponse(content=f"<div>Could Not Connect to API</div>") 
    
    return HTMLResponse(content=f"<div>Result: {result}</div>")


@app.post("/sentiment-reddit", response_class=HTMLResponse)
def sentiment_reddit(request: Request, url: str = Form(...)):
    
    # TODO: in get_comments() add error handling 
    # to deal with posts with 0 comments
    comments = get_comments(reddit, url)
    if isinstance(comments, dict):
        return HTMLResponse(content=f"<div>Result: {comments}</div>")
    
    else:
        result, table = orchestrate_pipeline(comments, sentiment_endpoint)
        
        context = {"overall_result": result, "comments": table}
       
        return templates.TemplateResponse(
            request=request,
            name="result_update.html",
            context=context
        )

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)