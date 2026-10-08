# Repository lifecycle and publishing

[Home](../README.md) · [Contributing](../CONTRIBUTING.md)

## Review and merge

Use GitHub flow: short-lived branch, focused commits, pull request, checks, review, squash merge, branch deletion. Keep `main` ready to publish. Prefer commit subjects such as `docs: add Redis stream concepts` or `fix: correct glossary navigation`; Conventional Commits are a convention here, not an automated versioning requirement.

Recommended repository settings are maintainer configuration, not settings enforced by committed files:

- Protect `main` with a ruleset and require the `validate` check.
- Require review for outside contributions; avoid a sole-maintainer rule that makes every change impossible to merge.
- Disable force pushes and branch deletion on `main`.
- Enable squash merging and automatic deletion of merged branches.
- Restrict workflow permissions and keep action dependencies updated.
- Consider a tag ruleset protecting released `v*` tags against movement or deletion.

## Release lifecycle

1. Update `VERSION` and add a matching section in `CHANGELOG.md` through a reviewed pull request.
2. Validate and merge to `main`.
3. The release workflow validates that commit, builds static documentation, and checks for the version tag.
4. If the tag is absent, it creates an annotated tag pointing to that exact commit. An existing tag pointing elsewhere is never overwritten.
5. It publishes release notes, the catalog JSON, the static documentation archive, and SHA-256 checksums.
6. On a retry after partial failure, the workflow reuses the matching tag and completes the missing release. Existing published releases are not rewritten.

Before 1.0, minor versions add categories or substantial scope; patches correct naming, links, or infrastructure. After 1.0, major versions cover breaking catalog-schema or navigation changes. Adding explanations requires an explicit scope decision and a versioned content model.

## GitHub Pages

The repository was private at initial setup. Private-repository Pages availability depends on the account plan. In repository **Settings → Pages**, choose **GitHub Actions** as the source. If GitHub does not permit Pages for the current plan, the maintainer must choose an eligible plan or intentionally make the repository public. Do not change visibility automatically.

The Pages workflow deploys only validated `main` content and can also be rerun manually. It uses the standard `github-pages` environment, read-only contents permissions, Pages write permission, and OIDC for deployment. It does not deploy pull request code with privileged credentials.

The intended public URL is `https://iamsaad640.github.io/software-and-ai-engineering-concepts-directory/`. A generated artifact or successful release does not by itself prove this URL is live.

## Validation boundaries

Local checks cover catalog shape, duplicate names within categories, version/changelog alignment, generated-file consistency, relative file links, static-site assets and anchors, and basic Markdown structure. JavaScript syntax is checked separately. Search behavior and layout should be inspected in a browser after changes to assets. External-link availability and technical accuracy require editorial review.

## GitHub references

- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Markdown and relative links](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [Secure Actions usage](https://docs.github.com/en/actions/reference/security/secure-use)
- [Issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [GitHub Pages setup](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
