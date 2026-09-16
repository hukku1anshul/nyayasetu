# NyayaSetu & CardSmart Platform — Production Cloud Deployment Guide

This guide details how to deploy the **NyayaSetu & CardSmart** platform for 24/7 public access across India.

---

## 1. Zero-Cost 1-Click Cloud Deployment (Render.com)

**Render** offers a free cloud web service tier with automated SSL/HTTPS and zero maintenance:

1. **Push your code to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/nyayasetu.git
   git branch -M main
   git push -u origin main
   ```
2. **Deploy on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com/) and click **New + -> Blueprint**.
   - Connect your GitHub repository.
   - Render automatically reads [`render.yaml`](./render.yaml) and provisions:
     - **Build**: `pip install -r requirements.txt`
     - **Start**: `uvicorn nyayasetu.api:app --host 0.0.0.0 --port $PORT`
     - **Health Check**: `/health`
   - Your public HTTPS URL will be live instantly at: `https://nyayasetu-cardsmart.onrender.com`.

---

## 2. Fast Deployment via Railway.app / Fly.io

### Railway:
1. Go to [railway.app](https://railway.app/) and click **New Project -> Deploy from GitHub repo**.
2. Railway detects the `Procfile` and `requirements.txt` automatically.
3. In Project Settings -> **Networking**, click **Generate Domain** to get your public `.up.railway.app` URL.

### Fly.io:
1. Install flyctl: `winget install flyctl` or `curl -L https://fly.io/install.sh | sh`
2. Run in project directory:
   ```bash
   fly launch
   fly deploy
   ```

---

## 3. High-Performance Enterprise Deployment in India (AWS Mumbai / DigitalOcean)

To ensure sub-20ms latency directly inside Indian territory:

### AWS Mumbai (`ap-south-1`):
1. Build and push container to Amazon ECR:
   ```bash
   aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
   docker build -t nyayasetu .
   docker tag nyayasetu:latest <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/nyayasetu:latest
   docker push <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/nyayasetu:latest
   ```
2. Deploy as an **AWS App Runner** or **AWS ECS Fargate** service in `ap-south-1` (Mumbai).

### DigitalOcean Bangalore (`blr1`):
1. Create an App in DigitalOcean App Platform selecting Region **Bangalore (`blr1`)**.
2. Connect Git repo; select Dockerfile or Python buildpack.

---

## 4. Local Docker Container Run

To run locally inside a container that matches the exact cloud production environment:

```bash
docker build -t nyayasetu:latest .
docker run -p 8000:8000 nyayasetu:latest
```
Access at `http://localhost:8000/`.

---

## 5. Instant Live Public HTTPS Tunnel (Zero-Cost Testing)

To share the app with anyone across India right now without uploading to GitHub:
```powershell
# In terminal 1: Start local backend server
uvicorn nyayasetu.api:app --host 0.0.0.0 --port 8000

# In terminal 2: Expose via instant secure HTTPS tunnel
ssh -R 80:localhost:8000 a.pinggy.io
```
This gives you an immediate live URL (e.g. `https://XXXX.a.pinggy.link`) that anyone can open on mobile or desktop!
