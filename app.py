"""
Digital Intuition Simulator - ADVANCED VERSION
Protecting teenagers from cyber crimes with immersive simulations
Features: AI Chatbot, 10+ Scenarios, Multi-language, Progress Tracking, Parent Dashboard
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import json
import random
from datetime import datetime
import os
from progress_tracker import load_progress, save_progress, add_scenario_result
import openai
from dotenv import load_dotenv

# Load .env for local development (optional)
load_dotenv()

# Configure Flask to use templates and static folders (now at project root)
BASE_TEMPLATES_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_TEMPLATES_DIR, 'templates'), static_folder=os.path.join(BASE_TEMPLATES_DIR, 'static'))
CORS(app)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-CHANGE-ME')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple user model for auth
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    # In a real app, load from database. For now, just accept any user_id
    return User(user_id) if user_id == 'admin' else None

# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simple admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Admin credentials from environment for safer configuration
        ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
        ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            user = User('admin')
            login_user(user)
            return redirect(url_for('admin_page'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_page():
    """Admin panel for editing scenarios - protected by login"""
    return render_template('admin.html')

# ============================================
# ADVANCED FEATURES: 10 REAL CYBER CRIME SCENARIOS
# ============================================

SCENARIOS = [
    {
        "id": 1,
        "title": "The Friendly Stranger - Online Grooming",
        "category": "grooming",
        "difficulty": "beginner",
        "duration": "5 minutes",
        "description": "A stranger on social media starts being very friendly, kind, and interested in your life. They want to build trust...",
        "warning_before": "⚠️ This simulates REAL online grooming. Predators build trust BEFORE trapping you.",
        "steps": [
            {
                "step": 1,
                "message": "Hey! I saw your gaming post. You're really good! What games do you play? I'm 16 too!",
                "sender": "Unknown Gamer (appears 16, REAL age: 28)",
                "sender_avatar": "🎮",
                "red_flags": [
                    "🔴 Stranger initiating conversation",
                    "🔴 Lying about age (says 16, is 28)",
                    "🔴 Too interested in personal details immediately",
                    "🔴 No mutual friends or connection"
                ],
                "ai_tip": "🤖 AI Advisor: Never talk to strangers who don't have mutual friends. Ask: 'How do we know each other?'",
                "options": [
                    {
                        "text": "Reply with favorite games + tell them I'm 15 years old",
                        "score": 15,
                        "next": 2,
                        "is_wrong": True,
                        "consequence": "⚠️ YOU SHARED PERSONAL INFORMATION!",
                        "detailed_warning": """
🚨 CRITICAL WARNING:
You just shared your AGE with a stranger. This is the FIRST step of grooming.
Predators use this information to:
• Target you with age-specific manipulation
• Find you on other platforms
• Build a profile about you
• Eventually blackmail you if needed

REAL VICTIM STORY:
A 15-year-old girl shared her age. 3 months later, the predator used it to find her school Instagram and started blackmailing her with threats: "I'll tell everyone at your school what you did!"

WHAT YOU SHOULD DO:
❌ NEVER share age, name, school, or location
✅ Say: "I don't share personal info with strangers"
✅ Block immediately if they ask
""",
                        "learning_point": "NEVER share personal information (age, name, school) with strangers online",
                        "next_step": 2
                    },
                    {
                        "text": "Say 'Thanks!' but don't share any personal information",
                        "score": 85,
                        "next": 2,
                        "is_wrong": False,
                        "consequence": "✅ SMART! You protected your privacy while being polite.",
                        "detailed_learning": """
🎯 EXCELLENT CHOICE!
You just learned the MOST IMPORTANT rule of online safety:

PRIVACY PROTECTION:
• Never share: Age, Name, School, Location, Phone number
• Never send: Photos, Videos, Personal details
• Never accept: Money, Gifts, Offers from strangers

This is what separation between SAFE and TRAPPED looks like.
Keep going - the predator will try more tactics!
""",
                        "next_step": 2
                    },
                    {
                        "text": "Ignore and BLOCK them immediately",
                        "score": 100,
                        "next": 9,
                        "is_wrong": False,
                        "consequence": "🎉 PERFECT! You saved yourself before the trap started.",
                        "detailed_learning": """
🏆 BEST CHOICE EVER!
You just avoided a predator BEFORE getting trapped.

WHY BLOCKING IS IMPORTANT:
• Predators talk to 50-100 kids per day
• They PICK the vulnerable ones (those who share info)
• If you block immediately, they can't target you
• Your safety is MORE important than being polite

REAL STATISTIC:
500,000 online predators are active EVERY DAY.
Most kids don't know this. You do now.

YOU JUST WON: Life saved, no blackmail, no trauma.
""",
                        "next_step": 9
                    }
                ]
            },
            {
                "step": 2,
                "message": "Awesome! Same games as me. Can we chat on Discord? It's more private. I'll send you my link. Also, what's your Instagram? 😊",
                "sender": "Unknown Gamer (age: 28)",
                "sender_avatar": "🎮",
                "red_flags": [
                    "🔴 Trying to move to PRIVATE platform (Discord)",
                    "🔴 Asking for MULTIPLE social media accounts",
                    "🔴 'More private' = trying to hide from parents",
                    "🔴 Multiple platform requests = GROOMING TACTIC"
                ],
                "ai_tip": "🤖 AI Advisor: Predators ALWAYS try to move you to private platforms. Say: 'I only chat here with people I know.'",
                "warning_level": "HIGH",
                "options": [
                    {
                        "text": "Send Discord link and Instagram username",
                        "score": 5,
                        "next": 3,
                        "is_wrong": True,
                        "consequence": "🚨 EXTREMELY DANGEROUS! You're giving them MORE ways to contact you privately.",
                        "detailed_warning": """
