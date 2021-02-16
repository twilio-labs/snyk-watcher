import collections
from app.snyk.config import get_snyk_token


SnykObject = collections.namedtuple('SnykObject', 'name id')


def parse_project_name(project_name: str) -> str:
    name = project_name

    if ':' in name:
        name = name.split(':')[0]

    if '/' in name:
        name = name.split('/')[-1]

    return name


def normalize(base_obj: dict, id_key: str = 'id'):
    return SnykObject(
        name=base_obj.get('name'),
        id=base_obj.get(id_key)
    )
