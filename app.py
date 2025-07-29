from flask import Flask, render_template, request, redirect, url_for, session, send_file
from functools import wraps
import requests
import psycopg2
import os
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from datetime import datetime
import csv
from io import StringIO
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecret")

# PostgreSQL config
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_NAME = os.environ.get("POSTGRES_DB", "quickdashboarddb")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASS = os.environ.get("POSTGRES_PASSWORD", "password")

# API keys
WEATHER_KEY = os.environ.get("OPENWEATHERMAP_KEY")
STOCK_KEY = os.environ.get("ALPHA_VANTAGE_KEY")
NEWS_KEY = os.environ.get("NEWSAPI_KEY")

# Connect to PostgreSQL
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# Create logs table if not exists
def create_log_table():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS dashboard_logs (
                    id SERIAL PRIMARY KEY,
                    section TEXT,
                    content JSONB,
                    fetched_at TIMESTAMP
                )
            """)
            conn.commit()

# Log data to PostgreSQL
def log_data(section, content):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO dashboard_logs (section, content, fetched_at) VALUES (%s, %s, %s)",
                (section, json.dumps(content), datetime.now())
            )
            conn.commit()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin_logged_in" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

# Routes
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form["username"] == os.environ.get("ADMIN_USERNAME") and
            request.form["password"] == os.environ.get("ADMIN_PASSWORD")
        ):
            session["admin_logged_in"] = True
            return redirect(url_for("dashboard"))
        return "Invalid credentials", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("login"))

@app.route("/export")
@login_required
def export():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Section", "Content", "Fetched At"])

    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT section, content::text, fetched_at FROM dashboard_logs ORDER BY fetched_at DESC")
            for row in cur.fetchall():
                writer.writerow(row)

    output.seek(0)
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='dashboard_logs.csv'
    )
@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    section = request.args.get("section")
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    query = "SELECT section, content::text, fetched_at FROM dashboard_logs WHERE 1=1"
    params = []

    if section:
        query += " AND section = %s"
        params.append(section)

    if start_date:
        query += " AND fetched_at >= %s"
        params.append(start_date)

    if end_date:
        query += " AND fetched_at <= %s"
        params.append(end_date)

    query += " ORDER BY fetched_at DESC"

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Section", "Content", "Fetched At"])

    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, tuple(params))
            for row in cur.fetchall():
                writer.writerow(row)

    output.seek(0)
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name='filtered_report.csv'
    )

@app.route("/dashboard")
@login_required
def dashboard():
    create_log_table()

    # 🌦 Weather
    try:
        weather_data = get_weather()
        print("Weather API response:", weather_data)  # Add this
        weather = {
            "city": weather_data["name"],
            "temp": weather_data["main"]["temp"],
            "description": weather_data["weather"][0]["description"]
        }
        log_data("weather", weather_data)
    except Exception as e:
        print("Weather fetch error:", e)
        weather = None

    # ₿ Crypto
    cryptos = []
    try:
        res = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1").json()
        cryptos = [{"name": coin["name"], "current_price": coin["current_price"]} for coin in res]
        log_data("crypto", res)
    except Exception as e:
        print("Crypto fetch error:", e)

    # 📈 Stocks
    stock_symbols = ["AAPL", "MSFT", "GOOGL"]
    stocks = {}
    try:
        for symbol in stock_symbols:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={STOCK_KEY}"
            res = requests.get(url).json()
            price = res["Global Quote"]["05. price"]
            stocks[symbol] = {"price": round(float(price), 2)}
        log_data("stocks", stocks)
    except Exception as e:
        print("Stock fetch error:", e)

    # 📰 News
    news = []
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=5&apiKey={NEWS_KEY}"
        res = requests.get(url).json()
        articles = res.get("articles", [])
        news = [{"title": a["title"], "url": a["url"], "source": a["source"]["name"]} for a in articles]
        log_data("news", res)
    except Exception as e:
        print("News fetch error:", e)

    return render_template("dashboard.html", weather=weather, cryptos=cryptos, stocks=stocks, news=news)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
