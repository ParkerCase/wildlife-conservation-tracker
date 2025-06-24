import React, { useState, useEffect } from 'react';
import {
  Search,
  Filter,
  Download,
  Eye,
  ExternalLink,
  Calendar,
  MapPin,
  AlertTriangle,
  Shield,
  Database,
  FileText,
  Image,
  Link,
  Clock
} from 'lucide-react';
import WildGuardDataService from '../services/supabaseService';

const EvidenceArchive = () => {
  const [evidence, setEvidence] = useState([]);
  const [filteredEvidence, setFilteredEvidence] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    platform: '',
    threatLevel: '',
    dateFrom: '',
    dateTo: '',
    hasUrl: false,
    alertSent: false
  });
  const [platforms, setPlatforms] = useState([]);
  const [stats, setStats] = useState({});

  useEffect(() => {
    loadEvidenceData();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [evidence, filters, searchTerm]);

  const loadEvidenceData = async () => {
    setIsLoading(true);
    try {
      // Load recent evidence with comprehensive data
      const result = await WildGuardDataService.searchEvidence('', {}, 200);
      
      if (result.success) {
        setEvidence(result.data);
        
        // Extract unique platforms
        const uniquePlatforms = [...new Set(result.data.map(item => item.platform).filter(Boolean))];
        setPlatforms(uniquePlatforms);
        
        // Calculate stats
        calculateStats(result.data);
      }
    } catch (error) {
      console.error('Error loading evidence:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const calculateStats = (data) => {
    const stats = {
      total: data.length,
      withUrls: data.filter(item => item.listing_url).length,
      highThreat: data.filter(item => ['HIGH', 'CRITICAL'].includes(item.threat_level)).length,
      alertsSent: data.filter(item => item.alert_sent).length,
      platforms: [...new Set(data.map(item => item.platform).filter(Boolean))].length,
      avgThreatScore: data.reduce((sum, item) => sum + (item.threat_score || 0), 0) / data.length
    };
    setStats(stats);
  };

  const applyFilters = () => {
    let filtered = [...evidence];

    // Text search
    if (searchTerm.trim()) {
      const searchLower = searchTerm.toLowerCase();
      filtered = filtered.filter(item =>
        item.listing_title?.toLowerCase().includes(searchLower) ||
        item.search_term?.toLowerCase().includes(searchLower) ||
        item.species_involved?.toLowerCase().includes(searchLower) ||
        item.evidence_id?.toLowerCase().includes(searchLower)
      );
    }

    // Platform filter
    if (filters.platform) {
      filtered = filtered.filter(item => item.platform === filters.platform);
    }

    // Threat level filter
    if (filters.threatLevel) {
      filtered = filtered.filter(item => item.threat_level === filters.threatLevel);
    }

    // Date filters
    if (filters.dateFrom) {
      filtered = filtered.filter(item => 
        new Date(item.timestamp) >= new Date(filters.dateFrom)
      );
    }

    if (filters.dateTo) {
      filtered = filtered.filter(item => 
        new Date(item.timestamp) <= new Date(filters.dateTo + 'T23:59:59')
      );
    }

    // Has URL filter
    if (filters.hasUrl) {
      filtered = filtered.filter(item => item.listing_url);
    }

    // Alert sent filter
    if (filters.alertSent) {
      filtered = filtered.filter(item => item.alert_sent);
    }

    setFilteredEvidence(filtered);
  };

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const handleAdvancedSearch = async () => {
    if (!searchTerm.trim()) return;
    
    setIsLoading(true);
    try {
      const result = await WildGuardDataService.searchEvidence(searchTerm, filters, 100);
      if (result.success) {
        setFilteredEvidence(result.data);
      }
    } catch (error) {
      console.error('Error performing advanced search:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const exportEvidence = () => {
    const csvContent = [
      [
        'Evidence ID', 'Timestamp', 'Platform', 'Threat Level', 'Threat Score',
        'Species', 'Listing Title', 'Listing Price', 'Listing URL', 'Alert Sent', 'Status'
      ],
      ...filteredEvidence.map(item => [
        item.evidence_id,
        item.timestamp,
        item.platform,
        item.threat_level,
        item.threat_score,
        item.search_term,
        item.listing_title,
        item.listing_price,
        item.listing_url,
        item.alert_sent,
        item.status
      ])
    ].map(row => row.map(cell => `"${cell || ''}"`).join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `wildguard-evidence-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const getSeverityColor = (level) => {
    switch (level) {
      case 'CRITICAL': return 'bg-red-100 text-red-800 border-red-200';
      case 'HIGH': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (isLoading && evidence.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-600">Loading evidence archive from Supabase...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header with Statistics */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 flex items-center">
              <Database size={28} className="text-blue-600 mr-3" />
              Evidence Archive
            </h2>
            <p className="text-gray-600 mt-1">
              Comprehensive database of {stats.total?.toLocaleString() || 0} wildlife trafficking detections
            </p>
          </div>
          
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-blue-600">{stats.total?.toLocaleString() || 0}</p>
              <p className="text-sm text-gray-600">Total Records</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-red-600">{stats.highThreat || 0}</p>
              <p className="text-sm text-gray-600">High Threat</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-green-600">{stats.withUrls || 0}</p>
              <p className="text-sm text-gray-600">With URLs</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-purple-600">{stats.platforms || 0}</p>
              <p className="text-sm text-gray-600">Platforms</p>
            </div>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="space-y-4">
          <div className="flex flex-col lg:flex-row gap-4">
            <div className="flex-1 relative">
              <Search size={20} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search evidence... (listing titles, species, evidence IDs)"
                value={searchTerm}
                onChange={(e) => handleSearch(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAdvancedSearch()}
                className="pl-10 pr-4 py-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={handleAdvancedSearch}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center"
            >
              <Search size={16} className="mr-2" />
              Search
            </button>
            <button
              onClick={exportEvidence}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center"
            >
              <Download size={16} className="mr-2" />
              Export
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-4">
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
              value={filters.threatLevel}
              onChange={(e) => setFilters(prev => ({ ...prev, threatLevel: e.target.value }))}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Threat Levels</option>
              <option value="CRITICAL">Critical</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
              <option value="UNRATED">Unrated</option>
            </select>

            <input
              type="date"
              value={filters.dateFrom}
              onChange={(e) => setFilters(prev => ({ ...prev, dateFrom: e.target.value }))}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="From Date"
            />

            <input
              type="date"
              value={filters.dateTo}
              onChange={(e) => setFilters(prev => ({ ...prev, dateTo: e.target.value }))}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="To Date"
            />

            <label className="flex items-center px-3 py-2 border border-gray-300 rounded-lg">
              <input
                type="checkbox"
                checked={filters.hasUrl}
                onChange={(e) => setFilters(prev => ({ ...prev, hasUrl: e.target.checked }))}
                className="mr-2"
              />
              <span className="text-sm">Has URL</span>
            </label>

            <label className="flex items-center px-3 py-2 border border-gray-300 rounded-lg">
              <input
                type="checkbox"
                checked={filters.alertSent}
                onChange={(e) => setFilters(prev => ({ ...prev, alertSent: e.target.checked }))}
                className="mr-2"
              />
              <span className="text-sm">Alert Sent</span>
            </label>
          </div>

          <div className="text-sm text-gray-600">
            Showing {filteredEvidence.length.toLocaleString()} of {evidence.length.toLocaleString()} records
            {(filters.dateFrom || filters.dateTo) && ' (filtered by date)'}
          </div>
        </div>
      </div>

      {/* Evidence Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredEvidence.map((item, index) => (
          <div
            key={item.id || index}
            className="bg-white rounded-xl shadow-lg border hover:shadow-xl transition-shadow cursor-pointer"
            onClick={() => setSelectedEvidence(item)}
          >
            <div className="p-6">
              {/* Header */}
              <div className="flex justify-between items-start mb-4">
                <div className="flex items-center">
                  <FileText size={20} className="text-blue-500 mr-2" />
                  <span className="font-mono text-xs text-gray-600">
                    {item.evidence_id?.substring(0, 25)}...
                  </span>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getSeverityColor(item.threat_level)}`}>
                  {item.threat_level}
                </span>
              </div>

              {/* Content */}
              <div className="space-y-3">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-1">
                    {item.search_term || 'Detection'}
                  </h3>
                  {item.listing_title && (
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {item.listing_title}
                    </p>
                  )}
                </div>

                <div className="flex items-center justify-between text-sm text-gray-600">
                  <div className="flex items-center">
                    <MapPin size={14} className="mr-1" />
                    <span className="capitalize">{item.platform}</span>
                  </div>
                  {item.threat_score && (
                    <div className="flex items-center">
                      <Shield size={14} className="mr-1" />
                      <span>{item.threat_score}</span>
                    </div>
                  )}
                </div>

                <div className="flex items-center text-sm text-gray-600">
                  <Clock size={14} className="mr-1" />
                  <span>{formatDate(item.timestamp)}</span>
                </div>

                {item.listing_price && (
                  <div className="text-lg font-semibold text-green-600">
                    ${item.listing_price}
                  </div>
                )}

                {/* Status Indicators */}
                <div className="flex items-center space-x-2">
                  {item.listing_url && (
                    <span className="inline-flex items-center text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                      <Link size={10} className="mr-1" />
                      URL
                    </span>
                  )}
                  {item.alert_sent && (
                    <span className="inline-flex items-center text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                      <AlertTriangle size={10} className="mr-1" />
                      Alert Sent
                    </span>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-100">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedEvidence(item);
                  }}
                  className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
                >
                  <Eye size={14} className="mr-1" />
                  Details
                </button>
                
                {item.listing_url && (
                  <a
                    href={item.listing_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="text-blue-600 hover:text-blue-800 text-sm flex items-center"
                  >
                    <ExternalLink size={14} className="mr-1" />
                    View Original
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredEvidence.length === 0 && !isLoading && (
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <Database size={48} className="text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Evidence Found</h3>
          <p className="text-gray-600">
            {searchTerm || Object.values(filters).some(f => f)
              ? 'Try adjusting your search terms or filters to see more results.'
              : 'No evidence records available in the database.'}
          </p>
        </div>
      )}

      {/* Evidence Details Modal */}
      {selectedEvidence && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-6">
                <h3 className="text-xl font-bold text-gray-900">Evidence Details</h3>
                <button
                  onClick={() => setSelectedEvidence(null)}
                  className="text-gray-400 hover:text-gray-600 text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Left Column */}
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Evidence ID</label>
                    <p className="font-mono text-sm bg-gray-50 p-2 rounded">
                      {selectedEvidence.evidence_id}
                    </p>
                  </div>

                  <div>
                    <label className="text-sm font-medium text-gray-700">Detection Time</label>
                    <p className="text-gray-900">{formatDate(selectedEvidence.timestamp)}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-700">Platform</label>
                      <p className="capitalize">{selectedEvidence.platform}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-700">Threat Level</label>
                      <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getSeverityColor(selectedEvidence.threat_level)}`}>
                        {selectedEvidence.threat_level}
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-700">Threat Score</label>
                      <p className="text-2xl font-bold text-red-600">
                        {selectedEvidence.threat_score || 'N/A'}
                      </p>
                    </div>
                    {selectedEvidence.listing_price && (
                      <div>
                        <label className="text-sm font-medium text-gray-700">Listing Price</label>
                        <p className="text-2xl font-bold text-green-600">
                          ${selectedEvidence.listing_price}
                        </p>
                      </div>
                    )}
                  </div>

                  <div>
                    <label className="text-sm font-medium text-gray-700">Species/Search Term</label>
                    <p className="text-gray-900">{selectedEvidence.search_term}</p>
                  </div>

                  {selectedEvidence.species_involved && (
                    <div>
                      <label className="text-sm font-medium text-gray-700">Species Involved</label>
                      <p className="text-gray-900">{selectedEvidence.species_involved}</p>
                    </div>
                  )}
                </div>

                {/* Right Column */}
                <div className="space-y-4">
                  {selectedEvidence.listing_title && (
                    <div>
                      <label className="text-sm font-medium text-gray-700">Listing Title</label>
                      <p className="text-gray-900 bg-gray-50 p-3 rounded">
                        {selectedEvidence.listing_title}
                      </p>
                    </div>
                  )}

                  {selectedEvidence.listing_url && (
                    <div>
                      <label className="text-sm font-medium text-gray-700">Original Listing</label>
                      <a
                        href={selectedEvidence.listing_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:text-blue-800 flex items-center break-all"
                      >
                        View Original Listing <ExternalLink size={16} className="ml-2 flex-shrink-0" />
                      </a>
                    </div>
                  )}

                  <div>
                    <label className="text-sm font-medium text-gray-700">Status</label>
                    <div className="space-y-2">
                      <p className="text-gray-900">{selectedEvidence.status}</p>
                      <div className="flex space-x-2">
                        {selectedEvidence.alert_sent && (
                          <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">
                            Alert Sent
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-medium text-blue-900 mb-2">Detection Metadata</h4>
                    <div className="text-sm space-y-1">
                      <p><strong>Database ID:</strong> {selectedEvidence.id}</p>
                      <p><strong>Detection Type:</strong> {selectedEvidence.status}</p>
                      <p><strong>Data Source:</strong> Real Supabase Database</p>
                    </div>
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

export default EvidenceArchive;
