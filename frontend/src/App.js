import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  useLocation,
} from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
// Removed Recharts dependency - using custom charts instead
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
  PieChart as PieChartIcon,
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
  ChevronRight,
  ArrowUpRight,
  ArrowDownRight,
  Wifi,
  Panda,
  Server,
  Lock,
  ShieldCheck,
  Leaf,
  Turtle,
} from "lucide-react";

// Enhanced API Service
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

// Enhanced Professional Sidebar
const ProfessionalSidebar = ({ isOpen, setIsOpen }) => {
  const location = useLocation();
  const [isLargeScreen, setIsLargeScreen] = useState(window.innerWidth >= 1024);

  useEffect(() => {
    const handleResize = () => {
      setIsLargeScreen(window.innerWidth >= 1024);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  const navItems = [
    {
      path: "/",
      icon: Activity, // Changed from LayoutDashboard
      label: "Live Operations",
      gradient: "from-blue-500 to-blue-600",
      bgColor: "bg-blue-500/10",
      borderColor: "border-blue-500/20",
    },
    ,
    {
      path: "/analytics",
      icon: BarChart3,
      label: "Intelligence Analytics",
      gradient: "from-purple-500 to-purple-600",
      bgColor: "bg-purple-500/10",
      borderColor: "border-purple-500/20",
    },
    {
      path: "/threats",
      icon: AlertTriangle,
      label: "Threat Detection",
      gradient: "from-red-500 to-red-600",
      bgColor: "bg-red-500/10",
      borderColor: "border-red-500/20",
    },
    {
      path: "/evidence",
      icon: Database,
      label: "Evidence Vault",
      gradient: "from-emerald-500 to-emerald-600",
      bgColor: "bg-emerald-500/10",
      borderColor: "border-emerald-500/20",
    },
    {
      path: "/reports",
      icon: FileText,
      label: "Executive Reports",
      gradient: "from-orange-500 to-orange-600",
      bgColor: "bg-orange-500/10",
      borderColor: "border-orange-500/20",
    },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}

      <motion.div
        initial={false}
        animate={{
          x: isLargeScreen ? 0 : isOpen ? 0 : "-100%",
        }}
        transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
        className="fixed left-0 top-0 h-100 w-64 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white z-50 lg:translate-x-0 lg:static lg:z-auto border-r border-slate-700/50"
        style={{
          background:
            "linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95))",
        }}
      >
        {/* Enhanced Header */}
        <div className="relative p-6 border-b border-slate-700/50">
          {/* Background Pattern */}
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5"></div>

          <div className="relative flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-500/25">
                  <Leaf size={24} className="text-white" />
                </div>
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border border-slate-900 animate-pulse"></div>
              </div>
              <div>
                <h1 className="text-lg font-bold bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
                  The Conservatron 12000
                </h1>
                <p className="text-xs text-slate-400 font-medium">
                  Conservation Intelligence Platform
                </p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="lg:hidden p-2 hover:bg-slate-700/50 rounded-xl transition-colors"
            >
              <X size={18} />
            </button>
          </div>

          {/* System Status */}
          <div className="mt-4 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="relative">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <div className="absolute inset-0 w-2 h-2 bg-green-400 rounded-full animate-ping opacity-30"></div>
              </div>
              <span className="text-sm font-semibold text-green-400">
                System Active
              </span>
            </div>
            <Wifi size={16} className="text-green-400" />
          </div>
        </div>

        {/* Enhanced Navigation */}
        <nav className="p-6 space-y-3">
          {navItems.map((item, index) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <motion.div
                key={item.path}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Link
                  to={item.path}
                  onClick={() => setIsOpen(false)}
                  className={`group relative flex items-center space-x-4 px-6 py-4 rounded-2xl transition-all duration-300 ${
                    isActive
                      ? `${item.bgColor} border ${item.borderColor} shadow-lg shadow-blue-500/10`
                      : "hover:bg-slate-700/30 hover:border-slate-600/30 border border-transparent"
                  }`}
                >
                  {/* Active indicator */}
                  {isActive && (
                    <motion.div
                      layoutId="activeTab"
                      className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-blue-400 to-blue-600 rounded-full"
                    />
                  )}

                  <div
                    className={`p-2 rounded-xl transition-all duration-300 ${
                      isActive
                        ? `bg-gradient-to-br ${item.gradient} shadow-lg`
                        : "bg-slate-700/50 group-hover:bg-slate-600/50"
                    }`}
                  >
                    <Icon
                      size={20}
                      className={
                        isActive
                          ? "text-white"
                          : "text-slate-400 group-hover:text-slate-300"
                      }
                    />
                  </div>

                  <div className="flex-1">
                    <span
                      className={`font-semibold transition-colors ${
                        isActive
                          ? "text-white"
                          : "text-slate-300 group-hover:text-white"
                      }`}
                    >
                      {item.label}
                    </span>
                  </div>

                  <ChevronRight
                    size={16}
                    className={`transition-all duration-300 ${
                      isActive
                        ? "text-white rotate-90"
                        : "text-slate-500 group-hover:text-slate-400 group-hover:translate-x-1"
                    }`}
                  />
                </Link>
              </motion.div>
            );
          })}
        </nav>
      </motion.div>
    </>
  );
};

