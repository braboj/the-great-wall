```yaml
# This workflow uses actions that are not certified by GitHub.
# They are provided by a third-party and are governed by
# separate terms of service, privacy policy, and support
# documentation.

# GitHub recommends pinning actions to a commit SHA.
# To get a newer version, you will need to update the SHA.
# You can also reference a tag or branch, but the action may change without warning.

name: Deploy Docker Image

# Controls when the action will run.
on:

  # Manual trigger
  workflow_dispatch:

  # Trigger the deployment on push to the main branch
  push:

    # Only the main branch
    branches: [ "main" ]

#    # Only when the Dockerfile changes
#    tags:
#      - '*'

# The jobs that run in the workflow
jobs:

  # Build and push the Docker image
  push_to_registry:
    name: Build and push Docker image to Docker Hub
    runs-on: ubuntu-latest
    steps:

      - name: Check out the repo
        uses: actions/checkout@v4

      - name: Build and push Docker image
        uses: mr-smithers-excellent/docker-build-push@v6.4
        with:
          image: braboj/wall_project
          registry: docker.io
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
          addLatest: true
          pushImage: true
```