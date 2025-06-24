import { useState, useEffect } from 'react';
import WildGuardDataService from '../services/supabaseService';

/**
 * Custom hook for managing dashboard data with real Supabase connection
 * Handles loading states, error states, and automatic data refresh
 */
export const useRealDashboardData = (refreshInterval = 30000) => {
  // Loading states
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  // Data states - all real from Supabase
  const [realTimeStats, setRealTimeStats] = useState({});
  const [threatTrends, setThreatTrends] = useState([]);
  const [platformActivity, setPlatformActivity] = useState([]);
  const [speciesDistribution, setSpeciesDistribution] = useState([]);
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [multilingualStats, setMultilingualStats] = useState({});
  const [performanceMetrics, setPerformanceMetrics] = useState({});

  /**
   * Load all dashboard data from real Supabase database
   */
  const loadDashboardData = async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setIsRefreshing(true);
      } else {
        setIsLoading(true);
      }
      setError(null);

      // Fetch all real data in parallel
      const [
        statsResult,
        trendsResult,
        platformsResult,
        speciesResult,
        alertsResult,
        multilingualResult,
        performanceResult,
      ] = await Promise.all([
        WildGuardDataService.getRealTimeStats(),
        WildGuardDataService.getThreatTrends(7),
        WildGuardDataService.getPlatformActivity(),
        WildGuardDataService.getSpeciesDistribution(),
        WildGuardDataService.getRecentAlerts(20),
        WildGuardDataService.getMultilingualAnalytics(),
        WildGuardDataService.getPerformanceMetrics(),
      ]);

      // Update all states with real data
      if (statsResult.success) {
        setRealTimeStats(statsResult.data);
      } else {
        console.error('Failed to fetch real-time stats:', statsResult.error);
      }

      if (trendsResult.success) {
        setThreatTrends(trendsResult.data);
      } else {
        console.error('Failed to fetch threat trends:', trendsResult.error);
      }

      if (platformsResult.success) {
        setPlatformActivity(platformsResult.data);
      } else {
        console.error('Failed to fetch platform activity:', platformsResult.error);
      }

      if (speciesResult.success) {
        setSpeciesDistribution(speciesResult.data);
      } else {
        console.error('Failed to fetch species distribution:', speciesResult.error);
      }

      if (alertsResult.success) {
        setRecentAlerts(alertsResult.data);
      } else {
        console.error('Failed to fetch recent alerts:', alertsResult.error);
      }

      if (multilingualResult.success) {
        setMultilingualStats(multilingualResult.data);
      } else {
        console.error('Failed to fetch multilingual analytics:', multilingualResult.error);
      }

      if (performanceResult.success) {
        setPerformanceMetrics(performanceResult.data);
      } else {
        console.error('Failed to fetch performance metrics:', performanceResult.error);
      }

      setLastUpdated(new Date());

    } catch (error) {
      console.error('Error loading dashboard data:', error);
      setError(error.message);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  /**
   * Load dashboard data with custom time range
   */
  const loadTrendsData = async (days = 7) => {
    try {
      const result = await WildGuardDataService.getThreatTrends(days);
      if (result.success) {
        setThreatTrends(result.data);
      }
    } catch (error) {
      console.error('Error loading trends data:', error);
    }
  };

  /**
   * Search evidence with filters
   */
  const searchEvidence = async (searchTerm, filters = {}) => {
    try {
      const result = await WildGuardDataService.searchEvidence(searchTerm, filters);
      return result;
    } catch (error) {
      console.error('Error searching evidence:', error);
      return { success: false, error: error.message };
    }
  };

  /**
   * Get detailed information about a specific detection
   */
  const getDetectionDetails = async (detectionId) => {
    try {
      const result = await WildGuardDataService.getDetectionDetails(detectionId);
      return result;
    } catch (error) {
      console.error('Error fetching detection details:', error);
      return { success: false, error: error.message };
    }
  };

  /**
   * Manual refresh function
   */
  const refreshData = () => {
    loadDashboardData(true);
  };

  // Load data on component mount
  useEffect(() => {
    loadDashboardData();
  }, []);

  // Set up automatic refresh interval
  useEffect(() => {
    if (!refreshInterval) return;

    const interval = setInterval(() => {
      loadDashboardData(true);
    }, refreshInterval);

    return () => clearInterval(interval);
  }, [refreshInterval]);

  // Calculate summary statistics
  const summaryStats = {
    totalDetections: realTimeStats.totalDetections || 0,
    todayDetections: realTimeStats.todayDetections || 0,
    threatRate: realTimeStats.totalDetections > 0 
      ? ((realTimeStats.highPriorityAlerts || 0) / realTimeStats.totalDetections * 100).toFixed(2)
      : 0,
    platformCount: realTimeStats.platformsMonitored || 0,
    speciesCount: realTimeStats.speciesProtected || 0,
    multilingualCoverage: multilingualStats.multilingualCoverage || 95,
    isSystemHealthy: !error && realTimeStats.totalDetections > 0
  };

  return {
    // Data states
    realTimeStats,
    threatTrends,
    platformActivity,
    speciesDistribution,
    recentAlerts,
    multilingualStats,
    performanceMetrics,
    summaryStats,
    
    // Loading states
    isLoading,
    isRefreshing,
    error,
    lastUpdated,
    
    // Actions
    refreshData,
    loadTrendsData,
    searchEvidence,
    getDetectionDetails,
  };
};

