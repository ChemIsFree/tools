name: Catalogue accepted tool

on:
  issues:
    types:
      - labeled

permissions:
  contents: write
  issues: write

jobs:
  catalogue:
    if: github.event.label.name == 'accepted'
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: pip install pyyaml

      - name: Add accepted tool to catalogue
        env:
          ISSUE_BODY: ${{ github.event.issue.body }}
          ISSUE_NUMBER: ${{ github.event.issue.number }}
        run: |
          python .github/scripts/process_accepted_tool.py

      - name: Regenerate category pages
        run: |
          python .github/scripts/generate_categories.py

      - name: Commit catalogue changes
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

          git add data/tools.yaml categories/

          if git diff --cached --quiet; then
            echo "No catalogue changes."
          else
            git commit -m "Add accepted tool from issue #${{ github.event.issue.number }}"
            git push
          fi

      - name: Mark issue as catalogued
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh issue edit "${{ github.event.issue.number }}" \
            --add-label "catalogued"

          gh issue close "${{ github.event.issue.number }}"
