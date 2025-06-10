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
} from "lucide-react";

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState("overview");
  const [timeRange, setTimeRange] = useState("24h");
  const [selectedRegion, setSelectedRegion] = useState("global");

  // Mock data - replace with real API calls
  const [dashboardData, setDashboardData] = useState({
    realTimeStats: {
      activeScans: 847,
      threatsDetected: 23,
      alertsSent: 8,
      platformsMonitored: 4,
      speciesProtected: 156,
      authoritiesConnected: 34,
    },
    threatTrends: [
      { date: "2024-06-01", threats: 45, resolved: 38 },
      { date: "2024-06-02", threats: 52, resolved: 41 },
      { date: "2024-06-03", threats: 38, resolved: 35 },
      { date: "2024-06-04", threats: 61, resolved: 48 },
      { date: "2024-06-05", threats: 43, resolved: 39 },
      { date: "2024-06-06", threats: 57, resolved: 44 },
      { date: "2024-06-07", threats: 39, resolved: 36 },
    ],
    speciesDistribution: [
      { name: "Ivory", value: 35, color: "#ff6b6b" },
      { name: "Rhino Horn", value: 28, color: "#4ecdc4" },
      { name: "Tiger Parts", value: 18, color: "#45b7d1" },
      { name: "Pangolin Scales", value: 12, color: "#96ceb4" },
      { name: "Other", value: 7, color: "#ffeaa7" },
    ],
    platformActivity: [
      { platform: "eBay", threats: 45, percentage: 32 },
      { platform: "Craigslist", threats: 38, percentage: 27 },
      { platform: "Poshmark", threats: 29, percentage: 21 },
      { platform: "Ruby Lane", threats: 18, percentage: 20 },
    ],
    recentAlerts: [
      {
        id: "ALT-2024-001",
        timestamp: "2024-06-09 14:23",
        threat: "Ivory Carving",
        platform: "eBay",
        severity: "HIGH",
        location: "New York, NY",
      },
      {
        id: "ALT-2024-002",
        timestamp: "2024-06-09 13:45",
        threat: "Rhino Horn Powder",
        platform: "Craigslist",
        severity: "CRITICAL",
        location: "Los Angeles, CA",
      },
      {
        id: "ALT-2024-003",
        timestamp: "2024-06-09 12:10",
        threat: "Tiger Bone Medicine",
        platform: "Poshmark",
        severity: "HIGH",
        location: "Houston, TX",
      },
      {
        id: "ALT-2024-004",
        timestamp: "2024-06-09 11:30",
        threat: "Antique Ivory",
        platform: "Ruby Lane",
        severity: "MEDIUM",
        location: "Miami, FL",
      },
    ],
  });

  const StatCard = ({ title, value, change, icon: Icon, color }) => (
    <div
      className="bg-white rounded-xl shadow-lg p-6 border-l-4"
      style={{ borderLeftColor: color }}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {change && (
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

  const ThreatMap = () => (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-semibold mb-4">Global Threat Distribution</h3>
      <div className="h-64 bg-gradient-to-br from-blue-50 to-indigo-100 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <MapPin size={48} className="text-indigo-400 mx-auto mb-2" />
          <p className="text-gray-600">
            Interactive world map showing threat hotspots
          </p>
          <p className="text-sm text-gray-500">
            Integration with Leaflet/MapBox for real-time visualization
          </p>
        </div>
      </div>
    </div>
  );

  const NetworkAnalysis = () => (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-semibold mb-4">
        Trafficking Network Analysis
      </h3>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900">Identified Networks</h4>
          <p className="text-2xl font-bold text-blue-600">8</p>
          <p className="text-sm text-gray-600">Active criminal networks</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900">Connected Actors</h4>
          <p className="text-2xl font-bold text-orange-600">47</p>
          <p className="text-sm text-gray-600">Individual sellers linked</p>
        </div>
      </div>
      <div className="mt-4 h-32 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <Users size={32} className="text-purple-400 mx-auto mb-2" />
          <p className="text-sm text-gray-600">Network graph visualization</p>
        </div>
      </div>
    </div>
  );

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Real-time Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <StatCard
          title="Active Scans"
          value={dashboardData.realTimeStats.activeScans}
          change={12}
          icon={Eye}
          color="#3b82f6"
        />
        <StatCard
          title="Threats Detected Today"
          value={dashboardData.realTimeStats.threatsDetected}
          change={-8}
          icon={AlertTriangle}
          color="#ef4444"
        />
        <StatCard
          title="Alerts Sent"
          value={dashboardData.realTimeStats.alertsSent}
          change={15}
          icon={Bell}
          color="#f59e0b"
        />
        <StatCard
          title="Platforms Monitored"
          value={dashboardData.realTimeStats.platformsMonitored}
          icon={Globe}
          color="#10b981"
        />
        <StatCard
          title="Species Protected"
          value={dashboardData.realTimeStats.speciesProtected}
          icon={Shield}
          color="#8b5cf6"
        />
        <StatCard
          title="Authorities Connected"
          value={dashboardData.realTimeStats.authoritiesConnected}
          icon={Users}
          color="#06b6d4"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4">
            Threat Detection Trends
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={dashboardData.threatTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area
                type="monotone"
                dataKey="threats"
                stackId="1"
                stroke="#ef4444"
                fill="#ef444420"
              />
              <Area
                type="monotone"
                dataKey="resolved"
                stackId="1"
                stroke="#10b981"
                fill="#10b98120"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4">
            Threatened Species Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={dashboardData.speciesDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={120}
                paddingAngle={5}
                dataKey="value"
              >
                {dashboardData.speciesDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Platform Activity & Map */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Platform Activity</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={dashboardData.platformActivity}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="platform" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="threats" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <ThreatMap />
      </div>
    </div>
  );

  const renderAlerts = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-semibold">Critical Alerts</h3>
          <div className="flex space-x-2">
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Export Report
            </button>
            <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              Filter
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Alert ID
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Timestamp
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Threat Type
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Platform
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Severity
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Location
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {dashboardData.recentAlerts.map((alert) => (
                <tr
                  key={alert.id}
                  className="border-b border-gray-100 hover:bg-gray-50"
                >
                  <td className="py-3 px-4 font-mono text-sm">{alert.id}</td>
                  <td className="py-3 px-4 text-sm text-gray-600">
                    {alert.timestamp}
                  </td>
                  <td className="py-3 px-4 text-sm">{alert.threat}</td>
                  <td className="py-3 px-4 text-sm">{alert.platform}</td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        alert.severity === "CRITICAL"
                          ? "bg-red-100 text-red-800"
                          : alert.severity === "HIGH"
                          ? "bg-orange-100 text-orange-800"
                          : "bg-yellow-100 text-yellow-800"
                      }`}
                    >
                      {alert.severity}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-sm text-gray-600">
                    {alert.location}
                  </td>
                  <td className="py-3 px-4">
                    <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderIntelligence = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <NetworkAnalysis />

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4">AI Threat Analysis</h3>
          <div className="space-y-4">
            <div className="bg-gradient-to-r from-red-50 to-pink-50 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-2">
                High-Risk Patterns Detected
              </h4>
              <p className="text-sm text-gray-600 mb-2">
                Code words: "white gold", "traditional medicine"
              </p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-red-500 h-2 rounded-full"
                  style={{ width: "85%" }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">85% confidence</p>
            </div>

            <div className="bg-gradient-to-r from-orange-50 to-yellow-50 rounded-lg p-4">
              <h4 className="font-medium text-gray-900 mb-2">
                Suspicious Shipping Patterns
              </h4>
              <p className="text-sm text-gray-600 mb-2">
                Cross-border routes identified
              </p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-orange-500 h-2 rounded-full"
                  style={{ width: "73%" }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">73% confidence</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-lg font-semibold mb-4">
          Language Analysis Dashboard
        </h3>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">15</p>
            <p className="text-sm text-gray-600">Languages Monitored</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-green-600">342</p>
            <p className="text-sm text-gray-600">Translated Threats</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-purple-600">89%</p>
            <p className="text-sm text-gray-600">Translation Accuracy</p>
          </div>
          <div className="text-center">
            <p className="text-2xl font-bold text-orange-600">127</p>
            <p className="text-sm text-gray-600">Cultural Variants</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderEvidence = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-lg font-semibold">Evidence Archive</h3>
          <div className="flex space-x-2">
            <div className="relative">
              <Search
                size={20}
                className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"
              />
              <input
                type="text"
                placeholder="Search evidence..."
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center">
              <Download size={16} className="mr-2" />
              Export
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((item) => (
            <div
              key={item}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-mono text-gray-600">
                  EV-2024-{item.toString().padStart(3, "0")}
                </span>
                <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                  HIGH
                </span>
              </div>
              <h4 className="font-medium text-gray-900 mb-2">
                Ivory Carving Evidence
              </h4>
              <p className="text-sm text-gray-600 mb-3">
                Archived from eBay listing with AI analysis
              </p>
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-500">2024-06-09 14:23</span>
                <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

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
                  Wildlife Conservation Intelligence Platform
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
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-gray-600">Live Monitoring</span>
              </div>

              <button className="p-2 bg-gray-100 rounded-lg hover:bg-gray-200">
                <Settings size={20} className="text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-sm mb-8">
          <nav className="flex space-x-8 px-6">
            {[
              { id: "overview", label: "Overview", icon: TrendingUp },
              { id: "alerts", label: "Alerts", icon: AlertTriangle },
              { id: "intelligence", label: "Threat Intelligence", icon: Eye },
              { id: "evidence", label: "Evidence Archive", icon: Shield },
            ].map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`flex items-center py-4 px-2 border-b-2 font-medium text-sm ${
                  activeTab === id
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700"
                }`}
              >
                <Icon size={16} className="mr-2" />
                {label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        {activeTab === "overview" && renderOverview()}
        {activeTab === "alerts" && renderAlerts()}
        {activeTab === "intelligence" && renderIntelligence()}
        {activeTab === "evidence" && renderEvidence()}
      </div>
    </div>
  );
};

export default Dashboard;
