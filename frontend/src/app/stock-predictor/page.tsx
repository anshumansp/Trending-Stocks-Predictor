'use client';

import React, { useState } from 'react';
import { Filter, Search, RefreshCw, BarChart2, TrendingUp, AlertTriangle } from 'lucide-react';
import { Button } from "@/components/ui/button";

interface Stock {
  symbol: string;
  name: string;
  price: number;
  change: number;
  prediction: {
    recommendation: 'buy' | 'sell' | 'hold';
    confidence: number;
    targetPrice: number;
    timeframe: string;
  };
  analysis: {
    technical: {
      rsi: number;
      macd: string;
      movingAverages: string;
    };
    fundamental: {
      peRatio: number;
      marketCap: string;
      revenue: string;
    };
    sentiment: {
      score: number;
      newsCount: number;
      socialMentions: number;
    };
  };
  risk: {
    level: 'low' | 'medium' | 'high';
    volatility: number;
    betaValue: number;
  };
}

const mockStocks: Stock[] = [
  {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    price: 189.84,
    change: 2.34,
    prediction: {
      recommendation: 'buy',
      confidence: 85,
      targetPrice: 205.00,
      timeframe: '3 months'
    },
    analysis: {
      technical: {
        rsi: 62,
        macd: 'bullish',
        movingAverages: 'uptrend'
      },
      fundamental: {
        peRatio: 28.5,
        marketCap: '2.95T',
        revenue: '383.93B'
      },
      sentiment: {
        score: 0.78,
        newsCount: 156,
        socialMentions: 25000
      }
    },
    risk: {
      level: 'low',
      volatility: 0.23,
      betaValue: 1.12
    }
  },
  {
    symbol: 'MSFT',
    name: 'Microsoft Corporation',
    price: 378.85,
    change: 4.12,
    prediction: {
      recommendation: 'buy',
      confidence: 82,
      targetPrice: 400.00,
      timeframe: '3 months'
    },
    analysis: {
      technical: {
        rsi: 58,
        macd: 'bullish',
        movingAverages: 'uptrend'
      },
      fundamental: {
        peRatio: 35.2,
        marketCap: '2.82T',
        revenue: '211.92B'
      },
      sentiment: {
        score: 0.82,
        newsCount: 134,
        socialMentions: 20000
      }
    },
    risk: {
      level: 'low',
      volatility: 0.21,
      betaValue: 0.98
    }
  }
];

