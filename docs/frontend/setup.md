# Frontend Setup Guide

## Prerequisites

- Node.js (v14.0.0 or higher)
- npm (v6.0.0 or higher)
- Git

## Installation Steps

1. Clone the repository:
```bash
git clone [repository-url]
cd stocks-ai/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
```
Edit `.env` file with your configuration:
```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=ws://localhost:5000
```

4. Start development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/         # Page components
│   ├── services/      # API services
│   ├── store/         # State management
│   ├── utils/         # Utility functions
│   └── App.js         # Root component
├── public/            # Static assets
└── package.json       # Dependencies and scripts
```

## Available Scripts

- `npm start`: Runs development server
- `npm test`: Runs test suite
- `npm run build`: Creates production build
- `npm run lint`: Runs linter
- `npm run format`: Formats code using Prettier

## Testing

Run the test suite:
```bash
npm test
```

Run tests with coverage:
```bash
npm test -- --coverage
```
