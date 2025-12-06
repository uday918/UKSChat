# UKSChat

UKSChat is a full-stack chat application that combines a **FastAPI** backend with a **Vite + React** frontend. It demonstrates user authentication, JWT-based sessions, OpenAI-powered chat functionality, and basic subscription/billing management. Use it as a starter template for building AI-enabled chat applications.

## Features

- **User Authentication**: Registration, login, and JWT-based session management
- **Chat Interface**: Real-time chat UI built with React + Vite
- **OpenAI Integration**: Chat powered by OpenAI API (configure API key in `.env`)
- **Subscription & Billing**: Example admin routes and models for managing plans and payments
- **Modular Backend**: FastAPI with organized routers and Pydantic schemas
- **Fast Frontend Dev**: Vite for rapid development and hot module replacement (HMR)
- **Environment-Based Config**: Secrets and keys managed via `.env` (not committed)

## Project Structure

```
UKSChat/
├── backend/                      # FastAPI application
│   ├── main.py                   # Entry point
│   ├── models.py                 # Database models
│   ├── schemas.py                # Pydantic schemas
│   ├── database.py               # Database setup
│   ├── auth_utils.py             # JWT and auth helpers
│   ├── requirements.txt           # Python dependencies
│   ├── README.md                 # Backend setup guide
│   ├── routers/                  # API route handlers
│   │   ├── auth.py               # Authentication endpoints
│   │   ├── chat.py               # Chat endpoints
│   │   ├── payments.py           # Payment endpoints
│   │   ├── admin_plans.py        # Plan management
│   │   ├── admin_billing.py      # Billing admin
│   │   └── subscriptions.py      # Subscription management
│   ├── utils/                    # Utility modules
│   │   ├── mailer.py             # Email utilities
│   │   └── invoice.py            # Invoice generation
│   └── dbseeders/                # Database seeder scripts
│
├── frontend/                     # Vite + React application
│   ├── src/
│   │   ├── main.jsx              # React entry point
│   │   ├── App.jsx               # Root component
│   │   ├── api.js                # API client
│   │   ├── components/           # Reusable components
│   │   │   ├── ChatMessage.jsx   # Chat message display
│   │   │   └── Navbar.jsx        # Navigation bar
│   │   └── pages/                # Page components
│   │       ├── Login.jsx         # Login page
│   │       ├── Register.jsx      # Registration page
│   │       ├── Chat.jsx          # Main chat interface
│   │       ├── Billing.jsx       # Billing page
│   │       ├── Pricing.jsx       # Pricing page
│   │       ├── Profile.jsx       # User profile
│   │       ├── AdminDashboard.jsx
│   │       ├── AdminPayments.jsx
│   │       └── AdminPlans.jsx
│   ├── vite.config.js            # Vite configuration
│   ├── package.json              # Node dependencies
│   ├── index.html                # HTML template
│   └── README.md                 # Frontend setup guide
│
├── .gitignore                    # Git ignore rules (includes .env, venv, node_modules)
└── README.md                     # This file
```

## Quick Start

### Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 16+** (for frontend)
- **Git** with GitHub CLI (`gh`) optional but recommended
- **OpenAI API Key** (get one at https://platform.openai.com/account/api-keys)

### Backend Setup

1. Navigate to the backend directory:
```powershell
cd backend
```

2. Create and activate a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (cmd.exe):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Upgrade pip and install dependencies:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Create `.env` file from the example and set secrets:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Windows (cmd.exe):**
```cmd
copy .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

5. Edit `.env` and add your keys:
```env
OPENAI_API_KEY=sk-...your-key-here...
JWT_SECRET=your_super_secret_jwt_key_here
DATABASE_URL=sqlite:///./chat.db
```

6. Install optional extras (if needed at runtime):
```bash
pip install "pydantic[email]"
pip install python-multipart
```

7. Run the development server:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend is now running at `http://localhost:8000`. API docs available at `http://localhost:8000/docs`.

### Frontend Setup

1. Navigate to the frontend directory (in a new terminal):
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

Frontend will typically run at `http://localhost:5173` (check terminal for the exact port).

4. Open the app in your browser and log in with your credentials.

## API Documentation

Once the backend is running, visit **`http://localhost:8000/docs`** for interactive Swagger UI documentation of all available endpoints.

Key endpoints:
- `POST /auth/register` – User registration
- `POST /auth/login` – User login
- `GET /chat/messages` – Fetch chat history
- `POST /chat/send` – Send a message (integrates with OpenAI)
- `GET /plans` – List subscription plans
- `GET /payments/history` – Payment history for admin
- And more (see `/docs` for full list)

## Environment Variables

Create a `.env` file in the `backend/` directory (never commit this file):

```env
# Required
OPENAI_API_KEY=sk-...your-openai-api-key...
JWT_SECRET=your-secret-jwt-key-keep-this-safe
DATABASE_URL=sqlite:///./chat.db

# Optional
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Development Workflow

### Running Both Services Locally

1. **Terminal 1** – Backend:
```powershell
cd backend
.\venv\Scripts\Activate.ps1  # or source venv/bin/activate on Linux/Mac
uvicorn main:app --reload
```

2. **Terminal 2** – Frontend:
```powershell
cd frontend
npm run dev
```

3. **Terminal 3** (Optional) – Database admin/seeding:
```powershell
cd backend
python backend/dbseeders/UserSeeder.py  # Example seeder
```

### Making Changes

- **Backend changes**: Uvicorn auto-reloads on file save
- **Frontend changes**: Vite's HMR instantly updates the browser

## Deployment

### Backend (FastAPI + Uvicorn)

For production, replace `--reload` with proper settings:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or containerize with Docker:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Vite)

Build for production:
```bash
cd frontend
npm run build
```

This generates a `dist/` folder with static files. Deploy to any static host (Vercel, Netlify, GitHub Pages, S3, etc.).

## Security Notes

⚠️ **Important**:
- Never commit `.env` files (included in `.gitignore`)
- Keep `JWT_SECRET` and `OPENAI_API_KEY` safe and unique
- Use HTTPS in production
- Validate and sanitize all user inputs
- Consider rate limiting on public APIs
- Regularly update dependencies (`pip`, `npm`)

## Troubleshooting

### Backend won't start

- Ensure Python 3.10+ is installed: `python --version`
- Check virtual environment is activated
- Verify `.env` exists and `OPENAI_API_KEY` is set
- Review error logs in terminal

### Frontend build errors

- Clear `node_modules` and reinstall: `rm -r node_modules; npm install`
- Clear Vite cache: `rm -r .vite`
- Ensure Node.js 16+ is installed: `node --version`

### Cannot connect to backend from frontend

- Ensure backend is running: `http://localhost:8000/docs` accessible
- Check `src/api.js` has correct backend URL (should be `http://localhost:8000` for local dev)
- Check browser console for CORS errors; backend may need CORS config

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "feat: add your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request

## License

This project is provided as-is for educational and development purposes. See `LICENSE` file (if present) for details.

## Support & Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **Vite Docs**: https://vitejs.dev/
- **OpenAI API**: https://platform.openai.com/docs/
- **Pydantic Docs**: https://docs.pydantic.dev/

---

**Built with ❤️ – Happy coding!**
