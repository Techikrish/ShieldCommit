# QuickStart Guide - ShieldCommit

Get started with ShieldCommit in **60 seconds**.

## 🚀 Installation

```bash
pip install shieldcommit
```

## 📋 Basic Usage

### 1. Install as Git Hook
```bash
cd your-project
shieldcommit install
```

### 2. Try a Commit
```bash
# Add a file
echo "api_key = 'AKIAAAAAAAAAAAAAAAAA'" > config.py
git add config.py

# Try to commit
git commit -m "Add config"
# ❌ Blocked! Secret detected ✅
```

### 3. Remove the Secret
```bash
rm config.py
git reset
git commit -m "Add config" --allow-empty
# ✅ Success!
```

## 🔒 What It Detects

✅ **AWS Keys** (AKIA*, Secret Keys)  
✅ **API Keys** (Stripe, GitHub, Google, etc.)  
✅ **Passwords & Tokens**  
✅ **Private Keys** (RSA, EC, PGP)  
✅ **Database Credentials**  
✅ **Slack/Discord Webhooks**  

## 📚 Learn More

- Full docs: See [README.md](README.md)
- Contributing: See [CONTRIBUTING.md](CONTRIBUTING.md)
- Branching: See [BRANCHING.md](BRANCHING.md)

## ❓ Troubleshooting

**Hook not working?**
```bash
shieldcommit install  # Reinstall
```

**False positive?**
Check [README.md - Smart False Positive Prevention](README.md#smart-false-positive-prevention)

---

**Happy secure committing!** 🔐
