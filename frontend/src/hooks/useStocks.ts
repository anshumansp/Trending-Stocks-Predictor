import { useState, useEffect } from 'react';
import axios from 'axios';

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

interface UseStocksOptions {
    filters?: {
        recommendation?: string;
        risk?: string;
        sentiment?: string;
        growthPotential?: string;
    };
    search?: string;
}

export const useStocks = (options: UseStocksOptions = {}) => {
    const [stocks, setStocks] = useState<Stock[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchStocks = async () => {
            try {
                setLoading(true);
                const response = await axios.get('/api/stocks', {
                    params: {
                        ...options.filters,
                        search: options.search
                    }
                });
                setStocks(response.data);
                setError(null);
            } catch (err) {
                setError('Failed to fetch stock data');
                console.error('Error fetching stocks:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchStocks();
    }, [options.filters, options.search]);

    const refreshStocks = async () => {
        try {
            setLoading(true);
            const response = await axios.get('/api/stocks/refresh');
            setStocks(response.data);
            setError(null);
        } catch (err) {
            setError('Failed to refresh stock data');
            console.error('Error refreshing stocks:', err);
        } finally {
            setLoading(false);
        }
    };

    return {
        stocks,
        loading,
        error,
        refreshStocks
    };
};

export default useStocks;
