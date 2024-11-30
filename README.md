# Stock Recommendation AI System

A comprehensive machine learning platform for intelligent stock analysis and investment recommendations. This system combines real-time data, sentiment analysis, and technical indicators to provide data-driven investment insights.

## Features

- Real-time stock price tracking and updates
- Interactive stock charts with TradingView integration
- AI-powered stock analysis and recommendations
- Technical indicator calculations
- Sentiment analysis from multiple sources
- Responsive web interface
- Comprehensive monitoring and logging

## Tech Stack

### Frontend
- Next.js
- React
- Tailwind CSS
- Framer Motion
- TradingView Widget
- WebSocket for real-time updates

### Backend
- FastAPI
- Python 3.8+
- HuggingFace Transformers (for NLP)
- scikit-learn
- pandas
- WebSocket for real-time data

### Data Storage
- MongoDB
- Redis (caching and queues)

### Scheduling & Automation
- Node.js
- Bull Queue
- node-cron

### Monitoring
- Prometheus
- Grafana
- Custom metrics and logging

## Prerequisites

- Python 3.8+
- Node.js 14+
- Docker and Docker Compose
- MongoDB
- Redis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-recommendation-system.git
cd stock-recommendation-system
```

2. Create and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations
```

3. Run the deployment script:
```bash
chmod +x deploy.sh
./deploy.sh
```

## Environment Variables

```env
# API Keys
HUGGINGFACE_API_KEY=your_huggingface_key

# Database
MONGODB_URI=mongodb://localhost:27017/stock_analysis
REDIS_URL=redis://localhost:6379

# API Configuration
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# Monitoring
GRAFANA_PASSWORD=your_grafana_password
```

## Project Structure

```
aws-orchestrator/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Next.js pages
│   │   ├── hooks/          # Custom React hooks
│   │   └── styles/         # CSS and styling
│   └── public/             # Static assets
├── services/
│   ├── api/                # FastAPI backend
│   │   ├── middleware/     # API middleware
│   │   ├── models/        # Data models
│   │   └── routes/        # API endpoints
│   ├── agents/            # AI agents for analysis
│   ├── models/            # ML models
│   ├── scheduler/         # Node.js scheduler
│   ├── stock_scraper/     # Data collection
│   └── monitoring/        # Monitoring configuration
└── docker-compose.yml     # Container orchestration
```

## Available Scripts

### Frontend
```bash
cd frontend
npm install
npm run dev     # Development
npm run build   # Production build
npm start       # Start production server
```

### Backend
```bash
cd services/api
pip install -r requirements.txt
uvicorn main:app --reload
```

### Scheduler
```bash
cd services/scheduler
npm install
node scheduler.js
```

## Accessing Services

- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- Grafana Dashboard: http://localhost:3001
- Prometheus: http://localhost:9090

## Monitoring & Metrics

The system includes comprehensive monitoring:

- API request rates and latency
- Analysis duration metrics
- Memory and CPU usage
- WebSocket connection stats
- Database performance
- Queue metrics

Access these metrics through the Grafana dashboard.

## Error Handling

The system includes robust error handling:

- Custom exception classes
- Detailed error logging
- Error tracking with unique IDs
- Automatic retry mechanisms
- Rate limiting protection

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- TradingView for chart widgets
- HuggingFace for NLP models
- NSE India for stock data

## Support

For support, email support@yourdomain.com or open an issue in the repository.
