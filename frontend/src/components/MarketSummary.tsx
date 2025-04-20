import React from 'react';
import { useTranslation } from 'react-i18next';
import { Box, Typography, Paper, Grid } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';

interface MarketStats {
  total: number;
  positive: number;
  negative: number;
  neutral: number;
}

const MarketSummary: React.FC = () => {
  const { t } = useTranslation();
  
  // Sample data - replace with actual API call
  const stats: MarketStats = {
    total: 1000,
    positive: 650,
    negative: 250,
    neutral: 100,
  };

  const StatCard: React.FC<{
    title: string;
    value: number;
    percentage: number;
    icon: React.ReactNode;
    color: string;
  }> = ({ title, value, percentage, icon, color }) => (
    <Paper sx={{ p: 2, textAlign: 'center' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
        {icon}
        <Typography variant="h6" sx={{ ml: 1 }}>
          {title}
        </Typography>
      </Box>
      <Typography variant="h4" sx={{ color }}>
        {value}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {percentage}% of total
      </Typography>
    </Paper>
  );

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        {t('market.summary')}
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <StatCard
            title={t('sentiment.positive')}
            value={stats.positive}
            percentage={(stats.positive / stats.total) * 100}
            icon={<TrendingUpIcon color="success" />}
            color="success.main"
          />
        </Grid>
        <Grid item xs={12}>
          <StatCard
            title={t('sentiment.negative')}
            value={stats.negative}
            percentage={(stats.negative / stats.total) * 100}
            icon={<TrendingDownIcon color="error" />}
            color="error.main"
          />
        </Grid>
        <Grid item xs={12}>
          <StatCard
            title={t('sentiment.neutral')}
            value={stats.neutral}
            percentage={(stats.neutral / stats.total) * 100}
            icon={<TrendingFlatIcon color="action" />}
            color="text.secondary"
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default MarketSummary; 