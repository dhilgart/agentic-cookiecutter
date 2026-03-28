# commit-push-pr

Inner loop workflow: verify → commit → push → open PR.

## Steps

1. **Verify quality gates pass locally**
   ```bash
   uv run ruff format src/ tests/
   uv run ruff check src/ tests/
   uv run mypy src/
   uv run pytest
   ```

2. **Commit with a meaningful message**
   - Subject line: imperative mood, under 72 chars
   - Body: WHY, not what (what is in the diff)
   - Reference story file if applicable

3. **Push to feature branch** (never main)
   ```bash
   git push -u origin HEAD
   ```

4. **Open PR**
   - Title mirrors commit subject
   - Body: link to story file, acceptance criteria checklist
   - Request review via `/code-review` before merging

## Invariants

- Never push directly to main
- All quality gates must be green before pushing
- PR description must include the acceptance criteria from the story file
