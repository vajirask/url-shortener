# 🔗 Microservices URL Shortener

A Bit.ly-style URL shortener built using a **microservices architecture**, demonstrating real-world DevOps practices: containerization, orchestration, and CI/CD automation.

---

## 🏗️ Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Client      │ --> │  Flask API    │ --> │  PostgreSQL   │
│  (Browser)    │     │   Service     │     │  (Database)   │
└──────────────┘     └──────────────┘     └──────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │ Redis Cache   │
                      └──────────────┘
```

**How it works:**
1. User sends a long URL to `/shorten`
2. API generates a random short code and saves the mapping in PostgreSQL
3. The mapping is also cached in Redis for fast lookups
4. Visiting `/<short_code>` redirects to the original URL (served from cache if available)

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python (Flask) |
| Database | PostgreSQL |
| Cache | Redis |
| Containerization | Docker, Docker Compose |
| Orchestration | Kubernetes (Minikube) |
| CI/CD | GitHub Actions |
| Version Control | Git, GitHub |

---

## 📂 Project Structure

```
url-shortener/
├── api/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .dockerignore
├── k8s/
│   ├── api-deployment.yaml
│   ├── postgres-deployment.yaml
│   └── redis-deployment.yaml
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── docker-compose.yml
└── README.md
```

---

## 🚀 How to Run

### Option A — Docker Compose (Quick local testing)

```bash
# Clone the repo
git clone https://github.com/vajirask/url-shortener.git
cd url-shortener

# Build and start all services
docker-compose up --build
```

App will be available at: **http://127.0.0.1:5000**

To stop:
```bash
docker-compose down
```

---

### Option B — Kubernetes (Minikube)

```bash
# Start Minikube
minikube start --driver=docker

# Build the API image inside Minikube's Docker environment
minikube docker-env | Invoke-Expression   # PowerShell
docker build -t url-shortener-api:latest ./api

# Deploy all services
cd k8s
kubectl apply -f postgres-deployment.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f api-deployment.yaml

# Check pod status
kubectl get pods

# Access the app
minikube service api --url
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health/info message |
| GET | `/health` | Health check |
| POST | `/shorten` | Create a short URL |
| GET | `/<short_code>` | Redirect to the original URL |

### Example: Shorten a URL

```bash
curl -X POST http://127.0.0.1:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

**Response:**
```json
{
  "short_code": "OZgdC4",
  "short_url": "http://localhost:5000/OZgdC4",
  "original_url": "https://www.google.com"
}
```

Visiting `http://127.0.0.1:5000/OZgdC4` redirects to `https://www.google.com`.

---

## ⚙️ CI/CD Pipeline

On every push to `main`, GitHub Actions automatically:
1. Builds the Docker image for the API
2. Spins up the full stack with Docker Compose
3. Runs health checks against `/health` and `/shorten`
4. Tears down the environment

See `.github/workflows/ci-cd.yml` for details.

---

## 🎓 What This Project Demonstrates

- Multi-container microservices architecture
- Service-to-service communication (API ↔ DB ↔ Cache)
- Infrastructure orchestration with Kubernetes (including self-healing pods)
- Automated testing and build pipelines with GitHub Actions
- Real-world DevOps workflow from local development to deployment

---

## 👤 Author

**vajirask**
GitHub: [github.com/vajirask](https://github.com/vajirask)