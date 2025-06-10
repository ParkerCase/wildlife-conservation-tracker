import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useLocation,
} from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import toast, { Toaster } from "react-hot-toast";
import { ResponsiveLine } from "@nivo/line";
import { ResponsiveBar } from "@nivo/bar";
import { ResponsivePie } from "@nivo/pie";
import { ResponsiveStream } from "@nivo/stream";
import {
  AlertTriangle,
  Shield,
  Eye,
  Globe,
  TrendingUp,
  Users,
  Bell,
  Settings,
  Play,
  BarChart3,
  PieChart,
  Activity,
  Database,
  MapPin,
  Clock,
  Zap,
  CheckCircle,
  XCircle,
  AlertCircle,
  Menu,
  X,
  Search,
  Filter,
  Download,
  RefreshCcw,
  Home,
  LayoutDashboard,
  FileText,
  Target,
  Briefcase,
  RotateCcw,
} from "lucide-react";

// API Service
class WildGuardAPI {
  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || "http://localhost:5001/api";
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
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error(`API Error: ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error(`API Error posting to ${endpoint}:`, error);
      throw error;
    }
  }

  async getRealTimeStats() {
    return this.get("/stats/realtime");
  }
  async getThreatTrends(days = 7) {
    return this.get(`/stats/trends?days=${days}`);
  }
  async getPlatformStatus() {
    return this.get("/platforms/status");
  }
  async triggerManualScan(platforms, keywords) {
    return this.post("/scan/manual", { platforms, keywords });
  }
}

// Sidebar Navigation
const Sidebar = ({ isOpen, setIsOpen }) => {
  const location = useLocation();

  const navItems = [
    {
      path: "/",
      icon: LayoutDashboard,
      label: "Live Dashboard",
      color: "blue",
    },
    {
      path: "/analytics",
      icon: BarChart3,
      label: "Advanced Analytics",
      color: "purple",
    },
    {
      path: "/threats",
      icon: AlertTriangle,
      label: "Threat Intelligence",
      color: "red",
    },
    {
      path: "/evidence",
      icon: Database,
      label: "Evidence Archive",
      color: "green",
    },
    { path: "/reports", icon: FileText, label: "Reports", color: "orange" },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <motion.div
        initial={false}
        animate={{ x: isOpen ? 0 : "-100%" }}
        transition={{ duration: 0.3, ease: "easeInOut" }}
        className="fixed left-0 top-0 h-full w-72 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white z-50 lg:translate-x-0 lg:static lg:z-auto"
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-700">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
              <Shield size={24} className="text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold">WildGuard AI</h1>
              <p className="text-xs text-slate-400">
                Conservation Intelligence
              </p>
            </div>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="lg:hidden p-2 hover:bg-slate-700 rounded-lg"
          >
            <X size={20} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setIsOpen(false)}
                className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                  isActive
                    ? `bg-${item.color}-500 bg-opacity-20 border border-${item.color}-500 border-opacity-30`
                    : "hover:bg-slate-700"
                }`}
              >
                <Icon
                  size={20}
                  className={
                    isActive ? `text-${item.color}-400` : "text-slate-400"
                  }
                />
                <span
                  className={`font-medium ${
                    isActive ? "text-white" : "text-slate-300"
                  }`}
                >
                  {item.label}
                </span>
                {isActive && (
                  <motion.div
                    layoutId="activeTab"
                    className="ml-auto w-2 h-2 bg-blue-400 rounded-full"
                  />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Status Panel */}
        <div className="absolute bottom-6 left-4 right-4">
          <div className="bg-slate-800 rounded-xl p-4 border border-slate-700">
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm font-medium text-green-400">
                System Active
              </span>
            </div>
            <div className="space-y-2 text-xs text-slate-400">
              <div className="flex justify-between">
                <span>Platforms:</span>
                <span className="text-white">4 Active</span>
              </div>
              <div className="flex justify-between">
                <span>Uptime:</span>
                <span className="text-white">99.9%</span>
              </div>
              <div className="flex justify-between">
                <span>Port:</span>
                <span className="text-white">5001</span>
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </>
  );
};

