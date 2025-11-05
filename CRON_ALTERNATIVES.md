# 🔄 Free Cron Job Alternatives for Daily Pipeline

Since Render removed free cron jobs, here are **100% FREE alternatives** to run your daily pipeline:

---

## ⭐ **Option 1: GitHub Actions (RECOMMENDED)**

✅ **Best option** - Completely free, reliable, integrated with your repo

### How it works:
- Runs directly on GitHub's infrastructure
- 2000 minutes/month free (you'll use ~50 minutes/month)
- Auto-commits updated predictions back to your repo
- Render API auto-deploys when repo updates

### Setup (Already done for you!):

The workflow file is already created: `.github/workflows/daily-pipeline.yml`

**Just commit and push:**

```bash
cd C:\Users\danie\Desktop\Python\buon_giorno
git add .github/
git commit -m "Add GitHub Actions workflow for daily pipeline"
git push
```

### How to use:

1. **Automatic**: Runs every day at 8:00 AM UTC
2. **Manual trigger**: Go to GitHub → Actions → "Daily Gold Price Prediction Pipeline" → "Run workflow"

### View logs:
- Go to your GitHub repo → **Actions** tab
- Click on any workflow run to see logs

---

## 🌐 **Option 2: Free Webhook Cron Service**

Use a free external cron service to ping your API endpoint.

### Setup:

1. **Deploy your API to Render** (as you're doing)
2. **Use endpoint**: `https://your-api.onrender.com/api/pipeline/run`
3. **Pick a free cron service**:

#### **cron-job.org** (Recommended)
- Free tier: Unlimited jobs
- Visit: [cron-job.org](https://cron-job.org)
- Create account → New Cron Job
- Configure:
  - **URL**: `https://your-render-url.onrender.com/api/pipeline/run`
  - **Schedule**: Daily at 8:00 AM
  - **Method**: POST

#### **EasyCron**
- Free tier: 1 job
- Visit: [easycron.com](https://easycron.com)
- Similar setup as above

#### **cron-job.io**
- Free tier: 3 jobs
- Visit: [cron-job.io](https://cron-job.io)

### Optional: Add security

Add a secret token to your Render API:

1. In Render → Your service → Environment
2. Add variable:
   - **Key**: `PIPELINE_SECRET`
   - **Value**: `your-random-secret-123`
3. In cron service, add header:
   - **Header**: `Authorization: Bearer your-random-secret-123`

---

## 🚀 **Option 3: Vercel Cron (If deploying API to Vercel)**

If you deploy the API to Vercel instead of Render:

Create `vercel.json`:

```json
{
  "crons": [{
    "path": "/api/pipeline/run",
    "schedule": "0 8 * * *"
  }]
}
```

**Note**: Vercel cron is only available on **Pro plan** ($20/month)

---

## 🔧 **Option 4: Railway.app**

Railway offers free cron jobs:

1. Sign up at [railway.app](https://railway.app)
2. Import your GitHub repo
3. Add cron service (similar to Render blueprint)
4. Free tier: $5 credit/month (enough for daily crons)

---

## 📊 **Comparison**

| Option | Cost | Reliability | Setup Difficulty | Recommended |
|--------|------|-------------|------------------|-------------|
| **GitHub Actions** | FREE ♾️ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ Easy | ✅ **YES** |
| **Webhook Cron** | FREE | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ Easy | ✅ Alternative |
| **Railway** | FREE ($5 credit) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ Medium | If you prefer |
| **Vercel Cron** | $20/month | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ Easy | ❌ Not free |

---

## 🎯 **Recommended Setup (100% FREE)**

### **Best Free Stack:**

1. **Backend API**: Render Free Web Service
2. **Daily Pipeline**: GitHub Actions (already configured!)
3. **Frontend**: Vercel Free

### **Alternative Free Stack:**

1. **Backend API**: Render Free Web Service
2. **Daily Pipeline**: cron-job.org → Webhook
3. **Frontend**: Vercel Free

---

## ⚡ **Quick Start with GitHub Actions**

Since the workflow is already created, just push it:

```bash
# 1. Add the workflow file
git add .github/workflows/daily-pipeline.yml

# 2. Add the new pipeline endpoint
git add backend/api/routers/pipeline.py
git add backend/api/main.py

# 3. Commit
git commit -m "Add GitHub Actions workflow for daily pipeline and webhook endpoint"

# 4. Push
git push
```

**That's it!** The pipeline will now run automatically every day at 8:00 AM UTC.

---

## 🧪 **Testing**

### Test GitHub Actions:
1. Go to GitHub → Your repo → **Actions** tab
2. Click "Daily Gold Price Prediction Pipeline"
3. Click **"Run workflow"** → **"Run workflow"**
4. Watch it execute in real-time
5. Check your repo - predictions should be updated

### Test Webhook (if using Option 2):
```bash
curl -X POST https://your-render-url.onrender.com/api/pipeline/run
```

Or visit: `https://your-render-url.onrender.com/docs` and test from there

---

## 📝 **What Happens**

### GitHub Actions flow:
1. Runs daily at 8:00 AM UTC
2. Checks out your code
3. Installs Python dependencies
4. Runs the pipeline
5. Commits updated predictions
6. Pushes to GitHub
7. Render detects update → Auto-deploys API
8. Frontend shows new predictions

### Webhook flow:
1. External cron service sends POST request
2. Your API receives request
3. Triggers pipeline execution
4. Predictions update in memory
5. API serves new data

---

## 🎉 **Recommendation**

**Use GitHub Actions (Option 1)** because:
- ✅ Zero configuration needed (file already created)
- ✅ Completely free forever
- ✅ More reliable than external webhooks
- ✅ Auto-commits predictions to repo
- ✅ Triggers automatic Render redeployment
- ✅ Full logs and history
- ✅ Can manually trigger anytime

Just push the workflow file and you're done!

---

## ❓ **FAQ**

**Q: Will GitHub Actions wake up my sleeping Render API?**
A: No need! The pipeline runs on GitHub and commits to repo. Render auto-deploys, keeping API updated.

**Q: What timezone is 8:00 AM?**
A: UTC. Adjust the cron schedule if needed: `0 8 * * *` = 8 AM UTC

**Q: Can I run it more than once a day?**
A: Yes! Just add more cron schedules. GitHub Actions free tier is generous.

**Q: What if I want it at a different time?**
A: Edit `.github/workflows/daily-pipeline.yml` and change the cron expression.

Examples:
- `0 12 * * *` = Noon UTC
- `0 0 * * *` = Midnight UTC
- `0 */6 * * *` = Every 6 hours

---

**Ready to go? Just push the GitHub Actions workflow and you're all set!** 🚀
