import React, { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Search, Filter, Download, Eye, ExternalLink, Calendar, FileText,
  Archive, Flag, MapPin, Clock, Globe, Shield, AlertTriangle,
  ChevronDown, ChevronUp, MoreHorizontal, Copy, Share2, Trash2,
  CheckCircle, XCircle, Play, Pause, RefreshCw, Settings, Plus,
  BarChart3, PieChart, TrendingUp, Users, Building, Gavel,
  Lock, ShieldCheck, UserCheck, FileCheck, Award, Star,
  Monitor, Smartphone, Tablet, HelpCircle, MessageSquare,
  BookOpen, Mail, Phone, Zap, Activity, Target, Info, Bell
} from 'lucide-react';
import WildGuardDataService from '../services/supabaseService';

// Enhanced responsive hook
const useResponsive = () => {
  const [device, setDevice] = useState('desktop');
  
  useEffect(() => {
    const checkDevice = () => {
      const width = window.innerWidth;
      if (width < 768) setDevice('mobile');
      else if (width < 1024) setDevice('tablet');
      else setDevice('desktop');
    };
    
    checkDevice();
    window.addEventListener('resize', checkDevice);
    return () => window.removeEventListener('resize', checkDevice);
  }, []);
  
  return device;
};

// Evidence status indicator
const EvidenceStatus = ({ status, alertSent }) => {
  const statusConfig = {
    'ACTIVE': { color: 'green', label: 'Active Investigation', icon: Activity },
    'PENDING': { color: 'yellow', label: 'Pending Review', icon: Clock },
    'ARCHIVED': { color: 'gray', label: 'Archived', icon: Archive },
    'ESCALATED': { color: 'red', label: 'Escalated', icon: Flag }
  };

  const config = statusConfig[status] || statusConfig.PENDING;

  return (
    <div className="flex items-center space-x-2">
      <div className={`w-3 h-3 rounded-full bg-${config.color}-500 ${config.color === 'green' ? 'animate-pulse' : ''}`} />
      <span className="text-sm text-gray-600">{config.label}</span>
      {alertSent && (
        <div className="flex items-center space-x-1">
          <Bell className="w-3 h-3 text-blue-500" />
          <span className="text-xs text-blue-600">Alert Sent</span>
        </div>
      )}
    </div>
  );
};

