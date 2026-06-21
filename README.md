# Digital Intuition Simulator

> A web-based educational platform that teaches teenagers to recognize and defend against online cyber crimes through interactive, immersive scenarios.

## 🎯 Mission

Protect teenagers from:
- **Online Grooming** — predators building false trust to exploit
- **Sextortion** — blackmail using intimate content
- **Scams & Fraud** — fake offers stealing accounts/money
- **Blackmail** — threats to expose personal information
- **Cyber Bullying** — harassment and public shaming online

**Key Stats:**
- 10+ real-world scenarios based on actual crimes
- Progress tracking & score system
- Emergency help triggers with 24/7 hotline contacts
- Admin panel to manage scenarios
- Completely free & safe

---

## 🚀 Quick Start (Windows)

### 1. Clone & Setup

```powershell
# Clone the repo (if using Git)
git clone https://github.com/yourusername/digital-intuition-simulator.git
cd digital-intuition-simulator

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Locally

```powershell
python app.py
```

Visit: **http://127.0.0.1:5000**

### 3. Access Admin Panel

- **URL:** http://127.0.0.1:5000/login
- **Username:** `admin`
- **Password:** `admin123`

⚠️ *Change credentials before production deployment*

---

## 📁 Project Structure

```
digital-intuition-simulator/
├── app.py                          # Main Flask application
├── progress_tracker.py             # User progress & score storage
├── requirements.txt                # Python dependencies
├── Procfile                        # Heroku deployment config
├── runtime.txt                     # Python version for Heroku
├── README.md                       # This file
│
├── templates/
│   ├── home.html                  # Landing page with scenario list
│   ├── scenario.html              # Interactive scenario gameplay
│   ├── login.html                 # Admin login page
│   └── admin.html                 # Admin scenario editor
│
├── static/
│   ├── css/
│   │   └── style.css              # Base styles
│   └── js/
│       └── admin.js               # Admin editor functionality
│
├── .github/
│   └── workflows/
│       └── test-deploy.yml        # CI/CD pipeline (GitHub Actions)
│
├── .data/                         # User progress data (created at runtime)
│   └── progress_*.json
│
└── tools/
    ├── check_scenario.py          # Test endpoint script
    └── save_scenarios.py           # Export scenarios to JSON
```

---

## 🛠️ Features

### Student Experience
✅ Interactive scenarios with branching choices  
✅ Real-time scoring feedback  
✅ Emergency help modal with hotline contacts  
✅ Progress tracking (localStorage + server)  
✅ Mobile-responsive Bootstrap UI  
✅ No sign-up required — play anonymously or with user ID  

### Admin Panel
✅ View all scenarios in JSON format  
✅ Edit scenarios live  
✅ Save changes to `scenarios.json`  
✅ Protected by Flask-Login (admin/admin123)  

### Safety Features
✅ High-risk choices trigger emergency help modal  
✅ Direct links to India Cyber Crime Helpline (1930)  
✅ Child Helpline (1098) and Police (112)  
✅ WhatsApp helpline integration  
✅ Empowering language — no victim-shaming  

---

## 📊 API Endpoints

### Environment / Secrets

Create a `.env` file in the project root (copy from `.env.example`) before running locally. Do NOT commit `.env`.

Example `.env` variables (see `.env.example`):

```
SECRET_KEY=change_this_to_a_random_secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
OPENAI_API_KEY=sk-REPLACE_WITH_YOUR_KEY  # optional, enables richer AI replies
```

On Heroku add these as config vars (Dashboard → Settings → Reveal Config Vars) or via CLI:

```powershell
heroku config:set SECRET_KEY="your-secret" ADMIN_USERNAME="admin" ADMIN_PASSWORD="your-password" OPENAI_API_KEY="sk-..."
```


### Public Endpoints
- `GET /` — Home page with scenario list
- `GET /scenario/<id>` — Play a scenario
- `GET /api/scenarios` — Get all scenarios (JSON)
- `GET /api/scenario/<id>` — Get specific scenario
- `POST /api/save-progress` — Save user progress

### Admin Endpoints (requires login)
- `GET /login` — Admin login page
- `POST /login` — Submit login credentials
- `GET /logout` — Clear session
- `GET /admin` — Scenario editor
- `POST /api/admin/save-scenarios` — Save scenario JSON

---

## 🌐 Deployment

### Option 1: Heroku (Recommended)

**Prerequisites:**
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [Git](https://git-scm.com/)
- GitHub account

**Steps:**

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secure-random-key
heroku config:set ADMIN_PASSWORD=your-secure-password

# Deploy
git push heroku main

# Open app
heroku open
```

