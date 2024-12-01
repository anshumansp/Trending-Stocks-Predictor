'use client';

import React, { useState } from 'react';
import { Filter, Search, RefreshCw } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { sectorData, nifty50Data } from '@/data/stockData';
import { motion } from 'framer-motion';

export default function StockPredictor() {
  const [activeTab, setActiveTab] = useState('sectors');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-black text-white py-16">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4">Indian Stock Market Analysis</h1>
          <p className="text-gray-300">Comprehensive analysis of Nifty 50 stocks and sectors</p>
        </div>
      </section>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Navigation Tabs */}
        <div className="flex space-x-4 mb-8">
          {['sectors', 'stocks', 'performance'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg transition-colors ${
                activeTab === tab
                  ? 'bg-black text-white'
                  : 'bg-white text-black hover:bg-gray-100'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Sector Analysis */}
        {activeTab === 'sectors' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="space-y-8"
          >
            {/* Monthly Top Performers */}
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-bold mb-6">Monthly Top Performers</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {sectorData.monthlyTopPerformers.map((sector) => (
                  <div key={sector.sector} className="border p-4 rounded-lg">
                    <h3 className="font-medium text-lg mb-2">{sector.sector}</h3>
                    <p className="text-2xl font-bold text-green-600">{sector.return}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Sector Details */}
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-bold mb-6">Sector Analysis</h2>
              <div className="space-y-6">
                {sectorData.sectorDetails.map((sector) => (
                  <div key={sector.name} className="border-t pt-4 first:border-t-0">
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="text-xl font-semibold">{sector.name}</h3>
                      <div className="text-right">
                        <p className="text-sm text-gray-600">1-Month Return</p>
                        <p className={`font-bold ${
                          sector.monthReturn.startsWith('-') ? 'text-red-600' : 'text-green-600'
                        }`}>
                          {sector.monthReturn}
                        </p>
                      </div>
                    </div>
                    <div className="space-y-2">
                      {sector.topStocks.map((stock) => (
                        <div key={stock.name} className="flex justify-between items-center bg-gray-50 p-2 rounded">
                          <span>{stock.name}</span>
                          <span className={`font-medium ${
                            stock.return.startsWith('-') ? 'text-red-600' : 'text-green-600'
                          }`}>
                            {stock.return}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {/* Stock Analysis */}
        {activeTab === 'stocks' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-bold mb-6">Top Performing Stocks</h2>
              <div className="space-y-6">
                {nifty50Data.topStocks.map((stock) => (
                  <div key={stock.name} className="border p-6 rounded-lg hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-bold">{stock.name}</h3>
                        <p className="text-gray-600">{stock.sector}</p>
                      </div>
                      <span className="text-2xl font-bold text-green-600">{stock.monthReturn}</span>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600">Current Price</p>
                        <p className="font-medium">{stock.price}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Market Cap</p>
                        <p className="font-medium">{stock.marketCap}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}

        {/* Performance Metrics */}
        {activeTab === 'performance' && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className="bg-white p-6 rounded-lg shadow-lg">
              <h2 className="text-2xl font-bold mb-6">Sector Performance Overview</h2>
              <div className="space-y-4">
                {nifty50Data.sectorPerformance.map((item) => (
                  <div key={item.sector} className="border p-4 rounded-lg hover:bg-gray-50">
                    <div className="flex justify-between items-center">
                      <h3 className="font-medium">{item.sector}</h3>
                      <div className="space-x-6">
                        <span className={`font-medium ${
                          item.monthly.startsWith('-') ? 'text-red-600' : 'text-green-600'
                        }`}>
                          1M: {item.monthly}
                        </span>
                        <span className="font-medium text-gray-600">
                          3M: {item.quarterly}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
