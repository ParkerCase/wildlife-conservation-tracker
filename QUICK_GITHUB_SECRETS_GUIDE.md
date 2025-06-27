# 🚨 QUICK FIX: Add GitHub Secrets

## The Problem

Your GitHub Actions workflow is failing because it can't find the required environment variables. The workflow is looking for these in GitHub Secrets, but they're not set.

## The Solution

Add these 5 secrets to your GitHub repository:

### Step 1: Go to GitHub Secrets

1. Go to your repository: `https://github.com/[your-username]/wildlife-conservation-tracker`
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### Step 2: Add Each Secret

#### Secret 1: SUPABASE_URL

- **Name**: `SUPABASE_URL`
- **Value**: `https://hgnefrvllutcagdutcaa.supabase.co`

#### Secret 2: SUPABASE_ANON_KEY

- **Name**: `SUPABASE_ANON_KEY`
- **Value**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhnbmVmcnZsbHV0Y2FnZHV0Y2FhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDkzMjU4NzcsImV4cCI6MjA2NDkwMTg3N30.ftaP4Xa1vTXumTlcPy0OwdG1s-4JSYz10-ENiWB_QZ0`

#### Secret 3: GOOGLE_VISION_API_KEY

- **Name**: `GOOGLE_VISION_API_KEY`
- **Value**: `AIzaSyDpfXySa9vplsSY3CUm9BSAUtazDZDJpoY`

#### Secret 4: EBAY_APP_ID

- **Name**: `EBAY_APP_ID`
- **Value**: `ParkerCa-Wildlife-PRD-7f002a9fc-43ad918c`

#### Secret 5: EBAY_CERT_ID

- **Name**: `EBAY_CERT_ID`
- **Value**: `PRD-f002a9fc485b-06cf-4a0e-bdf4-b37b`

### Step 3: Test the Workflow

1. Go to **Actions** tab
2. Find the "Human Trafficking Scanner" workflow
3. Click **Run workflow**
4. Click the green **Run workflow** button
5. Watch the logs to see if it works

## Expected Results

After adding these secrets, you should see:

- ✅ Environment variables loaded successfully
- ✅ Scan runs without errors
- ✅ Results file created
- ✅ Artifacts uploaded successfully

## If It Still Fails

Check the workflow logs for specific error messages. The most common issues are:

1. **ModuleNotFoundError**: Missing Python dependencies
2. **ConnectionError**: Network issues
3. **AuthenticationError**: Invalid credentials

Let me know what specific error you see and I can help further!
