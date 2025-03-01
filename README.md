# 📌 Transcendence - Real-Time Multiplayer Pong Game

A **real-time multiplayer Pong game** built using **Django, Docker, and PostgreSQL**, with **OAuth authentication, live chat, tournaments, and 2FA security**. Designed as part of the **42 Paris curriculum**, focusing on **full-stack development, DevOps, and real-time applications**.

---

## 🚀 Features
### 👉 Major Modules
- **Backend Framework**: Django
- **Real-time Multiplayer**: Remote players with WebSockets
- **Live Chat**: Integrated real-time messaging
- **User Management & Authentication**:
  - Standard user management
  - OAuth 2.0 authentication via 42 Intra
  - **Two-Factor Authentication (2FA) & JWT security**
- **Frontend with JavaScript**: Interactive UI built with vanilla JavaScript
- **Server-Side Pong Logic**: Game physics computed on the server

### 👉 Minor Modules
- **Database**: PostgreSQL
- **Cross-Browser Compatibility**
- **Bootstrap for UI styling**
- **Responsive Design**: Works on all devices
- **Monitoring System**: Prometheus, Grafana, AlertManager

---

## 🛠️ Tech Stack
| Category      | Technologies Used |
|--------------|-----------------|
| **Backend**  | Django, WebSockets |
| **Frontend** | JavaScript, Bootstrap |
| **Database** | PostgreSQL |
| **Auth**     | OAuth 2.0 (42 Intra), JWT, 2FA |
| **DevOps**   | Docker, Prometheus, Grafana |

---

## 📝 Installation & Setup
### 📂 1️⃣ Clone the Repository
```sh
git clone https://github.com/karagoz36/transcendence.git
cd transcendence
```

### 🔧 2️⃣ Configure Environment Variables
Copy the example environment file:
```sh
cp srcs/.env.template srcs/.env
```
Then, open the `.env` file and fill in the required values:

```ini
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=

# OAUTH42
OAUTH_SECRET_KEY=
OAUTH_CLIENT_ID=
OAUTH_REDIRECT_URI=
```
📈 **These variables are required for authentication and AlertManager functionality.**
📈 **Make sure to provide valid credentials before running the project.**

### 🎮 3️⃣ Build & Start the Containers
```sh
make build
make up
```
🔹 **This will:**
- Build the **Django backend** container
- Start all required services (**PostgreSQL, Nginx, Prometheus, Grafana**)
- Set up **OAuth authentication and WebSockets**

### 💪 4️⃣ Run Tests
To execute unit tests inside the Django container:
```sh
make test
```

### ⚡ 5️⃣ Stop & Clean Up
To stop the containers:
```sh
make down
```
To completely remove all Docker containers, images, and volumes:
```sh
make clean
```

---

## 🌍 Monitoring & Logs
**Monitoring stack** includes:
- **Prometheus** (Metrics Collection)
- **Grafana** (Visualization)
- **AlertManager** (Notifications)

### 📊 Access Dashboards
| Service       | URL                                      |
|--------------|------------------------------------------|
| **Django Backend** | [http://localhost:8000/](http://localhost:8000/) |
| **Prometheus**     | [http://localhost:8000/prometheus/](http://localhost:8000/prometheus/) |
| **Grafana**        | [http://localhost:3000/grafana/](http://localhost:3000/grafana/) |

---

## 🎨 Screenshots
| Home Page | Game Interface |
|-----------|---------------|
| ![Home Page](https://via.placeholder.com/500x250) | ![Game Interface](https://via.placeholder.com/500x250) |

---

## 💡 Updates
- Contributors and License sections removed.
- `.env.template` file should be renamed to `.env` before running `make`.
- Authentication and AlertManager required environment variables are listed.

---
