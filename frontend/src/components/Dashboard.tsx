'use client';

import React, { useState } from 'react';
import { Filter, Search, RefreshCw, Grid, List } from 'react-feather';
import StockList from './StockList';
import StockGrid from './StockGrid';

interface Stock {
  symbol: string;
  name: string;
  price: number;
  change: number;
  recommendation: 'buy' | 'sell' | 'hold';
  sentiment: number;
  risk: 'low' | 'medium' | 'high';
  growthPotential: number;
}

const mockStocks: Stock[] = [
  {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    price: 150.23,
    change: 2.5,
    recommendation: 'buy',
    sentiment: 0.85,
    risk: 'low',
    growthPotential: 15
  },
  {
    symbol: 'GOOGL',
    name: 'Alphabet Inc.',
    price: 2750.10,
    change: -1.2,
    recommendation: 'hold',
    sentiment: 0.65,
    risk: 'medium',
    growthPotential: 12
  }
];

const Dashboard = () => {
  const [viewMode, setViewMode] = useState<'list' | 'grid'>('list');
  const [filterOpen, setFilterOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Stock Recommendations</h1>
          <p className="mt-2 text-gray-600">AI-powered stock analysis and recommendations</p>
        </div>
        
        {viewMode === 'list' ? (
          <StockList stocks={mockStocks} />
        ) : (
          <StockGrid stocks={mockStocks} />
        )}
      </div>
    </div>
  );
};

export default Dashboard;
