import React, { useState, useEffect } from 'react';
import { Row, Col, message } from 'antd';
import type { RowProps } from 'antd/es/grid/row';
import type { ColProps } from 'antd/es/grid/col';
import Card from 'antd/es/card';
import Statistic from 'antd/es/statistic';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import { Line } from '@ant-design/charts';
import { analyzeSentiment, getApiInfo, getTimeline, getRecentAnalyses } from '../services/api';

interface MarketData {
  price: number;
  change: number;
  change_percent: number;
  volume: number;
  timestamp: string;
}

interface SentimentData {
  timestamp: string;
  sentiment_score: number;
}

interface DashboardData {
  market_data: MarketData;
  sentiment_data: SentimentData[];
}

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [marketData, setMarketData] = useState<MarketData | null>(null);
  const [sentimentData, setSentimentData] = useState<SentimentData[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchRealTimeData = async () => {
    try {
      setError(null);
      const response = await fetch('http://localhost:8000/api/dashboard/real-time');
      console.log('API Response:', response);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('API Data:', result);
      
      if (result.status === 'success' && result.data) {
        const data: DashboardData = result.data;
        setMarketData(data.market_data);
        setSentimentData(data.sentiment_data);
      } else {
        throw new Error('Invalid data format received from API');
      }
    } catch (error) {
      console.error('Error fetching real-time data:', error);
      setError(error instanceof Error ? error.message : 'Failed to fetch data');
      message.error('Failed to fetch real-time data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRealTimeData();
    // Fetch new data every 5 minutes
    const interval = setInterval(fetchRealTimeData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const config = {
    data: sentimentData,
    xField: 'timestamp',
    yField: 'sentiment_score',
    point: {
      size: 5,
      shape: 'diamond',
    },
    label: {
      style: {
        fill: '#aaa',
      },
    },
  };

  const renderStatisticCard = (
    title: string,
    value: number,
    options: {
      prefix?: React.ReactNode;
      suffix?: string;
      precision?: number;
      valueStyle?: React.CSSProperties;
    } = {}
  ) => (
    <Card loading={loading}>
      <Statistic
        title={title}
        value={value}
        precision={options.precision ?? 0}
        prefix={options.prefix}
        suffix={options.suffix}
        valueStyle={options.valueStyle}
      />
    </Card>
  );

  return (
    <div style={{ padding: '24px' }}>
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} md={6}>
          {renderStatisticCard('TEDPIX', marketData?.price || 0, {
            valueStyle: { color: '#1890ff' }
          })}
        </Col>
        <Col xs={24} sm={12} md={6}>
          {renderStatisticCard('Change', marketData?.change_percent || 0, {
            precision: 2,
            prefix: marketData?.change_percent && marketData.change_percent > 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />,
            suffix: '%',
            valueStyle: { color: marketData?.change_percent && marketData.change_percent > 0 ? '#3f8600' : '#cf1322' }
          })}
        </Col>
        <Col xs={24} sm={12} md={6}>
          {renderStatisticCard('Volume', marketData?.volume || 0, {
            valueStyle: { color: '#1890ff' }
          })}
        </Col>
        <Col xs={24} sm={12} md={6}>
          {renderStatisticCard('Market Sentiment', sentimentData.length > 0 ? sentimentData[0].sentiment_score * 100 : 0, {
            precision: 1,
            suffix: '%',
            valueStyle: { 
              color: sentimentData.length > 0 && sentimentData[0].sentiment_score > 0.5 ? '#3f8600' : '#cf1322'
            }
          })}
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24}>
          <Card title="Market Sentiment Trend" loading={loading}>
            <Line {...config} />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard; 