# Git Branching Strategy

## 🌳 Branch Structure

```
main (primary branch, all changes via PRs)
  ↑ (merge via feature/fix/docs/chore PRs)
  │
├─ feature/*  (new features)
├─ fix/*      (bug fixes)
├─ docs/*     (documentation)
└─ chore/*    (CI/CD, dependencies, config)
```

## 📋 Branch Types

### ✨ Feature Branches (`feature/*`)
**Purpose**: New features and enhancements

```bash
# Create
git checkout main
git pull upstream main
git checkout -b feature/add-slack-detection

# Example names
✅ feature/add-slack-detection
✅ feature/improve-entropy-calculation
✅ feature/add-azure-version-check

# Merge
# Create PR: main <- feature/add-slack-detection
```

### 🐛 Fix Branches (`fix/*`)
**Purpose**: Bug fixes

```bash
# Create
git checkout main
git pull upstream main
git checkout -b fix/false-positive-arns

# Example names
✅ fix/false-positive-arns
✅ fix/entropy-scoring-bug
✅ fix/confidence-calculation

# Merge
# Create PR: main <- fix/false-positive-arns
```

### 📚 Documentation Branches (`docs/*`)
**Purpose**: Documentation updates

```bash
# Create
git checkout main
git pull upstream main
git checkout -b docs/update-readme

# Example names
✅ docs/update-readme
✅ docs/api-documentation
✅ docs/installation-guide

# Merge
# Create PR: main <- docs/update-readme
```

### 🔧 Chore Branches (`chore/*`)
**Purpose**: CI/CD, dependencies, configuration

```bash
# Create
git checkout main
git pull upstream main
git checkout -b chore/update-github-actions

# Example names
✅ chore/update-dependencies
✅ chore/update-python-version
✅ chore/add-security-scanning

# Merge
# Create PR: main <- chore/update-github-actions
```

## 🔄 Workflow Summary

### Create Feature
```bash
git checkout main
git pull upstream main
git checkout -b feature/your-feature
# Make changes
git add .
git commit -m "feat: description"
git push origin feature/your-feature
# Create PR on GitHub
```

### Fix a Bug
```bash
git checkout main
git pull upstream main
git checkout -b fix/bug-name
# Make changes + tests
git add .
git commit -m "fix: description"
git push origin fix/bug-name
# Create PR on GitHub
```

### Update Docs
```bash
git checkout main
git pull upstream main
git checkout -b docs/update-name
# Make changes
git add .
git commit -m "docs: description"
git push origin docs/update-name
# Create PR on GitHub
```

### Update CI/Config
```bash
git checkout main
git pull upstream main
git checkout -b chore/update-name
# Make changes
git add .
git commit -m "chore: description"
git push origin chore/update-name
# Create PR on GitHub
```

## ✅ Branch Protection Rules

**develop branch**:
- ✅ Require PR reviews (1 approved)
- ✅ Require status checks pass
- ✅ Require branches up to date
- ✅ No force push

**main branch**:
- ✅ Require PR reviews (2 approved)
- ✅ Require status checks pass
- ✅ Require branches up to date
- ✅ No force push
- ✅ Dismiss stale PR approvals

## 🧹 Cleanup

After PR is merged:

```bash
# Delete local branch
git branch -d feature/your-feature

# Delete remote branch
git push origin --delete feature/your-feature

# Keep fork synced
git fetch upstream
git checkout develop
git rebase upstream/develop
git push origin develop
```

## 📊 Branch Naming Conventions

```
✅ Correct Format:
  feature/add-slack-detection
  feature/improve-entropy-detection
  feature/add-oauth-support
  
  fix/false-positive-arns
  fix/entropy-scoring-issue
  fix/confidence-calculation-bug
  
  docs/update-readme
  docs/installation-guide
  docs/api-reference
  
  chore/update-dependencies
  chore/update-github-actions
  chore/add-pre-commit-hooks

❌ Wrong Format:
  my-feature
  fix-stuff
  temp
  wip
  feature_name (use hyphens, not underscores)
  Feature/name (lowercase only)
```

## 🎯 Quick Reference

| Type | Branch | Target | Use Case |
|------|--------|--------|----------|
| New Feature | `feature/*` | develop | New functionality |
| Bug Fix | `fix/*` | develop | Bug fixes |
| Documentation | `docs/*` | develop | Doc updates |
| CI/Config | `chore/*` | develop | Dependencies, CI/CD |

## 🆘 Common Issues

### Branch behind develop
```bash
git fetch upstream
git rebase upstream/develop
git push origin branch-name --force-with-lease
```

### Merge conflicts
```bash
git fetch upstream
git rebase upstream/develop
# Resolve conflicts in editor
git add .
git rebase --continue
git push origin branch-name --force-with-lease
```

### Delete wrong branch
```bash
# Recover from git reflog
git reflog
git checkout -b branch-name commit-hash
```

---

**See [CONTRIBUTING.md](CONTRIBUTING.md) for complete guide**
