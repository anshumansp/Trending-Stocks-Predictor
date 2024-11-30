import React, { useEffect, useRef } from 'react';

declare global {
    interface Window {
        TradingView: any;
    }
}

interface TradingViewWidgetProps {
    symbol: string;
}

const TradingViewWidget: React.FC<TradingViewWidgetProps> = ({ symbol }) => {
    const container = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://s3.tradingview.com/tv.js';
        script.async = true;
        script.onload = () => {
            if (container.current) {
                new window.TradingView.widget({
                    width: '100%',
                    height: '100%',
                    symbol: `NSE:${symbol}`,
                    interval: 'D',
                    timezone: 'Asia/Kolkata',
                    theme: 'light',
                    style: '1',
                    locale: 'in',
                    toolbar_bg: '#f1f3f6',
                    enable_publishing: false,
                    allow_symbol_change: true,
                    container_id: container.current.id,
                    hide_side_toolbar: false,
                    studies: [
                        'MASimple@tv-basicstudies',
                        'RSI@tv-basicstudies',
                        'MACD@tv-basicstudies'
                    ],
                    show_popup_button: true,
                    popup_width: '1000',
                    popup_height: '650'
                });
            }
        };
        document.head.appendChild(script);

        return () => {
            script.remove();
        };
    }, [symbol]);

    return (
        <div 
            id={`tradingview_${symbol}`}
            ref={container}
            className="w-full h-full"
        />
    );
};

export default TradingViewWidget;
