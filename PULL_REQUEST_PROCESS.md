# Pull Request Process

## 📊 PR Workflow

```
1. Create Branch from develop
   ↓
2. Make Changes + Add Tests
   ↓
3. Run Tests Locally (All 92 passing)
   ↓
4. Commit with Conventional Commit Message
   ↓
5. Push to Your Fork
   ↓
6. Create PR on GitHub
   ↓
7. Automated Checks Run
   ├─ pytest (92 tests)
   ├─ flake8 (code style)
   ├─ black (formatting)
   └─ security scan
   ↓
8. Code Review
   ├─ Feedback
   └─ Changes Requested
   ↓
9. Address Feedback
   ├─ Make changes
   ├─ Re-run tests
   └─ Push updates
   ↓
10. Approval ✅
    ↓
11. Merge to develop
    ↓
12. Delete branch
```

## 📝 PR Template

When you create a PR, fill this out:

```markdown
## Description
<!-- Brief description of changes -->

## Related Issue
<!-- Link to issue this fixes -->
Closes #123

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] CI/CD update

## Testing
- [x] Tests added
- [x] All tests passing
- [x] Coverage > 80%

## Checklist
- [x] Code follows PEP 8
- [x] Self-review completed
- [x] Tests updated
- [x] Docs updated
- [x] PR targets develop (not main)
```

## ✅ PR Checklist

Before submitting:

- [ ] Code follows PEP 8 style
- [ ] Tests added for new code
- [ ] All 92 tests passing: `pytest tests/ -v`
- [ ] Coverage > 80%: `pytest --cov=src/shieldcommit`
- [ ] Code formatted: `black src/ tests/`
- [ ] Linting passes: `flake8 src/ tests/`
- [ ] Docstrings added
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow convention
- [ ] PR targets **develop** branch (not main)
- [ ] No merge conflicts

## 🔍 PR Review Checklist

Reviewers will check:

### Code Quality
- Does it solve the problem?
- Is code readable and well-structured?
- Are there better approaches?
- Is there code duplication?

### Testing
- Are tests comprehensive?
- Do tests make sense?
- Are edge cases covered?
- Is coverage adequate (>80%)?

### Documentation
- Is README updated?
- Are docstrings added?
- Are examples provided?

### Git & PR
- Are commits logical?
- Do commit messages follow convention?
- Is PR description clear?
- Are there conflicts?

## 📋 Types of Review Feedback

### ✅ Approved
- No changes needed
- PR can be merged

### 💬 Comment
- Questions or suggestions
- Not blocking merge
- Can be addressed later

### 👀 Changes Requested
- Changes required
- PR cannot merge until fixed
- Reviewer must approve again

## 🔧 Addressing Feedback

1. **Read feedback carefully**
2. **Ask if unclear**: Comment on PR with questions
3. **Make changes**: Update your code
4. **Test again**: Run `pytest tests/ -v`
5. **Push changes**: `git push origin your-branch`
6. **Request re-review**: GitHub button to re-request

## 🚀 Merging

When PR is ready:

1. **All checks pass** ✅
2. **At least 1 approval** ✅
3. **No conflicts** ✅
4. **All feedback addressed** ✅

Then **Maintainer merges** to develop branch.

## 🧹 After Merge

```bash
# Delete local branch
git branch -d feature/your-feature

# Delete remote branch
git push origin --delete feature/your-feature

# Update local develop
git checkout develop
git pull upstream develop
```

## 💡 PR Best Practices

### ✅ Good PR
- Single feature/fix per PR
- Focused changes
- Clear description
- Good test coverage
- Updated documentation
- Clean commit history

### ❌ Bad PR
- Multiple unrelated changes
- Huge PR (hard to review)
- No tests
- Missing documentation
- Messy commit history
- Force pushes to main

## 🆘 Common PR Issues

### "Conflicts with develop"
```bash
git fetch upstream
git rebase upstream/develop
# Fix conflicts in editor
git add .
git rebase --continue
git push origin your-branch --force-with-lease
```

### "CI/CD checks failing"
1. Check GitHub Actions logs
2. Run locally: `pytest tests/ -v`
3. Fix issues
4. Push fixes

### "PR is behind develop"
```bash
git fetch upstream
git rebase upstream/develop
git push origin your-branch --force-with-lease
```

## 📞 Getting Help

- **Questions?** Comment in the PR
- **Stuck?** Open GitHub Discussion
- **Urgent?** Contact maintainers

---

**See [BRANCHING.md](BRANCHING.md) and [CONTRIBUTING.md](CONTRIBUTING.md) for more details**