// Enhanced Professional Stat Card
const ProfessionalStatCard = ({
  title,
  value,
  change,
  icon: Icon,
  gradient,
  trend,
  subtitle,
}) => {
  const isPositive = change > 0;

  return (
    <motion.div
      whileHover={{
        y: -4,
        boxShadow: "0 20px 40px rgba(0,0,0,0.1)",
      }}
      transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
      className="group relative bg-white rounded-2xl p-6 border border-gray-100/50 overflow-hidden"
      style={{
        background:
          "linear-gradient(145deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9))",
      }}
    >
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-50/50 to-white/30"></div>
      <div className="absolute top-0 right-0 w-32 h-32 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity duration-500">
        <Icon size={128} />
      </div>

      {/* Floating Icon */}
      <div className="relative z-10">
        <div className="flex items-start justify-between mb-6">
          <motion.div
            whileHover={{ scale: 1.1, rotate: 5 }}
            className={`relative p-4 rounded-2xl bg-gradient-to-br ${gradient} shadow-lg group-hover:shadow-xl transition-all duration-300`}
          >
            <Icon size={28} className="text-white" />
            <div className="absolute inset-0 bg-white/20 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </motion.div>

          {change !== undefined && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2 }}
              className={`flex items-center space-x-2 px-4 py-2 rounded-full text-sm font-bold ${
                isPositive
                  ? "bg-emerald-500/10 text-emerald-700 border border-emerald-200/50"
                  : "bg-red-500/10 text-red-700 border border-red-200/50"
              }`}
            >
              {isPositive ? (
                <ArrowUpRight size={16} className="text-emerald-600" />
              ) : (
                <ArrowDownRight size={16} className="text-red-600" />
              )}
              <span>{Math.abs(change)}%</span>
            </motion.div>
          )}
        </div>

        {/* Value and Title */}
        <div className="space-y-2 mb-6">
          <motion.h3
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-4xl font-black text-gray-900 tracking-tight"
          >
            {typeof value === "number"
              ? value.toLocaleString()
              : value || "..."}
          </motion.h3>
          <p className="text-lg font-semibold text-gray-600">{title}</p>
          {subtitle && (
            <p className="text-sm text-gray-500 font-medium">{subtitle}</p>
          )}
        </div>

        {/* Trend Sparkline */}
        {trend && (
          <div className="relative h-12 overflow-hidden">
            <svg
              className="w-full h-full"
              viewBox="0 0 120 40"
              preserveAspectRatio="none"
            >
              <defs>
                <linearGradient
                  id={`gradient-${title}`}
                  x1="0%"
                  y1="0%"
                  x2="0%"
                  y2="100%"
                >
                  <stop offset="0%" stopColor="rgba(59, 130, 246, 0.3)" />
                  <stop offset="100%" stopColor="rgba(59, 130, 246, 0.05)" />
                </linearGradient>
              </defs>
              <motion.path
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1.5, delay: 0.3 }}
                d={`M 0 ${40 - trend[0]} ${trend
                  .map(
                    (point, i) =>
                      `L ${(i / (trend.length - 1)) * 120} ${40 - point}`
                  )
                  .join(" ")}`}
                fill="none"
                stroke="rgb(59, 130, 246)"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <motion.path
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 1.5, delay: 0.3 }}
                d={`M 0 ${40 - trend[0]} ${trend
                  .map(
                    (point, i) =>
                      `L ${(i / (trend.length - 1)) * 120} ${40 - point}`
                  )
                  .join(" ")} L 120 40 L 0 40 Z`}
                fill={`url(#gradient-${title})`}
              />
            </svg>
          </div>
        )}
      </div>
    </motion.div>
  );
};

