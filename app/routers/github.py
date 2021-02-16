from fastapi import APIRouter, Response, Request, Header
from typing import Optional

from app.common.logging import getLogger
from app.github.webhook_validator import verify_webhook
from app.github.webhook_model import Webhook
from app.github.config import get_github_secret
from app.snyk.client import SnykClient
from app.snyk.utils import get_snyk_token

logger = getLogger(__name__)
router = APIRouter()

github_secret = get_github_secret()
snyk_token = get_snyk_token()


@router.post('/webhook')
async def handle_webhook(
        # Raw body is required to compute sha1
        request: Request,
        # Parsed request object
        webhook: Webhook,
        # Required header X-Hub-Signature
        x_hub_signature: Optional[str] = Header(...),
        # Required header X-Github-Event
        x_github_event: Optional[str] = Header(...)):
    # Raw body is required to compute sha1
    request_body = await request.body()

    # Verify payload sha1 to ensure request is valid
    if not verify_webhook(request_body, x_hub_signature, github_secret):
        logger.error('Webhook validation failed.')
        return Response(status_code=401)

    # Ensure this is event and action pair is implemented
    if not webhook.is_implemented(x_github_event):
        logger.error('Webhook event is not implemented.')
        return Response(content='Not implemented', status_code=200)

    # Snyk client to add / remove repositories
    client = SnykClient(snyk_token)

    org_name = webhook.repository.org
    repo_name = webhook.repository.name

    try:
        if webhook.requires_delete():
            delete_repo = webhook.get_delete_repo()
            await client.delete_git_project(org_name, delete_repo)

        if webhook.requires_import():
            await client.import_git_project(org_name, repo_name)
    except Exception as e:
        logger.error(e)
        # Failed internally
        return Response(status_code=500)

    # Success all done
    return Response(status_code=200)
