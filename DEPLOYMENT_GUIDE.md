# 🚀 Buongiorno - Complete Deployment Guide

This guide will help you deploy the complete Buongiorno application using **free hosting services**:
- **Backend API** → Render (free tier)
- **Frontend** → Vercel (free tier)
- **Daily Pipeline** → Render Cron Job (free tier)

---

## 📋 Prerequisites

1. **GitHub Account** - For code repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
4. **Git installed** - To push code to GitHub

---

## 🗂️ Step 1: Push Code to GitHub

### 1.1 Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Name your repository: `buongiorno`
3. Make it **Public** (required for free tiers)
4. **Don't** initialize with README (we already have code)
5. Click **Create repository**

### 1.2 Push Your Code

```bash
cd C:\Users\danie\Desktop\Python\buon_giorno

# Check current status
git status

# Add all deployment files
git add .

# Commit
git commit -m "Add deployment configuration for Render and Vercel

- Added unified requirements.txt for deployment
- Created Procfile for Render web service
- Created render.yaml for infrastructure as code
- Added production pipeline runner script
- Updated frontend to use environment variables for API URL
- Updated CORS to allow deployed frontend
- Added comprehensive .gitignore
- Updated pipeline requirements to include statsmodels

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to GitHub (replace with your repository URL if different)
git push origin main
```

---

## 🌐 Step 2: Deploy Backend to Render

### 2.1 Deploy Using render.yaml (Recommended)

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository (`buongiorno`)
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**
6. Wait for deployment (5-10 minutes)

✅ This will create TWO services:
- **buongiorno-api** - Web service (FastAPI)
- **buongiorno-daily-pipeline** - Cron job (runs daily at 8 AM UTC)

### 2.2 Manual Deployment (Alternative)

If you prefer manual setup:

#### Deploy API:
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository
3. Configure:
   - **Name**: `buongiorno-api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend/api && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
4. Click **"Create Web Service"**

#### Deploy Cron Job:
1. Click **"New +"** → **"Cron Job"**
2. Connect same GitHub repository
3. Configure:
   - **Name**: `buongiorno-daily-pipeline`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Command**: `python run_pipeline_prod.py`
   - **Schedule**: `0 8 * * *` (Daily at 8 AM UTC)
4. Click **"Create Cron Job"**

### 2.3 Get Your API URL

After deployment:
1. Go to your **buongiorno-api** service
2. Copy the URL (e.g., `https://buongiorno-api-xxxx.onrender.com`)
3. **Save this URL** - you'll need it for the frontend

### 2.4 Test the API

Visit these URLs to verify:
- `https://your-api-url.onrender.com/` - Should show API info
- `https://your-api-url.onrender.com/health` - Should return `{"status":"healthy"}`
- `https://your-api-url.onrender.com/docs` - API documentation
- `https://your-api-url.onrender.com/api/predictions/latest` - Latest prediction

⚠️ **Note**: First request may take 30-60 seconds (free tier spins down after inactivity)

---

## 🎨 Step 3: Deploy Frontend to Vercel

### 3.1 Deploy from GitHub

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your **buongiorno** repository
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)

### 3.2 Add Environment Variable

**IMPORTANT**: Before deploying, add your API URL:

1. In Vercel project settings, go to **"Environment Variables"**
2. Add:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-api-url.onrender.com/api` (from Step 2.3)
   - **Environment**: Production
3. Click **"Save"**

### 3.3 Deploy

1. Click **"Deploy"**
2. Wait 1-2 minutes
3. Vercel will give you a URL like: `https://buongiorno-xxx.vercel.app`

### 3.4 Test the Frontend

1. Visit your Vercel URL
2. You should see the Buongiorno dashboard
3. It will load the latest prediction from your Render API

---

## ✅ Step 4: Verify Everything Works

### Backend API Checklist:
- [ ] API accessible at Render URL
- [ ] `/health` endpoint returns healthy status
- [ ] `/api/predictions/latest` returns prediction data
- [ ] API docs accessible at `/docs`
- [ ] Cron job shows as "Healthy" in Render dashboard

### Frontend Checklist:
- [ ] Frontend accessible at Vercel URL
- [ ] Dashboard loads without errors
- [ ] Prediction data displays correctly
- [ ] Trend indicators working
- [ ] Model information showing

### Integration Checklist:
- [ ] Frontend successfully fetches data from backend
- [ ] No CORS errors in browser console
- [ ] Refresh button works
- [ ] Data updates correctly

---

