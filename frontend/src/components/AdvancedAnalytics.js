import React, { useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts";
import {
  Calendar,
  Download,
  Filter,
  TrendingUp,
  AlertCircle,
  MapPin,
  Clock,
  Users,
  Globe,
  Eye,
  Shield,
  Target,
} from "lucide-react";

const AdvancedAnalytics = () => {
  const [dateRange, setDateRange] = useState("30d");
  const [selectedMetric, setSelectedMetric] = useState("threats");
  const [reportType, setReportType] = useState("executive");

  // Mock advanced analytics data
  const analyticsData = {
    threatTrends: [
      { month: "Jan", ivory: 45, rhino: 23, tiger: 18, pangolin: 12, other: 8 },
      {
        month: "Feb",
        ivory: 52,
        rhino: 28,
        tiger: 22,
        pangolin: 15,
        other: 10,
      },
      {
        month: "Mar",
        ivory: 48,
        rhino: 31,
        tiger: 25,
        pangolin: 18,
        other: 12,
      },
      {
        month: "Apr",
        ivory: 61,
        rhino: 35,
        tiger: 28,
        pangolin: 21,
        other: 15,
      },
      {
        month: "May",
        ivory: 58,
        rhino: 39,
        tiger: 32,
        pangolin: 24,
        other: 18,
      },
      {
        month: "Jun",
        ivory: 73,
        rhino: 42,
        tiger: 35,
        pangolin: 28,
        other: 22,
      },
    ],
    geographicDistribution: [
      { region: "North America", threats: 245, resolved: 198, percentage: 35 },
      { region: "Asia Pacific", threats: 189, resolved: 142, percentage: 27 },
      { region: "Europe", threats: 156, resolved: 129, percentage: 22 },
      { region: "Africa", threats: 78, resolved: 61, percentage: 11 },
      { region: "South America", threats: 32, resolved: 25, percentage: 5 },
    ],
    platformEffectiveness: [
      {
        platform: "eBay",
        detectionRate: 92,
        falsePositives: 8,
        responseTime: 2.3,
      },
      {
        platform: "Craigslist",
        detectionRate: 87,
        falsePositives: 12,
        responseTime: 3.1,
      },
      {
        platform: "Facebook",
        detectionRate: 84,
        falsePositives: 15,
        responseTime: 4.2,
      },
      {
        platform: "Mercari",
        detectionRate: 79,
        falsePositives: 18,
        responseTime: 5.8,
      },
    ],
    aiPerformance: [
      { metric: "Accuracy", score: 94 },
      { metric: "Precision", score: 91 },
      { metric: "Recall", score: 87 },
      { metric: "F1-Score", score: 89 },
      { metric: "Speed", score: 96 },
      { metric: "Language Coverage", score: 92 },
    ],
    networkAnalytics: {
      totalNetworks: 23,
      activeNetworks: 15,
      disrupted: 8,
      averageSize: 6.3,
      connectionStrength: 0.78,
    },
    impactMetrics: {
      listingsRemoved: 1247,
      sellersBlocked: 89,
      authoritiesNotified: 156,
      casesForwarded: 34,
      estimatedValue: 2.4e6,
    },
  };

  const COLORS = [
    "#ff6b6b",
    "#4ecdc4",
    "#45b7d1",
    "#96ceb4",
    "#ffeaa7",
    "#dda0dd",
  ];

  const MetricCard = ({
    title,
    value,
    change,
    icon: Icon,
    color,
    format = "number",
  }) => {
    const formatValue = (val) => {
      if (format === "currency") return `$${(val / 1000000).toFixed(1)}M`;
      if (format === "percentage") return `${val}%`;
      return val.toLocaleString();
    };

    return (
      <div
        className="bg-white rounded-xl shadow-lg p-6 border-l-4"
        style={{ borderLeftColor: color }}
      >
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <p className="text-2xl font-bold text-gray-900">
              {formatValue(value)}
            </p>
            {change !== undefined && (
              <p
                className={`text-sm ${
                  change > 0 ? "text-green-600" : "text-red-600"
                }`}
              >
                {change > 0 ? "+" : ""}
                {change}% from last period
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
  };

  const ExecutiveReport = () => (
    <div className="space-y-8">
      {/* Executive Summary */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-8 border border-blue-200">
        <h3 className="text-2xl font-bold text-gray-900 mb-4">
          Executive Summary - Wildlife Trade Intelligence
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <p className="text-3xl font-bold text-blue-600">73%</p>
            <p className="text-gray-700">Threat Detection Increase</p>
          </div>
          <div className="text-center">
            <p className="text-3xl font-bold text-green-600">$2.4M</p>
            <p className="text-gray-700">Estimated Illegal Trade Prevented</p>
          </div>
          <div className="text-center">
            <p className="text-3xl font-bold text-purple-600">156</p>
            <p className="text-gray-700">Law Enforcement Alerts</p>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <MetricCard
          title="Active Threat Networks"
          value={analyticsData.networkAnalytics.activeNetworks}
          change={12}
          icon={Users}
          color="#ef4444"
        />
        <MetricCard
          title="Detection Accuracy"
          value={94}
          change={3}
          icon={Target}
          color="#10b981"
          format="percentage"
        />
        <MetricCard
          title="Response Time (avg)"
          value={3.1}
          change={-15}
          icon={Clock}
          color="#f59e0b"
        />
        <MetricCard
          title="Listings Removed"
          value={analyticsData.impactMetrics.listingsRemoved}
          change={28}
          icon={Shield}
          color="#8b5cf6"
        />
        <MetricCard
          title="Cases Forwarded"
          value={analyticsData.impactMetrics.casesForwarded}
          change={45}
          icon={AlertCircle}
          color="#06b6d4"
        />
        <MetricCard
          title="Economic Impact"
          value={analyticsData.impactMetrics.estimatedValue}
          change={67}
          icon={TrendingUp}
          color="#84cc16"
          format="currency"
        />
      </div>

      {/* Threat Intelligence Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            Threat Trends by Species (6 Months)
          </h4>
          <ResponsiveContainer width="100%" height={350}>
            <AreaChart data={analyticsData.threatTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
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
                dataKey="pangolin"
                stackId="1"
                stroke="#96ceb4"
                fill="#96ceb4"
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
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            Geographic Distribution
          </h4>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart
              data={analyticsData.geographicDistribution}
              layout="horizontal"
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="region" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="threats" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              <Bar dataKey="resolved" fill="#10b981" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* AI Performance Radar */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-4">
          AI System Performance Matrix
        </h4>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={analyticsData.aiPerformance}>
              <PolarGrid />
              <PolarAngleAxis dataKey="metric" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} />
              <Radar
                name="Performance"
                dataKey="score"
                stroke="#8884d8"
                fill="#8884d8"
                fillOpacity={0.6}
              />
            </RadarChart>
          </ResponsiveContainer>

          <div className="space-y-4">
            <h5 className="font-medium text-gray-900">Performance Insights</h5>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                <span className="text-sm font-medium">Overall Accuracy</span>
                <span className="text-lg font-bold text-green-600">94%</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span className="text-sm font-medium">Processing Speed</span>
                <span className="text-lg font-bold text-blue-600">96%</span>
              </div>
              <div className="flex justify-between items-center p-3 bg-orange-50 rounded-lg">
                <span className="text-sm font-medium">Language Coverage</span>
                <span className="text-lg font-bold text-orange-600">92%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const TechnicalReport = () => (
    <div className="space-y-8">
      {/* Platform Performance */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h4 className="text-lg font-semibold text-gray-900 mb-6">
          Platform Detection Performance
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Platform
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Detection Rate
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  False Positives
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Avg Response Time
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-900">
                  Status
                </th>
              </tr>
            </thead>
            <tbody>
              {analyticsData.platformEffectiveness.map((platform, index) => (
                <tr key={index} className="border-b border-gray-100">
                  <td className="py-3 px-4 font-medium">{platform.platform}</td>
                  <td className="py-3 px-4">
                    <div className="flex items-center">
                      <div className="w-16 bg-gray-200 rounded-full h-2 mr-3">
                        <div
                          className="bg-green-500 h-2 rounded-full"
                          style={{ width: `${platform.detectionRate}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">
                        {platform.detectionRate}%
                      </span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        platform.falsePositives < 10
                          ? "bg-green-100 text-green-800"
                          : platform.falsePositives < 15
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-red-100 text-red-800"
                      }`}
                    >
                      {platform.falsePositives}%
                    </span>
                  </td>
                  <td className="py-3 px-4">{platform.responseTime}s</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                      Active
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Network Analytics Deep Dive */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            Network Analysis Metrics
          </h4>
          <div className="space-y-4">
            <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
              <span className="font-medium">Total Networks Identified</span>
              <span className="text-xl font-bold text-blue-600">
                {analyticsData.networkAnalytics.totalNetworks}
              </span>
            </div>
            <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
              <span className="font-medium">Currently Active</span>
              <span className="text-xl font-bold text-orange-600">
                {analyticsData.networkAnalytics.activeNetworks}
              </span>
            </div>
            <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
              <span className="font-medium">Successfully Disrupted</span>
              <span className="text-xl font-bold text-green-600">
                {analyticsData.networkAnalytics.disrupted}
              </span>
            </div>
            <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
              <span className="font-medium">Average Network Size</span>
              <span className="text-xl font-bold text-purple-600">
                {analyticsData.networkAnalytics.averageSize}
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h4 className="text-lg font-semibold text-gray-900 mb-4">
            Impact Assessment
          </h4>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Enforcement Actions
                </span>
                <span className="text-sm text-gray-600">89%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full"
                  style={{ width: "89%" }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Platform Cooperation
                </span>
                <span className="text-sm text-gray-600">76%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-600 h-2 rounded-full"
                  style={{ width: "76%" }}
                ></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">
                  Case Prosecution Rate
                </span>
                <span className="text-sm text-gray-600">43%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-orange-600 h-2 rounded-full"
                  style={{ width: "43%" }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Advanced Analytics & Reporting
              </h1>
              <p className="text-gray-600 mt-1">
                Comprehensive intelligence analysis and impact assessment
              </p>
            </div>

            <div className="flex items-center space-x-4">
              <select
                value={dateRange}
                onChange={(e) => setDateRange(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
              >
                <option value="7d">Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
                <option value="90d">Last 90 Days</option>
                <option value="1y">Last Year</option>
              </select>

              <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                <Download size={16} className="mr-2" />
                Export Report
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Report Type Selection */}
        <div className="bg-white rounded-lg shadow-sm mb-8">
          <nav className="flex space-x-8 px-6">
            {[
              { id: "executive", label: "Executive Summary" },
              { id: "technical", label: "Technical Analysis" },
              { id: "impact", label: "Impact Assessment" },
            ].map(({ id, label }) => (
              <button
                key={id}
                onClick={() => setReportType(id)}
                className={`py-4 px-2 border-b-2 font-medium text-sm ${
                  reportType === id
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700"
                }`}
              >
                {label}
              </button>
            ))}
          </nav>
        </div>
        {/* Report Content */}
        {reportType === "executive" && <ExecutiveReport />}
        {reportType === "technical" && <TechnicalReport />}
        {reportType === "impact" && <ExecutiveReport />}{" "}
        {/* Reusing for demo */}
      </div>
    </div>
  );
};

export default AdvancedAnalytics;