**Enable GitHub Actions deployment** (auto-deploy on `main` branch push):
1. Go to Heroku dashboard → Account Settings → API Key
2. Copy your API key
3. Go to GitHub Repo → Settings → Secrets and variables → Actions
4. Add secrets:
   - `HEROKU_API_KEY`
   - `HEROKU_APP_NAME`
   - `HEROKU_EMAIL`
   - `SECRET_KEY`

### Option 2: Google Cloud Run

```bash
# Create container
gcloud builds submit --tag gcr.io/PROJECT-ID/dis

# Deploy
gcloud run deploy dis --image gcr.io/PROJECT-ID/dis --platform managed
```

### Option 3: Docker (Local/Any Server)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app"]
```

```bash
docker build -t dis .
docker run -p 5000:5000 dis
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Development
export FLASK_ENV=development
export SECRET_KEY=dev-key

# Production
export SECRET_KEY=your-secure-random-key
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=your-password
```

### Change Admin Credentials

Edit `app.py`, find the login route (~line 47):

```python
if username == 'admin' and password == 'admin123':  # ← Change these
```

---

## 📈 User Progress Storage

- **Local Storage:** Progress saved to browser localStorage with user ID
- **Server Storage:** Progress saved to `.data/progress_*.json` files
- **Migration:** Export `.data/` files for backup/migration to database

### Sample Progress Data

```json
{
  "scenarios": {
    "1": {
      "score": 85,
      "completed": true,
      "timestamp": "2026-06-21T10:30:00"
    }
  }
}
```

---

## 🧪 Testing

### Manual Testing

```bash
# Test endpoints
python tools/check_scenario.py

# Verify app imports
python -c "import app; print('✅ App OK')"
```

### Automated Tests (CI/CD)

Pushing to `main` branch triggers `.github/workflows/test-deploy.yml`:
- Installs dependencies
- Runs basic syntax checks
- Attempts import test
- (Optional) Deploy to Heroku

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

**Code Style:**
- Python: PEP 8 (use `flake8` to check)
- JavaScript: Modern ES6+, no framework dependencies
- HTML/CSS: Bootstrap 5, semantic HTML

---

## 🆘 Emergency Resources (India)

| Service | Number | Website |
|---------|--------|---------|
| Cyber Crime Helpline | 1930 | cybercrime.gov.in |
| Child Helpline | 1098 | childlineindia.org |
| Police Emergency | 112 | – |
| WhatsApp Help | +91 7887887887 | WhatsApp |

---

## 📜 License

This project is **Open Source** (MIT License). See LICENSE file for details.

---

## 🙏 Credits & Acknowledgments

Built with ❤️ to protect India's youth from cyber crimes.

- Framework: Flask, Bootstrap 5
- Languages: Python, JavaScript, HTML/CSS
- Inspired by real victim stories and cyber crime prevention research

---

## 📞 Support & Contact

- **Report bugs:** GitHub Issues
- **Suggestions:** GitHub Discussions
- **Contact:** khushipundir@example.com (Replace with actual contact)

**In Crisis?** Don't wait. Call **1930** or **1098** immediately.

---

## ⚡ Roadmap

- [ ] Multi-language support (Hindi, regional languages)
- [ ] Parent/teacher dashboard
- [ ] Gamification (badges, leaderboard)
- [ ] AI-powered personalized recommendations
- [ ] Integration with real cyber crime reporting
- [ ] Mobile app (React Native)
- [ ] Offline mode for schools
- [ ] Analytics dashboard for educators

---

**Made with care to save lives. 🛡️**
