import React, { useState } from 'react';
import {
  Box,
  Button,
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
  Paper,
  CircularProgress,
  Grid,
  Tabs,
  Tab,
} from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginTop: theme.spacing(3),
  marginBottom: theme.spacing(3),
}));

const DataPoint = styled(Box)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  '& .label': {
    fontWeight: 'bold',
    color: theme.palette.text.secondary,
  },
  '& .value': {
    fontSize: '1.1rem',
  },
}));

interface StockData {
  symbol: string;
  exchange: string;
  current_price: string;
  market_cap: string;
  pe_ratio: number;
  volume: number;
  fifty_two_week_high: string;
  fifty_two_week_low: string;
  year_price_change: number;
  analysis: any;
  timestamp: string;
  status: string;
}

interface MarketData {
  nifty50: any;
  sensex: any;
  market_analysis: string;
  timestamp: string;
  status: string;
}

const IndianStockAnalysis: React.FC = () => {
  const [symbol, setSymbol] = useState('');
  const [exchange, setExchange] = useState('NSE');
  const [loading, setLoading] = useState(false);
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [error, setError] = useState('');
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const analyzeStock = async () => {
    if (!symbol) {
      setError('Please enter a stock symbol');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/stock/analyze/indian', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': 'your-api-key', // Replace with actual API key management
        },
        body: JSON.stringify({
          symbol,
          exchange,
          include_technical: true,
          include_sentiment: true,
          include_growth: true,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch stock data');
      }

      const data = await response.json();
      setStockData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getMarketSummary = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/stock/market/india', {
        headers: {
          'X-API-Key': 'your-api-key', // Replace with actual API key management
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch market data');
      }

      const data = await response.json();
      setMarketData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Typography variant="h4" component="h1" gutterBottom align="center" sx={{ mt: 4 }}>
        Indian Stock Market Analysis
      </Typography>

      <Tabs value={tabValue} onChange={handleTabChange} centered sx={{ mb: 3 }}>
        <Tab label="Stock Analysis" />
        <Tab label="Market Summary" />
      </Tabs>

      {tabValue === 0 && (
        <Box>
          <StyledPaper>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={5}>
                <TextField
                  fullWidth
                  label="Stock Symbol"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                  placeholder="e.g., RELIANCE, TCS"
                />
              </Grid>
              <Grid item xs={12} md={5}>
                <FormControl fullWidth>
                  <InputLabel>Exchange</InputLabel>
                  <Select value={exchange} onChange={(e) => setExchange(e.target.value)}>
                    <MenuItem value="NSE">NSE</MenuItem>
                    <MenuItem value="BSE">BSE</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={2}>
                <Button
                  fullWidth
                  variant="contained"
                  onClick={analyzeStock}
                  disabled={loading}
                >
                  {loading ? <CircularProgress size={24} /> : 'Analyze'}
                </Button>
              </Grid>
            </Grid>
          </StyledPaper>

          {error && (
            <Typography color="error" align="center" sx={{ mt: 2 }}>
              {error}
            </Typography>
          )}

          {stockData && (
            <StyledPaper>
              <Typography variant="h5" gutterBottom>
                {stockData.symbol} ({stockData.exchange})
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <DataPoint>
                    <Typography className="label">Current Price</Typography>
                    <Typography className="value">{stockData.current_price}</Typography>
                  </DataPoint>
                  <DataPoint>
                    <Typography className="label">Market Cap</Typography>
                    <Typography className="value">{stockData.market_cap}</Typography>
                  </DataPoint>
                  <DataPoint>
                    <Typography className="label">P/E Ratio</Typography>
                    <Typography className="value">{stockData.pe_ratio}</Typography>
                  </DataPoint>
                  <DataPoint>
                    <Typography className="label">Volume</Typography>
                    <Typography className="value">
                      {stockData.volume.toLocaleString()}
                    </Typography>
                  </DataPoint>
                </Grid>
                <Grid item xs={12} md={6}>
                  <DataPoint>
                    <Typography className="label">52 Week High</Typography>
                    <Typography className="value">{stockData.fifty_two_week_high}</Typography>
                  </DataPoint>
                  <DataPoint>
                    <Typography className="label">52 Week Low</Typography>
                    <Typography className="value">{stockData.fifty_two_week_low}</Typography>
                  </DataPoint>
                  <DataPoint>
                    <Typography className="label">Year Price Change</Typography>
                    <Typography className="value">
                      {stockData.year_price_change}%
                    </Typography>
                  </DataPoint>
                </Grid>
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>
                    Analysis
                  </Typography>
                  <Typography
                    component="pre"
                    sx={{
                      whiteSpace: 'pre-wrap',
                      fontFamily: 'inherit',
                      fontSize: '0.875rem',
                    }}
                  >
                    {stockData.analysis}
                  </Typography>
                </Grid>
              </Grid>
            </StyledPaper>
          )}
        </Box>
      )}

      {tabValue === 1 && (
        <Box>
          <StyledPaper>
            <Button
              fullWidth
              variant="contained"
              onClick={getMarketSummary}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Get Market Summary'}
            </Button>

            {marketData && (
              <Box sx={{ mt: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Market Analysis
                </Typography>
                <Typography
                  component="pre"
                  sx={{
                    whiteSpace: 'pre-wrap',
                    fontFamily: 'inherit',
                    fontSize: '0.875rem',
                  }}
                >
                  {marketData.market_analysis}
                </Typography>

                <Grid container spacing={3} sx={{ mt: 2 }}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Nifty 50
                    </Typography>
                    <pre>{JSON.stringify(marketData.nifty50, null, 2)}</pre>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      Sensex
                    </Typography>
                    <pre>{JSON.stringify(marketData.sensex, null, 2)}</pre>
                  </Grid>
                </Grid>
              </Box>
            )}
          </StyledPaper>
        </Box>
      )}
    </Container>
  );
};

export default IndianStockAnalysis;