/**
 * Hook for managing evidence search functionality
 */
export const useEvidenceSearch = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [searchError, setSearchError] = useState(null);
  const [searchFilters, setSearchFilters] = useState({
    platform: '',
    threatLevel: '',
    dateFrom: '',
    dateTo: ''
  });

  const performSearch = async (searchTerm) => {
    if (!searchTerm.trim()) {
      setSearchResults([]);
      return;
    }

    setIsSearching(true);
    setSearchError(null);

    try {
      const result = await WildGuardDataService.searchEvidence(searchTerm, searchFilters);
      
      if (result.success) {
        setSearchResults(result.data);
      } else {
        setSearchError(result.error);
        setSearchResults([]);
      }
    } catch (error) {
      setSearchError(error.message);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const clearSearch = () => {
    setSearchResults([]);
    setSearchError(null);
  };

  const updateFilters = (newFilters) => {
    setSearchFilters(prev => ({ ...prev, ...newFilters }));
  };

  return {
    searchResults,
    isSearching,
    searchError,
    searchFilters,
    performSearch,
    clearSearch,
    updateFilters
  };
};

/**
 * Hook for real-time status monitoring
 */
export const useSystemStatus = () => {
  const [systemStatus, setSystemStatus] = useState({
    database: 'checking',
    scanner: 'checking',
    alerts: 'checking',
    multilingual: 'checking'
  });

  const checkSystemStatus = async () => {
    try {
      // Check database connectivity
      const statsResult = await WildGuardDataService.getRealTimeStats();
      const databaseStatus = statsResult.success ? 'healthy' : 'error';

      // Check recent scanner activity
      const recentAlerts = await WildGuardDataService.getRecentAlerts(5);
      const scannerStatus = recentAlerts.success && recentAlerts.data.length > 0 ? 'active' : 'inactive';

      // Check multilingual capabilities
      const multilingualResult = await WildGuardDataService.getMultilingualAnalytics();
      const multilingualStatus = multilingualResult.success ? 'active' : 'error';

      setSystemStatus({
        database: databaseStatus,
        scanner: scannerStatus,
        alerts: recentAlerts.success ? 'active' : 'error',
        multilingual: multilingualStatus
      });

    } catch (error) {
      console.error('Error checking system status:', error);
      setSystemStatus({
        database: 'error',
        scanner: 'error', 
        alerts: 'error',
        multilingual: 'error'
      });
    }
  };

  useEffect(() => {
    checkSystemStatus();
    
    // Check status every 2 minutes
    const interval = setInterval(checkSystemStatus, 120000);
    return () => clearInterval(interval);
  }, []);

  const isSystemHealthy = Object.values(systemStatus).every(status => 
    status === 'healthy' || status === 'active'
  );

  return {
    systemStatus,
    isSystemHealthy,
    checkSystemStatus
  };
};

export default useRealDashboardData;
