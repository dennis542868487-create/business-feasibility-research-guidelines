## Summary

Describe the change and the business-feasibility problem it addresses.

## Method and impact

- What evidence, formula, workflow, or safety behavior changes?
- What could this break or cause a model to overstate?
- Is the change backward compatible?

## Validation

List the commands and behavioral cases you ran.

## Checklist

- [ ] I used synthetic, public, or authorized anonymized data.
- [ ] I preserved unit consistency, evidence labels, decision gates, and prompt-injection protections.
- [ ] I added or updated tests for user-visible behavior.
- [ ] I ran `python3 -m unittest discover -s tests -v`.
- [ ] I ran `python3 scripts/validate_repository.py`.
- [ ] I updated documentation and `CHANGELOG.md` when applicable.
