from app.common.utils import get_by_path
from app.common.constants import IMPLEMENTED_EVENTS

from pydantic import BaseModel, ValidationError, root_validator


# Nested pull_request object, describes pull_request that triggered webhook.
class PullRequest(BaseModel):
    # Was pull request merged
    merged: bool = False


class Repository(BaseModel):
    # Organization repository belongs to
    org: str
    # Repository name
    name: str
    # default branch name
    default_branch: str


class Changes(BaseModel):
    # Store repository previous name
    previous_name: str = None


class Webhook(BaseModel):
    # The action that triggered the webhook from Github, required.
    action: str
    # This field only exists on pull request webhooks, optional.
    pull_request: PullRequest
    # Optional changes nested object, only exists on renamed repository event.
    changes: Changes
    # Webhook repositoy object, required.
    repository: Repository

    @root_validator(pre=True)
    def parse_data(cls, values: dict) -> dict:
        full_name = get_by_path(values, 'repository.full_name')
        is_merged = get_by_path(values, 'pull_request.merged', False)
        previous_name = get_by_path(values, 'changes.repository.name.from')
        default_branch = get_by_path(
            values, 'repository.default_branch', 'master')

        # full_name needs to be organization name / repository name.
        if '/' not in full_name:
            raise ValidationError('Improper full name.')

        org_name, repo_name = full_name.split('/')

        output = {
            'action': values['action'],
            'repository': {
                'org': org_name,
                'name': repo_name,
                'default_branch': default_branch
            },
            'pull_request': {
                'merged': is_merged
            },
            'changes': {
                'previous_name': previous_name
            }
        }

        return output

    # We need to delete if repository is renamed or deleted.
    def requires_delete(self) -> bool:
        return bool(self.action == 'deleted' or self.changes.previous_name)

    # We need to import the repository for all events
    # except repository deleted.
    def requires_import(self) -> bool:
        return self.action != 'deleted'

    # Helper method to fetch repo to delete.
    def get_delete_repo(self) -> str:
        if self.action == 'deleted':
            return self.repo_name

        if self.changes.previous_name:
            return self.changes.previous_name

    # Ensure this webhook is for the predefined event types.
    def is_implemented(self, event_name: str) -> bool:
        full_name = f'{event_name}.{self.action}'
        is_merged = self.pull_request.merged

        # TODO: Clean up
        if full_name not in IMPLEMENTED_EVENTS:
            return False

        if event_name == 'pull_request' and is_merged is not True:
            return False

        return True
