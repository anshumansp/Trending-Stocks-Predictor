'use client';

import React from 'react';
import { TrendingUp, TrendingDown } from 'react-feather';

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

interface StockListProps {
  stocks: Stock[];
}

const StockList = ({ stocks }: StockListProps) => {
  return (
    <div className="space-y-4">
      {stocks.map((stock) => (
        <div key={stock.symbol} className="bg-white p-4 rounded-lg shadow">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="text-lg font-semibold">{stock.symbol}</h3>
              <p className="text-gray-500">{stock.name}</p>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-bold">${stock.price.toFixed(2)}</span>
              <div className="flex items-center">
                {stock.change >= 0 ? (
                  <TrendingUp className="w-4 h-4 text-green-500" />
                ) : (
                  <TrendingDown className="w-4 h-4 text-red-500" />
                )}
                <span className={stock.change >= 0 ? 'text-green-500' : 'text-red-500'}>
                  {Math.abs(stock.change)}%
                </span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StockList;