import React from 'react';
import { useTranslation } from 'react-i18next';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Chip,
  Box,
} from '@mui/material';

interface Analysis {
  id: string;
  text: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  confidence: number;
  timestamp: string;
  market: string;
}

const RecentAnalysis: React.FC = () => {
  const { t } = useTranslation();
  
  // Sample data - replace with actual API call
  const analyses: Analysis[] = [
    {
      id: '1',
      text: 'Market shows strong bullish momentum',
      sentiment: 'positive',
      confidence: 0.92,
      timestamp: '2024-01-05T10:30:00Z',
      market: 'Stock',
    },
    {
      id: '2',
      text: 'Concerns over market volatility',
      sentiment: 'negative',
      confidence: 0.85,
      timestamp: '2024-01-05T09:15:00Z',
      market: 'Forex',
    },
    {
      id: '3',
      text: 'Market remains stable',
      sentiment: 'neutral',
      confidence: 0.78,
      timestamp: '2024-01-05T08:45:00Z',
      market: 'Crypto',
    },
  ];

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'success';
      case 'negative':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        {t('analysis.recent')}
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>{t('analysis.text')}</TableCell>
              <TableCell>{t('analysis.sentiment')}</TableCell>
              <TableCell>{t('analysis.confidence')}</TableCell>
              <TableCell>{t('analysis.market')}</TableCell>
              <TableCell>{t('analysis.timestamp')}</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {analyses.map((analysis) => (
              <TableRow key={analysis.id}>
                <TableCell>{analysis.text}</TableCell>
                <TableCell>
                  <Chip
                    label={t(`sentiment.${analysis.sentiment}`)}
                    color={getSentimentColor(analysis.sentiment)}
                    size="small"
                  />
                </TableCell>
                <TableCell>{Math.round(analysis.confidence * 100)}%</TableCell>
                <TableCell>{analysis.market}</TableCell>
                <TableCell>
                  {new Date(analysis.timestamp).toLocaleString()}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default RecentAnalysis; 