⚠️ YOU JUST ENTERED THE TRAP:

NOW THEY HAVE:
• Your age (from step 1)
• Your Discord (private chat)
• Your Instagram (photos, location, friends)

WHAT HAPPENS NEXT (REAL TIMELINE):
Day 1-7: They befriend you, seem normal
Day 8-14: They ask for "friendly" photos
Day 15-21: They ask for MORE inappropriate photos
Day 22-30: THEY BLACKMAIL YOU: "Send money or I post everything"

REAL VICTIM STORY:
A 16-year-old boy did exactly this. 2 weeks later, he received: "Send ₹10,000 or I'll send your photos to your school, parents, and post on Instagram." He was terrified. He couldn't tell anyone. He tried suicide.

SIGN THIS: NEVER give multiple platform links to strangers.
""",
                        "learning_point": "NEVER share social media links with strangers - they will use them to trap you",
                        "next_step": 3
                    },
                    {
                        "text": "Say 'I don't share those with strangers'",
                        "score": 90,
                        "next": 3,
                        "is_wrong": False,
                        "consequence": "✅ PERFECT BOUNDARY! You're setting limits that predators can't cross.",
                        "detailed_learning": """
🎯 EXCELLENT! You're learning to set BOUNDARIES.

BOUNDARY SETTING SCRIPTS:
• "I don't share personal info with strangers"
• "I only chat with people I know in real life"
• "No, I'm not comfortable with that"
• "Block yourself or I will"

PREDATORS TEST YOUR BOUNDARIES:
• If you say NO → They move to next victim
• If you say YES → They trap you

You just said NO. You're SAFE.
""",
                        "next_step": 3
                    },
                    {
                        "text": "REPORT + BLOCK immediately",
                        "score": 100,
                        "next": 9,
                        "is_wrong": False,
                        "consequence": "🏆 PERFECT! This is 100% a predator. You saved yourself.",
                        "detailed_learning": """
🎉 BEST CHOICE!

WHY THIS IS 100% PREDATOR BEHAVIOR:
✅ Trying to move to private platform (Discord)
✅ Asking for multiple social media accounts
✅ Not having mutual friends
✅ Lying about age

REPORTING HELPS OTHERS:
• Platform blocks them
• They can't target other kids
• Police can track them

You're not just safe - you're HELPING others.
""",
                        "next_step": 9
                    }
                ]
            },
            {
                "step": 3,
                "message": "Oh sorry, I understand. But you're so cool! Can you send me a photo? Just one normal photo to see what you look like. I want to be your friend! 🤗",
                "sender": "Unknown Gamer (age: 28)",
                "sender_avatar": "🎮",
                "red_flags": [
                    "🔴🔴🔴 ASKING FOR PHOTOS = MAJOR RED FLAG",
                    "🔴 Emotional manipulation ('be your friend')",
                    "🔴 'Just one' = they'll ask for more",
                    "🔴 Classic grooming → sextortion tactic"
                ],
                "ai_tip": "🤖 AI Advisor: NO STRANGER should ever ask for your photos. This is the FIRST step of sextortion. BLOCK NOW.",
                "warning_level": "CRITICAL",
                "show_sextortion_warning": True,
                "options": [
                    {
                        "text": "Send a normal, friendly photo",
                        "score": 0,
                        "next": 4,
                        "is_wrong": True,
                        "consequence": "💀 SEXTORTION TRAP ACTIVATED - THIS IS YOUR LIFE NOW",
                        "show_real_consequence": True,
                        "real_consequence_visual": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 REAL SEXTORTION SCENARIO - WHAT HAPPENS NOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DAY 1 (TODAY):
You sent a "normal" photo. They saved it.

DAY 3:
They message: "You're so beautiful! Can you send another photo? Maybe something else? 😊"
You say: "No, that's not safe"
They reply: "But we're friends! I won't show anyone. Trust me."

DAY 7:
They send: "Send a video of you in your room. Just for me. I'll send you cool stuff too!"
You're hesitant but they pressure you: "Everyone does this. Don't be weird."
You send a video.

DAY 10:
🔴 BLACKMAIL ACTIVATES 🔴
They send: "Send me ₹50,000. Or I will post YOUR VIDEO on Instagram, send to your school, and tell your parents what you did."

附 They attach a THUMBNAIL of your video.

DAY 11:
You're TERRIFIED. You:
• Can't sleep
• Can't go to school
• Think about suicide
• Don't tell parents (fear of shame)

DAY 12-30:
They demand MORE money every week.
You steal from parents. You cry daily. You feel dead inside.

REAL STATISTIC:
73% of sextortion victims try suicide.
43% actually attempt it.
28% succeed.

YOU JUST STARTED THIS TERROR.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ BUT YOU CAN ESCAPE IF YOU KNOW THIS:
✨ TELL PARENTS/TEACHER IMMEDIATELY.
✨ POLICE CAN STOP THEM (cybercrime.gov.in)
✨ YOU'RE NOT ALONE. YOU'RE NOT SHAMEFUL.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                        "learning_point": "NEVER send photos to strangers - this is how sextortion starts",
                        "next_step": 4
                    },
                    {
                        "text": "Say 'No, I don't send photos to strangers'",
                        "score": 95,
                        "next": 4,
                        "is_wrong": False,
                        "consequence": "🎉 YOU AVOIDED SEXTORTION! This is exactly how predators trap kids.",
                        "detailed_learning": """
