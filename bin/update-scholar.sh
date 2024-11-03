name: Update Scholar Stats

on:
  schedule:
    - cron: '0 */12 * * *'  # Runs every 12 hours
  workflow_dispatch:  # Allows manual trigger

jobs:
  update-stats:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install scholarly

    - name: Update scholar stats
      run: python bin/fetch_scholar_stats.py

    - name: Commit and push if changed
      run: |
        git config --global user.email "github-actions[bot]@users.noreply.github.com"
        git config --global user.name "GitHub Actions"
        git add asset/data/scholar_stats.json
        git diff --quiet && git diff --staged --quiet || (git commit -m "Update scholar stats" && git push)