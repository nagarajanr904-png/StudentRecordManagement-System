# Free Hosting & GitHub Deployment Guide

This guide explains how to push this project to a **GitHub repository** and deploy it to **100% free hosting platforms** (Vercel, Netlify, GitHub Pages, Render, and Free Online MySQL).

---

## Part 1: Push Project to Your GitHub Repository

The local Git repository is already initialized and staged. Follow these 3 simple steps to publish it to your GitHub account:

### 1. Create a Repository on GitHub
1. Go to [github.com/new](https://github.com/new).
2. Enter a repository name (e.g., `scholarpulse-student-records`).
3. Leave it **Public** (or Private) and **do not** check "Add a README" (since this project already includes one).
4. Click **Create repository**.

### 2. Link & Push from Your Terminal
Run the following commands in your project terminal:

```bash
# Add your GitHub repository as origin (replace with your GitHub username and repository name):
git remote add origin https://github.com/YOUR_USERNAME/scholarpulse-student-records.git

# Set the default branch to main:
git branch -M main

# Push all files to GitHub:
git push -u origin main
```

---

## Part 2: Deploy to Free Hosting Platforms

You can host this application completely free using any of these top platforms:

### Option A: Vercel (Recommended - Fastest Setup)
1. Go to [vercel.com](https://vercel.com) and log in with your GitHub account.
2. Click **"Add New..."** → **"Project"**.
3. Select your GitHub repository (`scholarpulse-student-records`) and click **Import**.
4. Vercel automatically detects the Vite configuration via `vercel.json`.
5. Click **Deploy**.
6. **Result**: Your live site is online in ~30 seconds with an instant free SSL URL (e.g. `https://your-project.vercel.app`).

### Option B: Netlify (1-Click Deploy)
1. Go to [netlify.com](https://netlify.com) and log in with GitHub.
2. Click **"Add new site"** → **"Import an existing project"**.
3. Select GitHub and choose your repository.
4. Netlify will automatically detect `netlify.toml` (Build command: `npm run build`, Directory: `dist`).
5. Click **Deploy Site**.
6. **Result**: Free live deployment with automatic custom domain and HTTPS (e.g. `https://your-project.netlify.app`).

### Option C: GitHub Pages (Zero Extra Accounts Needed)
The repository includes a ready-to-run GitHub Actions workflow in `.github/workflows/deploy.yml`:
1. Push your repository to GitHub.
2. In your GitHub repository, click **Settings** → **Pages** (under Code and automation).
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Next time you push (or run workflow), GitHub Actions will build and publish your app automatically to `https://YOUR_USERNAME.github.io/scholarpulse-student-records/`.

### Option D: Render.com (Free Static Site)
1. Go to [render.com](https://render.com) and sign in with GitHub.
2. Click **New +** → **Static Site**.
3. Connect your GitHub repository.
4. Set Build Command: `npm run build` and Publish Directory: `dist`.
5. Click **Create Static Site**.

---

## Part 3: Free Online Cloud MySQL Setup

The Python application communicates directly with any free remote cloud MySQL database without needing MySQL Workbench:

1. **Aiven.io (Recommended Free Managed Cloud MySQL)**:
   - Sign up for free at [aiven.io](https://aiven.io).
   - Create a free MySQL 8.0 instance.
   - Copy **Host**, **Port**, **Database**, **User**, and **Password**.
2. **TiDB Cloud (Free Forever Serverless MySQL)**:
   - Sign up at [tidbcloud.com](https://tidbcloud.com) for instant cloud MySQL.
3. **Configure & Initialize in 1 Command**:
   - Paste credentials into `.env`:
     ```ini
     DB_HOST=your-cloud-host.aivencloud.com
     DB_PORT=3306
     DB_NAME=defaultdb
     DB_USER=avnadmin
     DB_PASSWORD=your_password
     ```
   - Run the automated initializer (no workbench needed):
     ```bash
     python init_database.py
     ```
   - Launch application:
     ```bash
     python main.py
     ```

---

## Part 4: Updating Your Live Deployment

Whenever you make changes to the code:
```bash
git add .
git commit -m "Describe your update"
git push origin main
```
Vercel, Netlify, and GitHub Actions will automatically re-build and re-deploy your changes within seconds!
