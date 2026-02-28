📊 Quick Dashboard

A Flask-based Admin Analytics Dashboard for monitoring and exporting real-time data from multiple sources such as Weather, Crypto, Stocks, and News.

Built with PostgreSQL, Docker, and Pandas, this project demonstrates modular backend design, containerized deployment, and efficient data reporting workflows.

🚀 Project Overview

Quick Dashboard is a lightweight web-based analytics tool designed for administrative and data teams who need structured visibility into system logs and external data feeds.

It allows users to:

Monitor real-time logs across multiple data sections

Filter records by category and date range

Export structured reports in Excel format

Authenticate securely via session-based login

Deploy locally or in a containerized environment

The system emphasizes clean architecture, maintainability, and scalability for future enhancements.

⚙️ Core Features

🔐 Admin Authentication (session-based login)

📦 Section Filtering (Weather, Crypto, Stocks, News)

📅 Date-Range Report Generation

📊 Structured Tabular Log View

📤 Excel Export (.xlsx)

🐳 Dockerized Deployment

🧪 Debug-Friendly Logging

🛠️ Tech Stack
Layer	Technology
Backend	Python, Flask
Database	PostgreSQL
Data Engine	Pandas, OpenPyXL
Frontend	HTML5, CSS3
Deployment	Docker, Docker Compose
📁 Project Structure
quick-dashboard/
│
├── app.py                  # Main Flask application
├── .env                    # Environment configuration
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Multi-container setup
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── dashboard.html
│   └── login.html
│
├── static/                 # Static assets
│   └── style.css
│
├── exports/                # Export utilities
│   └── export_utils.py
│
├── reports/                # Report filters and query logic
│   └── filters.py
│
├── data/                   # Data storage & archives
│   └── archive/
│
├── migrations/             # Database migrations (Alembic)
└── .gitignore
🖥️ Setup & Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/quick-dashboard.git
cd quick-dashboard
2️⃣ Configure Environment Variables

Create a .env file in the root directory:

FLASK_APP=app.py
FLASK_ENV=development

POSTGRES_DB=quickdashboarddb
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123

DATABASE_URL=postgresql://admin:admin123@db:5432/quickdashboarddb
SECRET_KEY=your-secure-secret
3️⃣ Build & Run with Docker
docker-compose up --build

Access the application at:

http://localhost:5000
📤 Exporting Reports

Navigate to:

/report

or

/export

You can:

Select a data section (weather, crypto, stocks, news)

Define a date range

Download structured .xlsx reports

🧪 Example PostgreSQL Query
SELECT *
FROM dashboard_logs
WHERE section = 'crypto'
AND fetched_at BETWEEN '2025-07-01' AND '2025-07-29'
ORDER BY fetched_at DESC;
🛡️ Security Considerations

The current version uses a basic admin authentication system.

For production environments:

Implement password hashing (e.g., bcrypt)

Add role-based access control

Disable debug mode

Use environment-based secrets management

📈 Future Improvements

✅ Pagination for large datasets

✅ Multiple export formats (CSV / PDF)

🔒 Multi-user authentication & RBAC

📊 Integrated data visualizations

🌐 Cloud deployment (Render / AWS EC2 / Railway)

📡 Background job scheduling for automated data ingestion

👨‍💻 Author

Branton Kieti
Entrepreneur | Data Scientist | Data Engineer

Passionate about building data-driven systems, ETL workflows, and scalable reporting solutions.

📄 License

This project is licensed under the MIT License.
