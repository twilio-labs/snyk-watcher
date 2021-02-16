import os

# Currently implemented actions for the below even.action pairs
IMPLEMENTED_EVENTS = {
    "repository.created",
    "repository.deleted",
    "repository.renamed",
    "pull_request.closed"
}

# TODO: make required
SNYK_INTEGRATION = os.environ.get('SNYK_INTEGRATION', 'github-enterprise')
