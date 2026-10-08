# Contributing

Contributions should improve coverage, naming, categorization, or maintainability. This release contains concept names only.

## GitHub flow

1. Open an issue for a substantial taxonomy change; small corrections can go straight to a pull request.
2. Create a short-lived branch from current `main`, such as `docs/redis-cluster` or `fix/concept-name`.
3. Edit `catalog/directory.json`. Keep concept names concise and group related terms within an entry.
4. Run `python3 -m pip install -r requirements-docs.txt
python3 scripts/build.py --site` and `python3 scripts/check.py`.
5. Open a pull request with the change, rationale, and validation results. Link a related issue when one exists.
6. Address review feedback and pass checks. A maintainer squash-merges the change and deletes the branch.

Keep pull requests focused. Do not combine broad formatting changes with unrelated concept additions. A draft pull request is appropriate when categorization is still being discussed.

## Content requirements

- Stay within software engineering, applied LLM applications, and principal-level engineering judgment.
- Include distributed storage and production concerns, not only framework or vendor names.
- Exclude classical ML, model training, and training mathematics from the core scope.
- Prefer established terms. Identify emerging terms without presenting them as universal standards.
- Add primary reference starting points for new categories.
- Avoid repeating a display name within a category. Cross-category repetition is allowed when useful.
- Never include credentials, private datasets, private conversation content, or production secrets.

Use [the style guide](STYLE_GUIDE.md) for Markdown and naming. Generated pages must be committed with catalog edits. Maintainers own version bumps and releases; ordinary contributions should not create tags.

## Local validation

```bash
python3 scripts/build.py --site
python3 scripts/check.py
node --check site-assets/shortcuts.js
```

The check validates catalog structure, generated-file consistency, local file links, static-site anchors, and basic Markdown conventions. External links are reference starting points; CI does not claim to validate the technical content of those pages.

## Documentation theme

The site uses Material for MkDocs. Edit `mkdocs.yml` for theme settings and `site-assets/shortcuts.js` for the Ctrl+K / Cmd+K binding. Navigation is generated from the catalog; keep names-only concept content in `catalog/directory.json`.
