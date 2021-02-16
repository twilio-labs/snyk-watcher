import os

from fastapi import FastAPI
from app.routers.health_check import router as health_check_router
from app.routers.github import router as github_router

app_config = {
    'title': 'Snyk Watcher',
    'description': 'A Github app to automatically sync projects to snyk',
    'docs_url': None,
    'redoc_url': None
}

# Enable swagger / redoc endpoints
if os.environ.get('DEBUG') in [True, 'True', 'true']:
    app_config['docs_url'] = '/docs'
    app_config['redoc_url'] = '/redocs'


app = FastAPI(**app_config)

app.include_router(health_check_router)
app.include_router(github_router, prefix='/github')
