import uvicorn
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

uvicorn.run(
    'app.app:app',
    host='127.0.0.1',
    port=8080,
)
