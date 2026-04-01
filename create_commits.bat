@echo off
echo Initializing Git...
git init

echo Committing project setup...
git add .gitignore requirements.txt README.md
git commit -m "Initialize project structure and documentation"

echo Committing Core settings and Database...
git add app/__init__.py app/core/ app/db/database.py app/db/__init__.py
git commit -m "Setup configuration and SQLAlchemy connection"

echo Committing Database Models and Schemas...
git add app/db/models.py app/db/schemas.py
git commit -m "Create Product and PriceHistory database schemas"

echo Committing Core Services...
git add app/services/
git commit -m "Implement data fetching, parsing, and monitoring engines"

echo Committing API Layer...
git add app/api/ app/main.py run_refresh.py
git commit -m "Build FastAPI routing, endpoints, and background tasks"

echo Committing Tests...
git add tests/
git commit -m "Add unit and integration tests"

echo Committing Frontend Base...
git add frontend/package.json frontend/vite.config.js frontend/postcss.config.js frontend/tailwind.config.js frontend/index.html
git commit -m "Scaffold Vite React frontend and Tailwind"

echo Committing Frontend UI...
git add frontend/src/
git commit -m "Build dashboard UI and API integration"

echo Committing remaining files and datasets...
git add .
git commit -m "Include sample datasets and frontend lockfiles"

echo.
echo ==============================================
echo Done! Run 'git log' to see your step-by-step commits!
echo You can now push this to GitHub manually.
echo ==============================================
