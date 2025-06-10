import React, { useState } from "react";
import {
  X,
  ExternalLink,
  Download,
  AlertTriangle,
  MapPin,
  Clock,
  User,
  Globe,
  Camera,
  FileText,
  Hash,
} from "lucide-react";

const ThreatAnalysisModal = ({ isOpen, onClose, threat }) => {
  const [activeSection, setActiveSection] = useState("overview");

  if (!isOpen) return null;

  const mockThreatData = {
    id: "THR-2024-089",
    title: "Carved Ivory Elephant Figurine - Antique Collection",
    platform: "eBay",
    seller: "antique_collector_92",
    location: "Los Angeles, CA",
    price: "$850.00",
    detectedAt: "2024-06-09T14:23:45Z",
    threatScore: 89,
    confidence: 94,
    status: "ACTIVE",
    aiAnalysis: {
      speciesIdentified: ["African Elephant"],
      riskFactors: [
        "Carved ivory material detected",
        "Historical provenance claims",
        "High-value pricing typical of illegal trade",
        "Seller location in trafficking hotspot",
      ],
      languageAnalysis: {
        originalLanguage: "English",
        suspiciousTerms: ["antique", "estate sale", "no questions"],
        codeWords: ["decorative purposes only"],
      },
      imageAnalysis: {
        ivoryConfidence: 0.92,
        speciesMatch: 0.87,
        artificialAging: 0.73,
      },
    },
    evidence: {
      screenshots: 3,
      originalListing: "Preserved in blockchain",
      metadata: "Complete HTTP headers captured",
      relatedListings: 7,
    },
    networkAnalysis: {
      sellerRisk: "HIGH",
      connectionStrength: 0.78,
      relatedSellers: ["vintage_trader_44", "estate_finds_2024"],
      suspiciousPatterns: ["Similar posting times", "Shared shipping methods"],
    },
  };

  const SectionButton = ({ id, label, isActive, onClick }) => (
    <button
      onClick={() => onClick(id)}
      className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
        isActive
          ? "bg-blue-100 text-blue-700"
          : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
      }`}
    >
      {label}
    </button>
  );

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Threat Summary */}
      <div className="bg-gradient-to-r from-red-50 to-orange-50 rounded-lg p-6 border border-red-200">
        <div className="flex items-start justify-between">
          <div className="flex items-center">
            <AlertTriangle className="text-red-500 mr-3" size={24} />
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                High-Risk Wildlife Trade Detected
              </h3>
              <p className="text-gray-600 mt-1">
                Threat Score: {mockThreatData.threatScore}/100 • Confidence:{" "}
                {mockThreatData.confidence}%
              </p>
            </div>
          </div>
          <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">
            CRITICAL
          </span>
        </div>
      </div>

      {/* Key Details Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white border rounded-lg p-4">
          <div className="flex items-center mb-2">
            <Globe className="text-blue-500 mr-2" size={16} />
            <span className="text-sm font-medium text-gray-900">Platform</span>
          </div>
          <p className="text-lg font-semibold">{mockThreatData.platform}</p>
        </div>

        <div className="bg-white border rounded-lg p-4">
          <div className="flex items-center mb-2">
            <User className="text-green-500 mr-2" size={16} />
            <span className="text-sm font-medium text-gray-900">Seller</span>
          </div>
          <p className="text-lg font-semibold">{mockThreatData.seller}</p>
        </div>

        <div className="bg-white border rounded-lg p-4">
          <div className="flex items-center mb-2">
            <MapPin className="text-purple-500 mr-2" size={16} />
            <span className="text-sm font-medium text-gray-900">Location</span>
          </div>
          <p className="text-lg font-semibold">{mockThreatData.location}</p>
        </div>

        <div className="bg-white border rounded-lg p-4">
          <div className="flex items-center mb-2">
            <Clock className="text-orange-500 mr-2" size={16} />
            <span className="text-sm font-medium text-gray-900">Price</span>
          </div>
          <p className="text-lg font-semibold">{mockThreatData.price}</p>
        </div>
      </div>

      {/* AI Analysis Summary */}
      <div className="bg-white border rounded-lg p-6">
        <h4 className="font-semibold text-gray-900 mb-4">
          AI Analysis Summary
        </h4>
        <div className="space-y-4">
          <div>
            <h5 className="font-medium text-gray-900 mb-2">
              Species Identified
            </h5>
            <div className="flex flex-wrap gap-2">
              {mockThreatData.aiAnalysis.speciesIdentified.map(
                (species, index) => (
                  <span
                    key={index}
                    className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm"
                  >
                    {species}
                  </span>
                )
              )}
            </div>
          </div>

          <div>
            <h5 className="font-medium text-gray-900 mb-2">Risk Factors</h5>
            <ul className="space-y-1">
              {mockThreatData.aiAnalysis.riskFactors.map((factor, index) => (
                <li
                  key={index}
                  className="flex items-center text-sm text-gray-700"
                >
                  <div className="w-2 h-2 bg-red-400 rounded-full mr-3"></div>
                  {factor}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );

  const renderEvidence = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Screenshot Evidence */}
        <div className="bg-white border rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h4 className="font-semibold text-gray-900">Visual Evidence</h4>
            <span className="text-sm text-gray-600">
              {mockThreatData.evidence.screenshots} screenshots
            </span>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center"
              >
                <Camera className="text-gray-400" size={32} />
              </div>
            ))}
            <div className="aspect-square bg-gray-50 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
              <span className="text-gray-400 text-sm">
                +{mockThreatData.evidence.screenshots - 3} more
              </span>
            </div>
          </div>
        </div>

        {/* Digital Evidence */}
        <div className="bg-white border rounded-lg p-6">
          <h4 className="font-semibold text-gray-900 mb-4">Digital Evidence</h4>
          <div className="space-y-3">
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <div className="flex items-center">
                <FileText className="text-blue-500 mr-3" size={16} />
                <span className="text-sm">Original Listing HTML</span>
              </div>
              <button className="text-blue-600 hover:text-blue-800 text-sm">
                Download
              </button>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <div className="flex items-center">
                <Hash className="text-green-500 mr-3" size={16} />
                <span className="text-sm">Blockchain Record</span>
              </div>
              <button className="text-blue-600 hover:text-blue-800 text-sm">
                Verify
              </button>
            </div>
            <div className="flex items-center justify-between py-2">
              <div className="flex items-center">
                <Globe className="text-purple-500 mr-3" size={16} />
                <span className="text-sm">Network Metadata</span>
              </div>
              <button className="text-blue-600 hover:text-blue-800 text-sm">
                View
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Legal Documentation */}
      <div className="bg-white border rounded-lg p-6">
        <h4 className="font-semibold text-gray-900 mb-4">
          Legal Documentation
        </h4>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-blue-800 text-sm mb-2">
            Evidence has been preserved according to legal standards for
            potential prosecution.
          </p>
          <ul className="text-blue-700 text-sm space-y-1">
            <li>• Chain of custody maintained</li>
            <li>• Timestamped with blockchain verification</li>
            <li>• Metadata preserved for forensic analysis</li>
            <li>• Ready for law enforcement handover</li>
          </ul>
        </div>
      </div>
    </div>
  );

  const renderNetworkAnalysis = () => (
    <div className="space-y-6">
      {/* Seller Profile */}
      <div className="bg-white border rounded-lg p-6">
        <h4 className="font-semibold text-gray-900 mb-4">
          Seller Risk Profile
        </h4>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-700">
                Risk Level
              </label>
              <div className="mt-1">
                <div className="flex items-center">
                  <div className="flex-1 bg-gray-200 rounded-full h-2 mr-3">
                    <div
                      className="bg-red-500 h-2 rounded-full"
                      style={{ width: "85%" }}
                    ></div>
                  </div>
                  <span className="text-sm font-medium text-red-600">HIGH</span>
                </div>
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700">
                Account Age
              </label>
              <p className="text-lg font-semibold">2.3 years</p>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700">
                Feedback Score
              </label>
              <p className="text-lg font-semibold">847 (98.2%)</p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium text-gray-700">
                Suspicious Listings
              </label>
              <p className="text-lg font-semibold text-orange-600">12</p>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700">
                Network Connections
              </label>
              <p className="text-lg font-semibold">7 sellers</p>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-700">
                Geographic Pattern
              </label>
              <p className="text-lg font-semibold">West Coast Cluster</p>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <h5 className="font-medium text-gray-900 mb-2">
              Behavioral Patterns
            </h5>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• Posts during off-hours</li>
              <li>• Uses coded language</li>
              <li>• Rapid listing removal</li>
              <li>• Avoids direct communication</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Network Connections */}
      <div className="bg-white border rounded-lg p-6">
        <h4 className="font-semibold text-gray-900 mb-4">Connected Sellers</h4>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-2 text-sm font-medium text-gray-700">
                  Seller ID
                </th>
                <th className="text-left py-2 text-sm font-medium text-gray-700">
                  Connection Type
                </th>
                <th className="text-left py-2 text-sm font-medium text-gray-700">
                  Strength
                </th>
                <th className="text-left py-2 text-sm font-medium text-gray-700">
                  Risk Level
                </th>
                <th className="text-left py-2 text-sm font-medium text-gray-700">
                  Last Activity
                </th>
              </tr>
            </thead>
            <tbody>
              {mockThreatData.networkAnalysis.relatedSellers.map(
                (seller, index) => (
                  <tr key={index} className="border-b border-gray-100">
                    <td className="py-3 text-sm font-mono">{seller}</td>
                    <td className="py-3 text-sm">Shipping Address</td>
                    <td className="py-3">
                      <div className="flex items-center">
                        <div className="w-16 bg-gray-200 rounded-full h-1 mr-2">
                          <div
                            className="bg-orange-500 h-1 rounded-full"
                            style={{ width: "78%" }}
                          ></div>
                        </div>
                        <span className="text-sm">78%</span>
                      </div>
                    </td>
                    <td className="py-3">
                      <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded-full text-xs">
                        MEDIUM
                      </span>
                    </td>
                    <td className="py-3 text-sm text-gray-600">2 days ago</td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      <div
        className="absolute inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      ></div>

      <div className="relative flex h-full">
        <div className="flex flex-col w-full max-w-6xl ml-auto bg-white shadow-xl">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                {mockThreatData.title}
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                Threat ID: {mockThreatData.id}
              </p>
            </div>
            <div className="flex items-center space-x-3">
              <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                <ExternalLink size={16} className="mr-2" />
                View Original
              </button>
              <button className="flex items-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
                <Download size={16} className="mr-2" />
                Export Report
              </button>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X size={20} />
              </button>
            </div>
          </div>

          {/* Navigation */}
          <div className="flex space-x-4 px-6 py-3 border-b border-gray-200 bg-gray-50">
            <SectionButton
              id="overview"
              label="Overview"
              isActive={activeSection === "overview"}
              onClick={setActiveSection}
            />
            <SectionButton
              id="evidence"
              label="Evidence"
              isActive={activeSection === "evidence"}
              onClick={setActiveSection}
            />
            <SectionButton
              id="network"
              label="Network Analysis"
              isActive={activeSection === "network"}
              onClick={setActiveSection}
            />
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6">
            {activeSection === "overview" && renderOverview()}
            {activeSection === "evidence" && renderEvidence()}
            {activeSection === "network" && renderNetworkAnalysis()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThreatAnalysisModal;
