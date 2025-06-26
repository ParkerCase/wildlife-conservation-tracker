# WildGuard AI Dashboard - Login Credentials

## 🔐 Access Credentials

The enhanced WildGuard AI dashboard now requires authentication to access the real-time wildlife trafficking intelligence platform.

### Valid Login Credentials:

**Primary Admin Account:**
- Username: `admin`
- Password: `wildguard2025`

**Alternative Accounts:**
- Username: `wildguard` | Password: `conservation2025`
- Username: `parker` | Password: `wildlife123`
- Username: `demo` | Password: `demo123`
- Username: `conservation` | Password: `tracker123`
- Username: `wildlife` | Password: `guard2025`

## 🚀 Accessing the Dashboard

1. **Start the Frontend Application:**
   ```bash
   cd frontend
   npm start
   ```

2. **Navigate to:** `http://localhost:3000`

3. **Login:** Use any of the credentials above

4. **Dashboard Features:**
   - **Real-time data** from Supabase database
   - **7-platform monitoring** (eBay, Craigslist, OLX, Marktplaats, MercadoLibre, Gumtree, Avito)
   - **Multilingual intelligence** (16 languages, 1,452 keywords)
   - **Government-grade analytics** and reporting
   - **Mobile-responsive** design
   - **Auto-refresh** every 30 seconds

## 📊 Platform Coverage

### Active Platforms (7 Total):
- **eBay (Global)** - Primary marketplace monitoring
- **Craigslist (North America)** - Regional coverage
- **OLX (Europe/Asia)** - International markets
- **Marktplaats (Netherlands)** - Dutch marketplace
- **MercadoLibre (Latin America)** - Spanish/Portuguese markets
- **Gumtree (UK/Australia)** - English-speaking regions
- **Avito (Russia/CIS)** - Russian/Eastern European markets

## 🌍 Real-time Data Integration

The dashboard now displays **live data** from your Supabase database including:

- **Total Detections:** Real count from `detections` table
- **Today's Activity:** Current day detection count
- **High-Priority Alerts:** CRITICAL and HIGH threat level cases
- **Platform Breakdown:** Actual detection counts per platform
- **Recent Alerts:** Latest trafficking attempts with real URLs
- **Multilingual Analytics:** Language distribution analysis

## 🔄 Auto-Refresh System

- **Dashboard data** refreshes every 30 seconds
- **Manual refresh** button available in header
- **Real-time status indicators** show system health
- **Error handling** with graceful fallbacks

## 🎯 Demo for Conservation Organizations

Perfect for demonstrating to:
- **Wildlife conservation organizations**
- **Government agencies**
- **Law enforcement partners**
- **Funding organizations**
- **Technology investors**

## 🔧 Technical Details

- **Frontend:** React 18 with real-time hooks
- **Backend:** Supabase PostgreSQL database
- **Authentication:** Local storage with 24-hour sessions
- **Data Source:** Live production database (no mock data)
- **Refresh Rate:** 30-second intervals for real-time updates
- **Error Handling:** Comprehensive error states and fallbacks

---

**🚨 Security Note:** Change these credentials before production deployment. Current credentials are for development and demonstration purposes only.

**📧 Contact:** For credential updates or access issues, contact the development team.
