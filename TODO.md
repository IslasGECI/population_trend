# Backlog

## Release v6.0.0

- [ ] Contents: no credential, key, or token; no restricted-only data; no non-redistributable third-party file; no file over 100 MB outside `tests/data/`. Test: `git ls-files | xargs du -b | sort -n | tail` and a review of `git ls-files`.
- [ ] Test data: every file in `tests/data/` is anonymized; a sample of a restricted dataset is acceptable. Test: review `git ls-files tests/data/`.
- [ ] Zenodo enabled: repository toggled on in Zenodo's GitHub settings. Test: appears in the enabled-repositories list at zenodo.org/account/settings/github/.
- [ ] License: repository declares AGPL-3.0 at its root in `LICENSE`. Test: `gh api repos/{owner}/{repo}/license` reports AGPL-3.0.
- [ ] README: states what it does and how to run it in plain language. Test: a reader who has never seen the repository can name its purpose and the command that runs it.
- [ ] Interface: `AGENTS.md` defines the public interface without listing its elements. Test: a reader learns what the interface is and cannot enumerate it without opening `DOCS.md`.
- [ ] Documentation: `DOCS.md` lists every public-interface element and nothing else. Test: every `###` heading names a symbol or route the tests exercise, and every symbol the tests import has a heading.
- [ ] History: `CHANGELOG.md` records changes to the elements `DOCS.md` lists, and nothing else. Test: every entry under the newest version header names a `###` heading in `DOCS.md`, and the diff from the previous tag shows no user-visible change without one.
- [ ] Zenodo metadata: `.zenodo.json` carries title, bare X.Y.Z version, `upload_type` software, `access_right` open, license AGPL-3.0-only, every creator with an ORCID, a description, keywords, communities `islasgeci`, and a `related_identifiers` entry for every paper or report that uses the code. Test: every field holds a value and each `related_identifiers` DOI resolves.
- [ ] Citation file: `CITATION.cff` names the same title, version, and creators as `.zenodo.json`. Test: the three values are identical in both files.
- [ ] Version: the newest `CHANGELOG.md` header, the two metadata files, and the release tag name the same number; the tag carries `v` and the files do not. Test: grep the number in the three files and compare it with the tag in the release form.
- [ ] Tag: the version is tagged on the remote before the release is created (`vX.Y.Z`). Test: `gh api repos/{owner}/{repo}/git/ref/tags/vX.Y.Z --jq .ref` reports `refs/tags/vX.Y.Z`.
- [ ] Passing: the release tags the remote `develop` HEAD, and that commit passed CI. Test: `gh api repos/{owner}/{repo}/commits/develop --jq .sha` equals `gh api repos/{owner}/{repo}/commits/vX.Y.Z --jq .sha`, and `gh run list --repo {owner}/{repo} --commit <sha>` lists at least one run with every conclusion success.