export default function StockPredictor() {
  const [viewMode, setViewMode] = useState<'list' | 'detailed'>('detailed');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStock, setSelectedStock] = useState<Stock | null>(null);

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case 'buy': return 'text-emerald-green';
      case 'sell': return 'text-crimson-red';
      case 'hold': return 'text-gold';
      default: return 'text-muted-gray';
    }
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'low': return 'text-emerald-green';
      case 'medium': return 'text-gold';
      case 'high': return 'text-crimson-red';
      default: return 'text-muted-gray';
    }
  };

  return (
    <div className="min-h-screen bg-light-gray">
      <div className="container mx-auto px-4 py-8">
        {/* Header Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-4 text-navy-blue">
            Stock Predictor
          </h1>
          <p className="text-muted-gray max-w-2xl">
            AI-powered stock analysis and predictions using advanced algorithms, technical indicators, 
            fundamental analysis, and sentiment analysis.
          </p>
        </div>

        {/* Search and Filter Section */}
        <div className="flex flex-wrap gap-4 mb-8">
          <div className="flex-1 min-w-[300px]">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-gray" />
              <input
                type="text"
                placeholder="Search stocks..."
                className="input-primary w-full pl-10"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <Button className="btn-secondary flex items-center gap-2">
            <Filter size={16} />
            Filter
          </Button>
          <Button className="btn-secondary flex items-center gap-2">
            <RefreshCw size={16} />
            Refresh
          </Button>
        </div>

        {/* Stocks Grid */}
        <div className="grid grid-cols-1 gap-6">
          {mockStocks.map((stock) => (
            <div
              key={stock.symbol}
              className="card hover:shadow-lg"
            >
              {/* Stock Header */}
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-bold text-navy-blue mb-1">
                    {stock.symbol} - {stock.name}
                  </h3>
                  <div className="flex items-center gap-4">
                    <span className="text-xl text-dark-charcoal">${stock.price}</span>
                    <span className={stock.change >= 0 ? 'text-emerald-green' : 'text-crimson-red'}>
                      {stock.change >= 0 ? '+' : ''}{stock.change}%
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-lg font-semibold mb-1 ${getRecommendationColor(stock.prediction.recommendation)}`}>
                    {stock.prediction.recommendation.toUpperCase()}
                  </div>
                  <div className="text-muted-gray">
                    {stock.prediction.confidence}% confidence
                  </div>
                </div>
              </div>

              {/* Analysis Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Technical Analysis */}
                <div className="space-y-4">
                  <h4 className="text-lg font-semibold flex items-center gap-2 text-navy-blue">
                    <BarChart2 className="text-gold" />
                    Technical Analysis
                  </h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-muted-gray">RSI</span>
                      <span className="text-dark-charcoal">{stock.analysis.technical.rsi}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-gray">MACD</span>
                      <span className="text-dark-charcoal capitalize">{stock.analysis.technical.macd}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-gray">Moving Averages</span>
                      <span className="text-dark-charcoal capitalize">{stock.analysis.technical.movingAverages}</span>
                    </div>
                  </div>
                </div>

                {/* Fundamental Analysis */}
                <div className="space-y-4">
                  <h4 className="text-lg font-semibold flex items-center gap-2 text-navy-blue">
                    <TrendingUp className="text-gold" />
                    Fundamental Analysis
                  </h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-muted-gray">P/E Ratio</span>
                      <span className="text-dark-charcoal">{stock.analysis.fundamental.peRatio}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-gray">Market Cap</span>
                      <span className="text-dark-charcoal">{stock.analysis.fundamental.marketCap}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-gray">Revenue</span>
                      <span className="text-dark-charcoal">{stock.analysis.fundamental.revenue}</span>
                    </div>
                  </div>
                </div>

                {/* Risk Assessment */}
                <div className="space-y-4">
                  <h4 className="text-lg font-semibold flex items-center gap-2 text-navy-blue">
                    <AlertTriangle className="text-gold" />
                    Risk Assessment
                  </h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-muted-gray">Risk Level</span>
                      <span className={getRiskColor(stock.risk.level)}>
                        {stock.risk.level.toUpperCase()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-gray">Volatility</span>
                      <span className="text-dark-charcoal">{(stock.risk.volatility * 100).toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-gray">Beta</span>
                      <span className="text-dark-charcoal">{stock.risk.betaValue}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Prediction Details */}
              <div className="mt-6 p-4 bg-navy-blue/5 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-muted-gray">Target Price:</span>
                    <span className="ml-2 text-lg font-semibold text-emerald-green">
                      ${stock.prediction.targetPrice}
                    </span>
                  </div>
                  <div>
                    <span className="text-muted-gray">Timeframe:</span>
                    <span className="ml-2 text-dark-charcoal">{stock.prediction.timeframe}</span>
                  </div>
                  <div>
                    <span className="text-muted-gray">Sentiment Score:</span>
                    <span className="ml-2 text-dark-charcoal">
                      {(stock.analysis.sentiment.score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Analysis Criteria Section */}
        <div className="mt-12 card">
          <h2 className="text-2xl font-bold mb-6 text-navy-blue">Analysis Criteria</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-semibold text-emerald-green mb-4">Technical Analysis</h3>
              <ul className="space-y-2 text-muted-gray">
                <li>• Relative Strength Index (RSI)</li>
                <li>• Moving Average Convergence Divergence (MACD)</li>
                <li>• Simple & Exponential Moving Averages</li>
                <li>• Volume Analysis</li>
                <li>• Price Action Patterns</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gold mb-4">Fundamental Analysis</h3>
              <ul className="space-y-2 text-muted-gray">
                <li>• Price-to-Earnings Ratio</li>
                <li>• Market Capitalization</li>
                <li>• Revenue Growth</li>
                <li>• Profit Margins</li>
                <li>• Industry Performance</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-crimson-red mb-4">Risk Assessment</h3>
              <ul className="space-y-2 text-muted-gray">
                <li>• Historical Volatility</li>
                <li>• Beta Value</li>
                <li>• Market Sentiment</li>
                <li>• News Analysis</li>
                <li>• Social Media Trends</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
