```yaml
# Simple workflow for deploying static content to GitHub Pages
name: Deploy Pages

# Controls when the action will run.
on:

  # Trigger the deployment manually
  workflow_dispatch:

  # Trigger the deployment on push to the main branch
  push:

    # Only the main branch
    branches:
      - "main"

    # Only when the docs directory or mkdocs.yml file changes
    paths:
      - "docs/**"
      - mkdocs.yml

# Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

# Allow one concurrent deployment
concurrency:
  group: "pages"
  cancel-in-progress: true

# Define the jobs that run in the workflow
jobs:

  # The build job
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - run: ls -la
      - name: Setup Pages
        uses: actions/configure-pages@v2
      - name: Setup Python, install plugins, and build site
        uses: actions/setup-python@v4
        with:
          python-version: 3.x
      - run: pip install mkdocs
      - run: pip install mkdocs-section-index
      - run: mkdocs build --site-dir ./_site
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v1

  # The deployment job
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v1
```