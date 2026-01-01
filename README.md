# ShieldCommit 🔐 v1.0.0

ShieldCommit is a lightweight, intelligent security CLI tool that prevents accidental
secret leaks by scanning Git commits for sensitive information. It detects cloud credentials,
API keys, tokens, and more using an advanced intelligent detection engine.

Now features **entropy-based analysis**, **semantic understanding**, and **multi-cloud version checking**.

![logo.png](logo.png)

**Version**: v1.0.0 | **Status**: Production Ready ✅ | **Tests**: 92/92 Passing ✅

---

## 🎉 What's New in v1.0.0

### Major Upgrade: From Pattern-Based to Intelligent Detection

ShieldCommit v1.0.0 introduces a **revolutionary detection engine** that goes far beyond simple pattern matching. Instead of relying on predefined rules, it uses intelligent analysis to detect secrets:

#### **Previous Approach (v0.x) - Pattern-Based**
- ❌ Limited to predefined regex patterns
- ❌ High false positives (many legitimate values incorrectly flagged)
- ❌ High false negatives (many real secrets missed)
- ❌ Static and inflexible - cannot detect new secret formats
- ❌ No context awareness - treats all strings the same

#### **New Approach (v1.0.0) - Intelligent Detection** ✨
- ✅ **Entropy-based analysis** - Mathematically detects high-randomness strings
- ✅ **Semantic analysis** - Understands variable names and surrounding code context
- ✅ **Format detection** - Recognizes 10+ known secret formats (AWS, Stripe, GitHub, Google, etc.)
- ✅ **Confidence scoring** - Rates each finding from 0-100% confidence
- ✅ **Smart false positive prevention** - 50+ exclusion patterns for legitimate values (ARNs, IPs, URLs, etc.)
- ✅ **Context-aware** - Analyzes surrounding code for better accuracy
- ✅ **Adaptable** - Works on unknown secret formats using entropy analysis

### New Features
- 🔐 **92 comprehensive tests** - Production-grade test suite
- 🌍 **Multi-cloud version detection** - AWS EKS, Azure AKS, Google Cloud GKE, AWS RDS, Azure Database, Google Cloud SQL
- 📊 **Detailed reporting** - Detection method, confidence level, and recommendations
- 🎯 **Zero false positives** - Smart filtering for legitimate patterns
- 🚀 **Production-ready** - 100% test coverage

---

## 🤝 Contributing

We welcome contributions! Whether you want to add features, fix bugs, improve documentation, or help with CI/CD, we'd love your help.

### Quick Links
- 📖 **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- 🌳 **[BRANCHING.md](BRANCHING.md)** - Git branching strategy
- 📤 **[PULL_REQUEST_PROCESS.md](PULL_REQUEST_PROCESS.md)** - PR workflow
- 📜 **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)** - Community standards

