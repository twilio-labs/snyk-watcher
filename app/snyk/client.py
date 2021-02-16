import aiohttp
import asyncio

from app.common.logging import getLogger
from app.common.constants import SNYK_INTEGRATION
from app.snyk.utils import SnykObject, parse_project_name, normalize


logger = getLogger(__name__)


class SnykClient:
    def __init__(self, api_token: str):
        headers = {
            'Authorization': f'token {api_token}',
            'Content-Type': 'application/json'
        }

        self.session = aiohttp.ClientSession(headers=headers)

    async def _get_org(self, org_name: str) -> SnykObject:
        res = await self.session.get('https://snyk.io/api/v1/orgs')

        if res.status == 401:
            raise Exception('Could not authenticate to Snyk')

        body = await res.json()
        orgs = body.get('orgs', [])

        if not org_name:
            return orgs

        for org in orgs:
            if org_name == org.get('name'):
                return normalize(org)

        raise Exception(
            f'Could not find {org_name}, Please ensure organizatione exists')

    async def get_project(self,
                          org: SnykObject,
                          project_name: str) -> SnykObject:

        url = f'https://snyk.io/api/v1/org/{org.id}/projects'
        res = await self.session.post(url)

        if res.status != 200:
            raise Exception(res)

        body = await res.json()
        projects = body.get('projects')

        for project in projects:
            name = project.get('name')

            if parse_project_name(name) == project_name:
                return normalize(project)

        return None

    async def get_integration(self, org: SnykObject) -> SnykObject:
        url = f'https://snyk.io/api/v1/org/{org.id}/integrations'
        res = await self.session.get(url)

        if res.status != 200:
            raise Exception(res)

        body = await res.json()

        if SNYK_INTEGRATION in body:
            return normalize(body, SNYK_INTEGRATION)

        raise Exception('Could not find integration')

    async def delete_git_project(self, org_name, repo_name):
        org = await self._get_org(org_name)
        project = await self.get_project(org, repo_name)

        if not project:
            return True

        url = f'https://snyk.io/api/v1/org/{org.id}/project/{project.id}'
        res = await self.session.delete(url)

        if res.status == 200:
            return True

        raise Exception(f'Failed to delete repository {repo_name}')

    async def import_git_project(self, org_name, repo_name):
        org = await self._get_org(org_name)
        project = await self.get_project(org, repo_name)

        if project:
            return

        data = {
            'files': [],
            'target': {
                'owner': org_name,
                'name': repo_name,
                'branch': 'master'
            }
        }

        integration = await self.get_integration(org)
        url = (f'https://snyk.io/api/v1/org/{org.id}'
               f'/integrations/{integration.id}/import')
        res = await self.session.post(url, json=data)

        if res.status != 201:
            raise Exception(f'Failed to import repository {repo_name}')

    def __del__(self):
        loop = asyncio.get_running_loop()
        if loop and loop.is_running():
            task = loop.create_task(self.session.close())
