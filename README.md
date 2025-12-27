🚀 Task Manager (Full-Stack Project)

A full-fledged task management web application built using modern technologies and best testing practices (QA).

🔗 Live Demo

👉 Open Website (Frontend): task-man-project-omega.vercel.app
👉 API Documentation (Swagger): https://task-man-project.onrender.com

(Note: Since the project is hosted on free tiers, the backend may take up to 50 seconds to "wake up" due to cold start).

🛠️ Tech Stack

Backend: Python, FastAPI, SQLAlchemy, Pydantic

Frontend: React, Vite, Material-UI (MUI), Axios

Database: PostgreSQL (Supabase)

DevOps & CI/CD: Docker, GitHub Actions, Render, Vercel

🧪 Testing Methods (Coursework Topic)

The project implements a comprehensive quality assurance strategy:

Unit Testing: Isolated testing of business logic (CRUD) using pytest.

Integration Testing: Testing API endpoints and database interaction (TestClient, sqlite::memory).

Frontend Testing: Testing React components using Vitest and React Testing Library.

Static Analysis: Automatic style and error checking using Ruff.

Coverage Analysis: Code coverage monitoring (98% Backend, 90% Frontend).


📦 How to Run Locally

Clone the repository:

git clone https://github.com/Andrm888/Task_Man_Project.git


Backend Setup:

cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Configure your .env file here
uvicorn main:app --reload


Frontend Setup:

cd frontend
npm install
npm run dev
