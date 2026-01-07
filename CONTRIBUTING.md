# Contributing to ShieldCommit 🚀

Thank you for your interest in contributing to ShieldCommit! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- GitHub account

### Fork & Clone

```bash
# 1. Fork the repository (GitHub UI)
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/ShieldCommit.git
cd ShieldCommit

# 3. Add upstream remote
git remote add upstream https://github.com/techikrish/ShieldCommit.git

# 4. Verify remotes
git remote -v
```

---

## 🛠️ Development Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

---

## 🌳 Branching Strategy

We use **four types of branches**:

### 1. **feature/** - New Features
```bash
git checkout main
git pull upstream main
git checkout -b feature/add-slack-detection

# Make changes, commit, push, create PR
git push origin feature/add-slack-detection
```

### 2. **fix/** - Bug Fixes
```bash
git checkout main
git pull upstream main
git checkout -b fix/false-positive-arns

# Make changes, commit, push, create PR
git push origin fix/false-positive-arns
```

### 3. **docs/** - Documentation
```bash
git checkout main
git pull upstream main
git checkout -b docs/update-readme

# Make changes, commit, push, create PR
git push origin docs/update-readme
```

### 4. **chore/** - CI/CD & Config
```bash
git checkout main
git pull upstream main
git checkout -b chore/update-dependencies

# Make changes, commit, push, create PR
git push origin chore/update-dependencies
```

### Branch Naming
```
✅ feature/add-github-token-detection
✅ fix/entropy-false-positives
✅ docs/installation-guide
✅ chore/update-github-actions
❌ my-feature
❌ temp
❌ wip
```

---

## 📝 Making Changes

```bash
# 1. Create branch from main
git checkout main
git pull upstream main
git checkout -b feature/your-feature

# 2. Make changes
nano src/shieldcommit/file.py

# 3. Test locally
pytest tests/ -v
black src/ tests/
flake8 src/ tests/

# 4. Commit
git add .
git commit -m "feat: add new detection method"

# 5. Push
git push origin feature/your-feature

# 6. Create PR on GitHub (target main branch)
```

---

## 🧪 Testing

**All code MUST have tests!**

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/shieldcommit

# Coverage must be > 80%
```

### Test Example
```python
def test_my_feature(self):
    """Clear description of what you're testing"""
    # Arrange
    detector = IntelligentDetector()
    line = 'api_key = "sk_live_fake123456789abc"'
    
    # Act
    result = detector.detect_in_line(line)
    
    # Assert
    assert len(result) > 0
    assert result[0]['confidence'] > 0.9
```

---

## 📤 Submitting Pull Requests

### PR Checklist
- [ ] Code follows PEP 8
- [ ] Tests added/updated
- [ ] All tests passing (92/92)
- [ ] Coverage > 80%
- [ ] Documentation updated
- [ ] PR targets `main` branch
- [ ] Commit messages follow convention

### Create PR
1. Push to your fork: `git push origin feature/your-feature`
2. Go to GitHub and click "New Pull Request"
3. Set Base: `main`, Compare: `feature/your-feature`
4. Fill PR template (auto-fills)
5. Submit!

### PR Template
Your PR should include:
```markdown
## Description
Brief description of changes

## Related Issue
Closes #123

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Documentation

## Testing
- [x] Tests added
- [x] All tests passing
- [x] Coverage > 80%

## Checklist
- [x] Code follows style guidelines
- [x] Self-review completed
- [x] Tests updated
- [x] Docs updated
```

---

## 💬 Commit Messages

Follow **Conventional Commits** format:

```
type(scope): description

Optional body with more details
```

### Types
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `chore:` CI/CD, deps, config
- `refactor:` Code refactoring
- `test:` Test improvements
- `perf:` Performance

### Examples
```
✅ feat(detector): add GitHub token detection
✅ fix(entropy): reduce false positives by 15%
✅ docs(readme): update installation guide
✅ chore(github-actions): update test matrix
❌ fix stuff
❌ update code
```

---

## 🎨 Code Style

We follow **PEP 8**:

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Sort imports
isort src/ tests/
```

---

## ❓ FAQ

**Q: What branch should I target?**  
A: Always `main`. All changes go through PRs to main.

**Q: How long until my PR is reviewed?**  
A: Usually 1-3 days.

**Q: Do I need tests?**  
A: Yes! All code must have tests.

**Q: My PR got rejected. What now?**  
A: Get feedback, make changes, and try again!

---

## 🤝 Need Help?

- 📖 See [BRANCHING.md](BRANCHING.md) for branching details
- 📤 See [PULL_REQUEST_PROCESS.md](PULL_REQUEST_PROCESS.md) for PR workflow
- 💬 Open a GitHub Discussion
- 🐛 Create a GitHub Issue

---

**Thank you for contributing! 🎉**
