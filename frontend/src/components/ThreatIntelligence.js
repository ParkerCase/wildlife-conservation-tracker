import React, { useState, useEffect } from 'react';
import { 
  AlertTriangle, 
  Shield, 
  Clock, 
  ExternalLink, 
  Eye, 
  Filter,
  Download,
  Search,
  MapPin,
  Calendar
} from 'lucide-react';
import WildGuardDataService from '../services/supabaseService';

const ThreatIntelligence = () => {
  const [alerts, setAlerts] = useState([]);
  const [filteredAlerts, setFilteredAlerts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [filters, setFilters] = useState({
    severity: '',
    platform: '',
    dateRange: '7d',
    searchTerm: ''
  });
  const [platforms, setPlatforms] = useState([]);

  useEffect(() => {
    loadAlertsData();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [alerts, filters]);

  const loadAlertsData = async () => {
    setIsLoading(true);
    try {
      const result = await WildGuardDataService.getRecentAlerts(100);
      if (result.success) {
        setAlerts(result.data);
        
        // Extract unique platforms for filter dropdown
        const uniquePlatforms = [...new Set(result.data.map(alert => alert.platform).filter(Boolean))];
        setPlatforms(uniquePlatforms);
      }
    } catch (error) {
      console.error('Error loading alerts:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...alerts];

    // Filter by severity
    if (filters.severity) {
      filtered = filtered.filter(alert => alert.severity === filters.severity);
    }

    // Filter by platform
    if (filters.platform) {
      filtered = filtered.filter(alert => alert.platform === filters.platform);
    }

    // Filter by search term
    if (filters.searchTerm) {
      const searchLower = filters.searchTerm.toLowerCase();
      filtered = filtered.filter(alert => 
        alert.threat?.toLowerCase().includes(searchLower) ||
        alert.listingTitle?.toLowerCase().includes(searchLower) ||
        alert.id?.toLowerCase().includes(searchLower)
      );
    }

    // Filter by date range
    if (filters.dateRange !== 'all') {
      const days = parseInt(filters.dateRange.replace('d', ''));
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - days);
      
      filtered = filtered.filter(alert => {
        const alertDate = new Date(alert.timestamp);
        return alertDate >= cutoffDate;
      });
    }

    setFilteredAlerts(filtered);
  };

  const handleAlertClick = async (alert) => {
    setSelectedAlert(alert);
    
    // If we have more detailed data available, fetch it
    try {
      const result = await WildGuardDataService.getDetectionDetails(alert.id);
      if (result.success) {
        setSelectedAlert(result.data);
      }
    } catch (error) {
      console.error('Error fetching alert details:', error);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'CRITICAL': return 'bg-red-100 text-red-800 border-red-200';
      case 'HIGH': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const exportAlerts = () => {
    const csvContent = [
      ['Alert ID', 'Timestamp', 'Threat', 'Platform', 'Severity', 'Score', 'Listing URL'],
      ...filteredAlerts.map(alert => [
        alert.id,
        alert.timestamp,
        alert.threat,
        alert.platform,
        alert.severity,
        alert.threatScore,
        alert.listingUrl
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `wildguard-alerts-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">Loading real threat intelligence...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Stats */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">🚨 Threat Intelligence Center</h2>
            <p className="text-gray-600 mt-1">Real-time analysis of {alerts.length} threat detections</p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-red-600">
                {alerts.filter(a => a.severity === 'CRITICAL').length}
              </p>
              <p className="text-sm text-gray-600">Critical</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-orange-600">
                {alerts.filter(a => a.severity === 'HIGH').length}
              </p>
              <p className="text-sm text-gray-600">High</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-600">
                {alerts.filter(a => a.severity === 'MEDIUM').length}
              </p>
              <p className="text-sm text-gray-600">Medium</p>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
          <div className="relative">
            <Search size={16} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search threats..."
              value={filters.searchTerm}
              onChange={(e) => setFilters(prev => ({ ...prev, searchTerm: e.target.value }))}
              className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <select
            value={filters.severity}
            onChange={(e) => setFilters(prev => ({ ...prev, severity: e.target.value }))}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
          </select>

          <select
            value={filters.platform}
            onChange={(e) => setFilters(prev => ({ ...prev, platform: e.target.value }))}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Platforms</option>
            {platforms.map(platform => (
              <option key={platform} value={platform}>{platform}</option>
            ))}
          </select>

          <select
            value={filters.dateRange}
            onChange={(e) => setFilters(prev => ({ ...prev, dateRange: e.target.value }))}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="1d">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="all">All Time</option>
          </select>

          <button
            onClick={exportAlerts}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center justify-center"
          >
            <Download size={16} className="mr-2" />
            Export
          </button>
        </div>

        <div className="text-sm text-gray-600">
          Showing {filteredAlerts.length} of {alerts.length} total alerts
        </div>
      </div>

      {/* Alerts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredAlerts.map((alert, index) => (
          <div
            key={alert.id || index}
            className="bg-white rounded-xl shadow-lg border-l-4 hover:shadow-xl transition-shadow cursor-pointer"
            style={{
              borderLeftColor: 
                alert.severity === 'CRITICAL' ? '#ef4444' :
                alert.severity === 'HIGH' ? '#f97316' :
                alert.severity === 'MEDIUM' ? '#eab308' : '#3b82f6'
            }}
            onClick={() => handleAlertClick(alert)}
          >
            <div className="p-6">
              {/* Header */}
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center">
                  <AlertTriangle size={20} className="text-red-500 mr-2" />
                  <span className="font-mono text-sm text-gray-600">
                    {alert.id?.substring(0, 20)}...
                  </span>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getSeverityColor(alert.severity)}`}>
                  {alert.severity}
                </span>
              </div>

              {/* Threat Details */}
              <h3 className="font-semibold text-gray-900 mb-2">
                {alert.threat || 'Threat Detection'}
              </h3>

              <div className="space-y-2 text-sm text-gray-600 mb-4">
                <div className="flex items-center">
                  <MapPin size={14} className="mr-2" />
                  <span className="capitalize">{alert.platform}</span>
                </div>
                <div className="flex items-center">
                  <Clock size={14} className="mr-2" />
                  <span>{alert.timestamp}</span>
                </div>
                {alert.threatScore && (
                  <div className="flex items-center">
                    <Shield size={14} className="mr-2" />
                    <span>Score: {alert.threatScore}</span>
                  </div>
                )}
              </div>

              {/* Listing Info */}
              {alert.listingTitle && (
                <div className="mb-4">
                  <p className="text-sm font-medium text-gray-900 mb-1">Listing:</p>
                  <p className="text-sm text-gray-600 line-clamp-2">
                    {alert.listingTitle}
                  </p>
                  {alert.listingPrice && (
                    <p className="text-sm font-semibold text-green-600 mt-1">
                      ${alert.listingPrice}
                    </p>
                  )}
                </div>
              )}

              {/* Actions */}
              <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-100">
                <div className="flex items-center space-x-2">
                  {alert.alertSent && (
                    <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                      Alert Sent
                    </span>
                  )}
                </div>
                
                <div className="flex space-x-2">
                  {alert.listingUrl && (
                    <a
                      href={alert.listingUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="text-blue-600 hover:text-blue-800 flex items-center text-sm"
                    >
                      <ExternalLink size={14} className="mr-1" />
                      View
                    </a>
                  )}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleAlertClick(alert);
                    }}
                    className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
                  >
                    <Eye size={14} className="mr-1" />
                    Details
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredAlerts.length === 0 && (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <AlertTriangle size={48} className="text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Threats Found</h3>
          <p className="text-gray-600">
            {filters.severity || filters.platform || filters.searchTerm
              ? 'Try adjusting your filters to see more results.'
              : 'No threat detections match your current criteria.'}
          </p>
        </div>
      )}

      {/* Alert Details Modal */}
      {selectedAlert && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-bold text-gray-900">Threat Details</h3>
                <button
                  onClick={() => setSelectedAlert(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Alert ID</label>
                    <p className="font-mono text-sm">{selectedAlert.id}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Severity</label>
                    <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(selectedAlert.severity)}`}>
                      {selectedAlert.severity}
                    </span>
                  </div>
                </div>

                <div>
                  <label className="text-sm font-medium text-gray-700">Threat Description</label>
                  <p className="text-gray-900">{selectedAlert.threat}</p>
                </div>

                {selectedAlert.listingTitle && (
                  <div>
                    <label className="text-sm font-medium text-gray-700">Listing Title</label>
                    <p className="text-gray-900">{selectedAlert.listingTitle}</p>
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Platform</label>
                    <p className="capitalize">{selectedAlert.platform}</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-gray-700">Detection Time</label>
                    <p>{selectedAlert.timestamp}</p>
                  </div>
                </div>

                {selectedAlert.listingUrl && (
                  <div>
                    <label className="text-sm font-medium text-gray-700">Original Listing</label>
                    <a
                      href={selectedAlert.listingUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 flex items-center"
                    >
                      View Original Listing <ExternalLink size={16} className="ml-2" />
                    </a>
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  {selectedAlert.threatScore && (
                    <div>
                      <label className="text-sm font-medium text-gray-700">Threat Score</label>
                      <p className="text-2xl font-bold text-red-600">{selectedAlert.threatScore}</p>
                    </div>
                  )}
                  {selectedAlert.listingPrice && (
                    <div>
                      <label className="text-sm font-medium text-gray-700">Listing Price</label>
                      <p className="text-2xl font-bold text-green-600">${selectedAlert.listingPrice}</p>
                    </div>
                  )}
                </div>

                <div className="bg-gray-50 p-4 rounded-lg">
                  <label className="text-sm font-medium text-gray-700">Status</label>
                  <div className="flex items-center space-x-4 mt-2">
                    <span className={`px-3 py-1 rounded-full text-sm ${
                      selectedAlert.alertSent 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {selectedAlert.alertSent ? 'Alert Sent' : 'Pending Review'}
                    </span>
                    <span className="text-sm text-gray-600">
                      {selectedAlert.status}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ThreatIntelligence;