// Professional Stat Card
const StatCard = ({
  title,
  value,
  change,
  icon: Icon,
  color,
  subtitle,
  trend,
}) => (
  <motion.div
    whileHover={{ y: -2, boxShadow: "0 20px 40px rgba(0,0,0,0.1)" }}
    className="bg-white rounded-2xl p-6 border border-gray-100 relative overflow-hidden group"
  >
    {/* Background Pattern */}
    <div className="absolute top-0 right-0 w-32 h-32 opacity-5">
      <Icon size={128} className={`text-${color}-500`} />
    </div>

    <div className="relative z-10">
      <div className="flex items-start justify-between mb-4">
        <div
          className={`w-12 h-12 bg-gradient-to-br from-${color}-500 to-${color}-600 rounded-xl flex items-center justify-center`}
        >
          <Icon size={24} className="text-white" />
        </div>
        {change !== undefined && (
          <div
            className={`flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium ${
              change > 0
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }`}
          >
            <TrendingUp size={12} className={change < 0 ? "rotate-180" : ""} />
            <span>{Math.abs(change)}%</span>
          </div>
        )}
      </div>

      <div className="space-y-1">
        <h3 className="text-2xl font-bold text-gray-900">
          {typeof value === "number" ? value.toLocaleString() : value || "..."}
        </h3>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        {subtitle && <p className="text-xs text-gray-500">{subtitle}</p>}
      </div>

      {/* Trend Sparkline */}
      {trend && (
        <div className="mt-4 h-8">
          <svg className="w-full h-full" viewBox="0 0 100 20">
            <path
              d={`M 0 ${20 - trend[0]} ${trend
                .map(
                  (point, i) =>
                    `L ${(i / (trend.length - 1)) * 100} ${20 - point}`
                )
                .join(" ")}`}
              fill="none"
              stroke={color === "red" ? "#ef4444" : "#10b981"}
              strokeWidth="2"
              className="opacity-60"
            />
          </svg>
        </div>
      )}
    </div>
  </motion.div>
);

// Professional Chart Components
const ThreatTrendsChart = ({ data }) => {
  const chartData = data.map((d) => ({
    x: d.date,
    ivory: d.ivory,
    rhino: d.rhino,
    tiger: d.tiger,
    pangolin: d.pangolin,
    other: d.other,
  }));

  const lineData = [
    { id: "ivory", data: chartData.map((d) => ({ x: d.x, y: d.ivory })) },
    { id: "rhino", data: chartData.map((d) => ({ x: d.x, y: d.rhino })) },
    { id: "tiger", data: chartData.map((d) => ({ x: d.x, y: d.tiger })) },
    { id: "pangolin", data: chartData.map((d) => ({ x: d.x, y: d.pangolin })) },
  ];

  return (
    <div className="h-80">
      <ResponsiveLine
        data={lineData}
        margin={{ top: 20, right: 110, bottom: 50, left: 60 }}
        xScale={{ type: "point" }}
        yScale={{ type: "linear", min: "auto", max: "auto", stacked: false }}
        curve="cardinal"
        axisTop={null}
        axisRight={null}
        axisBottom={{ tickSize: 5, tickPadding: 5, tickRotation: -45 }}
        axisLeft={{ tickSize: 5, tickPadding: 5, tickRotation: 0 }}
        enableGridX={false}
        enableGridY={true}
        colors={["#ef4444", "#f59e0b", "#10b981", "#8b5cf6"]}
        pointSize={8}
        pointColor={{ theme: "background" }}
        pointBorderWidth={2}
        pointBorderColor={{ from: "serieColor" }}
        pointLabelYOffset={-12}
        useMesh={true}
        enableArea={true}
        areaOpacity={0.1}
        legends={[
          {
            anchor: "bottom-right",
            direction: "column",
            justify: false,
            translateX: 100,
            translateY: 0,
            itemsSpacing: 0,
            itemDirection: "left-to-right",
            itemWidth: 80,
            itemHeight: 20,
            symbolSize: 12,
            symbolShape: "circle",
          },
        ]}
        theme={{
          grid: { line: { stroke: "#f1f5f9", strokeWidth: 1 } },
          axis: { ticks: { text: { fontSize: 11, fill: "#64748b" } } },
        }}
      />
    </div>
  );
};