// Simple Professional Chart (Fixed calculations)
const EnhancedThreatTrendsChart = ({ data = [] }) => {
  // Use mock data if no data provided or data is empty
  const mockData = [
    { date: "06-04", ivory: 12, rhino: 8, tiger: 6, pangolin: 4 },
    { date: "06-05", ivory: 15, rhino: 10, tiger: 8, pangolin: 6 },
    { date: "06-06", ivory: 8, rhino: 6, tiger: 12, pangolin: 5 },
    { date: "06-07", ivory: 18, rhino: 12, tiger: 7, pangolin: 8 },
    { date: "06-08", ivory: 14, rhino: 9, tiger: 11, pangolin: 7 },
    { date: "06-09", ivory: 20, rhino: 15, tiger: 9, pangolin: 10 },
    { date: "06-10", ivory: 16, rhino: 11, tiger: 13, pangolin: 9 },
  ];

  const chartData = data.length > 0 ? data.slice(0, 7) : mockData;

  return (
    <div className="h-80 w-full bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl p-6">
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mb-4 mx-auto">
            <TrendingUp size={32} className="text-white" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-2">
            Threat Trends
          </h3>
          <p className="text-gray-600 mb-4">Multi-species detection patterns</p>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="bg-white rounded-lg p-3">
              <div className="text-2xl font-bold text-red-500">45</div>
              <div className="text-gray-600">Ivory Threats</div>
            </div>
            <div className="bg-white rounded-lg p-3">
              <div className="text-2xl font-bold text-orange-500">28</div>
              <div className="text-gray-600">Rhino Horn</div>
            </div>
            <div className="bg-white rounded-lg p-3">
              <div className="text-2xl font-bold text-green-500">18</div>
              <div className="text-gray-600">Tiger Parts</div>
            </div>
            <div className="bg-white rounded-lg p-3">
              <div className="text-2xl font-bold text-purple-500">12</div>
              <div className="text-gray-600">Pangolin</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const EnhancedSpeciesDistributionChart = () => {
  const data = [
    { name: "Ivory Trade", value: 35, color: "#ef4444" },
    { name: "Rhino Horn", value: 28, color: "#f59e0b" },
    { name: "Tiger Parts", value: 18, color: "#10b981" },
    { name: "Pangolin", value: 12, color: "#8b5cf6" },
    { name: "Other Species", value: 7, color: "#6b7280" },
  ];

  return (
    <div className="h-80 w-full bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6">
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-600 rounded-2xl flex items-center justify-center mb-4 mx-auto">
            <PieChartIcon size={32} className="text-white" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Species Breakdown
          </h3>

          <div className="space-y-3">
            {data.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center justify-between bg-white rounded-lg p-3"
              >
                <div className="flex items-center space-x-3">
                  <div
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="font-medium text-gray-700">{item.name}</span>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-gray-900">
                    {item.value}%
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

const EnhancedPlatformActivityChart = () => {
  const data = [
    { platform: "eBay", threats: 45, color: "#3b82f6", status: "Excellent" },
    { platform: "Craigslist", threats: 38, color: "#10b981", status: "Good" },
    { platform: "Poshmark", threats: 29, color: "#f59e0b", status: "Active" },
    { platform: "Ruby Lane", threats: 18, color: "#8b5cf6", status: "Stable" },
  ];

  return (
    <div className="h-80 w-full bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl p-6">
      <div className="flex items-center justify-center h-full">
        <div className="text-center w-full">
          <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-blue-600 rounded-2xl flex items-center justify-center mb-4 mx-auto">
            <BarChart3 size={32} className="text-white" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Platform Performance
          </h3>

          <div className="grid grid-cols-2 gap-3">
            {data.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-lg p-4"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-gray-900">
                    {item.platform}
                  </span>
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: item.color }}
                  ></div>
                </div>
                <div className="text-2xl font-black text-gray-900 mb-1">
                  {item.threats}
                </div>
                <div className="text-xs text-gray-600">{item.status}</div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${(item.threats / 50) * 100}%` }}
                    transition={{ duration: 1, delay: index * 0.2 }}
                    className="h-2 rounded-full"
                    style={{ backgroundColor: item.color }}
                  />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

// Enhanced Platform Status Card
const EnhancedPlatformStatusCard = ({ platforms, onScan, isScanning }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-white rounded-3xl p-8 border border-gray-100/50"
    style={{
      background:
        "linear-gradient(145deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9))",
    }}
  >
    <div className="flex items-center justify-between mb-8">
      <div>
        <h3 className="text-2xl font-bold text-gray-900 mb-2">
          Platform Monitoring
        </h3>
        <p className="text-gray-600 font-medium">
          Real-time surveillance across 4 platforms
        </p>
      </div>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={onScan}
        disabled={isScanning}
        className={`relative flex items-center space-x-3 px-8 py-4 rounded-2xl font-bold text-lg transition-all duration-300 shadow-lg ${
          isScanning
            ? "bg-gray-100 text-gray-400 cursor-not-allowed"
            : "bg-gradient-to-r from-blue-500 to-blue-600 text-white hover:from-blue-600 hover:to-blue-700 hover:shadow-xl hover:shadow-blue-500/25"
        }`}
      >
        {isScanning ? (
          <>
            <div className="w-6 h-6 border-3 border-gray-400 border-t-transparent rounded-full animate-spin" />
            <span>Scanning...</span>
          </>
        ) : (
          <>
            <Play size={20} />
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
          className="group relative flex items-center justify-between p-6 bg-gradient-to-r from-gray-50 to-white rounded-2xl border border-gray-200/50 hover:border-gray-300/50 hover:shadow-lg transition-all duration-300"
        >
          <div className="flex items-center space-x-6">
            <div className="relative">
              <div
                className={`w-4 h-4 rounded-full shadow-lg ${
                  platform.status === "active"
                    ? "bg-emerald-400 shadow-emerald-400/30"
                    : "bg-red-400 shadow-red-400/30"
                } animate-pulse`}
              />
              <div
                className={`absolute inset-0 w-4 h-4 rounded-full animate-ping opacity-30 ${
                  platform.status === "active" ? "bg-emerald-400" : "bg-red-400"
                }`}
              />
            </div>
            <div>
              <h4 className="text-xl font-bold text-gray-900">
                {platform.name}
              </h4>
              <p className="text-gray-600 font-medium">
                Last scan: {new Date(platform.last_scan).toLocaleTimeString()}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="text-right">
              <div className="flex items-center space-x-3">
                <div className="w-24 bg-gray-200 rounded-full h-3 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${platform.success_rate}%` }}
                    transition={{ duration: 1.5, delay: index * 0.2 }}
                    className="bg-gradient-to-r from-emerald-500 to-emerald-600 h-3 rounded-full shadow-sm"
                  />
                </div>
                <span className="text-lg font-bold text-gray-900 min-w-[3rem]">
                  {platform.success_rate}%
                </span>
              </div>
            </div>
            <ChevronRight
              size={20}
              className="text-gray-400 group-hover:text-gray-600 group-hover:translate-x-1 transition-all duration-300"
            />
          </div>
        </motion.div>
      ))}
    </div>
  </motion.div>
);

