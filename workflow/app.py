import gradio as gr
import sqlite3
import hashlib
from apscheduler.schedulers.background import BackgroundScheduler
import time
from gather_news import gather_news
from workflow import main
import asyncio

# ---------------- Database Setup ---------------- #
conn = sqlite3.connect("newsletter.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password_hash TEXT,
    preferences TEXT,
    subscribed INTEGER
)
""")
conn.commit()

# ---------------- Helper Functions ---------------- #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(email, password):
    if not email or not password:
        return "Email and password required."
    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", 
                  (email, hash_password(password), "", 0))
        conn.commit()
        return "✅ Account created. Please log in."
    except sqlite3.IntegrityError:
        return "❌ Email already registered."

def login(email, password):
    c.execute("SELECT password_hash FROM users WHERE email=?", (email,))
    row = c.fetchone()
    if row and row[0] == hash_password(password):
        sessions[email] = True
        return (
            "✅ Login successful.",
            gr.update(visible=False),  # hide signup
            gr.update(visible=False),  # hide login
            email,                     # set email in state
            gr.update(visible=True)    # show dashboard
        )
    return (
        "❌ Invalid login",
        gr.update(),
        gr.update(),
        None,
        gr.update(visible=False)       # keep dashboard hidden
    )



def load_dashboard(email):
    c.execute("SELECT preferences, subscribed FROM users WHERE email=?", (email,))
    row = c.fetchone()
    if row:
        prefs, sub = row
        return prefs, bool(sub)
    return "", False

def save_preferences(email, prefs, subscribed):
    c.execute("UPDATE users SET preferences=?, subscribed=? WHERE email=?",
              (prefs, int(subscribed), email))
    conn.commit()
    return "✅ Preferences saved."

# ------------- Scheduler Jobs ------------- #
def scheduled_gather_news():
    """Run gather_news() every day at 4 AM."""
    print("Running gather_news() at 4 AM...")
    gather_news()

def scheduled_main_jobs():
    """Run workflow.main() for all subscribed users at 6 AM daily."""
    async def run_all():
        c.execute("SELECT email, preferences FROM users WHERE subscribed=1")
        users = c.fetchall()
        tasks = []
        for email, prefs in users:
            if not prefs:
                prefs = "Any important news"
            tasks.append(main(prompt=prefs, recipient_email=email))
        await asyncio.gather(*tasks)

    print("Running workflow.main() at 6 AM...")
    asyncio.run(run_all())

# ------------- Scheduler Setup ------------- #
scheduler = BackgroundScheduler()

# Gather news at 4 AM daily
scheduler.add_job(scheduled_gather_news, "cron", hour=4, minute=0)

# Run workflow.main for all subscribed users at 6 AM daily
scheduler.add_job(scheduled_main_jobs, "cron", hour=6, minute=0)

scheduler.start()

# ---------------- Gradio Interface ---------------- #
sessions = {}  # Track logged-in users (in-memory)

with gr.Blocks() as demo:
    state_email = gr.State()

    # --- Sign Up ---
    with gr.Row(visible=True) as signup_page:
        with gr.Column():
            gr.Markdown("## Sign Up")
            signup_email = gr.Textbox(label="Email")
            signup_password = gr.Textbox(label="Password", type="password")
            signup_btn = gr.Button("Sign Up")
            signup_output = gr.Markdown()
    signup_btn.click(signup, [signup_email, signup_password], signup_output)

    # --- Login ---
    with gr.Row(visible=True) as login_page:
        with gr.Column():
            gr.Markdown("## Login")
            login_email = gr.Textbox(label="Email")
            login_password = gr.Textbox(label="Password", type="password")
            login_btn = gr.Button("Login")
            login_output = gr.Markdown()

    # --- Dashboard (define `dashboard` row explicitly!) ---
    with gr.Row(visible=False) as dashboard:
        with gr.Column():
            gr.Markdown("## Dashboard")
            prefs_box = gr.Textbox(label="News Preferences")
            sub_box = gr.Checkbox(label="Subscribe to newsletter")
            save_btn = gr.Button("Save Preferences")
            save_output = gr.Markdown()

            # load user settings after login
            state_email.change(load_dashboard, [state_email], [prefs_box, sub_box])

            save_btn.click(save_preferences, [state_email, prefs_box, sub_box], save_output)

    # --- Hook up login button with 5 outputs ---
    login_btn.click(
        login,
        [login_email, login_password],
        [login_output, signup_page, login_page, state_email, dashboard]
    )

demo.launch()
