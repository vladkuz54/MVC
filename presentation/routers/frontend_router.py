from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["frontend"])
templates = Jinja2Templates(directory="presentation/templates")


@router.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@router.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")
