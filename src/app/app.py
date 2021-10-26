import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup() #подгружаем настройки


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from django.core.asgi import get_asgi_application
from starlette.responses import RedirectResponse
from .api.web import api as api_subapp
from django.conf import settings


app = FastAPI()

app.mount('/app', get_asgi_application()) #хостим через uvicorn
app.mount(
    settings.STATIC_URL,
    app=StaticFiles(directory=settings.STATIC_ROOT.as_posix(), check_dir=False),
    name='staticfiles',
)
app.mount('/api/v1/', api_subapp)
app.include_router(api_subapp.router, prefix='/api/v1')


@app.get('/')
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url='/docs')
