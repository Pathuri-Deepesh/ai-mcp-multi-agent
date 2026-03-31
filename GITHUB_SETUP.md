# GitHub Setup Instructions

## Step-by-Step Guide to Push Your Project to GitHub

Follow these steps to create a GitHub repository and push your project code to GitHub.

---

## Part 1: Create a GitHub Repository (One-Time Setup)

### Step 1: Go to GitHub
1. Open your web browser and go to [github.com](https://github.com)
2. Sign in to your GitHub account (create one if needed)

### Step 2: Create a New Repository
1. Click the **+** icon in the top-right corner → **New repository**
2. Fill in the repository details:
   - **Repository name**: `dummy-project` (or `langchain-mcp-agents` if you prefer)
   - **Description**: "A multi-server AI agent using LangChain and MCP (Model Context Protocol) for executing math operations and weather queries"
   - **Visibility**: Select **Public** (for visibility/portfolio) or **Private** (for private projects)
3. **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **Create repository**

### Step 3: Copy Your Repository URL
After creating, you'll see a page with:
```
https://github.com/YOUR_USERNAME/dummy-project.git
```
Copy this URL - you'll need it in the next steps.

---

## Part 2: Initialize Git & Push Code (Terminal Commands)

### Step 4: Open Terminal
Open **Command Prompt** (cmd.exe) or **PowerShell** in your project directory.

### Step 5: Initialize Git Repository

Execute these commands one by one:

```bash
# Navigate to your project directory
cd c:/Users/dp1/Desktop/dummy-project

# Initialize git
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: MCP servers with LangChain agent integration"

# Rename branch to main (GitHub default)
git branch -M main

# Add remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/dummy-project.git

# Push code to GitHub
git push -u origin main
```

### Step 6: Verify on GitHub
1. Go back to your GitHub repository page
2. Refresh the page
3. You should see all your project files uploaded!

---

## Part 3: Configure GitHub Repository

### Step 7: Add Repository Details

1. **Go to repository settings** → Click **Settings** tab
2. **Add Description**: Copy from pyproject.toml description
3. **Add Topics** (for discoverability):
   - `langchain`
   - `mcp`
   - `ai-agents`
   - `python`
   - `llm`
4. **Enable features** you want:
   - ☑️ Discussions (for Q&A)
   - ☑️ Issues (for bug tracking)
   - ☑️ Projects (for project management)

### Step 8: Add a License (Optional)
1. Click **Add file** → **Create new file**
2. Name it: `LICENSE`
3. Click **Choose a license template** → Select MIT License
4. Click **Review and submit**
5. Commit the license file

---

## Part 4: Future Updates (After First Push)

To push future changes to GitHub:

```bash
# Make your changes, then:
git add .
git commit -m "Your commit message"
git push origin main
```

---

## 🔧 Troubleshooting Common Issues

### Issue: "fatal: not a git repository"
**Solution:**
```bash
# Make sure you're in the project directory
cd c:/Users/dp1/Desktop/dummy-project
git init
```

### Issue: "fatal: error: The system cannot find the path specified"
**Solution:**
```bash
# Use correct path with forward slashes
git remote add origin https://github.com/YOUR_USERNAME/dummy-project.git
```

### Issue: "Permission denied" or "Authentication failed"
**Solution:** GitHub now requires Personal Access Tokens instead of passwords.

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control of private repositories)
4. Generate and copy the token
5. When pushing, use:
   ```bash
   git push -u origin main
   # When prompted for password, paste your token
   ```

### Issue: "Updates were rejected because the tip of your current branch is behind"
**Solution:**
```bash
# Pull latest changes first
git pull origin main
# Then push
git push origin main
```

---

## 📝 Quick Command Reference

```bash
# Check git status
git status

# View commit history
git log --oneline

# Add specific files instead of all
git add filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Check remote URL
git remote -v

# Change remote URL
git remote set-url origin https://github.com/NEW_URL/repo.git
```

---

## ✅ Final Checklist

- [ ] Created GitHub account (if needed)
- [ ] Created GitHub repository on github.com
- [ ] Copied repository URL
- [ ] Opened terminal in project directory
- [ ] Executed `git init`
- [ ] Executed `git add .`
- [ ] Executed `git commit -m "Initial commit..."`
- [ ] Executed `git branch -M main`
- [ ] Executed `git remote add origin https://...`
- [ ] Executed `git push -u origin main`
- [ ] Verified files appear on GitHub
- [ ] Added description and topics to repository
- [ ] (Optional) Added LICENSE file

---

## 🎉 You're Done!

Your project is now on GitHub! Share the repository URL with others:
```
https://github.com/YOUR_USERNAME/dummy-project
```

You can now:
- Showcase your work in your portfolio
- Collaborate with others via Issues and Pull Requests
- Track changes with Git version control
- Implement CI/CD pipelines with GitHub Actions

---

**Need help?** Refer to [GitHub Docs](https://docs.github.com) for more detailed information.
