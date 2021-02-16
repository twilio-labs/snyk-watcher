import os


def get_github_secret():
    return os.environ.get('SECRET_GITHUB_SECRET')