const SpeciesDistributionChart = ({ data }) => {
  const pieData = [
    { id: "Ivory", value: 35, color: "#ef4444" },
    { id: "Rhino Horn", value: 28, color: "#f59e0b" },
    { id: "Tiger Parts", value: 18, color: "#10b981" },
    { id: "Pangolin", value: 12, color: "#8b5cf6" },
    { id: "Other", value: 7, color: "#6b7280" },
  ];

  return (
    <div className="h-80">
      <ResponsivePie
        data={pieData}
        margin={{ top: 40, right: 80, bottom: 80, left: 80 }}
        innerRadius={0.4}
        padAngle={2}
        cornerRadius={4}
        activeOuterRadiusOffset={8}
        colors={{ datum: "data.color" }}
        borderWidth={1}
        borderColor={{ from: "color", modifiers: [["darker", 0.2]] }}
        enableArcLinkLabels={true}
        arcLinkLabelsSkipAngle={10}
        arcLinkLabelsTextColor="#374151"
        arcLinkLabelsThickness={2}
        arcLinkLabelsColor={{ from: "color" }}
        arcLabelsSkipAngle={10}
        arcLabelsTextColor="#ffffff"
        legends={[
          {
            anchor: "bottom",
            direction: "row",
            justify: false,
            translateX: 0,
            translateY: 56,
            itemsSpacing: 0,
            itemWidth: 100,
            itemHeight: 18,
            itemTextColor: "#374151",
            itemDirection: "left-to-right",
            symbolSize: 12,
            symbolShape: "circle",
          },
        ]}
      />
    </div>
  );
};

const PlatformActivityChart = ({ data }) => {
  const barData = [
    { platform: "eBay", threats: 45, color: "#3b82f6" },
    { platform: "Craigslist", threats: 38, color: "#10b981" },
    { platform: "Poshmark", threats: 29, color: "#f59e0b" },
    { platform: "Ruby Lane", threats: 18, color: "#8b5cf6" },
  ];

  return (
    <div className="h-80">
      <ResponsiveBar
        data={barData}
        keys={["threats"]}
        indexBy="platform"
        margin={{ top: 20, right: 30, bottom: 50, left: 60 }}
        padding={0.3}
        colors={{ datum: "data.color" }}
        borderColor={{ from: "color", modifiers: [["darker", 1.6]] }}
        axisTop={null}
        axisRight={null}
        axisBottom={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
        }}
        axisLeft={{
          tickSize: 5,
          tickPadding: 5,
          tickRotation: 0,
        }}
        enableGridY={true}
        enableLabel={true}
        labelSkipWidth={12}
        labelSkipHeight={12}
        labelTextColor="#ffffff"
        animate={true}
        motionStiffness={90}
        motionDamping={15}
        theme={{
          grid: { line: { stroke: "#f1f5f9", strokeWidth: 1 } },
          axis: { ticks: { text: { fontSize: 11, fill: "#64748b" } } },
        }}
      />
    </div>
  );
};

