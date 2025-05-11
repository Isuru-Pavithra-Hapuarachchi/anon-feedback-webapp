# 📬 Anonymous Feedback Web App (NGL-style Clone)

This is a lightweight anonymous feedback web application inspired by the NGL concept, allowing users to submit anonymous messages through a simple web interface. The backend is implemented using **Python (Flask)** and deployed on a **DigitalOcean Ubuntu cloud server**.

🔗 **Live Demo:** [https://anonymouse.gleeze.com](https://anonymouse.gleeze.com)

---

## 🚀 Features

- 🔒 Submit and receive anonymous feedback
- 🧱 Backend powered by Python (Flask) and SQLite
- 🌐 Hosted on a DigitalOcean Ubuntu cloud instance
- 🐍 Virtual environment used for dependency isolation
- 🌍 Custom domain mapped using Gleeze (Free domain)
- 📦 Lightweight and easy to deploy

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML (Jinja2 templates)
- **Database:** SQLite
- **Web Server:** NGINX
- **WSGI Server:** Gunicorn
- **Hosting:** DigitalOcean (Ubuntu Minimal)
- **Domain Provider:** gleeze.com

---

## ⚙️ Setup Instructions

Follow these steps to deploy the application on a fresh Ubuntu server (DigitalOcean):

### 1. Connect to your Server and Install Required Packages

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx -y
```

### 2. Clone the Repository & Set Up Project Directory

```bash
mkdir -p /var/www/ngl_app
cd /var/www/ngl_app
git clone https://github.com/Isuru-Pavithra-Hapuarachchi/anon-feedback-webapp.git
```

### 3. Create and Activate Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4.  Install Python Dependencies

```bash
pip install -r requirements.txt

```
### 5. Configure WSGI and NGINX

Set up wsgi.py for running with Gunicorn or uWSGI and configure NGINX to serve the app.

This part depends on your setup; you can provide your own config instructions or add an nginx.conf.example file.

```bash
sudo nano /etc/nginx/sites-available/ngl_app
```
```sh
server {
    listen 80;
    server_name domain name;

    location / {
        proxy_pass http://127.0.0.1:5000;
        include proxy_params;
        proxy_redirect off;
    }
}

```
```bash
sudo ln -s /etc/nginx/sites-available/ngl_app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. Set Up SSL (HTTPS) Using Let's Encrypt and Certbot:

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d domainname

```
### 7. Run the application

```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app --daemon

```

