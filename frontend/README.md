# Frontend Setup (React + Vite)

This is the frontend for **UKSChat** — a modern React + Vite application for the chat interface, authentication, and user dashboard.

## Prerequisites

- **Node.js 16+** (includes npm or yarn)
- **npm** or **yarn** package manager
- Backend running at `http://localhost:8000` (for API calls)

## Quick Start

### 1. Navigate to the frontend directory

```bash
cd frontend
```

### 2. Install dependencies

Using npm:
```bash
npm install
```

Or using yarn:
```bash
yarn install
```

### 3. Start the development server

Using npm:
```bash
npm run dev
```

Or using yarn:
```bash
yarn dev
```

The app will start on **`http://localhost:5173`** (or another port if 5173 is in use — check terminal output).

### 4. Open in browser

Navigate to `http://localhost:5173` and you should see the UKSChat login page.

## Project Structure

```
frontend/
 src/
    main.jsx              # Vite entry point
    App.jsx               # Root component
    api.js                # API client (axios or fetch wrapper)
    components/           # Reusable components
       ChatMessage.jsx   # Chat message display
       Navbar.jsx        # Navigation bar
       ...other components
    pages/                # Full page components
       Login.jsx         # Login page
       Register.jsx      # Registration page
       Chat.jsx          # Main chat interface
       Billing.jsx       # Billing/subscription page
       Pricing.jsx       # Pricing page
       Profile.jsx       # User profile
       AdminDashboard.jsx
    App.css               # Global styles
    index.css             # Base styles
    styles.css            # Component styles
 public/                   # Static assets
 index.html                # HTML template
 vite.config.js            # Vite configuration
 eslint.config.js          # ESLint configuration
 package.json              # Dependencies
 README.md                 # This file
```

## Available Scripts

```bash
# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Preview the production build locally
npm run preview

# Run ESLint to check code quality
npm run lint
```

## API Integration

The frontend communicates with the FastAPI backend via HTTP requests. The base URL is configured in `src/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';  // Update for production
```

**Key endpoints used:**
- `POST /auth/register` – User registration
- `POST /auth/login` – User login (stores JWT token)
- `GET /chat/messages` – Fetch chat history
- `POST /chat/send` – Send a message
- `GET /payments/history` – Payment history
- `GET /plans` – List subscription plans
- And more (see backend `/docs` for full API spec)

### Authentication

JWT tokens are stored in localStorage after login:
```javascript
localStorage.setItem('token', response.data.access_token);
```

Include the token in request headers:
```javascript
headers: {
  'Authorization': `Bearer ${localStorage.getItem('token')}`
}
```

## Development Workflow

1. **Edit files** in `src/` — changes auto-reload via Vite's HMR (Hot Module Replacement)
2. **Check browser console** for errors
3. **Use browser DevTools** to debug React components
4. **Backend API** must be running for chat and auth features to work

## Building for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized, minified static files. Deploy this folder to:
- **Vercel** (recommended for Vite projects)
- **Netlify**
- **GitHub Pages**
- **AWS S3 + CloudFront**
- Or any static file host

### Environment Variables for Production

Create a `.env.production` file (or use host environment):
```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

Then update `src/api.js` to use:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

## Linting & Code Quality

Run ESLint to check code style:
```bash
npm run lint
```

Fix common issues automatically:
```bash
npm run lint -- --fix
```

## Technology Stack

- **React 18+** – UI library
- **Vite** – Build tool and dev server
- **Axios** or **Fetch API** – HTTP client
- **ESLint** – Code linting
- **CSS** or **Tailwind CSS** (if configured) – Styling

## Troubleshooting

### Port 5173 already in use

Vite will automatically use the next available port. Check terminal for the actual URL.

Or manually specify a port:
```bash
npm run dev -- --port 3000
```

### CORS errors when calling backend

**Error:** `Access to XMLHttpRequest has been blocked by CORS policy`

**Solution:** Ensure backend has CORS enabled. In FastAPI `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Backend not responding

1. Verify backend is running: `http://localhost:8000/docs`
2. Check `src/api.js` for correct backend URL
3. Ensure no firewall is blocking localhost connections
4. Check browser console for detailed error messages

### Changes not reflecting in browser

1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Clear browser cache and cookies
3. Clear node_modules and reinstall: `rm -r node_modules; npm install`

## Resources

- **React Documentation**: https://react.dev/
- **Vite Documentation**: https://vitejs.dev/
- **Axios Documentation**: https://axios-http.com/
- **MDN Web Docs**: https://developer.mozilla.org/

---

**Happy coding! **
