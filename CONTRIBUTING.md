# Contributing

Contributions are welcome when they improve evidence quality, dimensional correctness, reproducibility, safety, or cross-industry usefulness.

By participating, follow [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [GOVERNANCE.md](GOVERNANCE.md). Fork the repository, create a focused branch, push it to your fork, and open a pull request against `main`. Do not request direct write access for an initial contribution.

Before submitting a change:

1. Keep the main Skill standalone and under 500 lines.
2. Put detailed method in directly linked references; avoid duplicated rules.
3. Use only `name` and `description` in Skill frontmatter.
4. Preserve statement types, evidence profiles, decision gates, and untrusted-source protections.
5. Add or update deterministic tests for script changes.
6. Add a behavioral case for a newly discovered failure mode.
7. Use synthetic or authorized anonymized data.
8. Run `python3 -m unittest discover -s tests -v` and `python3 scripts/validate_repository.py`.
9. Update `CHANGELOG.md` for user-visible behavior.

Do not commit generated model responses containing personal or confidential information. Do not add paid or network runtime dependencies to the core calculation path.