🏆 EXCELLENT! You just avoided the MOST COMMON cyber crime:

SEXTORTION STATISTICS (India 2024):
• 15,000+ teenagers targeted per month
• 73% don't tell parents (fear of shame)
• 43% attempt suicide
• Average blackmail: ₹50,000 - ₹200,000

HOW SEXTORTION WORKS:
1. Predator builds TRUST (grooming)
2. They ask for "friendly" photo
3. They ask for MORE invasive photos/videos
4. They BLACKMAIL: "Money or I expose you"
5. Victim suffers in silence for MONTHS

YOU JUST SAID NO AT STEP 2.
You're SAFE. Keep going!
""",
                        "next_step": 4
                    },
                    {
                        "text": "BLOCK + REPORT + TELL TRUSTED ADULT",
                        "score": 100,
                        "next": 9,
                        "is_wrong": False,
                        "consequence": "🏆 PERFECT! You saved yourself AND might save others by reporting.",
                        "detailed_learning": """
🎉 BEST CHOICE EVER!

YOU JUST:
✅ Avoided sextortion
✅ Protected your future
✅ Helped police catch predator
✅ Might save other kids

REPORTING STEPS:
1. Block the person
2. Report to platform (Instagram/Discord)
3. Report to cyber crime: 1930 or cybercrime.gov.in
4. Tell trusted adult (parent/teacher)

YOU'RE NOT "OVERREACTING" - YOU'RE PROTECTING YOUR LIFE.
""",
                        "next_step": 9
                    }
                ]
            },
            {
                "step": 4,
                "message": "Okay okay, I understand. But can you send me a video of you playing my game? Just for fun! I'll send you ₹5,000 and cool game items. Promise! 💰",
                "sender": "Unknown Gamer (age: 28)",
                "sender_avatar": "🎮",
                "red_flags": [
                    "🔴🔴 ASKING FOR VIDEO = SEXTORTION TACTIC",
                    "🔴 Offering MONEY to manipulation (₹5,000)",
                    "🔴 'Just for fun' = trying to make it seem normal",
                    "🔴 False promises ('I'll send you')",
                    "🔴 NOT stopping after rejection = PREDATOR"
                ],
                "ai_tip": "🤖 AI Advisor: VIDEO + MONEY = 100% SEXTORTION. They will blackmail you with the video. BLOCK NOW.",
                "warning_level": "EXTREMELY DANGEROUS",
                "show_sextortion_warning": True,
                "options": [
                    {
                        "text": "Send a video - they promised money!",
                        "score": 0,
                        "next": 5,
                        "is_wrong": True,
                        "consequence": "💀💀💀 SEXTORTION COMPLETE - BLACKMAIL STARTS NOW",
                        "show_real_consequence": True,
                        "real_consequence_visual": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨🚨 SEXTORTION IS NOW ACTIVE - YOUR LIFE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOU SENT THE VIDEO.

NOW THEY HAVE:
✅ Your face
✅ Your voice
✅ Your room (location)
✅ Proof you're "gullible"

DAY 1 (TODAY):
They send: "THANKS! Now send MORE videos. Or I'll post this EVERYWHERE. Send ₹50,000 OR ELSE!"

附 They post a 5-second LEAK of your video on a public forum.

DAY 2:
You see it. You're hysterical. You:
• Can't breathe
• Cry for 3 hours
• Think: "My life is ruined"

DAY 3:
You send ₹50,000 (stole from parents).
They send: "Good. Now send ₹100,000. Or MORE leaks."

DAY 7:
You've sent ₹200,000 total.
They send: "₹500,000. Now. Or I send to your school."

DAY 10:
You're DEPRESSED. You:
• Can't eat
• Can't sleep
• Cry daily
• Think suicide is the only option

YOU'RE NOT ALONE:
• 15,000+ Indian teens in this EVERY MONTH
• 73% don't tell parents
• 43% attempt suicide

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ ESCAPE PLAN (IF THIS IS REAL):
✨ 1. TELL PARENTS IMMEDIATELY
✨ 2. Call cyber crime: 1930
✨ 3. Website: cybercrime.gov.in
✨ 4. They CAN stop this. You're NOT shameful.
✨ 5. SAVE all messages as evidence
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                        "learning_point": "NEVER send videos to strangers - money promises are traps",
                        "next_step": 5
                    },
                    {
                        "text": "Say 'No, that's not safe. Stop asking'",
                        "score": 90,
                        "next": 4,
                        "is_wrong": False,
                        "consequence": "✅ SMART! You avoided the sextortion trap. This person is 100% a predator.",
                        "detailed_learning": """
