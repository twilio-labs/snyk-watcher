import os


def get_snyk_token():
    return os.environ.get('SECRET_SNYK_API_TOKEN')