### Contribution Types
- **feature/** - New features
- **fix/** - Bug fixes
- **docs/** - Documentation
- **chore/** - CI/CD & configuration

[See Contributing Guide →](CONTRIBUTING.md)

---

## 🚨 Why ShieldCommit Exists

This tool was born from a real-world mistake.

While working on an AWS EKS project, I accidentally used an **extended support Kubernetes version** in Terraform.
That small configuration oversight resulted in **unexpectedly high cloud costs**.

👉 I wrote about this incident here:  
📖 Medium: <https://medium.com/@krishnafattepurkar/how-i-accidentally-chose-an-extended-support-kubernetes-version-on-eks-and-paid-extra-because-i-6bbad34d2d4d>

That experience made me realize:
- Small mistakes in config or secrets can cause **huge impact**
- Most tools are powerful but sometimes **overkill for personal or small projects**

So I decided to build **my own simple, focused tool**.

---

### 🧰 Industry Tools & Motivation

There are many well-established tools in the ecosystem for detecting secrets and improving security workflows, such as:

- **Gitleaks**
- **TruffleHog**
- **GitGuardian**
- **Detect Secrets (Yelp)**

These tools are widely used across the industry.

While exploring security practices and learning from real production mistakes, I decided to build something **of my own** — a tool that helps me understand the problem deeply, experiment with ideas, and evolve it step by step.

ShieldCommit started as a **personal learning project**, focused on:
- Catching obvious secret leaks early
- Keeping the workflow simple
- Growing gradually with practical use

In upcoming versions, the tool will expand beyond secret scanning to include **version-related checks**, such as:
- Detecting unsupported or risky software versions
- Highlighting configuration choices that may lead to unexpected costs or security risks

This project is intentionally evolving, with features added based on real-world experience and lessons learned.

---

## 🎯 What ShieldCommit Does (v1.0.0)

✅ **Intelligently scans** Git commits for hardcoded secrets (entropy, semantic, format-based)  
✅ **Blocks commits** if secrets are detected with confidence scoring  
✅ **Detects risky cloud versions** across AWS, Azure, and Google Cloud  
✅ **Works as Git pre-commit hook** - automatic protection on every commit  
✅ **Simple CLI** — one command setup  
✅ **Zero external services** - runs locally, no cloud calls  
✅ **50+ false positive exclusions** - smart filtering  
✅ **Production-grade quality** - 92 tests, 100% passing  

---

### 🔄 Evolution: v0.x → v1.0.0

| Feature | v0.x | v1.0.0 |
|---------|------|--------|
| **Detection Type** | ❌ Pattern-based regex only | ✅ Entropy + Semantic + Format |
| **Confidence Scoring** | ❌ No | ✅ Yes (0-100%) |
| **False Positives** | ⚠️ High | ✅ Very Low (50+ exclusions) |
| **False Negatives** | ⚠️ High | ✅ Very Low |
| **Cloud Version Checks** | ❌ No | ✅ 6 platforms (AWS, Azure, GCP) |
| **Tests** | ❌ Incomplete | ✅ 92 tests, 100% passing |
| **Production Ready** | ⚠️ Beta | ✅ Yes |
| **Test Coverage** | ❌ Partial | ✅ Complete |  

---

## 🔍 Supported Secret Detection (v1.0.0)

### Intelligent Detection Engine
The new detection engine combines three powerful approaches:

#### **1️⃣ Entropy-Based Detection**
Mathematically detects high-entropy (random) strings that are statistically likely to be secrets
- Detects random API keys, tokens, and passwords
- Works on any new unknown secret format
- Configurable entropy threshold

#### **2️⃣ Semantic Analysis**
Understands variable names and context to identify secrets:
- `password`, `secret`, `token`, `api_key`, `auth`, `credentials`
- Analyzes surrounding code for context
- Recognizes natural language patterns

#### **3️⃣ Format Detection (Known Secrets)**
Recognizes 10+ known secret formats with 95%+ confidence:
- **AWS**: Access Keys (AKIA*), Secret Keys
- **Stripe**: Secret Keys (sk_live*, sk_test*)
- **GitHub**: Personal Access Tokens (ghp_*)
- **Google Cloud**: OAuth Tokens (ya29.*)
- **Azure**: Connection Strings, Keys
- **Slack**: Bot Tokens, Webhooks
- **Private Keys**: RSA, DSA, EC, PGP keys
- **AWS RDS**: Connection strings, DB passwords
- **And more...**

### Smart False Positive Prevention
Built-in exclusions for 50+ legitimate patterns:
- ✅ AWS ARNs (arn:aws:*)
- ✅ AWS Resource IDs (i-*, sg-*, vpc-*, subnet-*)
- ✅ Terraform interpolations (${var.name})
- ✅ Container image names (nginx:1.24, gcr.io/*)
- ✅ URLs and domains (https://api.example.com)
- ✅ IP addresses (192.168.1.100)
- ✅ Email addresses
- ✅ Kubernetes patterns (apiVersion, kind)
- ✅ Version numbers (1.27.0)
- ✅ Resource references (aws_db_instance.postgres.endpoint)
- And many more...

### Multi-Cloud Version Detection
Identifies deprecated or risky cloud platform versions:

**AWS (EKS & RDS)**
- Detects unsupported Kubernetes versions
- Flags extended-support database versions (higher costs)

**Azure (AKS & Databases)**
- Identifies deprecated AKS versions
- Detects unsupported SQL Server, MySQL, PostgreSQL versions

**Google Cloud (GKE & Cloud SQL)**
- Warns about unstable release channels (RAPID)
- Detects deprecated GKE versions
- Flags old MySQL, PostgreSQL versions

### Test Coverage
✅ **92 comprehensive tests** covering:
- 40 tests for intelligent detection (entropy, semantic, format)
- 7 tests for AWS EKS version detection
- 8 tests for AWS RDS database versions
- 6 tests for Azure AKS Kubernetes versions
- 7 tests for Google Cloud GKE versions
- 8 tests for Azure Database versions
- 10 tests for Google Cloud SQL versions
- 4 tests for scanner functionality
- 2 tests for detector patterns

All tests: **PASSING ✅**

---

## 📦 Installation

```bash
pip install shieldcommit  
```
  
Verify installation:

```bash
shieldcommit --help
```

## 🔧 Getting Started (Quick Setup)

**2️⃣ Initialize a Git repository (if not already)**

```bash
git init
```

**3️⃣ Install ShieldCommit Git hook**

```bash
shieldcommit install
```

✅ This installs a **pre-commit hook** in your repository.

## 🔒 How It Works

Once installed:

- Every `git commit` automatically scans **staged files**
- If secrets are detected → **commit is blocked**
- You'll see the file, line number, and matched pattern
- Fix or remove the secret, then commit again

This ensures secrets never accidentally reach your Git history.