// Main Dashboard Component
const ProfessionalDashboard = () => {
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

      // Try to connect to API, but provide fallback data
      try {
        const [statsData, trendsData, platformData] = await Promise.all([
          api.getRealTimeStats(),
          api.getThreatTrends(getDaysFromTimeRange(timeRange)),
          api.getPlatformStatus(),
        ]);

        setRealTimeStats(statsData);
        setThreatTrends(trendsData.daily_trends || []);
        setPlatformStatus(platformData.platforms || []);
      } catch (apiError) {
        // Use mock data if API fails
        console.warn("API connection failed, using mock data:", apiError);
        setError("API_OFFLINE"); // Set a special error flag
        setRealTimeStats({
          active_scans: 4,
          threats_detected_today: 12,
          alerts_sent_today: 3,
          platforms_monitored: 4,
          total_species_protected: 150,
          authorities_connected: 12,
          platform_names: ["eBay", "Craigslist", "Poshmark", "Ruby Lane"],
        });
        setThreatTrends([
          { date: "2024-06-04", ivory: 5, rhino: 3, tiger: 2, pangolin: 1 },
          { date: "2024-06-05", ivory: 7, rhino: 4, tiger: 3, pangolin: 2 },
          { date: "2024-06-06", ivory: 6, rhino: 2, tiger: 4, pangolin: 1 },
          { date: "2024-06-07", ivory: 8, rhino: 5, tiger: 2, pangolin: 3 },
          { date: "2024-06-08", ivory: 4, rhino: 3, tiger: 5, pangolin: 2 },
          { date: "2024-06-09", ivory: 9, rhino: 6, tiger: 3, pangolin: 4 },
          { date: "2024-06-10", ivory: 6, rhino: 4, tiger: 4, pangolin: 2 },
        ]);
        setPlatformStatus([
          {
            name: "eBay",
            status: "active",
            last_scan: new Date().toISOString(),
            success_rate: 92,
          },
          {
            name: "Craigslist",
            status: "active",
            last_scan: new Date().toISOString(),
            success_rate: 87,
          },
          {
            name: "Poshmark",
            status: "active",
            last_scan: new Date().toISOString(),
            success_rate: 84,
          },
          {
            name: "Ruby Lane",
            status: "active",
            last_scan: new Date().toISOString(),
            success_rate: 79,
          },
        ]);
        // Don't clear error - keep it to show demo mode
      }
    } catch (err) {
      console.error("Dashboard loading error:", err);
      // Still provide mock data even on error
      setRealTimeStats({
        active_scans: 4,
        threats_detected_today: 12,
        alerts_sent_today: 3,
        platforms_monitored: 4,
        total_species_protected: 150,
        authorities_connected: 12,
        platform_names: ["eBay", "Craigslist", "Poshmark", "Ruby Lane"],
      });
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
      setTimeout(() => loadDashboardData(), 5000);
    } catch (err) {
      console.error("Scan failed:", err);
    } finally {
      setIsScanning(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="w-20 h-20 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-6"
          />
          <p className="text-xl font-bold text-gray-700">
            Loading Conservatron Intelligence...
          </p>
          <p className="text-gray-500 mt-2">
            Connecting to conservation networks
          </p>
        </div>
      </div>
    );
  }

  // Show dashboard even if there are API errors - just with mock data
  if (!realTimeStats) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
            className="w-20 h-20 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-6"
          />
          <p className="text-xl font-bold text-gray-700">
            Initializing Dashboard...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-10">
      {/* Demo Mode Indicator */}
      {error === "API_OFFLINE" && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-2xl p-4"
        >
          <div className="flex items-center justify-center space-x-3">
            <AlertCircle size={20} className="text-amber-600" />
            <span className="text-amber-800 font-semibold">
              Demo Mode: Backend API offline - showing demonstration data
            </span>
            <button
              onClick={loadDashboardData}
              className="text-amber-700 hover:text-amber-900 text-sm font-medium underline"
            >
              Retry Connection
            </button>
          </div>
        </motion.div>
      )}

      {/* Enhanced Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col lg:flex-row lg:items-center lg:justify-between"
      >
        <div className="mb-6 lg:mb-0">
          <h1 className="text-5xl font-black text-gray-900 mb-3 tracking-tight">
            Live Operations Center
          </h1>
          <p className="text-xl text-gray-600 font-medium">
            Real-time wildlife conservation intelligence & threat monitoring
          </p>
          <div className="flex items-center space-x-4 mt-4">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-emerald-400 rounded-full animate-pulse shadow-lg shadow-emerald-400/30"></div>
              <span className="text-sm font-bold text-emerald-600">
                LIVE MONITORING
              </span>
            </div>
            <div className="text-sm text-gray-500">
              Last updated: {new Date().toLocaleTimeString()}
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="bg-white border border-gray-300 rounded-2xl px-6 py-3 text-sm font-medium focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-lg"
          >
            <option value="1h">Last Hour</option>
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
          </select>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={loadDashboardData}
            className="p-3 bg-white border border-gray-300 hover:border-gray-400 rounded-2xl transition-all duration-300 shadow-lg hover:shadow-xl"
          >
            <RefreshCcw size={20} className="text-gray-600" />
          </motion.button>
        </div>
      </motion.div>

      {/* Enhanced Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 lg:gap-8">
        <ProfessionalStatCard
          title="Active Scans"
          value={realTimeStats.active_scans}
          change={12}
          icon={Eye}
          gradient="from-blue-500 to-blue-600"
          subtitle="Platforms monitored 24/7"
          trend={[8, 12, 6, 15, 10, 18, 14, 20]}
        />
        <ProfessionalStatCard
          title="Threats Detected"
          value={realTimeStats.threats_detected_today}
          change={25}
          icon={AlertTriangle}
          gradient="from-red-500 to-red-600"
          subtitle="High-confidence detections today"
          trend={[4, 8, 6, 12, 15, 10, 12, 18]}
        />
        <ProfessionalStatCard
          title="Alerts Dispatched"
          value={realTimeStats.alerts_sent_today}
          change={15}
          icon={Bell}
          gradient="from-orange-500 to-orange-600"
          subtitle="Authorities notified"
          trend={[2, 4, 3, 6, 5, 7, 3, 8]}
        />
        <ProfessionalStatCard
          title="Global Platforms"
          value={realTimeStats.platforms_monitored}
          icon={Globe}
          gradient="from-emerald-500 to-emerald-600"
          subtitle="eBay • Craigslist • Poshmark • Ruby Lane"
        />
        <ProfessionalStatCard
          title="Protected Species"
          value={realTimeStats.total_species_protected}
          icon={Leaf}
          gradient="from-purple-500 to-purple-600"
          subtitle="CITES-listed coverage"
        />
        <ProfessionalStatCard
          title="Enforcement Partners"
          value={realTimeStats.authorities_connected}
          change={8}
          icon={Users}
          gradient="from-cyan-500 to-cyan-600"
          subtitle="Active agency connections"
        />
      </div>

      {/* Enhanced Charts Section */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 lg:gap-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-3xl p-8 border border-gray-100/50"
          style={{
            background:
              "linear-gradient(145deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9))",
          }}
        >
          <div className="flex items-center justify-between mb-8">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                Threat Detection Trends
              </h3>
              <p className="text-gray-600">
                Species-specific intelligence over time
              </p>
            </div>
            <TrendingUp className="text-blue-500" size={32} />
          </div>
          <EnhancedThreatTrendsChart data={threatTrends} />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-3xl p-8 border border-gray-100/50"
          style={{
            background:
              "linear-gradient(145deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9))",
          }}
        >
          <div className="flex items-center justify-between mb-8">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                Species Distribution
              </h3>
              <p className="text-gray-600">Threat composition breakdown</p>
            </div>
            <PieChartIcon className="text-purple-500" size={32} />
          </div>
          <EnhancedSpeciesDistributionChart />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-3xl p-8 border border-gray-100/50"
          style={{
            background:
              "linear-gradient(145deg, rgba(255,255,255,0.9), rgba(248,250,252,0.9))",
          }}
        >
          <div className="flex items-center justify-between mb-8">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                Platform Performance
              </h3>
              <p className="text-gray-600">Detection activity by marketplace</p>
            </div>
            <BarChart3 className="text-green-500" size={32} />
          </div>
          <EnhancedPlatformActivityChart />
        </motion.div>

        <EnhancedPlatformStatusCard
          platforms={platformStatus}
          onScan={triggerScan}
          isScanning={isScanning}
        />
      </div>

      {/* Enhanced Status Banner */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative overflow-hidden bg-gradient-to-r from-emerald-500 via-blue-500 to-purple-600 rounded-3xl p-8 text-white"
      >
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/80 via-blue-500/80 to-purple-600/80"></div>
        <div className="absolute inset-0 bg-black/10"></div>

        <div className="relative z-10 flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <div className="relative">
              <div className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center">
                <ShieldCheck size={32} className="text-white" />
              </div>
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-emerald-400 rounded-full flex items-center justify-center">
                <CheckCircle size={16} className="text-white" />
              </div>
            </div>

            <div>
              <h3 className="text-2xl font-bold mb-2">
                System Status: {error ? "Demo Mode" : "Fully Operational"}
              </h3>
              <p className="text-white/90 text-lg font-medium">
                {error
                  ? "Running with demonstration data • Backend API offline • UI fully functional"
                  : "All systems online • Backend API connected on port 5001"}{" "}
                • Last updated: {new Date().toLocaleTimeString()}
              </p>
              <div className="flex items-center space-x-8 mt-3 text-white/80">
                <span className="font-medium">
                  🌐 Monitoring: {realTimeStats.platform_names?.join(" • ")}
                </span>
                <span className="font-medium">⚡ Uptime: 99.9%</span>
                <span className="font-medium">🚀 Response: &lt;200ms</span>
              </div>
            </div>
          </div>

          <div className="hidden lg:block">
            <div className="flex flex-col items-end space-y-2">
              <div className="text-3xl font-bold">24/7</div>
              <div className="text-sm text-white/80 font-medium">
                ACTIVE MONITORING
              </div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

// Professional Analytics Dashboard
const AdvancedAnalytics = () => {
  const [timeframe, setTimeframe] = useState("30d");
  const [selectedMetric, setSelectedMetric] = useState("threats");

  const analyticsData = {
    threatIntelligence: [
      {
        category: "Ivory Trade",
        current: 45,
        previous: 38,
        trend: "up",
        change: 18,
      },
      {
        category: "Rhino Horn",
        current: 28,
        previous: 31,
        trend: "down",
        change: -10,
      },
      {
        category: "Tiger Parts",
        current: 18,
        previous: 14,
        trend: "up",
        change: 29,
      },
      {
        category: "Pangolin",
        current: 12,
        previous: 9,
        trend: "up",
        change: 33,
      },
    ],
    networkAnalysis: {
      activeNetworks: 8,
      totalNodes: 47,
      suspiciousConnections: 23,
      disruptedNetworks: 3,
    },
    aiPerformance: {
      accuracy: 94.2,
      precision: 91.8,
      recall: 87.3,
      falsePositives: 5.8,
    },
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-4xl font-black text-gray-900 mb-2">
            Intelligence Analytics
          </h1>
          <p className="text-xl text-gray-600">
            Advanced threat intelligence & predictive analysis
          </p>
        </div>
        <div className="flex items-center space-x-4 mt-4 lg:mt-0">
          <select
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="bg-white border border-gray-300 rounded-xl px-4 py-2 text-sm font-medium"
          >
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
          <button className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-xl hover:bg-purple-700">
            <Download size={16} />
            <span>Export Report</span>
          </button>
        </div>
      </div>

      {/* Threat Intelligence Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {analyticsData.threatIntelligence.map((item, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white rounded-2xl p-6 border border-gray-100 hover:shadow-lg transition-all duration-300"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-gray-900">{item.category}</h3>
              <div
                className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${
                  item.trend === "up"
                    ? "bg-red-100 text-red-700"
                    : "bg-green-100 text-green-700"
                }`}
              >
                {item.trend === "up" ? (
                  <ArrowUpRight size={12} />
                ) : (
                  <ArrowDownRight size={12} />
                )}
                <span>{Math.abs(item.change)}%</span>
              </div>
            </div>
            <div className="space-y-2">
              <div className="text-3xl font-bold text-gray-900">
                {item.current}
              </div>
              <div className="text-sm text-gray-600">
                vs {item.previous} last period
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl p-6 border border-gray-100"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Network Analysis
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-4 bg-purple-50 rounded-xl">
              <div className="text-2xl font-bold text-purple-600">
                {analyticsData.networkAnalysis.activeNetworks}
              </div>
              <div className="text-sm text-purple-700">Active Networks</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-xl">
              <div className="text-2xl font-bold text-blue-600">
                {analyticsData.networkAnalysis.totalNodes}
              </div>
              <div className="text-sm text-blue-700">Total Nodes</div>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-xl">
              <div className="text-2xl font-bold text-orange-600">
                {analyticsData.networkAnalysis.suspiciousConnections}
              </div>
              <div className="text-sm text-orange-700">Suspicious Links</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-xl">
              <div className="text-2xl font-bold text-green-600">
                {analyticsData.networkAnalysis.disruptedNetworks}
              </div>
              <div className="text-sm text-green-700">Disrupted</div>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-2xl p-6 border border-gray-100"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            AI Performance Metrics
          </h3>
          <div className="space-y-4">
            {[
              {
                label: "Detection Accuracy",
                value: analyticsData.aiPerformance.accuracy,
                color: "blue",
              },
              {
                label: "Precision Rate",
                value: analyticsData.aiPerformance.precision,
                color: "green",
              },
              {
                label: "Recall Rate",
                value: analyticsData.aiPerformance.recall,
                color: "purple",
              },
              {
                label: "False Positive Rate",
                value: analyticsData.aiPerformance.falsePositives,
                color: "red",
                inverse: true,
              },
            ].map((metric, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">
                  {metric.label}
                </span>
                <div className="flex items-center space-x-3">
                  <div className="w-24 bg-gray-200 rounded-full h-2">
                    <div
                      className={`bg-${metric.color}-500 h-2 rounded-full transition-all duration-1000`}
                      style={{
                        width: `${
                          metric.inverse ? 100 - metric.value : metric.value
                        }%`,
                      }}
                    />
                  </div>
                  <span className="text-sm font-bold text-gray-900 w-12">
                    {metric.value}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

// Professional Threat Detection Center
const ThreatIntelligence = () => {
  const [selectedThreat, setSelectedThreat] = useState(null);
  const [filterSeverity, setFilterSeverity] = useState("all");

  const threatData = [
    {
      id: "THR-2024-001",
      title: "Ivory Carving Marketplace Network",
      severity: "CRITICAL",
      platform: "eBay",
      confidence: 94,
      species: "African Elephant",
      detected: "2024-06-10T14:23:00Z",
      status: "Active Investigation",
      riskScore: 89,
      evidence: 5,
    },
    {
      id: "THR-2024-002",
      title: "Rhino Horn Traditional Medicine",
      severity: "HIGH",
      platform: "Craigslist",
      confidence: 87,
      species: "Black Rhino",
      detected: "2024-06-10T13:45:00Z",
      status: "Evidence Collection",
      riskScore: 76,
      evidence: 3,
    },
    {
      id: "THR-2024-003",
      title: "Tiger Bone Supplement Sales",
      severity: "HIGH",
      platform: "Ruby Lane",
      confidence: 91,
      species: "Siberian Tiger",
      detected: "2024-06-10T12:15:00Z",
      status: "Law Enforcement Notified",
      riskScore: 82,
      evidence: 7,
    },
    {
      id: "THR-2024-004",
      title: "Pangolin Scale Distribution",
      severity: "MEDIUM",
      platform: "Poshmark",
      confidence: 73,
      species: "Pangolin",
      detected: "2024-06-10T11:30:00Z",
      status: "Monitoring",
      riskScore: 64,
      evidence: 2,
    },
  ];

  const getSeverityColor = (severity) => {
    switch (severity) {
      case "CRITICAL":
        return "bg-red-100 text-red-800 border-red-200";
      case "HIGH":
        return "bg-orange-100 text-orange-800 border-orange-200";
      case "MEDIUM":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-4xl font-black text-gray-900 mb-2">
            Threat Detection Center
          </h1>
          <p className="text-xl text-gray-600">
            AI-powered threat analysis & network intelligence
          </p>
        </div>
        <div className="flex items-center space-x-4 mt-4 lg:mt-0">
          <select
            value={filterSeverity}
            onChange={(e) => setFilterSeverity(e.target.value)}
            className="bg-white border border-gray-300 rounded-xl px-4 py-2 text-sm font-medium"
          >
            <option value="all">All Severities</option>
            <option value="CRITICAL">Critical Only</option>
            <option value="HIGH">High Priority</option>
            <option value="MEDIUM">Medium Risk</option>
          </select>
          <button className="flex items-center space-x-2 px-4 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700">
            <AlertTriangle size={16} />
            <span>Emergency Alert</span>
          </button>
        </div>
      </div>

      {/* Threat Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <AlertTriangle size={32} />
            <span className="text-red-100 text-sm font-medium">CRITICAL</span>
          </div>
          <div className="text-3xl font-bold mb-1">1</div>
          <div className="text-red-100">Active Critical Threats</div>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <Target size={32} />
            <span className="text-orange-100 text-sm font-medium">HIGH</span>
          </div>
          <div className="text-3xl font-bold mb-1">2</div>
          <div className="text-orange-100">High Priority Cases</div>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <Eye size={32} />
            <span className="text-blue-100 text-sm font-medium">
              MONITORING
            </span>
          </div>
          <div className="text-3xl font-bold mb-1">1</div>
          <div className="text-blue-100">Under Surveillance</div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <ShieldCheck size={32} />
            <span className="text-green-100 text-sm font-medium">RESOLVED</span>
          </div>
          <div className="text-3xl font-bold mb-1">24</div>
          <div className="text-green-100">Cases This Month</div>
        </div>
      </div>

      {/* Active Threats Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-2xl border border-gray-100 overflow-hidden"
      >
        <div className="p-6 border-b border-gray-100">
          <h3 className="text-lg font-semibold text-gray-900">
            Active Threat Intelligence
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Threat ID
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Description
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Severity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Platform
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Confidence
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {threatData.map((threat, index) => (
                <motion.tr
                  key={threat.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="hover:bg-gray-50 cursor-pointer"
                  onClick={() => setSelectedThreat(threat)}
                >
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">
                    {threat.id}
                  </td>
                  <td className="px-6 py-4">
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {threat.title}
                      </div>
                      <div className="text-sm text-gray-500">
                        {threat.species}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full border ${getSeverityColor(
                        threat.severity
                      )}`}
                    >
                      {threat.severity}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {threat.platform}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="w-16 bg-gray-200 rounded-full h-2 mr-3">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${threat.confidence}%` }}
                        />
                      </div>
                      <span className="text-sm text-gray-900">
                        {threat.confidence}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                    {threat.status}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button className="text-blue-600 hover:text-blue-900">
                      View Details
                    </button>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
};

// Professional Evidence Archive
const EvidenceArchive = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState("all");

  const evidenceData = [
    {
      id: "EV-2024-001",
      title: "Ivory Carving Listing Screenshots",
      type: "Digital Evidence",
      platform: "eBay",
      date: "2024-06-10T14:23:00Z",
      status: "Preserved",
      hash: "SHA256: a7b2c3d4...",
      fileCount: 5,
      legalStatus: "Chain of Custody Maintained",
    },
    {
      id: "EV-2024-002",
      title: "Rhino Horn Communication Logs",
      type: "Message Archive",
      platform: "Craigslist",
      date: "2024-06-10T13:45:00Z",
      status: "Analyzed",
      hash: "SHA256: e5f6g7h8...",
      fileCount: 12,
      legalStatus: "Ready for Prosecution",
    },
    {
      id: "EV-2024-003",
      title: "Tiger Parts Network Analysis",
      type: "Investigation Report",
      platform: "Multiple",
      date: "2024-06-10T12:15:00Z",
      status: "Under Review",
      hash: "SHA256: i9j0k1l2...",
      fileCount: 8,
      legalStatus: "Pending Verification",
    },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-4xl font-black text-gray-900 mb-2">
            Evidence Vault
          </h1>
          <p className="text-xl text-gray-600">
            Blockchain-secured evidence preservation & legal documentation
          </p>
        </div>
        <div className="flex items-center space-x-4 mt-4 lg:mt-0">
          <div className="relative">
            <Search
              size={20}
              className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
            />
            <input
              type="text"
              placeholder="Search evidence..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500"
            />
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700">
            <Lock size={16} />
            <span>Verify Chain</span>
          </button>
        </div>
      </div>

      {/* Evidence Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <Database size={32} />
            <span className="text-emerald-100 text-sm font-medium">TOTAL</span>
          </div>
          <div className="text-3xl font-bold mb-1">247</div>
          <div className="text-emerald-100">Evidence Packages</div>
        </div>

        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <ShieldCheck size={32} />
            <span className="text-blue-100 text-sm font-medium">VERIFIED</span>
          </div>
          <div className="text-3xl font-bold mb-1">198</div>
          <div className="text-blue-100">Blockchain Verified</div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <FileText size={32} />
            <span className="text-purple-100 text-sm font-medium">LEGAL</span>
          </div>
          <div className="text-3xl font-bold mb-1">34</div>
          <div className="text-purple-100">Court Ready</div>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-2xl p-6 text-white">
          <div className="flex items-center justify-between mb-4">
            <Clock size={32} />
            <span className="text-orange-100 text-sm font-medium">RECENT</span>
          </div>
          <div className="text-3xl font-bold mb-1">12</div>
          <div className="text-orange-100">Last 24 Hours</div>
        </div>
      </div>

      {/* Evidence Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {evidenceData.map((evidence, index) => (
          <motion.div
            key={evidence.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white rounded-2xl p-6 border border-gray-100 hover:shadow-lg transition-all duration-300"
          >
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-mono text-gray-500">
                {evidence.id}
              </span>
              <span
                className={`px-2 py-1 rounded-full text-xs font-medium ${
                  evidence.status === "Preserved"
                    ? "bg-green-100 text-green-800"
                    : evidence.status === "Analyzed"
                    ? "bg-blue-100 text-blue-800"
                    : "bg-yellow-100 text-yellow-800"
                }`}
              >
                {evidence.status}
              </span>
            </div>

            <h3 className="font-semibold text-gray-900 mb-2">
              {evidence.title}
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              {evidence.type} • {evidence.platform}
            </p>

            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Files:</span>
                <span className="font-medium">{evidence.fileCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Date:</span>
                <span className="font-medium">
                  {new Date(evidence.date).toLocaleDateString()}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Legal Status:</span>
                <span className="font-medium text-green-600">
                  {evidence.legalStatus}
                </span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100">
              <div className="flex items-center space-x-2 text-xs text-gray-500">
                <Lock size={12} />
                <span className="font-mono">{evidence.hash}</span>
              </div>
            </div>

            <div className="mt-4 flex space-x-2">
              <button className="flex-1 px-3 py-2 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700">
                View Evidence
              </button>
              <button className="px-3 py-2 border border-gray-300 rounded-lg text-sm hover:bg-gray-50">
                Verify
              </button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

// Professional Reports Dashboard
const Reports = () => {
  const [reportType, setReportType] = useState("executive");
  const [dateRange, setDateRange] = useState("monthly");

  const reportMetrics = {
    totalDetections: 247,
    successfulInterventions: 198,
    economicImpact: 2400000,
    speciesSaved: 150,
    lawEnforcementAlerts: 89,
    platformCooperation: 76,
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-4xl font-black text-gray-900 mb-2">
            Executive Reports
          </h1>
          <p className="text-xl text-gray-600">
            Comprehensive impact analysis & compliance documentation
          </p>
        </div>
        <div className="flex items-center space-x-4 mt-4 lg:mt-0">
          <select
            value={reportType}
            onChange={(e) => setReportType(e.target.value)}
            className="bg-white border border-gray-300 rounded-xl px-4 py-2 text-sm font-medium"
          >
            <option value="executive">Executive Summary</option>
            <option value="technical">Technical Analysis</option>
            <option value="compliance">Compliance Report</option>
            <option value="impact">Impact Assessment</option>
          </select>
          <button className="flex items-center space-x-2 px-4 py-2 bg-orange-600 text-white rounded-xl hover:bg-orange-700">
            <Download size={16} />
            <span>Export PDF</span>
          </button>
        </div>
      </div>

      {/* Impact Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white">
          <div className="text-3xl font-bold mb-1">
            {reportMetrics.totalDetections}
          </div>
          <div className="text-blue-100 text-sm">Total Detections</div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-6 text-white">
          <div className="text-3xl font-bold mb-1">
            {reportMetrics.successfulInterventions}
          </div>
          <div className="text-green-100 text-sm">Interventions</div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white">
          <div className="text-3xl font-bold mb-1">
            ${(reportMetrics.economicImpact / 1000000).toFixed(1)}M
          </div>
          <div className="text-purple-100 text-sm">Economic Impact</div>
        </div>

        <div className="bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-2xl p-6 text-white">
          <div className="text-3xl font-bold mb-1">
            {reportMetrics.speciesSaved}
          </div>
          <div className="text-emerald-100 text-sm">Species Protected</div>
        </div>

        <div className="bg-gradient-to-br from-red-500 to-red-600 rounded-2xl p-6 text-white">
          <div className="text-3xl font-bold mb-1">
            {reportMetrics.lawEnforcementAlerts}
          </div>
          <div className="text-red-100 text-sm">Law Enforcement</div>
        </div>

        <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-2xl p-6 text-white">
          <div className="text-3xl font-bold mb-1">
            {reportMetrics.platformCooperation}%
          </div>
          <div className="text-orange-100 text-sm">Platform Response</div>
        </div>
      </div>

      {/* Executive Summary */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-2xl p-8 border border-gray-100"
      >
        <h3 className="text-2xl font-bold text-gray-900 mb-6">
          Monthly Impact Summary
        </h3>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <h4 className="text-lg font-semibold text-gray-900 mb-4">
              Conservation Impact
            </h4>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-4 bg-green-50 rounded-lg">
                <span className="font-medium text-green-800">
                  Wildlife Trafficking Prevented
                </span>
                <span className="text-2xl font-bold text-green-600">
                  247 cases
                </span>
              </div>
              <div className="flex justify-between items-center p-4 bg-blue-50 rounded-lg">
                <span className="font-medium text-blue-800">
                  Economic Value Saved
                </span>
                <span className="text-2xl font-bold text-blue-600">$2.4M</span>
              </div>
              <div className="flex justify-between items-center p-4 bg-purple-50 rounded-lg">
                <span className="font-medium text-purple-800">
                  Species Protected
                </span>
                <span className="text-2xl font-bold text-purple-600">150</span>
              </div>
            </div>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-gray-900 mb-4">
              Operational Efficiency
            </h4>
            <div className="space-y-4">
              {[
                { label: "Detection Accuracy", value: 94, color: "blue" },
                { label: "Response Time", value: 87, color: "green" },
                { label: "Platform Cooperation", value: 76, color: "purple" },
                { label: "Case Resolution", value: 82, color: "orange" },
              ].map((metric, index) => (
                <div key={index} className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">
                    {metric.label}
                  </span>
                  <div className="flex items-center space-x-3">
                    <div className="w-24 bg-gray-200 rounded-full h-2">
                      <div
                        className={`bg-${metric.color}-500 h-2 rounded-full transition-all duration-1000`}
                        style={{ width: `${metric.value}%` }}
                      />
                    </div>
                    <span className="text-sm font-bold text-gray-900 w-12">
                      {metric.value}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-8 p-6 bg-gradient-to-r from-orange-50 to-red-50 rounded-xl border border-orange-200">
          <h4 className="text-lg font-semibold text-gray-900 mb-3">
            Key Achievements This Month
          </h4>
          <ul className="space-y-2">
            <li className="flex items-center space-x-3">
              <CheckCircle size={20} className="text-green-500" />
              <span>Disrupted 3 major ivory trafficking networks</span>
            </li>
            <li className="flex items-center space-x-3">
              <CheckCircle size={20} className="text-green-500" />
              <span>Prevented $2.4M in illegal wildlife trade</span>
            </li>
            <li className="flex items-center space-x-3">
              <CheckCircle size={20} className="text-green-500" />
              <span>Achieved 94% detection accuracy across all platforms</span>
            </li>
            <li className="flex items-center space-x-3">
              <CheckCircle size={20} className="text-green-500" />
              <span>Expanded monitoring to 4 major e-commerce platforms</span>
            </li>
          </ul>
        </div>
      </motion.div>
    </div>
  );
};

const USERNAME = "conservatron12000"; // Set your admin username
const PASSWORD = "SavingPandasLeftRightLeftRight&LeftAgain4000"; // Set your admin password

function LoginModal({ onSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    if (username === USERNAME && password === PASSWORD) {
      onSuccess();
    } else {
      setError("Invalid credentials");
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100vw",
        height: "100vh",
        background: "rgba(0,0,0,0.9)",
        zIndex: 9999,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <form
        onSubmit={handleLogin}
        style={{
          background: "#fff",
          padding: 32,
          borderRadius: 12,
          minWidth: 320,
        }}
      >
        <h2>Login Required</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{ display: "block", margin: "16px 0", width: "100%" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ display: "block", margin: "16px 0", width: "100%" }}
        />
        {error && <div style={{ color: "red" }}>{error}</div>}
        <button type="submit" style={{ width: "100%" }}>
          Login
        </button>
      </form>
    </div>
  );
}

// Main App Component
const App = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);

  return (
    <>
      {!authenticated && (
        <LoginModal onSuccess={() => setAuthenticated(true)} />
      )}
      <div style={{ filter: authenticated ? "none" : "blur(2px)" }}>
        <Router>
          <div
            className="min-h-screen flex overflow-hidden"
            style={{
              background:
                "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%)",
            }}
          >
            <ProfessionalSidebar
              isOpen={sidebarOpen}
              setIsOpen={setSidebarOpen}
            />

            {/* Main Content */}
            <div className="flex-1 flex flex-col  overflow-hidden">
              {/* Enhanced Mobile Header */}
              <header className="bg-white/80 border-b border-gray-200/50 px-6 py-4 lg:hidden">
                <div className="flex items-center justify-between">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setSidebarOpen(true)}
                    className="p-3 hover:bg-gray-100 rounded-2xl transition-colors"
                  >
                    <Menu size={24} className="text-gray-600" />
                  </motion.button>

                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
                      <Leaf size={24} className="text-white" />
                    </div>
                    <h1 className="text-xl font-bold text-gray-900">
                      The Conservatron 12000
                    </h1>
                  </div>

                  <div className="w-12" />
                </div>
              </header>

              {/* Enhanced Page Content */}
              <main className="flex-1 overflow-y-auto">
                <div className="p-6 lg:p-8 xl:p-12">
                  <AnimatePresence mode="wait">
                    <Routes>
                      <Route path="/" element={<ProfessionalDashboard />} />
                      <Route
                        path="/analytics"
                        element={<AdvancedAnalytics />}
                      />
                      <Route path="/threats" element={<ThreatIntelligence />} />
                      <Route path="/evidence" element={<EvidenceArchive />} />
                      <Route path="/reports" element={<Reports />} />
                    </Routes>
                  </AnimatePresence>
                </div>
              </main>
            </div>
          </div>
        </Router>
      </div>
    </>
  );
};

export default App;
