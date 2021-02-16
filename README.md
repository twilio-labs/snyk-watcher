## What is it?

Snyk-Watcher is a Github App to sync your github repositories with the Snyk vulnerability scanning service. Snyk-Watcher will automatically import and delete repositories as they are created and deleted in your github organization.

## How does it work?

Snyk-Watcher listens for webhooks to trigger events. Currently, it only watches the master branch. It should recieve the following events from Github:
* Repository - Created, Deleted, Renamed
* Pull Request - All

For the pull request webhooks, Snyk-Watcher will only try to import a project if it has been merged to master.

## Running Snyk-Watcher

Snyk-Watcher is designed to be completely stand alone, you could build the container with the ```make build``` command.

A helper docker-compose file has been included with the following commands to streamline the process:

```docker-compose build```

```docker-compose up```

Snyk-Watcher requires two environment variables:
* SECRET_GITHUB_SECRET - Used to verify payloads from Github.
* SECRET_SNYK_API_TOKEN - Used to authenticate to Snyk to manage repositories.

## Installation

Snyk-Watcher needs to be installed into a Github organization through the developer settings -> Github Apps.

The shared secret is required for proper functionality and must exactly match the provided value for Github secret environment variable.

Snyk-Watcher will need permissions to recieve webhooks for the above described events.

It requires Repository Administration, and Pull Request read only permissions (Snyk Watcher will not communicate with Github). Make sure to subscribe to the required events.

## Limitations

At this time, Snyk-Watcher is only tested with Github Enterprise, but should work with other flavors. Support for other version control systems is not supported.

__Snyk-Watcher does not have access to your code or Github.__