import React from 'react';
import { useTranslation } from 'react-i18next';
import { Grid, Paper, Typography } from '@mui/material';
import SentimentChart from '../components/SentimentChart';
import MarketSummary from '../components/MarketSummary';
import RecentAnalysis from '../components/RecentAnalysis';

const Dashboard: React.FC = () => {
  const { t } = useTranslation();

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Typography variant="h4" gutterBottom>
          {t('dashboard.title')}
        </Typography>
      </Grid>
      
      <Grid item xs={12} md={8}>
        <Paper sx={{ p: 2 }}>
          <SentimentChart />
        </Paper>
      </Grid>
      
      <Grid item xs={12} md={4}>
        <Paper sx={{ p: 2 }}>
          <MarketSummary />
        </Paper>
      </Grid>
      
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <RecentAnalysis />
        </Paper>
      </Grid>
    </Grid>
  );
};

export default Dashboard; 