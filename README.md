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

```bash
# Clone the repo
git clone https://github.com/yourusername/digital-intuition-simulator.git
cd digital-intuition-simulator

# Create virtual environment
python -m venv .venv
# Activate
.\.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Locally

```bash
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
├── Procfile                        # Deployment config (Heroku/Render)
├── runtime.txt                     # Python version for deployment
├── README.md                       # Documentation
├── .gitignore                      # Git ignore rules
├── .env.example                    # Example environment variables
│
├── templates/                      # HTML templates
│   ├── home.html                   # Landing page with scenario list
│   ├── scenario.html               # Interactive scenario gameplay
│   ├── login.html                  # Admin login page
│   ├── admin.html                  # Admin scenario editor
│   └── scenarios.json              # Scenario data storage
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css               # Base styles
│   ├── js/
│   │   ├── ai.js                   # AI chat widget logic
│   │   └── admin.js                # Admin editor functionality
│   ├── data/                       # Scenario data files
│   └── assets/                     # Images/icons
│
├── tools/                          # Utility scripts
│   ├── check_scenario.py           # Test endpoint script
│   └── save_scenarios.py           # Export scenarios to JSON
│
├── .github/                        # GitHub Actions CI/CD
│   └── workflows/
│       └── test-deploy.yml         # Pipeline for testing & deployment
│
├── .venv/                          # Virtual environment (local only)
├── __pycache__/                    # Python cache files
└── .data/                          # User progress data (runtime)
    └── progress_*.json
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
## 🔑 Environment / Secrets

Create a `.env` file in the project root (copy from `.env.example`) before running locally. Do **NOT** commit `.env`.

Example `.env` variables:

```env
SECRET_KEY=change_this_to_a_random_secret
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
OPENAI_API_KEY=sk-REPLACE_WITH_YOUR_KEY  # optional, enables richer AI replies
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

### Option 1: Render (Recommended, Free)
- Push code to GitHub.
- [Go to](render.com)
- Create New Web Service → connect repo.
- Build Command:
```bash
pip install -r requirements.txt
```
Start Command:
```bash
python app.py
```
Render gives you a live URL:-
[https://digital-intuition-simulator.onrender.com]

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
| Cyber Crime Helpline | 1930 | [cybercrime.gov.in] |
| Child Helpline | 1098 | [childlineindia.org] |
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
- **Contact:** bhawanapundir123@gmail.com 

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
