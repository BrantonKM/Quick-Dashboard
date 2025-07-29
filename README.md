📊 Quick Dashboard
A Flask-based Admin Dashboard to monitor and export real-time data from multiple sources such as Weather, Crypto, Stocks, and News. Built with PostgreSQL, Docker, and Pandas for efficient data handling and reporting.

🚀 Project Overview
Quick Dashboard is a web-based analytics tool tailored for administrative teams to:

Monitor real-time logs across key sections.

Filter and export data based on date range and category.

Secure admin login with session-based authentication.

Generate downloadable reports in Excel format.

The dashboard is modular, lightweight, and optimized for local or containerized deployments.

📁 Directory Structure
quick-dashboard/
│
├── app.py                      # Main Flask application
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── docker-compose.yml          # Compose setup for web + DB
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   └── login.html
│
├── static/                     # Static assets (CSS, JS)
│   └── style.css
│
├── exports/                    # Utilities for generating exports
│   └── export_utils.py
│
├── reports/                    # Report filters and logic
│   └── filters.py
│
├── data/                       # Data output and archival
│   └── archive/
│
├── migrations/                 # DB migration folder (if using Alembic)
└── .gitignore
⚙️ Features
🔐 Secure Admin Login

📦 Filter by section (weather, crypto, stocks, news)

📅 Export reports within a date range

📊 Tabular view of fetched logs

🐳 Containerized with Docker

🧪 Debug-friendly with logging

🛠️ Tech Stack
Backend: Python, Flask

Frontend: HTML5, CSS3

Database: PostgreSQL

Export Engine: Pandas, OpenPyXL

Deployment: Docker & Docker Compose

🖥️ Setup & Installation
1. Clone the repo
git clone https://github.com/your-username/quick-dashboard.git
cd quick-dashboard
2. Add environment variables
Create a .env file at the root:

env
FLASK_APP=app.py
FLASK_ENV=development
POSTGRES_DB=quickdashboarddb
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
DATABASE_URL=postgresql://admin:admin123@db:5432/quickdashboarddb
SECRET_KEY=your-secure-secret
3. Build and run the containers
docker-compose up --build
Visit the app at http://localhost:5000

📤 Exporting Reports
Visit the /report or /export route:

Filter by section (e.g. weather, crypto, stocks)

Specify a date range

Click to download .xlsx reports

🧪 Sample Query (PostgreSQL)
sql
Copy
Edit
SELECT * FROM dashboard_logs
WHERE section = 'crypto'
AND fetched_at BETWEEN '2025-07-01' AND '2025-07-29'
ORDER BY fetched_at DESC;
🛡️ Security Notes
This app uses a simple admin login — for production, implement hashed passwords and user roles.

Debug mode is ON by default — remember to disable in production.

🧰 To Do (Optional Enhancements)
✅ Pagination for long logs

✅ Export format toggle: Excel / CSV / PDF

🔒 Multi-user authentication

📈 Visualization charts

🌐 Deploy to cloud (e.g., Render, Heroku, EC2)

👨‍💻 Author
Branton Kieti
Entrepreneur, Data Scientist
📫 Reach me via Github

📄 License
This project is licensed under the MIT License