import React, { useEffect, useState } from 'react';
import { TrendingUp, TrendingDown } from 'react-feather';

interface PriceUpdate {
    symbol: string;
    price: number;
    change: number;
    timestamp: string;
}

interface RealTimeUpdatesProps {
    symbols: string[];
    onPriceUpdate?: (update: PriceUpdate) => void;
}

const RealTimeUpdates: React.FC<RealTimeUpdatesProps> = ({ symbols, onPriceUpdate }) => {
    const [updates, setUpdates] = useState<Record<string, PriceUpdate>>({});
    const [connected, setConnected] = useState(false);

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:8000/ws/prices');

        ws.onopen = () => {
            setConnected(true);
            // Subscribe to symbols
            ws.send(JSON.stringify({
                type: 'subscribe',
                symbols: symbols
            }));
        };

        ws.onclose = () => {
            setConnected(false);
            // Attempt to reconnect after 5 seconds
            setTimeout(() => {
                setConnected(false);
            }, 5000);
        };

        ws.onmessage = (event) => {
            try {
                const update: PriceUpdate = JSON.parse(event.data);
                setUpdates(prev => ({
                    ...prev,
                    [update.symbol]: update
                }));
                onPriceUpdate?.(update);
            } catch (error) {
                console.error('Error parsing price update:', error);
            }
        };

        return () => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.close();
            }
        };
    }, [symbols]);

    return (
        <div className="fixed bottom-0 right-0 mb-4 mr-4 z-50">
            <div className="bg-white rounded-lg shadow-lg p-4 max-w-sm">
                <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Live Updates</h3>
                    <div className={`w-2 h-2 rounded-full ${
                        connected ? 'bg-green-500' : 'bg-red-500'
                    }`} />
                </div>
                
                <div className="space-y-2 max-h-60 overflow-y-auto">
                    {Object.values(updates)
                        .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
                        .map((update) => (
                            <div
                                key={update.symbol}
                                className="flex items-center justify-between p-2 bg-gray-50 rounded-lg"
                            >
                                <div>
                                    <span className="font-medium">{update.symbol}</span>
                                    <span className="ml-2">₹{update.price.toFixed(2)}</span>
                                </div>
                                <div className={`flex items-center ${
                                    update.change >= 0 ? 'text-green-600' : 'text-red-600'
                                }`}>
                                    {update.change >= 0 ? (
                                        <TrendingUp className="w-4 h-4" />
                                    ) : (
                                        <TrendingDown className="w-4 h-4" />
                                    )}
                                    <span className="ml-1">
                                        {Math.abs(update.change)}%
                                    </span>
                                </div>
                            </div>
                        ))}
                </div>

                {!connected && (
                    <div className="mt-4 text-sm text-red-600">
                        Disconnected. Attempting to reconnect...
                    </div>
                )}
            </div>
        </div>
    );
};

export default RealTimeUpdates;