## 🔄 Step 5: Test the Daily Pipeline

The pipeline runs automatically at 8:00 AM UTC daily, but you can test it manually:

### In Render Dashboard:
1. Go to your **buongiorno-daily-pipeline** cron job
2. Click **"Trigger Run"**
3. Watch the logs
4. Verify it completes successfully
5. Check the API to see updated predictions

### Expected Behavior:
- Fetches latest gold price data
- Processes and engineers features
- Trains ARIMA and Moving Average models
- Generates next-day prediction
- Updates the API data automatically

---

## 🎯 Optional: Custom Domain

### For Frontend (Vercel):
1. Go to Vercel project → **Settings** → **Domains**
2. Add your custom domain
3. Follow Vercel's DNS instructions

### For Backend (Render):
1. Go to Render service → **Settings**
2. Add custom domain (requires paid plan)

---

## 📊 Monitoring & Logs

### Render:
- **Logs**: Click on service → **Logs** tab
- **Metrics**: See CPU, memory usage
- **Events**: Deployment history

### Vercel:
- **Analytics**: Free analytics available
- **Logs**: Real-time function logs
- **Deployments**: See all deployments and rollback if needed

---

## 🔒 Security Best Practices

### 1. Update CORS for Production

After deployment, update `backend/api/main.py`:

```python
allow_origins=[
    "https://your-frontend.vercel.app",  # Your actual Vercel URL
],
allow_credentials=True,
```

### 2. Add Rate Limiting (Optional)

Consider adding rate limiting to prevent abuse:

```bash
pip install slowapi
```

### 3. Environment Variables

Never commit:
- `.env` files
- API keys
- Secrets

Already configured in `.gitignore`

---

## 💰 Cost Breakdown (Free Tiers)

| Service | Free Tier Limits |
|---------|-----------------|
| **Render Web** | 750 hours/month, sleeps after inactivity |
| **Render Cron** | Unlimited cron jobs on free plan |
| **Vercel** | 100 GB bandwidth/month, unlimited deployments |

⚠️ **Free tier limitations**:
- API sleeps after 15 min inactivity (cold starts)
- Daily pipeline runs once per day
- No custom domains on backend free tier

---

## 🛠️ Troubleshooting

### Backend Issues:

**Problem**: "Application failed to respond"
- **Solution**: Check logs in Render dashboard
- Verify `requirements.txt` includes all dependencies
- Check Python version compatibility

**Problem**: Pipeline fails
- **Solution**: Check cron job logs
- Ensure data files are writable
- Verify yfinance can fetch data

### Frontend Issues:

**Problem**: "Failed to fetch predictions"
- **Solution**: Verify `VITE_API_URL` environment variable
- Check CORS settings in backend
- Verify API is running and healthy

**Problem**: Blank page
- **Solution**: Check browser console for errors
- Verify build succeeded in Vercel
- Check Vercel deployment logs

### Integration Issues:

**Problem**: CORS errors
- **Solution**: Add Vercel URL to CORS origins in backend
- Set `allow_credentials=False` when using wildcard
- Redeploy backend after changes

---

## 🔄 Making Updates

### Update Frontend:
```bash
git add frontend/
git commit -m "Update frontend"
git push
```
Vercel auto-deploys on push to main

### Update Backend:
```bash
git add backend/
git commit -m "Update backend"
git push
```
Render auto-deploys on push to main

### Update Dependencies:
```bash
# Update requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## 📱 Share Your App

Once deployed:
- **Frontend URL**: `https://buongiorno-xxx.vercel.app`
- **API URL**: `https://buongiorno-api-xxx.onrender.com`
- **API Docs**: `https://buongiorno-api-xxx.onrender.com/docs`

Share the frontend URL with users!

---

## 🎓 Next Steps

After deployment:
1. ✅ Monitor daily pipeline execution
2. ✅ Collect 10+ days of predictions
3. ✅ Analyze prediction accuracy
4. ✅ Add new features (email notifications, SMS alerts)
5. ✅ Expand to other commodities (silver, oil)
6. ✅ Improve models (add LSTM, Prophet)

---

## 🆘 Need Help?

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Vite Docs**: [vitejs.dev](https://vitejs.dev)

---

## 📄 License & Credits

Built with:
- FastAPI + Python for backend
- React + Vite for frontend
- ARIMA & Moving Average models
- Yahoo Finance for data
- Render & Vercel for hosting

---

**You're all set! 🎉 Your Buongiorno app is now live and accessible worldwide!**
