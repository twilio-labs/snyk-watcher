## How does it work?

Snyk-Watcher listens for webhooks to trigger events. It watches the main branch for the following events from Github:

* Repository - Created, Deleted, Renamed
* Pull Request - All

For the pull request webhooks, Snyk-Watcher will only try to import a project if it has been merged to main.

## Installation

Snyk-Watcher runs completely standalone in a Docker container. We've included a docker-compose file to make it easy to build.

1. Clone this repository.

1. Build the container:

   `docker-compose build`

1. Start Snyk-Watcher:

   `docker-compose up`

   You can verify that Snyk-Watcher is running by navigating to:

   `localhost:8000/healthcheck`

1. In GitHub, go to the **GitHub Apps** developer setting and click **New GitHub App**.

1. Enter the following values in the **Register new GitHub App** form:

   * **GitHub App name**: `Snyk-Watcher`
   * **Webhook URL**: {server}`/github/webhook`
   * **Secret**: {a highly random string}

1. Give Snyk-Watcher access to the following Repository permissions:

   * **Repository Administration** (Read-only)
   * **Metadata** (Read-only)
   * **Pull requests** (Read-only)

1. Subscribe to the following events:

	* **Pull request**
	* **Repository**

1. Provide the Snyk-Watcher container your GitHub and Snyk tokens in these two environment variables:

   * `SECRET_GITHUB_SECRET`
   * `SECRET_SNYK_API_TOKEN`

1. Test Snyk-Watcher by adding a new repository, then looking in the app’s advanced settings to see if the request was successful.
    

## Limitations

* At this time, Snyk-Watcher has been tested only with GitHub and GitHub Enterprise.
* Snyk-Watcher does not have access to your code and does not make any changes to your GitHub organization or repositories.
