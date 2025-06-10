import React, { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import {
  AlertTriangle,
  Shield,
  Eye,
  Globe,
  TrendingUp,
  Users,
  MapPin,
  Clock,
  Download,
  Filter,
  Search,
  Bell,
  Settings,
  Play,
} from "lucide-react";

// API Service for real backend integration
class WildGuardAPI {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || "http://localhost:5000/api";
  }

  async get(endpoint) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`);
      if (!response.ok) throw new Error(`API Error: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error(`API Error fetching ${endpoint}:`, error);
      throw error;
    }
  }

  async post(endpoint, data) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error(`API Error: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error(`API Error posting to ${endpoint}:`, error);
      throw error;
    }
  }

  // Real API methods
  async getRealTimeStats() {
    return this.get("/stats/realtime");
  }

  async getThreatTrends(days = 7) {
    return this.get(`/stats/trends?days=${days}`);
  }

  async getThreats(filters = {}) {
    const params = new URLSearchParams(filters).toString();
    return this.get(`/threats?${params}`);
  }

  async getPlatformStatus() {
    return this.get("/platforms/status");
  }

  async triggerManualScan(platforms, keywords) {
    return this.post("/scan/manual", { platforms, keywords });
  }
}

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState("overview");
  const [timeRange, setTimeRange] = useState("24h");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Real data states
  const [realTimeStats, setRealTimeStats] = useState(null);
  const [threatTrends, setThreatTrends] = useState([]);
  const [platformStatus, setPlatformStatus] = useState([]);
  const [isScanning, setIsScanning] = useState(false);

  const api = new WildGuardAPI();

  // Load real data on component mount
  useEffect(() => {
    loadDashboardData();

    // Set up real-time updates every 30 seconds
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, [timeRange]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load all data in parallel
      const [statsData, trendsData, platformData] = await Promise.all([
        api.getRealTimeStats(),
        api.getThreatTrends(getDaysFromTimeRange(timeRange)),
        api.getPlatformStatus(),
      ]);

      setRealTimeStats(statsData);
      setThreatTrends(trendsData.daily_trends || []);
      setPlatformStatus(platformData.platforms || []);
    } catch (err) {
      setError(err.message);
      console.error("Dashboard data loading error:", err);
    } finally {
      setLoading(false);
    }
  };

  const getDaysFromTimeRange = (range) => {
    switch (range) {
      case "1h":
        return 1;
      case "24h":
        return 1;
      case "7d":
        return 7;
      case "30d":
        return 30;
      default:
        return 7;
    }
  };

  const triggerScan = async () => {
    try {
      setIsScanning(true);
      const result = await api.triggerManualScan(
        ["ebay", "craigslist", "poshmark", "ruby_lane"],
        ["ivory", "rhino horn", "tiger bone", "pangolin scales"]
      );

      alert(`Scan started successfully! Scan ID: ${result.scan_id}`);

      // Refresh data after scan
      setTimeout(() => {
        loadDashboardData();
      }, 5000);
    } catch (err) {
      alert(`Scan failed: ${err.message}`);
    } finally {
      setIsScanning(false);
    }
  };

  const StatCard = ({ title, value, change, icon: Icon, color }) => (
    <div
      className="bg-white rounded-xl shadow-lg p-6 border-l-4"
      style={{ borderLeftColor: color }}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">
            {value?.toLocaleString() || "..."}
          </p>
          {change !== undefined && (
            <p
              className={`text-sm ${
                change > 0 ? "text-green-600" : "text-red-600"
              }`}
            >
              {change > 0 ? "+" : ""}
              {change}% from yesterday
            </p>
          )}
        </div>
        <div
          className="p-3 rounded-full"
          style={{ backgroundColor: `${color}20` }}
        >
          <Icon size={24} style={{ color }} />
        </div>
      </div>
    </div>
  );

  const PlatformStatusCard = () => (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">
          Platform Status (Your 4 Working Platforms)
        </h3>
        <button
          onClick={triggerScan}
          disabled={isScanning}
          className={`flex items-center px-4 py-2 rounded-lg ${
            isScanning
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          } text-white`}
        >
          <Play size={16} className="mr-2" />
          {isScanning ? "Scanning..." : "Manual Scan"}
        </button>
      </div>

      <div className="space-y-3">
        {platformStatus.map((platform, index) => (
          <div
            key={index}
            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div className="flex items-center">
              <div
                className={`w-3 h-3 rounded-full mr-3 ${
                  platform.status === "active" ? "bg-green-500" : "bg-red-500"
                }`}
              ></div>
              <span className="font-medium">{platform.name}</span>
            </div>
            <div className="text-right">
              <p className="text-sm font-medium">
                {platform.success_rate}% success
              </p>
              <p className="text-xs text-gray-600">
                {new Date(platform.last_scan).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const ErrorDisplay = () => (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <div className="flex items-center">
        <AlertTriangle className="text-red-500 mr-3" size={20} />
        <div>
          <h3 className="text-red-800 font-medium">Connection Error</h3>
          <p className="text-red-700 text-sm mt-1">
            Unable to connect to backend API. Make sure your Flask server is
            running on port 5000.
          </p>
          <button
            onClick={loadDashboardData}
            className="mt-2 text-red-800 hover:text-red-900 text-sm underline"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
  );

  const LoadingDisplay = () => (
    <div className="flex items-center justify-center h-64">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p className="text-gray-600">Loading real-time data...</p>
      </div>
    </div>
  );

  const renderOverview = () => {
    if (loading) return <LoadingDisplay />;
    if (error) return <ErrorDisplay />;
    if (!realTimeStats) return <div>No data available</div>;

    return (
      <div className="space-y-6">
        {/* Real-time Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <StatCard
            title="Active Scans"
            value={realTimeStats.active_scans}
            icon={Eye}
            color="#3b82f6"
          />
          <StatCard
            title="Threats Detected Today"
            value={realTimeStats.threats_detected_today}
            icon={AlertTriangle}
            color="#ef4444"
          />
          <StatCard
            title="Alerts Sent"
            value={realTimeStats.alerts_sent_today}
            icon={Bell}
            color="#f59e0b"
          />
          <StatCard
            title="Platforms Monitored"
            value={realTimeStats.platforms_monitored}
            icon={Globe}
            color="#10b981"
          />
          <StatCard
            title="Species Protected"
            value={realTimeStats.total_species_protected}
            icon={Shield}
            color="#8b5cf6"
          />
          <StatCard
            title="Authorities Connected"
            value={realTimeStats.authorities_connected}
            icon={Users}
            color="#06b6d4"
          />
        </div>

        {/* Charts and Platform Status */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4">
              Threat Detection Trends (Real Data)
            </h3>
            {threatTrends.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={threatTrends}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area
                    type="monotone"
                    dataKey="ivory"
                    stackId="1"
                    stroke="#ff6b6b"
                    fill="#ff6b6b"
                    fillOpacity={0.6}
                  />
                  <Area
                    type="monotone"
                    dataKey="rhino"
                    stackId="1"
                    stroke="#4ecdc4"
                    fill="#4ecdc4"
                    fillOpacity={0.6}
                  />
                  <Area
                    type="monotone"
                    dataKey="tiger"
                    stackId="1"
                    stroke="#45b7d1"
                    fill="#45b7d1"
                    fillOpacity={0.6}
                  />
                  <Area
                    type="monotone"
                    dataKey="other"
                    stackId="1"
                    stroke="#ffeaa7"
                    fill="#ffeaa7"
                    fillOpacity={0.6}
                  />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-64 flex items-center justify-center text-gray-500">
                No trend data available yet. Run some scans to see trends.
              </div>
            )}
          </div>

          <PlatformStatusCard />
        </div>

        {/* Live Data Indicator */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse mr-3"></div>
            <div>
              <p className="text-green-800 font-medium">
                Live Data Connection Active
              </p>
              <p className="text-green-700 text-sm">
                Connected to your real backend • Last updated:{" "}
                {new Date().toLocaleTimeString()}
              </p>
              <p className="text-green-600 text-xs mt-1">
                Monitoring:{" "}
                {realTimeStats.platform_names?.join(", ") ||
                  "eBay, Craigslist, Poshmark, Ruby Lane"}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Shield size={32} className="text-blue-600 mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  WildGuard AI
                </h1>
                <p className="text-sm text-gray-600">
                  Live Wildlife Conservation Intelligence • 4 Platforms Active
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
              >
                <option value="1h">Last Hour</option>
                <option value="24h">Last 24 Hours</option>
                <option value="7d">Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
              </select>

              <div className="flex items-center space-x-2">
                <div
                  className={`w-3 h-3 rounded-full ${
                    error ? "bg-red-500" : "bg-green-500 animate-pulse"
                  }`}
                ></div>
                <span className="text-sm text-gray-600">
                  {error ? "Connection Error" : "Live Monitoring"}
                </span>
              </div>

              <button
                onClick={loadDashboardData}
                className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200"
              >
                <Settings size={20} className="text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Simple single tab for now - you can expand this */}
        <div className="bg-white rounded-lg shadow-sm mb-8">
          <nav className="flex space-x-8 px-6">
            <button className="flex items-center py-4 px-2 border-b-2 border-blue-500 text-blue-600 font-medium text-sm">
              <TrendingUp size={16} className="mr-2" />
              Live Dashboard
            </button>
          </nav>
        </div>

        {/* Main Content */}
        {renderOverview()}
      </div>
    </div>
  );
};

export default Dashboard;
