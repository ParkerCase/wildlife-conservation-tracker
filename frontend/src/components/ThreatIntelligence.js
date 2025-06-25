import React, { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  AlertTriangle, Shield, Eye, ExternalLink, Clock, MapPin, Globe,
  Filter, Download, Search, Calendar, FileText, Flag, Target,
  TrendingUp, BarChart3, Users, Building, Gavel, BookOpen,
  ChevronDown, ChevronUp, Play, Pause, RefreshCw, Settings,
  Bell, BellOff, Mail, Phone, Share2, Copy, Archive, Trash2,
  CheckCircle, XCircle, AlertCircle, Info, Zap, Activity,
  Monitor, Smartphone, Tablet, HelpCircle, MessageSquare,
  Lock, ShieldCheck, UserCheck, FileCheck, Award, Star
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

// Enhanced threat classification
const ThreatClassification = ({ threat, device }) => {
  const classifications = {
    'elephant ivory': { level: 'CRITICAL', category: 'CITES Appendix I', enforcement: 'Immediate', icon: '🐘' },
    'rhino horn': { level: 'CRITICAL', category: 'CITES Appendix I', enforcement: 'Immediate', icon: '🦏' },
    'tiger bone': { level: 'CRITICAL', category: 'CITES Appendix I', enforcement: 'Immediate', icon: '🐅' },
    'pangolin scales': { level: 'CRITICAL', category: 'CITES Appendix I', enforcement: 'Immediate', icon: '🦔' },
    'bear bile': { level: 'HIGH', category: 'CITES Appendix II', enforcement: 'Priority', icon: '🐻' },
    'leopard skin': { level: 'HIGH', category: 'CITES Appendix I', enforcement: 'Priority', icon: '🐆' },
    'shark fin': { level: 'HIGH', category: 'CITES Appendix II', enforcement: 'Priority', icon: '🦈' },
    'turtle shell': { level: 'MEDIUM', category: 'CITES Appendix II', enforcement: 'Monitor', icon: '🐢' },
    'coral': { level: 'MEDIUM', category: 'CITES Appendix II', enforcement: 'Monitor', icon: '🪸' }
  };

  const classification = classifications[threat?.toLowerCase()] || { 
    level: 'UNRATED', 
    category: 'Under Review', 
    enforcement: 'Monitor',
    icon: '🔍'
  };

  const levelColors = {
    CRITICAL: 'bg-red-100 text-red-800 border-red-300',
    HIGH: 'bg-orange-100 text-orange-800 border-orange-300',
    MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-300',
    LOW: 'bg-blue-100 text-blue-800 border-blue-300',
    UNRATED: 'bg-gray-100 text-gray-800 border-gray-300'
  };

  const enforcementColors = {
    'Immediate': 'bg-red-600 text-white',
    'Priority': 'bg-orange-600 text-white', 
    'Monitor': 'bg-blue-600 text-white'
  };

  const isMobile = device === 'mobile';

  return (
    <div className={`border rounded-lg p-4 ${levelColors[classification.level]} ${isMobile ? 'text-sm' : 'text-base'}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-3">
          <span className="text-2xl">{classification.icon}</span>
          <div>
            <h4 className="font-bold text-gray-900">{threat}</h4>
            <p className="text-sm opacity-75">{classification.category}</p>
          </div>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-bold ${enforcementColors[classification.enforcement]}`}>
          {classification.enforcement}
        </span>
      </div>
      
      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <span className="font-medium">Threat Level:</span>
          <br />
          <span className="font-bold">{classification.level}</span>
        </div>
        <div>
          <span className="font-medium">Legal Status:</span>
          <br />
          <span className="font-bold">{classification.category}</span>
        </div>
      </div>
    </div>
  );
};

// Enhanced alert card with government features
const EnhancedThreatCard = ({ alert, onAction, device }) => {
  const [expanded, setExpanded] = useState(false);
  const [actionTaken, setActionTaken] = useState(null);
  
  const severityConfig = {
    CRITICAL: { 
      color: 'red', 
      bgColor: 'bg-red-50', 
      borderColor: 'border-red-500',
      textColor: 'text-red-900',
      priority: 'IMMEDIATE ACTION REQUIRED'
    },
    HIGH: { 
      color: 'orange', 
      bgColor: 'bg-orange-50', 
      borderColor: 'border-orange-500',
      textColor: 'text-orange-900',
      priority: 'HIGH PRIORITY'
    },
    MEDIUM: { 
      color: 'yellow', 
      bgColor: 'bg-yellow-50', 
      borderColor: 'border-yellow-500',
      textColor: 'text-yellow-900',
      priority: 'MEDIUM PRIORITY'
    },
    LOW: { 
      color: 'blue', 
      bgColor: 'bg-blue-50', 
      borderColor: 'border-blue-500',
      textColor: 'text-blue-900',
      priority: 'LOW PRIORITY'
    }
  };

  const config = severityConfig[alert.severity] || severityConfig.MEDIUM;
  const isMobile = device === 'mobile';

  const handleAction = (action) => {
    setActionTaken(action);
    onAction(alert.id, action);
  };

  const platformConfig = {
    ebay: { icon: '🛒', region: 'Global' },
    craigslist: { icon: '📝', region: 'North America' },
    olx: { icon: '🌐', region: 'Europe/Asia' },
    marktplaats: { icon: '🇳🇱', region: 'Netherlands' },
    mercadolibre: { icon: '🇦🇷', region: 'Latin America' },
    gumtree: { icon: '🇬🇧', region: 'UK/Australia' },
    avito: { icon: '🇷🇺', region: 'Russia/CIS' }
  };

  const platform = platformConfig[alert.platform?.toLowerCase()] || { icon: '🌍', region: 'Unknown' };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`border-l-4 rounded-lg ${config.borderColor} ${config.bgColor} ${isMobile ? 'p-4' : 'p-6'} mb-4`}
    >
      {/* Alert Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start space-x-4">
          <div className={`p-2 rounded-full bg-${config.color}-100`}>
            <AlertTriangle className={`w-6 h-6 text-${config.color}-600`} />
          </div>
          
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <span className={`px-2 py-1 rounded-full text-xs font-bold bg-${config.color}-600 text-white`}>
                {config.priority}
              </span>
              <span className="text-xs text-gray-500">
                {platform.icon} {alert.platform} • {platform.region}
              </span>
            </div>
            
            <h3 className={`font-bold ${isMobile ? 'text-lg' : 'text-xl'} ${config.textColor} mb-2`}>
              {alert.threat}
            </h3>
            
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <div className="flex items-center space-x-1">
                <Clock className="w-4 h-4" />
                <span>{alert.timestamp}</span>
              </div>
              {alert.threatScore && (
                <div className="flex items-center space-x-1">
                  <Target className="w-4 h-4" />
                  <span>Score: {alert.threatScore}</span>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setExpanded(!expanded)}
            className={`p-2 rounded-lg bg-${config.color}-100 hover:bg-${config.color}-200 transition-colors`}
          >
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
          
          {alert.listingUrl && (
            <a 
              href={alert.listingUrl} 
              target="_blank" 
              rel="noopener noreferrer"
              className={`p-2 rounded-lg bg-${config.color}-100 hover:bg-${config.color}-200 transition-colors`}
            >
              <ExternalLink className="w-4 h-4" />
            </a>
          )}
        </div>
      </div>

      {/* Threat Classification */}
      {!isMobile && (
        <div className="mb-4">
          <ThreatClassification threat={alert.threat} device={device} />
        </div>
      )}

      {/* Listing Details */}
      {alert.listingTitle && (
        <div className="mb-4 p-3 bg-white bg-opacity-50 rounded-lg">
          <h4 className="font-medium text-gray-900 mb-1">Listing Details:</h4>
          <p className="text-sm text-gray-700 mb-2">{alert.listingTitle}</p>
          {alert.listingPrice && (
            <p className="text-sm font-medium text-green-700">Price: {alert.listingPrice}</p>
          )}
        </div>
      )}

      {/* Expanded Content */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 pt-4 border-t border-gray-200"
          >
            {/* Action Buttons */}
            <div className="mb-4">
              <h5 className="font-medium text-gray-900 mb-3">Enforcement Actions:</h5>
              <div className={`grid ${isMobile ? 'grid-cols-1 gap-2' : 'grid-cols-2 lg:grid-cols-4 gap-3'}`}>
                <button 
                  onClick={() => handleAction('investigate')}
                  className={`flex items-center space-x-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors ${
                    actionTaken === 'investigate' ? 'bg-green-600' : ''
                  }`}
                >
                  <Eye className="w-4 h-4" />
                  <span className="text-sm font-medium">Investigate</span>
                </button>
                
                <button 
                  onClick={() => handleAction('notify')}
                  className={`flex items-center space-x-2 px-3 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors ${
                    actionTaken === 'notify' ? 'bg-green-600' : ''
                  }`}
                >
                  <Bell className="w-4 h-4" />
                  <span className="text-sm font-medium">Alert Partners</span>
                </button>
                
                <button 
                  onClick={() => handleAction('escalate')}
                  className={`flex items-center space-x-2 px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors ${
                    actionTaken === 'escalate' ? 'bg-green-600' : ''
                  }`}
                >
                  <Flag className="w-4 h-4" />
                  <span className="text-sm font-medium">Escalate</span>
                </button>
                
                <button 
                  onClick={() => handleAction('archive')}
                  className={`flex items-center space-x-2 px-3 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors ${
                    actionTaken === 'archive' ? 'bg-green-600' : ''
                  }`}
                >
                  <Archive className="w-4 h-4" />
                  <span className="text-sm font-medium">Archive</span>
                </button>
              </div>
            </div>

            {/* Compliance Information */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
              <div className="bg-white bg-opacity-50 rounded-lg p-3">
                <h6 className="font-medium text-gray-900 mb-2">Legal Framework</h6>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>CITES Status:</span>
                    <span className="font-medium">Appendix I</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Jurisdiction:</span>
                    <span className="font-medium">{platform.region}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Enforcement:</span>
                    <span className="font-medium text-red-600">Required</span>
                  </div>
                </div>
              </div>

              <div className="bg-white bg-opacity-50 rounded-lg p-3">
                <h6 className="font-medium text-gray-900 mb-2">Investigation Status</h6>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>Evidence ID:</span>
                    <span className="font-medium">{alert.id}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Collected:</span>
                    <span className="font-medium">{alert.timestamp}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Status:</span>
                    <span className={`font-medium ${
                      actionTaken ? 'text-green-600' : 'text-orange-600'
                    }`}>
                      {actionTaken ? 'Action Taken' : 'Pending Review'}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {actionTaken && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="font-medium text-green-900">
                    Action Recorded: {actionTaken.charAt(0).toUpperCase() + actionTaken.slice(1)}
                  </span>
                </div>
                <p className="text-sm text-green-700 mt-1">
                  This action has been logged and relevant authorities have been notified.
                </p>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

// Intelligence summary panel
const IntelligenceSummary = ({ alerts, device }) => {
  const isMobile = device === 'mobile';

  const summary = useMemo(() => {
    const total = alerts.length;
    const critical = alerts.filter(a => a.severity === 'CRITICAL').length;
    const high = alerts.filter(a => a.severity === 'HIGH').length;
    const platforms = [...new Set(alerts.map(a => a.platform))].length;
    const species = [...new Set(alerts.map(a => a.threat))].length;

    return { total, critical, high, platforms, species };
  }, [alerts]);

  const metrics = [
    { label: 'Active Threats', value: summary.total, icon: AlertTriangle, color: 'red' },
    { label: 'Critical Alerts', value: summary.critical, icon: Flag, color: 'red' },
    { label: 'High Priority', value: summary.high, icon: AlertCircle, color: 'orange' },
    { label: 'Platforms Affected', value: summary.platforms, icon: Globe, color: 'blue' },
    { label: 'Species at Risk', value: summary.species, icon: Shield, color: 'green' }
  ];

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
      <h3 className={`font-bold ${isMobile ? 'text-lg' : 'text-xl'} text-gray-900 mb-6`}>
        Threat Intelligence Summary
      </h3>
      
      <div className={`grid ${isMobile ? 'grid-cols-2 gap-4' : 'grid-cols-5 gap-6'}`}>
        {metrics.map((metric, index) => (
          <div key={index} className="text-center">
            <div className={`w-12 h-12 mx-auto mb-3 rounded-full bg-${metric.color}-100 flex items-center justify-center`}>
              <metric.icon className={`w-6 h-6 text-${metric.color}-600`} />
            </div>
            <div className={`font-bold ${isMobile ? 'text-xl' : 'text-2xl'} text-gray-900 mb-1`}>
              {metric.value}
            </div>
            <div className="text-sm text-gray-600">{metric.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Filter and control panel
const ThreatControlPanel = ({ onFilter, onRefresh, isRefreshing, device }) => {
  const [filters, setFilters] = useState({
    severity: 'all',
    platform: 'all',
    timeframe: '24h',
    species: 'all'
  });
  const [showAdvanced, setShowAdvanced] = useState(false);

  const isMobile = device === 'mobile';

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilter(newFilters);
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className={`font-bold ${isMobile ? 'text-lg' : 'text-xl'} text-gray-900`}>
          Threat Intelligence Control Center
        </h3>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
          <span className="text-sm text-gray-600">Real-time Monitoring</span>
        </div>
      </div>

      {/* Primary Controls */}
      <div className={`grid ${isMobile ? 'grid-cols-1 gap-3' : 'grid-cols-2 lg:grid-cols-5 gap-4'} mb-4`}>
        <select 
          value={filters.severity}
          onChange={(e) => handleFilterChange('severity', e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg bg-white"
        >
          <option value="all">All Severities</option>
          <option value="CRITICAL">Critical Only</option>
          <option value="HIGH">High Priority</option>
          <option value="MEDIUM">Medium Priority</option>
          <option value="LOW">Low Priority</option>
        </select>

        <select 
          value={filters.platform}
          onChange={(e) => handleFilterChange('platform', e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg bg-white"
        >
          <option value="all">All Platforms</option>
          <option value="ebay">eBay</option>
          <option value="craigslist">Craigslist</option>
          <option value="olx">OLX</option>
          <option value="marktplaats">Marktplaats</option>
          <option value="mercadolibre">MercadoLibre</option>
          <option value="gumtree">Gumtree</option>
          <option value="avito">Avito</option>
        </select>

        <select 
          value={filters.timeframe}
          onChange={(e) => handleFilterChange('timeframe', e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg bg-white"
        >
          <option value="1h">Last Hour</option>
          <option value="24h">Last 24 Hours</option>
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
        </select>

        <button 
          onClick={onRefresh}
          disabled={isRefreshing}
          className="flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          <span>{isRefreshing ? 'Updating...' : 'Refresh'}</span>
        </button>

        <button 
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center justify-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          <Settings className="w-4 h-4" />
          <span>Advanced</span>
        </button>
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
                    placeholder="Min"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                  />
                  <input 
                    type="number" 
                    placeholder="Max"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Geographic Region
                </label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white">
                  <option value="all">All Regions</option>
                  <option value="north-america">North America</option>
                  <option value="europe">Europe</option>
                  <option value="asia">Asia</option>
                  <option value="latin-america">Latin America</option>
                  <option value="africa">Africa</option>
                  <option value="oceania">Oceania</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  CITES Appendix
                </label>
                <select className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white">
                  <option value="all">All Appendices</option>
                  <option value="I">Appendix I</option>
                  <option value="II">Appendix II</option>
                  <option value="III">Appendix III</option>
                </select>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

// Main Threat Intelligence Component
const ThreatIntelligence = () => {
  const device = useResponsive();
  const [alerts, setAlerts] = useState([]);
  const [filteredAlerts, setFilteredAlerts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState(null);

  // Load threat data
  useEffect(() => {
    loadThreatData();
    const interval = setInterval(loadThreatData, 60000); // Update every minute
    return () => clearInterval(interval);
  }, []);

  const loadThreatData = async () => {
    try {
      setIsRefreshing(true);
      
      const result = await WildGuardDataService.getRecentAlerts(50);
      
      if (result.success) {
        setAlerts(result.data);
        setFilteredAlerts(result.data);
      }
      
    } catch (error) {
      console.error('Threat data loading error:', error);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  const handleFilter = (filters) => {
    let filtered = [...alerts];

    if (filters.severity !== 'all') {
      filtered = filtered.filter(alert => alert.severity === filters.severity);
    }

    if (filters.platform !== 'all') {
      filtered = filtered.filter(alert => alert.platform?.toLowerCase() === filters.platform);
    }

    // Add more filter logic as needed

    setFilteredAlerts(filtered);
  };

  const handleAction = (alertId, action) => {
    console.log(`Action taken on alert ${alertId}: ${action}`);
    // Here you would typically call an API to record the action
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-xl font-medium text-gray-900">Loading Threat Intelligence...</p>
          <p className="text-gray-500">Analyzing global wildlife trafficking patterns</p>
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
              Threat Intelligence Center
            </h1>
            <p className={`text-gray-600 ${isMobile ? 'text-base' : 'text-xl'}`}>
              Real-time Wildlife Trafficking Detection & Law Enforcement Support
            </p>
          </div>
          
          {!isMobile && (
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-500">System Status</p>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                  <span className="font-medium text-green-600">Active Monitoring</span>
                </div>
              </div>
              <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-red-600" />
              </div>
            </div>
          )}
        </div>

        {/* Quick Stats */}
        <IntelligenceSummary alerts={filteredAlerts} device={device} />
      </div>

      {/* Control Panel */}
      <ThreatControlPanel 
        onFilter={handleFilter}
        onRefresh={loadThreatData}
        isRefreshing={isRefreshing}
        device={device}
      />

      {/* Alerts List */}
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className={`font-bold ${isMobile ? 'text-lg' : 'text-xl'} text-gray-900`}>
            Active Threat Alerts ({filteredAlerts.length})
          </h3>
          <div className="flex items-center space-x-2">
            <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">
              Live Feed
            </span>
          </div>
        </div>

        <div className="space-y-4">
          {filteredAlerts.length > 0 ? (
            filteredAlerts.map((alert, index) => (
              <EnhancedThreatCard
                key={alert.id || index}
                alert={alert}
                onAction={handleAction}
                device={device}
              />
            ))
          ) : (
            <div className="text-center py-12">
              <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
              <h4 className="text-xl font-medium text-gray-900 mb-2">No Active Threats</h4>
              <p className="text-gray-500">
                All systems are operating normally. Wildlife trafficking monitoring continues.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <div className={`flex ${isMobile ? 'flex-col space-y-4' : 'items-center justify-between'}`}>
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-green-600" />
              <span className="text-sm text-gray-600">CITES Compliant</span>
            </div>
            <div className="flex items-center space-x-2">
              <Lock className="w-5 h-5 text-blue-600" />
              <span className="text-sm text-gray-600">Secure Intelligence</span>
            </div>
            <div className="flex items-center space-x-2">
              <Globe className="w-5 h-5 text-purple-600" />
              <span className="text-sm text-gray-600">Global Network</span>
            </div>
          </div>
          
          <div className={`text-sm text-gray-500 ${isMobile ? 'text-center' : ''}`}>
            WildGuard AI Threat Intelligence • Real-time Global Protection
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThreatIntelligence;
