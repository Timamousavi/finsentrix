import React from 'react';
import { useTranslation } from 'react-i18next';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface SentimentData {
  date: string;
  positive: number;
  negative: number;
  neutral: number;
}

const SentimentChart: React.FC = () => {
  const { t } = useTranslation();
  
  // Sample data - replace with actual API call
  const data: SentimentData[] = [
    { date: '2024-01-01', positive: 65, negative: 25, neutral: 10 },
    { date: '2024-01-02', positive: 59, negative: 30, neutral: 11 },
    { date: '2024-01-03', positive: 80, negative: 15, neutral: 5 },
    { date: '2024-01-04', positive: 81, negative: 10, neutral: 9 },
    { date: '2024-01-05', positive: 56, negative: 35, neutral: 9 },
  ];

  const chartData = {
    labels: data.map(item => item.date),
    datasets: [
      {
        label: t('sentiment.positive'),
        data: data.map(item => item.positive),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
      },
      {
        label: t('sentiment.negative'),
        data: data.map(item => item.negative),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: t('sentiment.neutral'),
        data: data.map(item => item.neutral),
        borderColor: 'rgb(201, 203, 207)',
        backgroundColor: 'rgba(201, 203, 207, 0.5)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: t('sentiment.trend'),
      },
    },
  };

  return <Line options={options} data={chartData} />;
};

export default SentimentChart; 