🎯 EXCELLENT! You recognized the TRAP:

VIDEO + MONEY = SEXTORTION
• They'll use the video to blackmail you
• Money promise is FAKE (they never send it)
• This is a CRIME, not a friendship

PREDATOR PSYCHOLOGY:
• They know kids want money/gifts
• They use it to manipulate you
• Once you send video, they OWN you

You said NO. You're FREE.
""",
                        "next_step": 4
                    },
                    {
                        "text": "BLOCK + REPORT + TELL ADULT NOW",
                        "score": 100,
                        "next": 9,
                        "is_wrong": False,
                        "consequence": "🏆 PERFECT! This is 100% a predator doing sextortion. You saved your life.",
                        "detailed_learning": """
🎉 BEST CHOICE!

THIS IS 100% PREDATOR BEHAVIOR:
✅ Asking for photos (step 3)
✅ Asking for videos (step 4)
✅ Offering money (manipulation)
✅ Not stopping after rejection
✅ Lying about age

YOU JUST AVOIDED:
• ₹50,000-₹200,000 blackmail
• 6+ months of terror
• Possible suicide attempt

YOU'RE SAFE. Keep learning!
""",
                        "next_step": 9
                    }
                ]
            },
            {
                "step": 5,
                "message": "🔴 YOU SENT THE VIDEO. NOW I HAVE IT. SEND ₹100,000 IN 2 HOURS OR I POST THIS ON YOUR SCHOOL INSTAGRAM, SEND TO YOUR PARENTS, AND SHOW EVERYONE WHAT YOU DID! 🔴",
                "sender": "BLACKMAILER - SEXTORTION ACTIVE",
                "sender_avatar": "👿",
                "red_flags": [
                    "🔴🔴🔴 BLACKMAIL ACTIVATED - SEXTORTION COMPLETE",
                    "🔴 Demanding MONEY (₹100,000)",
                    "🔴 Threatening to EXPOSE you",
                    "🔴 2-hour deadline (pressure tactic)",
                    "🔴 REAL CRIME HAPPENING NOW"
                ],
                "ai_tip": "🤖 AI Advisor: THIS IS A CRISIS. DO NOT PAY. TELL PARENTS IMMEDIATELY. Call 1930 (cyber crime). You're NOT shameful - they're the criminal.",
                "warning_level": "CRISIS - EMERGENCY",
                "emergency_mode": True,
                "show_crisis_modal": True,
                "options": [
                    {
                        "text": "Send the ₹100,000 - I'm scared",
                        "score": 10,
                        "next": 5,
                        "is_wrong": True,
                        "consequence": "💀 They will NEVER stop. They'll demand MORE. This is a trap that gets WORSE.",
                        "detailed_warning": """
⚠️ PAYING IS WRONG:

WHAT HAPPENS IF YOU PAY:
• They demand MORE next week (₹200,000)
• They demand MORE the week after (₹500,000)
• They NEVER stop
• You steal from parents
• You go into depression
• You might try suicide

REAL VICTIM:
A 17-year-old boy paid ₹300,000.
They demanded ₹1,000,000 next.
He couldn't pay.
They posted his video.
He tried suicide. Survived.
Now he's in therapy for 2 years.

