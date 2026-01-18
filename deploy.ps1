$ErrorActionPreference = "Stop"
Write-Host "Initializing Git..."
git init

Write-Host "Adding files..."
git add .

Write-Host "Committing..."
git commit -m "Initial commit - Rug Predictor V1"

Write-Host "Renaming branch to main..."
git branch -M main

Write-Host "Adding remote..."
# Check if remote exists to avoid error on rerun
if ((git remote) -contains 'origin') {
    git remote set-url origin https://github.com/GoJackzi/rug-predictor.git
} else {
    git remote add origin https://github.com/GoJackzi/rug-predictor.git
}

Write-Host "Pushing to GitHub..."
git push -u origin main
