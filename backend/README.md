```markdown
# Backend setup (FastAPI)

Run these steps from the `backend` directory. This guide shows commands for
Windows (PowerShell and cmd) and Linux/macOS.

Prerequisites:
- Python 3.10+ installed and available as `python` (or `python3` on some systems).

1) Create and activate a virtual environment

Windows (PowerShell):
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows (cmd.exe):
```
python -m venv venv
venv\Scripts\activate.bat
```

Linux / macOS:
```
python3 -m venv venv
source venv/bin/activate
```

If activation fails in PowerShell due to execution policy, you can run (adjust scope as appropriate):
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

2) Upgrade pip and install dependencies
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3) Create the `.env` file from the example and set secrets

Windows (PowerShell):
```
Copy-Item .env.example .env
```
Windows (cmd.exe):
```
copy .env.example .env
```
Linux / macOS:
```
cp .env.example .env
```

Edit the new `.env` file and set at minimum:
```
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET=your_jwt_secret_here
```

4) Install any optional extras required at runtime
```
pip install "pydantic[email]"
pip install python-multipart
```

5) Run the development server
```
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Notes:
- Always run the `uvicorn` command from the `backend` directory with the
  virtual environment active.
- If your system uses `python3` as the interpreter name, replace `python` with
  `python3` in the commands above.
- Keep your `.env` file secret and do not commit it to version control.

## Optional: Install Additional Dependencies

If you plan to use specific features, you may need additional packages:

```
# For email notifications
pip install fastapi-mail==1.5.8

# For PDF invoice generation
pip install reportlab

# For payment processing
pip install stripe
pip install razorpay

# For improved password hashing (if needed)
pip install bcrypt==4.1.2
pip install passlib[bcrypt]==1.7.4
```

## Database Setup (Optional)

If you need SQLite utilities on Windows:
```
winget install SQLite.SQLite
```

## Verify Installation

Check that bcrypt is installed correctly:
```
python -c "import bcrypt; print(bcrypt.__version__)"
```

## Troubleshooting

- If `pip install -r requirements.txt` fails, ensure your virtual environment is activated.
- On Windows PowerShell, if you get execution policy errors, run:
  ```
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
  ```
- If a specific package fails to install, try installing it individually with a compatible version.