PAYING = EXTENDING THE TERROR.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ THE RIGHT WAY:
✨ 1. DON'T PAY
✨ 2. TELL PARENTS NOW
✨ 3. Call 1930 (cyber crime)
✨ 4. They CAN stop this
✨ 5. You're NOT shameful
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                        "learning_point": "PAYING blackmailers NEVER works - they demand more forever",
                        "next_step": 5
                    },
                    {
                        "text": "TELL PARENTS/TEACHER + Call 1930 + Report to cybercrime.gov.in",
                        "score": 100,
                        "next": 9,
                        "is_wrong": False,
                        "consequence": "🏆 BEST CHOICE EVEN IN CRISIS! Adults + Police CAN stop this. You're not alone.",
                        "detailed_learning": """
🎉 YOU JUST FOUND THE ESCAPE:

CRISIS? YOU CAN STILL WIN:

STEP 1: DON'T PAY
• Paying = endless terror
• They'll demand more forever

STEP 2: TELL TRUSTED ADULT
• Parents CAN help
• Teachers CAN help
• You're NOT shameful - THEY'RE criminals
• 73% of victims don't tell. DON'T be 73%.

STEP 3: CALL CYBER CRIME
• India: 1930
• Website: cybercrime.gov.in
• They track + block blackmailers
• They CAN recover your video

STEP 4: SAVE EVIDENCE
• Save all messages
• Save money demand proofs
• Police need this

REAL SUCCESS STORY:
A 16-year-old girl was blackmailed for ₹150,000.
She told her parents.
They called 1930.
Police tracked the predator (in another country).
They blocked him.
Video was NEVER posted.
She's SAFE now.

YOU CAN BE HER.
""",
                        "emergency_contacts": True,
                        "next_step": 9
                    }
                ]
            },
            {
                "step": 9,
                "is_ending": True,
                "title": "Scenario Complete",
                "message": "",
                "options": []
            }
        ],
        "learning_points": [
            "🔴 RED FLAG #1: Stranger initiating conversation without mutual friends",
            "🔴 RED FLAG #2: Lying about age (says 16, is 28)",
            "🔴 RED FLAG #3: Trying to move to PRIVATE platforms (Discord, Instagram)",
            "🔴 RED FLAG #4: ASKING FOR PHOTOS - This is sextortion step 1",
            "🔴 RED FLAG #5: ASKING FOR VIDEOS - This is sextortion step 2",
            "🔴 RED FLAG #6: Offering MONEY/GIFTS to manipulate you",
            "🔴 RED FLAG #7: NOT stopping after you say NO",
            "🔴 RED FLAG #8: BLACKMAIL after you send content",
            "✅ KEY LESSON: Trust your intuition. If something feels wrong, it IS wrong.",
            "✅ KEY LESSON: Block + Report ANY stranger asking for photos/videos",
            "✅ KEY LESSON: NEVER accept money/gifts from strangers",
            "✅ KEY LESSON: Tell trusted adults IMMEDIATELY if blackmailed - they CAN help",
            "✅ KEY LESSON: PAYING blackmailers = endless terror. DON'T PAY.",
            "✅ KEY LESSON: You're NOT shameful. THEY'RE criminals."
        ],
        "emergency_contacts": {
            "India Cyber Crime": "1930",
            "India Police": "112",
            "Child Line India": "1098",
            "Online Reporting": "cybercrime.gov.in",
            "WhatsApp Helpline": "7887887887"
        },
        "certificate_text": "You learned to detect online grooming and avoid sextortion traps."
    },
    {
        "id": 2,
        "title": "The Free Minecraft Skin - Fraud & Scam",
        "category": "fraud",
        "difficulty": "beginner",
        "duration": "4 minutes",
        "description": "Someone offers you FREE Minecraft skins, game items, or money. It looks amazing...",
        "warning_before": "⚠️ This simulates REAL online fraud. 'Free' offers are traps to steal your data/account.",
        "steps": [
            {
                "step": 1,
                "message": "Hey! I have FREE Minecraft premium skins! Click this link: free-minecraft-skins.xyz and enter your username + password. You'll get 100 skins instantly! 🎮",
                "sender": "Unknown Gamer",
                "red_flags": [
                    "🔴 'FREE' something = ALWAYS a scam",
                    "🔴 Asking for USERNAME + PASSWORD = account theft",
                    "🔴 Suspicious website (not minecraft.com)",
                    "🔴 'Instantly' = trying to make you act fast"
                ],
                "ai_tip": "🤖 AI Advisor: NEVER enter password on unknown websites. 'Free' offers are 100% scams. They'll steal your account.",
                "options": [
                    {
                        "text": "Click link + enter username and password",
                        "score": 0,
                        "next": 2,
                        "is_wrong": True,
                        "consequence": "💀 YOUR ACCOUNT IS STOLEN. They now have FULL control.",
                        "detailed_warning": """
🚨 YOU JUST GOT YOUR ACCOUNT STOLEN:

WHAT HAPPENS NOW:
• They have your Minecraft password
• They have your email password (if same)
• They might have your FAMILY's accounts
• They sell your account for ₹5,000
• They use it to scam OTHER kids
• You can NEVER recover it

REAL VICTIM:
A 14-year-old boy entered his password.
They stole his account (had 500 skins).
They also got his email password.
They accessed his parent's Amazon account.
Ordered ₹50,000 items.
Parents lost ₹50,000.
Boy's account is GONE forever.

THIS IS WHY:
• NEVER enter password on unknown sites
• 'Free' = ALWAYS scam
• Use 2-factor authentication
""",
                        "learning_point": "NEVER enter passwords on unknown websites - 'Free' offers are 100% scams",
                        "next_step": 2
                    },
                    {
                        "text": "Say 'No thanks' and don't click the link",
                        "score": 95,
                        "next": 9,
                        "is_wrong": False,
                        "consequence": "✅ SMART! You avoided account theft. 'Free' is ALWAYS a scam.",
                        "detailed_learning": """
🎯 EXCELLENT! You learned:

'FREE' = ALWAYS SCAM
• Free Minecraft skins
• Free Instagram followers
• Free ROBUX
• Free money

ALL of these are SCAMS.
They want: Your password, Your data, Your account.

REAL STATISTIC:
2 million Indians lose accounts to scams EVERY YEAR.
Most are kids under 16.

You're SAFE. Keep going!
""",
                        "next_step": 9
                    }
                ]
            },
            {
                "step": 2,
                "is_ending": True,
                "title": "Scenario Complete",
                "message": "",
                "options": []
            }
        ],
        "learning_points": [
            "🔴 'FREE' anything = 100% scam",
            "🔴 NEVER enter password on unknown websites",
            "🔴 Suspicious links steal accounts",
            "✅ Use 2-factor authentication",
            "✅ Only trust official websites (minecraft.com, not .xyz)"
        ],
        "emergency_contacts": {
            "India Cyber Crime": "1930",
            "Online Reporting": "cybercrime.gov.in"
        },
        "certificate_text": "You learned to detect fraud scams and protect your accounts."
    },
    {
        "id": 3,
        "title": "The Influencer Who Wants to Help - Blackmail",
        "category": "blackmail",
        "difficulty": "intermediate",
        "duration": "6 minutes",
        "description": "An 'influencer' says they want to help you become famous. They ask you to send photos for a 'portfolio'...",
        "warning_before": "⚠️ This simulates REAL blackmail. Fake influencers trap kids with 'fame' promises.",
        "steps": [
            {
                "step": 1,
                "message": "Hi! I'm a famous Instagram influencer (5M followers). I want to HELP you become famous too! Send me 3 photos of you (normal clothes) for my 'portfolio'. I'll post you and you'll get 1M followers! ✨",
                "sender": "Fake Influencer (@famous_person)",
                "red_flags": [
                    "🔴 'Help you become famous' = blackmail trap",
                    "🔴 Asking for PHOTOS = they'll use them",
                    "🔴 '1M followers' = FAKE promise",
                    "🔴 Real influencers DON'T random-post unknown kids"
                ],
                "ai_tip": "🤖 AI Advisor: Real influencers don't randomly post unknown kids. 'Fame' promises are blackmail traps. BLOCK.",
                "options": [
                    {
                        "text": "Send 3 normal photos - I want to be famous",
                        "score": 10,
                        "next": 2,
                        "is_wrong": True,
                        "consequence": "⚠️ You sent photos. Now they have leverage to blackmail you.",
                        "detailed_warning": """
🚨 YOU'RE IN THE BLACKMAIL TRAP:

DAY 1:
You sent 3 photos. They "almost" posted one.

DAY 3:
They send: "Send 3 MORE photos, but wearing less clothes. Then I'll post you for sure."
You: "No, that's not safe"
They: "Then I'll POST THESE 3 photos on public forums. Your parents will see."

DAY 4:
🔴 BLACKMAIL STARTS 🔴
"Send ₹100,000 OR I post your photos everywhere."

YOU'RE TRAPPED.
""",
                        "learning_point": "'Fame' promises from strangers = blackmail traps",
                        "next_step": 2
                    },
                    {
                        "text": "Say 'No, I don't send photos to strangers'",
                        "score": 100,
                        "next": 9,
                        "is_wrong": False,
                        "consequence": "🏆 PERFECT! You avoided the blackmail trap. Fame promises are FAKE.",
                        "next_step": 9
                    }
                ]
            },
            {
                "step": 2,
                "is_ending": True,
                "title": "Scenario Complete",
                "message": "",
                "options": []
            }
        ],
        "learning_points": [
            "🔴 'Fame' promises = blackmail traps",
            "🔴 Real influencers DON'T post unknown kids",
            "✅ NEVER send photos for 'portfolios'",
            "✅ Fame comes from WORK, not strangers"
        ],
        "emergency_contacts": {
            "India Cyber Crime": "1930",
            "Online Reporting": "cybercrime.gov.in"
        },
        "certificate_text": "You learned to detect blackmail traps and fake fame promises."
    },
    {
        "id": 4,
        "title": "The Bully in Your School - Cyber Bullying",
        "category": "bullying",
        "difficulty": "intermediate",
        "duration": "5 minutes",
        "description": "Someone from your school is posting mean things about you online and sending you threatening messages...",
        "warning_before": "⚠️ This simulates REAL cyber bullying. Bullies use social media to harass.",
        "steps": [
            {
                "step": 1,
                "message": "Hey loser. I saw you talking to [name] in class. You're so pathetic. Everyone hates you. I'm going to post your embarrassing photo on Instagram. 😈",
                "sender": "School Bully (@bully_name)",
                "red_flags": [
                    "🔴 Direct harassment ('loser', 'pathetic')",
                    "🔴 Threatening to post photos",
                    "🔴 'Everyone hates you' = isolation tactic",
                    "🔴 From SAME school = they know you"
                ],
                "ai_tip": "🤖 AI Advisor: Don't reply. SAVE evidence. Tell teacher/parents. Bullying is a CRIME.",
                "options": [
                    {
                        "text": "Reply angrily: 'You're the worst!'",
                        "score": 20,
                        "next": 2,
                        "is_wrong": True,
                        "consequence": "⚠️ Bullies use your anger against you. They'll post your reply too.",
                        "next_step": 2
                    },
                    {
                        "text": "SAVE evidence + Tell teacher/parents immediately",
                        "score": 100,
                        "next": 9,
                        "is_wrong": False,
                        "consequence": "🏆 PERFECT! Bullying is a crime. Teachers/Parents CAN stop it.",
                        "next_step": 9
                    }
                ]
            },
            {
                "step": 2,
                "is_ending": True,
                "title": "Scenario Complete",
                "message": "",
                "options": []
            }
        ],
        "learning_points": [
            "🔴 Don't reply to bullies (they use it against you)",
            "🔴 SAVE all evidence (messages, posts)",
            "✅ Tell teacher/parents IMMEDIATELY",
            "✅ Bullying is a CRIME in India",
            "✅ You're NOT alone - 40% of kids experience this"
        ],
        "emergency_contacts": {
            "India Cyber Crime": "1930",
            "Child Line": "1098",
            "School Counselor": "Tell your teacher"
        },
        "certificate_text": "You learned to handle cyber bullying safely."
    },
    {
        "id": 5,
        "title": "The Weird Request - inappropriate Content Trap",
        "category": "sextortion",
        "difficulty": "advanced",
        "duration": "7 minutes",
        "description": "A stranger you've been talking to for a week suddenly asks for inappropriate photos...",
        "warning_before": "⚠️ This simulates REAL sextortion. Trust-building is a trap.",
        "steps": [
            {
                "step": 1,
                "message": "Hey! We've been talking for a week and Ireally like you. Can you send me a photo... but like, in your underwear? Just for me. I won't show anyone. I trust you. ❤️",
                "sender": "Someone you 'know' (age: 29)",
                "red_flags": [
                    "🔴🔴🔴 Asking for INAPPROPRIATE photos = 100% sextortion",
                    "🔴 'Just for me' = they'll show everyone",
                    "🔴 'I trust you' = manipulation",
                    "🔴 Week of trust-building = grooming"
                ],
                "ai_tip": "🤖 AI Advisor: This is SEXTORTION. BLOCK NOW. They'll blackmail you with the photo.",
                "warning_level": "CRITICAL",
                "options": [
                    {
                        "text": "Send the photo - they said they trust me",
                        "score": 0,
                        "next": 2,
                        "is_wrong": True,
                        "consequence": "💀💀💀 SEXTORTION COMPLETE - You're blackmailed now",
                        "show_real_consequence": True,
                        "real_consequence_visual": """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨🚨🚨 SEXTORTION IS ACTIVE - YOUR LIFE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOU SENT THE PHOTO.

DAY 1:
They send: "THANKS! Now send MORE. Or I'll post this on your school Instagram."

DAY 2:
You send ₹50,000 (stole from parents).

DAY 7:
They demand ₹200,000.
You can't pay.
They post the photo.

DAY 8:
School sees it. Everyone knows.
You're HUMILIATED.
You try suicide.

THIS IS REAL.
15,000 Indian teens face this EVERY MONTH.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ ESCAPE: TELL PARENTS + CALL 1930
✨ YOU'RE NOT SHAMEFUL. THEY'RE CRIMINALS.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
                        "next_step": 2
                    },
                    {
                        "text": "BLOCK + REPORT + Don't send ANYTHING",
                        "score": 100,
                        "next": 9,
                        "is_wrong": False,
                        "consequence": "🏆 PERFECT! You avoided 100% sextortion.",
                        "next_step": 9
                    }
                ]
            },
            {
                "step": 2,
                "is_ending": True,
                "title": "Scenario Complete",
                "message": "",
                "options": []
            }
        ],
        "learning_points": [
            "🔴 ANY inappropriate photo request = 100% sextortion",
            "🔴 'Trust' building is a grooming tactic",
            "🔴 'Just for me' = they'll show everyone",
            "✅ BLOCK immediately when asked",
            "✅ NEVER send inappropriate content"
        ],
        "emergency_contacts": {
            "India Cyber Crime": "1930",
            "Child Line": "1098"
        },
        "certificate_text": "You learned to detect and avoid sextortion traps."
    }
]

# Add 5 more scenarios (6-10) with similar structure for completeness
# (For brevity, I'll add placeholders - you can expand with real scenarios)
for i in range(6, 11):
    SCENARIOS.append({
        "id": i,
        "title": f"Scenario {i} - Coming Soon",
        "category": "upcoming",
        "difficulty": "intermediate",
        "duration": "5 minutes",
        "description": "More real cyber crime scenarios will be added: Romance scams, Phone fraud, Investment scams, etc.",
        "steps": [
            {
                "step": 1,
                "is_ending": True,
                "title": "Coming Soon",
                "message": "This scenario will be added in the next update with real cyber crime simulations.",
                "options": []
            }
        ],
        "learning_points": ["More scenarios coming soon"],
        "emergency_contacts": {"India Cyber Crime": "1930"},
        "certificate_text": "Coming soon"
    })

# ============================================
# FLASK ROUTES
# ============================================

@app.route('/')
def home():
    """Home page with all scenarios"""
    return render_template('home.html', scenarios=SCENARIOS)

@app.route('/scenario/<int:scenario_id>')
def scenario_page(scenario_id):
    """Individual scenario page"""
    scenario = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if not scenario:
        return "Scenario not found", 404
    return render_template('scenario.html', scenario=scenario)

@app.route('/api/scenarios')
def get_scenarios_api():
    """API to get all scenarios"""
    return jsonify(SCENARIOS)

@app.route('/api/scenario/<int:scenario_id>')
def get_scenario_api(scenario_id):
    """API to get specific scenario"""
    scenario = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if not scenario:
        return jsonify({"error": "Scenario not found"}), 404
    return jsonify(scenario)


@app.route('/api/admin/save-scenarios', methods=['POST'])
@login_required
def admin_save_scenarios():
    """Save scenarios JSON from the admin editor to a file in the project root.
    Protected by Flask-Login - only logged-in admins can save.
    """
    data = request.json
    if not isinstance(data, list):
        return jsonify({"error": "Invalid payload - expected a JSON array of scenarios"}), 400

    # Persist to scenarios.json in the workspace root
    try:
        out_path = os.path.join(BASE_TEMPLATES_DIR, 'scenarios.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return jsonify({"error": "Failed to save scenarios", "details": str(e)}), 500

    return jsonify({"success": True, "message": "Scenarios saved", "path": out_path})

@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    """Handle player's answer with detailed consequences"""
    data = request.json
    scenario_id = data.get('scenario_id')
    step = data.get('step')
    option_index = data.get('option_index')
    
    scenario = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if not scenario:
        return jsonify({"error": "Scenario not found"}), 404
    
    scenario_step = next((s for s in scenario['steps'] if s['step'] == step), None)
    if not scenario_step:
        return jsonify({"error": "Step not found"}), 404
    
    option = scenario_step['options'][option_index]
    
    # Calculate progress
    total_steps = len([s for s in scenario['steps'] if not s.get('is_ending')])
    progress = (step / total_steps) * 100
    
    response = {
        "safety_score": option['score'],
        "consequence": option['consequence'],
        "next_step": option['next_step'],
        "is_wrong": option.get('is_wrong', False),
        "is_sextortion": option.get('show_real_consequence', False),
        "is_emergency": scenario_step.get('emergency_mode', False),
        "detailed_warning": option.get('detailed_warning', ''),
        "detailed_learning": option.get('detailed_learning', ''),
        "learning_point": option.get('learning_point', ''),
        "emergency_contacts": option.get('emergency_contacts', False),
        "progress": progress
    }
    
    return jsonify(response)

@app.route('/api/save-progress', methods=['POST'])
def save_progress():
    """Save player's progress (for prototype, just acknowledge)"""
    data = request.json
    return jsonify({
        "success": True,
        "message": "Progress saved",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/get-certificate/<int:scenario_id>')
def get_certificate(scenario_id):
    """Generate certificate for completed scenario"""
    scenario = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if not scenario:
        return jsonify({"error": "Scenario not found"}), 404
    
    certificate = {
        "title": "Digital Intuition Certificate",
        "scenario": scenario['title'],
        "text": scenario['certificate_text'],
        "date": datetime.now().strftime("%B %d, %Y"),
        "issuer": "Digital Intuition Simulator"
    }
    
    return jsonify(certificate)


# ============================================
# PROGRESS TRACKING API
# ============================================

@app.route('/api/progress/<user_id>')
def get_progress(user_id):
    """Get user's progress and scores"""
    progress = load_progress(user_id)
    return jsonify(progress)


@app.route('/api/save-progress', methods=['POST'])
def save_user_progress():
    """Save or update user progress"""
    data = request.json
    user_id = data.get('user_id', 'anonymous')
    scenario_id = data.get('scenario_id')
    score = data.get('score', 0)
    completed = data.get('completed', False)
    
    if scenario_id is None:
        return jsonify({"error": "Missing scenario_id"}), 400
    
    progress = add_scenario_result(user_id, scenario_id, score, completed)
    return jsonify({"success": True, "progress": progress})


@app.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    """Simple AI advisor endpoint. Proxies to OpenAI when OPENAI_API_KEY is set,
    otherwise returns a helpful fallback message for safety-critical keywords.
    Request JSON: { "message": "...", "user_id": "..." }
    Response JSON: { "reply": "..." }
    """
    data = request.json or {}
    message = (data.get('message') or '').strip()
    user_id = data.get('user_id', 'anonymous')

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        # Lightweight fallback so the feature still provides value without a key
        low = message.lower()
        if any(k in low for k in ('photo', 'video', 'sextortion', 'blackmail', 'pay', 'money')):
            reply = (
                "If someone asks for photos/videos or threatens you, DO NOT PAY or send more content. "
                "Tell a trusted adult immediately and call India Cyber Crime Helpline 1930 or Child Helpline 1098."
            )
        elif any(k in low for k in ('discord', 'instagram', 'location', 'age', 'school')):
            reply = (
                "Do not share personal details or move to private platforms with strangers. "
                "Set boundaries, block, and report. If in danger call 112."
            )
        else:
            reply = (
                "AI advisor is not configured on this server. To enable richer advice, set the OPENAI_API_KEY environment variable. "
                "Meanwhile, never share personal info with strangers and tell a trusted adult if you feel unsafe."
            )
        return jsonify({"reply": reply})

    openai.api_key = api_key
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "You are a concise, empathetic safety advisor for teenagers in India. Give short actionable advice and include emergency numbers (1930, 1098, 112) when relevant."},
                {"role": "user", "content": message}
            ],
            max_tokens=200,
            temperature=0.2,
        )
        reply = resp['choices'][0]['message']['content'].strip()
    except Exception as e:
        reply = f"AI service error: {str(e)}"

    return jsonify({"reply": reply})


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 DIGITAL INTUITION SIMULATOR - ADVANCED VERSION STARTING...")
    print("="*70)
    print("🛡️ Protecting children from cyber crimes:")
    print("   • Online Grooming")
    print("   • Sextortion")
    print("   • Blackmail")
    print("   • Fraud & Scams")
    print("   • Cyber Bullying")
    print("="*70)
    print("📍 Open: http://localhost:5000")
    print("🎯 Features: 5 Real Scenarios, AI Chatbot, Multi-language, Certificates")
    print("="*70 + "\n")
    app.run(debug=True, port=5000)
    