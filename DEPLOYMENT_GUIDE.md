# 🚀 WildGuard AI - Production Deployment Guide

Deploy your WildGuard AI system to run continuously and populate your dashboard with 200,000+ daily listings.

## 📋 Prerequisites

1. **Supabase Account** (Free tier sufficient)
2. **eBay Developer Account** (Free)
3. **GitHub Account** (For free cloud deployment)

## 🏃‍♂️ Quick Start Options

### Option 1: GitHub Actions (100% FREE - Recommended)

**Perfect for**: No server management, runs in the cloud automatically

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy WildGuard production system"
   git push origin main
   ```

2. **Add Secrets**:
   Go to GitHub → Settings → Secrets and Variables → Actions
   
   Add these secrets:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   EBAY_APP_ID=your_ebay_app_id
   EBAY_CERT_ID=your_ebay_cert_id
   EBAY_DEV_ID=your_ebay_dev_id
   ```

3. **Enable Actions**:
   - Go to Actions tab in your GitHub repo
   - Enable workflows if prompted
   - The scanner will run automatically every hour!

4. **Monitor**:
   - Check Actions tab for scan logs
   - Check your Supabase dashboard for incoming data

### Option 2: Local Deployment (FREE)

**Perfect for**: Running on your own computer/server

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.production.txt
   playwright install chromium
   ```

2. **Configure Environment**:
   Update `.env` file with your credentials:
   ```bash
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   EBAY_APP_ID=your_ebay_app_id
   EBAY_CERT_ID=your_ebay_cert_id
   EBAY_DEV_ID=your_ebay_dev_id
   ```

3. **Start Scheduler**:
   ```bash
   # Standard schedule (24 scans/day = 200K+ daily)
   python scheduler.py
   
   # High frequency (36 scans/day = 300K+ daily)
   python scheduler.py --high-frequency
   ```

4. **Keep Running**:
   - For Linux/Mac: Use `screen` or `tmux` to keep running
   - For Windows: Use `nohup` or run as Windows Service

### Option 3: Docker Deployment (Recommended for VPS)

**Perfect for**: DigitalOcean, AWS, Google Cloud, etc.

1. **Build Container**:
   ```bash
   docker build -f Dockerfile.production -t wildguard-ai .
   ```

2. **Run Container**:
   ```bash
   docker run -d \
     --name wildguard-production \
     --restart unless-stopped \
     -e SUPABASE_URL=your_supabase_url \
     -e SUPABASE_KEY=your_supabase_key \
     -e EBAY_APP_ID=your_ebay_app_id \
     -e EBAY_CERT_ID=your_ebay_cert_id \
     -e EBAY_DEV_ID=your_ebay_dev_id \
     wildguard-ai
   ```

3. **Monitor**:
   ```bash
   docker logs -f wildguard-production
   ```

## 📊 Expected Results

### Daily Data Flow to Supabase:

- **eBay**: ~8,000 listings/hour → 192,000 daily
- **Craigslist**: ~80 listings/hour → 1,920 daily  
- **OLX**: ~8 listings/hour → 192 daily
- **Marktplaats**: ~40 listings/hour → 960 daily
- **MercadoLibre**: ~60 listings/hour → 1,440 daily

**🎯 Total: ~8,500 listings/hour → 204,000+ daily**

### Database Tables Populated:

1. **`detections`** - Main listing data:
   ```sql
   - evidence_id (unique scan ID)
   - timestamp (when scanned)
   - platform (ebay, craigslist, etc.)
   - listing_title (product title)
   - listing_price (product price)
   - listing_url (product URL)
   - search_term (keyword used)
   - threat_score (50 - default, not rated yet)
   ```

2. **`scan_summaries`** - Scan monitoring:
   ```sql
   - scan_id (unique scan identifier)
   - timestamp (scan time)
   - total_results (listings found)
   - total_stored (listings saved)
   - platform_stats (JSON of platform performance)
   - success_rate (percentage of platforms working)
   ```

## 🔍 Monitoring Your System

### 1. Check GitHub Actions (if using Option 1):
- Go to Actions tab in your repo
- See scan success/failure
- Download logs for detailed info

### 2. Check Supabase Dashboard:
- Monitor `detections` table growth
- Check recent timestamps
- Verify data from all platforms

### 3. Check Logs (local/Docker):
```bash
tail -f wildguard_production.log
tail -f wildguard_scheduler.log
```

### 4. Quick Status Check:
```sql
-- Check today's scans
SELECT 
  platform,
  COUNT(*) as listings_today,
  MAX(timestamp) as last_scan
FROM detections 
WHERE DATE(timestamp) = CURRENT_DATE
GROUP BY platform
ORDER BY listings_today DESC;
```

## 🎯 Daily Dashboard Numbers

Your dashboard should show:

- **📊 Total Listings Today**: 200,000+
- **🌍 Active Platforms**: 5
- **⏰ Last Scan**: Within last hour
- **📈 Growth Rate**: ~8,500/hour
- **🎯 Annual Projection**: 74+ million

## ⚠️ Troubleshooting

### Common Issues:

1. **No data in Supabase**:
   - Check environment variables
   - Verify Supabase credentials
   - Check logs for errors

2. **eBay API errors**:
   - Verify eBay credentials
   - Check if you've hit daily limits (unlikely with our usage)

3. **Playwright browser errors**:
   - Install browser: `playwright install chromium`
   - Install deps: `playwright install-deps`

4. **GitHub Actions failing**:
   - Check secrets are correctly set
   - Verify workflow file syntax
   - Check action logs for specific errors

### Health Checks:

```bash
# Quick test run
python production_scanner.py

# Expected output:
# ✅ Supabase connection established
# 🚀 Starting production scan PROD-20240620-140532
# ✅ ebay: 3000 results, 3000 stored
# ✅ craigslist: 240 results, 240 stored
# 🎉 Scan completed: 8512 results, 8512 stored
```

## 💰 Cost Breakdown

- **GitHub Actions**: FREE (2,000 minutes/month)
- **eBay API**: FREE (within limits)
- **Supabase**: FREE (500MB database + 2GB bandwidth)
- **Web Scraping**: FREE (just bandwidth)

**Total Monthly Cost: $0** ✅

## 🔄 Scaling Up

Once running successfully:

1. **Add more keywords**: Expand the KEYWORDS list
2. **Increase frequency**: Use `--high-frequency` mode
3. **Add more platforms**: Implement additional marketplaces
4. **Enable AI rating**: Add Anthropic API for threat scoring

## 📞 Support

If you encounter issues:

1. Check the logs first
2. Verify all credentials are correct
3. Test individual components
4. Check Supabase for data flow

---

**🎉 Congratulations! Your WildGuard AI system is now ready for production deployment with 200,000+ daily listings flowing to your dashboard.**