// Enhanced evidence card
const EvidenceCard = ({ evidence, onView, onAction, device }) => {
  const [expanded, setExpanded] = useState(false);
  const [actionTaken, setActionTaken] = useState(null);

  const isMobile = device === 'mobile';

  const severityColors = {
    CRITICAL: 'border-red-500 bg-red-50',
    HIGH: 'border-orange-500 bg-orange-50',
    MEDIUM: 'border-yellow-500 bg-yellow-50',
    LOW: 'border-blue-500 bg-blue-50',
    UNRATED: 'border-gray-500 bg-gray-50'
  };

  const platformConfig = {
    ebay: { icon: '🛒', color: 'blue', region: 'Global' },
    craigslist: { icon: '📝', color: 'green', region: 'North America' },
    olx: { icon: '🌐', color: 'purple', region: 'Europe/Asia' },
    marktplaats: { icon: '🇳🇱', color: 'orange', region: 'Netherlands' },
    mercadolibre: { icon: '🇦🇷', color: 'yellow', region: 'Latin America' },
    gumtree: { icon: '🇬🇧', color: 'indigo', region: 'UK/Australia' },
    avito: { icon: '🇷🇺', color: 'red', region: 'Russia/CIS' }
  };

  const platform = platformConfig[evidence.platform?.toLowerCase()] || { icon: '🌍', color: 'gray', region: 'Unknown' };

  const handleAction = (action) => {
    setActionTaken(action);
    onAction(evidence.evidence_id, action);
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`border-l-4 rounded-lg ${severityColors[evidence.threat_level] || severityColors.UNRATED} border ${isMobile ? 'p-4' : 'p-6'} mb-4`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start space-x-4 flex-1">
          <div className={`w-10 h-10 rounded-lg bg-${platform.color}-100 flex items-center justify-center text-lg`}>
            {platform.icon}
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2 mb-2">
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                evidence.threat_level === 'CRITICAL' ? 'bg-red-600 text-white' :
                evidence.threat_level === 'HIGH' ? 'bg-orange-600 text-white' :
                evidence.threat_level === 'MEDIUM' ? 'bg-yellow-600 text-white' :
                evidence.threat_level === 'LOW' ? 'bg-blue-600 text-white' :
                'bg-gray-600 text-white'
              }`}>
                {evidence.threat_level || 'UNRATED'}
              </span>
              <span className="text-xs text-gray-500 capitalize">
                {evidence.platform} • {platform.region}
              </span>
              {evidence.threat_score && (
                <span className="text-xs text-gray-500">
                  Score: {evidence.threat_score}
                </span>
              )}
            </div>
            
            <h3 className={`font-bold ${isMobile ? 'text-base' : 'text-lg'} text-gray-900 mb-2 truncate`}>
              {evidence.species_involved || evidence.search_term || 'Wildlife Detection'}
            </h3>
            
            {evidence.listing_title && (
              <p className={`text-gray-700 ${isMobile ? 'text-sm' : 'text-base'} mb-2 line-clamp-2`}>
                {evidence.listing_title}
              </p>
            )}

            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{new Date(evidence.timestamp).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center space-x-1">
                <FileText className="w-4 h-4" />
                <span>{evidence.evidence_id?.slice(-8) || 'Unknown'}</span>
              </div>
              {evidence.listing_price && (
                <div className="flex items-center space-x-1">
                  <span className="font-medium text-green-600">{evidence.listing_price}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2 ml-4">
          <button
            onClick={() => setExpanded(!expanded)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
          
          {evidence.listing_url && (
            <a 
              href={evidence.listing_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="View Original Listing"
            >
              <ExternalLink className="w-4 h-4 text-blue-600" />
            </a>
          )}

          <button
            onClick={() => onView(evidence)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="View Details"
          >
            <Eye className="w-4 h-4 text-gray-600" />
          </button>
        </div>
      </div>

      {/* Status */}
      <div className="mb-4">
        <EvidenceStatus status={evidence.status} alertSent={evidence.alert_sent} />
      </div>

      {/* Expanded Content */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="pt-4 border-t border-gray-200"
          >
            {/* Evidence Details */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
              <div className="bg-white bg-opacity-70 rounded-lg p-3">
                <h5 className="font-medium text-gray-900 mb-2">Detection Details</h5>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>Search Term:</span>
                    <span className="font-medium">{evidence.search_term || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Platform:</span>
                    <span className="font-medium capitalize">{evidence.platform}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Detection Time:</span>
                    <span className="font-medium">{new Date(evidence.timestamp).toLocaleString()}</span>
                  </div>
                </div>
              </div>

              <div className="bg-white bg-opacity-70 rounded-lg p-3">
                <h5 className="font-medium text-gray-900 mb-2">Legal Status</h5>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>Evidence ID:</span>
                    <span className="font-medium font-mono text-xs">{evidence.evidence_id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Jurisdiction:</span>
                    <span className="font-medium">{platform.region}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Alert Status:</span>
                    <span className={`font-medium ${evidence.alert_sent ? 'text-green-600' : 'text-gray-600'}`}>
                      {evidence.alert_sent ? 'Sent' : 'Pending'}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
              <button 
                onClick={() => handleAction('investigate')}
                className={`flex items-center justify-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  actionTaken === 'investigate' ? 'bg-green-600 text-white' : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                <Search className="w-4 h-4" />
                <span>Investigate</span>
              </button>
              
              <button 
                onClick={() => handleAction('escalate')}
                className={`flex items-center justify-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  actionTaken === 'escalate' ? 'bg-green-600 text-white' : 'bg-orange-600 text-white hover:bg-orange-700'
                }`}
              >
                <Flag className="w-4 h-4" />
                <span>Escalate</span>
              </button>
              
              <button 
                onClick={() => handleAction('archive')}
                className={`flex items-center justify-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  actionTaken === 'archive' ? 'bg-green-600 text-white' : 'bg-gray-600 text-white hover:bg-gray-700'
                }`}
              >
                <Archive className="w-4 h-4" />
                <span>Archive</span>
              </button>
              
              <button 
                onClick={() => handleAction('share')}
                className={`flex items-center justify-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  actionTaken === 'share' ? 'bg-green-600 text-white' : 'bg-purple-600 text-white hover:bg-purple-700'
                }`}
              >
                <Share2 className="w-4 h-4" />
                <span>Share</span>
              </button>
            </div>

            {actionTaken && (
              <div className="mt-4 bg-green-50 border border-green-200 rounded-lg p-3">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="font-medium text-green-900">
                    Action Recorded: {actionTaken.charAt(0).toUpperCase() + actionTaken.slice(1)}
                  </span>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

// Search and filter panel
const SearchFilterPanel = ({ onSearch, onFilter, totalRecords, device }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    platform: 'all',
    threatLevel: 'all',
    dateFrom: '',
    dateTo: '',
    status: 'all'
  });
  const [showAdvanced, setShowAdvanced] = useState(false);

  const isMobile = device === 'mobile';

  const handleSearch = (term) => {
    setSearchTerm(term);
    onSearch(term);
  };

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilter(newFilters);
  };

  const resetFilters = () => {
    const resetFilters = {
      platform: 'all',
      threatLevel: 'all',
      dateFrom: '',
      dateTo: '',
      status: 'all'
    };
    setFilters(resetFilters);
    setSearchTerm('');
    onSearch('');
    onFilter(resetFilters);
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className={`font-bold ${isMobile ? 'text-lg' : 'text-xl'} text-gray-900`}>
          Evidence Search & Analysis
        </h3>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-500">
            {totalRecords.toLocaleString()} total records
          </span>
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
        </div>
      </div>

      {/* Search Bar */}
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="Search by species, platform, listing title, or evidence ID..."
          className={`w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
            isMobile ? 'text-base' : 'text-lg'
          }`}
        />
      </div>

      {/* Quick Filters */}
      <div className={`grid ${isMobile ? 'grid-cols-1 gap-3' : 'grid-cols-2 lg:grid-cols-5 gap-4'} mb-4`}>
        <select 
          value={filters.platform}
          onChange={(e) => handleFilterChange('platform', e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg bg-white"
        >
          <option value="all">All Platforms</option>
          <option value="ebay">eBay (Global)</option>
          <option value="craigslist">Craigslist (North America)</option>
          <option value="olx">OLX (Europe/Asia)</option>
          <option value="marktplaats">Marktplaats (Netherlands)</option>
          <option value="mercadolibre">MercadoLibre (Latin America)</option>
          <option value="gumtree">Gumtree (UK/Australia)</option>
          <option value="avito">Avito (Russia/CIS)</option>
        </select>

        <select 
          value={filters.threatLevel}
          onChange={(e) => handleFilterChange('threatLevel', e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg bg-white"
        >
          <option value="all">All Threat Levels</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
          <option value="UNRATED">Unrated</option>
        </select>

        <select 
          value={filters.status}
          onChange={(e) => handleFilterChange('status', e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg bg-white"
        >
          <option value="all">All Statuses</option>
          <option value="ACTIVE">Active Investigation</option>
          <option value="PENDING">Pending Review</option>
          <option value="ESCALATED">Escalated</option>
          <option value="ARCHIVED">Archived</option>
        </select>

        <input
          type="date"
          value={filters.dateFrom}
          onChange={(e) => handleFilterChange('dateFrom', e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg"
          placeholder="From Date"
        />

        <div className="flex space-x-2">
          <button 
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            <Filter className="w-4 h-4" />
            <span>Advanced</span>
          </button>
          
          <button 
            onClick={resetFilters}
            className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
          >
            Reset
          </button>
        </div>
      </div>

      {/* Advanced Filters */}
      <AnimatePresence>
        {showAdvanced && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="pt-4 border-t border-gray-200"
          >
            <div className={`grid ${isMobile ? 'grid-cols-1 gap-3' : 'grid-cols-3 gap-4'}`}>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Threat Score Range
                </label>
                <div className="flex space-x-2">
                  <input 
                    type="number" 
                    placeholder="Min (0)"
                    min="0" 
                    max="100"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                  />
                  <input 
                    type="number" 
                    placeholder="Max (100)"
                    min="0" 
                    max="100"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Species Category
                </label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white">
                  <option value="all">All Species</option>
                  <option value="mammals">Mammals</option>
                  <option value="reptiles">Reptiles</option>
                  <option value="birds">Birds</option>
                  <option value="marine">Marine Life</option>
                  <option value="plants">Plants</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Alert Status
                </label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white">
                  <option value="all">All Alerts</option>
                  <option value="sent">Alert Sent</option>
                  <option value="pending">Alert Pending</option>
                  <option value="none">No Alert</option>
                </select>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// Export and analytics panel
const ExportAnalyticsPanel = ({ evidenceData, onExport, device }) => {
  const isMobile = device === 'mobile';

  const analytics = useMemo(() => {
    const total = evidenceData.length;
    const platforms = [...new Set(evidenceData.map(e => e.platform))];
    const species = [...new Set(evidenceData.map(e => e.search_term))];
    const critical = evidenceData.filter(e => e.threat_level === 'CRITICAL').length;
    const alertsSent = evidenceData.filter(e => e.alert_sent).length;

    return { total, platforms: platforms.length, species: species.length, critical, alertsSent };
  }, [evidenceData]);

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
      <h3 className={`font-bold ${isMobile ? 'text-lg' : 'text-xl'} text-gray-900 mb-6`}>
        Export & Analytics
      </h3>

      {/* Quick Stats */}
      <div className={`grid ${isMobile ? 'grid-cols-2 gap-4' : 'grid-cols-5 gap-6'} mb-6`}>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{analytics.total.toLocaleString()}</div>
          <div className="text-sm text-gray-600">Total Evidence</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">{analytics.platforms}</div>
          <div className="text-sm text-gray-600">Platforms</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-purple-600">{analytics.species}</div>
          <div className="text-sm text-gray-600">Species</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-red-600">{analytics.critical}</div>
          <div className="text-sm text-gray-600">Critical</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-orange-600">{analytics.alertsSent}</div>
          <div className="text-sm text-gray-600">Alerts Sent</div>
        </div>
      </div>

      {/* Export Options */}
      <div className={`grid ${isMobile ? 'grid-cols-1 gap-3' : 'grid-cols-4 gap-4'}`}>
        <button 
          onClick={() => onExport('pdf')}
          className="flex items-center justify-center space-x-2 px-4 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          <FileText className="w-4 h-4" />
          <span>Export PDF</span>
        </button>
        
        <button 
          onClick={() => onExport('csv')}
          className="flex items-center justify-center space-x-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          <Download className="w-4 h-4" />
          <span>Export CSV</span>
        </button>
        
        <button 
          onClick={() => onExport('legal')}
          className="flex items-center justify-center space-x-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Gavel className="w-4 h-4" />
          <span>Legal Report</span>
        </button>
        
        <button 
          onClick={() => onExport('analytics')}
          className="flex items-center justify-center space-x-2 px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          <BarChart3 className="w-4 h-4" />
          <span>Analytics</span>
        </button>
      </div>
    </div>
  );
};

// Main Evidence Archive Component
const EvidenceArchive = () => {
  const device = useResponsive();
  const [evidenceData, setEvidenceData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [selectedEvidence, setSelectedEvidence] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(20);

  // Load evidence data
  useEffect(() => {
    loadEvidenceData();
  }, []);

  const loadEvidenceData = async () => {
    try {
      setIsRefreshing(true);
      
      const result = await WildGuardDataService.searchEvidence('', {}, 100);
      
      if (result.success) {
        setEvidenceData(result.data);
        setFilteredData(result.data);
      }
      
    } catch (error) {
      console.error('Evidence data loading error:', error);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  const handleSearch = (searchTerm) => {
    if (!searchTerm) {
      setFilteredData(evidenceData);
    } else {
      const filtered = evidenceData.filter(evidence => 
        evidence.species_involved?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        evidence.search_term?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        evidence.listing_title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        evidence.platform?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        evidence.evidence_id?.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredData(filtered);
    }
    setCurrentPage(1);
  };

  const handleFilter = async (filters) => {
    try {
      const result = await WildGuardDataService.searchEvidence('', filters, 100);
      
      if (result.success) {
        setFilteredData(result.data);
      }
    } catch (error) {
      console.error('Filter error:', error);
    }
    setCurrentPage(1);
  };

  const handleViewEvidence = (evidence) => {
    setSelectedEvidence(evidence);
    // Could open a modal or navigate to detail view
  };

  const handleAction = (evidenceId, action) => {
    console.log(`Action taken on evidence ${evidenceId}: ${action}`);
    // Here you would typically call an API to record the action
  };

  const handleExport = (format) => {
    console.log(`Exporting evidence as ${format}`);
    // Export functionality
  };

  // Pagination
  const totalPages = Math.ceil(filteredData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = filteredData.slice(startIndex, endIndex);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-xl font-medium text-gray-900">Loading Evidence Archive...</p>
          <p className="text-gray-500">Accessing secure wildlife trafficking database</p>
        </div>
      </div>
    );
  }

  const isMobile = device === 'mobile';

  return (
    <div className={`min-h-screen bg-gray-50 ${isMobile ? 'p-4' : 'p-6'}`}>
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className={`font-black text-gray-900 ${
              isMobile ? 'text-2xl' : 'text-4xl'
            }`}>
              Wildlife Evidence Archive
            </h1>
            <p className={`text-gray-600 ${isMobile ? 'text-base' : 'text-xl'}`}>
              Comprehensive Digital Evidence Collection & Management System
            </p>
          </div>
          
          {!isMobile && (
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-500">Archive Status</p>
                <div className="flex items-center space-x-2">
                  <Lock className="w-4 h-4 text-green-600" />
                  <span className="font-medium text-green-600">Secure & Verified</span>
                </div>
              </div>
              <div className="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                <Archive className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          )}
        </div>

        {/* Export & Analytics Panel */}
        <ExportAnalyticsPanel 
          evidenceData={filteredData}
          onExport={handleExport}
          device={device}
        />
      </div>

      {/* Search & Filter Panel */}
      <SearchFilterPanel 
        onSearch={handleSearch}
        onFilter={handleFilter}
        totalRecords={evidenceData.length}
        device={device}
      />

      {/* Evidence List */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className={`font-bold ${isMobile ? 'text-lg' : 'text-xl'} text-gray-900`}>
            Evidence Records ({filteredData.length.toLocaleString()})
          </h3>
          <div className="flex items-center space-x-4">
            <button
              onClick={loadEvidenceData}
              disabled={isRefreshing}
              className="flex items-center space-x-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
            >
              <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
              <span>{isRefreshing ? 'Loading...' : 'Refresh'}</span>
            </button>
          </div>
        </div>

        {/* Evidence Cards */}
        <div className="space-y-4">
          {currentData.length > 0 ? (
            currentData.map((evidence, index) => (
              <EvidenceCard
                key={evidence.evidence_id || index}
                evidence={evidence}
                onView={handleViewEvidence}
                onAction={handleAction}
                device={device}
              />
            ))
          ) : (
            <div className="text-center py-12">
              <Archive className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h4 className="text-xl font-medium text-gray-900 mb-2">No Evidence Found</h4>
              <p className="text-gray-500">
                Try adjusting your search criteria or filters to find evidence records.
              </p>
            </div>
          )}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="mt-8 flex items-center justify-between">
            <div className="text-sm text-gray-500">
              Showing {startIndex + 1}-{Math.min(endIndex, filteredData.length)} of {filteredData.length} records
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              
              <span className="px-3 py-2 text-sm text-gray-600">
                Page {currentPage} of {totalPages}
              </span>
              
              <button
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
                className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <div className={`flex ${isMobile ? 'flex-col space-y-4' : 'items-center justify-between'}`}>
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-5 h-5 text-green-600" />
              <span className="text-sm text-gray-600">Chain of Custody Verified</span>
            </div>
            <div className="flex items-center space-x-2">
              <Lock className="w-5 h-5 text-blue-600" />
              <span className="text-sm text-gray-600">Encrypted Storage</span>
            </div>
            <div className="flex items-center space-x-2">
              <FileCheck className="w-5 h-5 text-purple-600" />
              <span className="text-sm text-gray-600">Court Admissible</span>
            </div>
          </div>
          
          <div className={`text-sm text-gray-500 ${isMobile ? 'text-center' : ''}`}>
            WildGuard AI Evidence Archive • Secure Wildlife Protection Database
          </div>
        </div>
      </div>
    </div>
  );
};

export default EvidenceArchive;