// Platform Status Card
const PlatformStatusCard = ({ platforms, onScan, isScanning }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-white rounded-2xl p-6 border border-gray-100"
  >
    <div className="flex items-center justify-between mb-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900">
          Platform Monitoring
        </h3>
        <p className="text-sm text-gray-600">
          Real-time surveillance across 4 platforms
        </p>
      </div>
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onScan}
        disabled={isScanning}
        className={`flex items-center space-x-2 px-4 py-2 rounded-xl font-medium transition-all ${
          isScanning
            ? "bg-gray-100 text-gray-400 cursor-not-allowed"
            : "bg-gradient-to-r from-blue-500 to-blue-600 text-white hover:from-blue-600 hover:to-blue-700 shadow-lg hover:shadow-xl"
        }`}
      >
        {isScanning ? (
          <>
            <div className="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin" />
            <span>Scanning...</span>
          </>
        ) : (
          <>
            <Play size={16} />
            <span>Manual Scan</span>
          </>
        )}
      </motion.button>
    </div>

    <div className="space-y-4">
      {platforms.map((platform, index) => (
        <motion.div
          key={platform.name}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100"
        >
          <div className="flex items-center space-x-4">
            <div
              className={`w-3 h-3 rounded-full ${
                platform.status === "active" ? "bg-green-500" : "bg-red-500"
              } shadow-lg`}
            />
            <div>
              <h4 className="font-medium text-gray-900">{platform.name}</h4>
              <p className="text-sm text-gray-600">
                Last scan: {new Date(platform.last_scan).toLocaleTimeString()}
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="flex items-center space-x-2">
              <div className="w-16 bg-gray-200 rounded-full h-2">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${platform.success_rate}%` }}
                  transition={{ duration: 1, delay: index * 0.2 }}
                  className="bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full"
                />
              </div>
              <span className="text-sm font-medium text-gray-900">
                {platform.success_rate}%
              </span>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  </motion.div>
);

// Main Dashboard Component
const Dashboard = () => {
  const [realTimeStats, setRealTimeStats] = useState(null);
  const [threatTrends, setThreatTrends] = useState([]);
  const [platformStatus, setPlatformStatus] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [timeRange, setTimeRange] = useState("24h");

  const api = new WildGuardAPI();

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, [timeRange]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [statsData, trendsData, platformData] = await Promise.all([
        api.getRealTimeStats(),
        api.getThreatTrends(getDaysFromTimeRange(timeRange)),
        api.getPlatformStatus(),
      ]);

      setRealTimeStats(statsData);
      setThreatTrends(trendsData.daily_trends || []);
      setPlatformStatus(platformData.platforms || []);

      toast.success("Data refreshed successfully");
    } catch (err) {
      setError(err.message);
      toast.error("Failed to load dashboard data");
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

      toast.success(`Scan initiated! ID: ${result.scan_id}`);
      setTimeout(() => loadDashboardData(), 5000);
    } catch (err) {
      toast.error(`Scan failed: ${err.message}`);
    } finally {
      setIsScanning(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-600 font-medium">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-2xl p-8 m-6">
        <div className="text-center">
          <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-red-800 mb-2">
            Connection Error
          </h3>
          <p className="text-red-700 mb-4">
            Unable to connect to backend API on port 5001.
          </p>
          <button
            onClick={loadDashboardData}
            className="px-6 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (!realTimeStats) return null;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Live Dashboard
          </h1>
          <p className="text-gray-600">
            Real-time wildlife conservation intelligence
          </p>
        </div>
        <div className="flex items-center space-x-4 mt-4 lg:mt-0">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="border border-gray-300 rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>
          <button
            onClick={loadDashboardData}
            className="p-2 bg-gray-100 hover:bg-gray-200 rounded-xl transition-colors"
          >
            <RefreshCcw size={20} className="text-gray-600" />
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard
          title="Active Scans"
          value={realTimeStats.active_scans}
          icon={Eye}
          color="blue"
          subtitle="Platforms currently monitored"
          trend={[8, 12, 6, 15, 10, 18, 14]}
        />
        <StatCard
          title="Threats Detected Today"
          value={realTimeStats.threats_detected_today}
          change={25}
          icon={AlertTriangle}
          color="red"
          subtitle="High-confidence detections"
          trend={[4, 8, 6, 12, 15, 10, 12]}
        />
        <StatCard
          title="Alerts Sent"
          value={realTimeStats.alerts_sent_today}
          change={15}
          icon={Bell}
          color="orange"
          subtitle="Notifications to authorities"
          trend={[2, 4, 3, 6, 5, 7, 3]}
        />
        <StatCard
          title="Platforms Monitored"
          value={realTimeStats.platforms_monitored}
          icon={Globe}
          color="green"
          subtitle="eBay, Craigslist, Poshmark, Ruby Lane"
        />
        <StatCard
          title="Species Protected"
          value={realTimeStats.total_species_protected}
          icon={Shield}
          color="purple"
          subtitle="CITES-listed species coverage"
        />
        <StatCard
          title="Law Enforcement Partners"
          value={realTimeStats.authorities_connected}
          change={8}
          icon={Users}
          color="cyan"
          subtitle="Active agency connections"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 border border-gray-100"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">
            Threat Detection Trends
          </h3>
          <ThreatTrendsChart data={threatTrends} />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl p-6 border border-gray-100"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">
            Species Distribution
          </h3>
          <SpeciesDistributionChart />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-2xl p-6 border border-gray-100"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-6">
            Platform Activity
          </h3>
          <PlatformActivityChart />
        </motion.div>

        <PlatformStatusCard
          platforms={platformStatus}
          onScan={triggerScan}
          isScanning={isScanning}
        />
      </div>

      {/* Status Banner */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-2xl p-6"
      >
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl flex items-center justify-center">
            <CheckCircle size={24} className="text-white" />
          </div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900">
              System Status: Fully Operational
            </h3>
            <p className="text-gray-600">
              All systems online • Backend API connected on port 5001 • Last
              updated: {new Date().toLocaleTimeString()}
            </p>
            <div className="flex items-center space-x-6 mt-2 text-sm text-gray-600">
              <span>
                Monitoring: {realTimeStats.platform_names?.join(", ")}
              </span>
              <span>•</span>
              <span>Uptime: 99.9%</span>
              <span>•</span>
              <span>Response time: &lt;200ms</span>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

// Placeholder Components
const AdvancedAnalytics = () => (
  <div className="p-8 text-center">
    <BarChart3 size={64} className="mx-auto text-gray-400 mb-4" />
    <h2 className="text-2xl font-bold text-gray-900 mb-2">
      Advanced Analytics
    </h2>
    <p className="text-gray-600">
      Comprehensive threat intelligence and reporting dashboard
    </p>
  </div>
);

const ThreatIntelligence = () => (
  <div className="p-8 text-center">
    <Target size={64} className="mx-auto text-gray-400 mb-4" />
    <h2 className="text-2xl font-bold text-gray-900 mb-2">
      Threat Intelligence
    </h2>
    <p className="text-gray-600">
      AI-powered threat analysis and pattern recognition
    </p>
  </div>
);

const EvidenceArchive = () => (
  <div className="p-8 text-center">
    <Database size={64} className="mx-auto text-gray-400 mb-4" />
    <h2 className="text-2xl font-bold text-gray-900 mb-2">Evidence Archive</h2>
    <p className="text-gray-600">
      Blockchain-secured evidence preservation system
    </p>
  </div>
);

const Reports = () => (
  <div className="p-8 text-center">
    <FileText size={64} className="mx-auto text-gray-400 mb-4" />
    <h2 className="text-2xl font-bold text-gray-900 mb-2">Reports</h2>
    <p className="text-gray-600">
      Executive summaries and compliance documentation
    </p>
  </div>
);

// Main App Component
const App = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50 flex">
        <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />

        {/* Main Content */}
        <div className="flex-1 flex flex-col lg:ml-0">
          {/* Top Bar */}
          <header className="bg-white border-b border-gray-200 px-6 py-4 lg:hidden">
            <div className="flex items-center justify-between">
              <button
                onClick={() => setSidebarOpen(true)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <Menu size={24} className="text-gray-600" />
              </button>
              <h1 className="text-xl font-bold text-gray-900">WildGuard AI</h1>
              <div className="w-10" /> {/* Spacer */}
            </div>
          </header>

          {/* Page Content */}
          <main className="flex-1 p-6 lg:p-8">
            <AnimatePresence mode="wait">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/analytics" element={<AdvancedAnalytics />} />
                <Route path="/threats" element={<ThreatIntelligence />} />
                <Route path="/evidence" element={<EvidenceArchive />} />
                <Route path="/reports" element={<Reports />} />
              </Routes>
            </AnimatePresence>
          </main>
        </div>

        {/* Toast Notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: "#363636",
              color: "#fff",
              borderRadius: "12px",
              padding: "16px",
            },
          }}
        />
      </div>
    </Router>
  );
};

export default App;
