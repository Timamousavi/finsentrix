import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Table } from 'antd';
import { Line } from '@ant-design/charts';
import axios from 'axios';

interface MarketData {
  timestamp: string;
  price: number;
  volume: number;
  sentiment: number;
}

interface DashboardData {
  market_data: {
    current_price: number;
    price_change: number;
    volume: number;
    historical_data: MarketData[];
  };
  sentiment_data: {
    overall_sentiment: number;
    positive_count: number;
    negative_count: number;
    neutral_count: number;
  };
}

const Dashboard: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/dashboard/real-time');
        setData(response.data.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setLoading(false);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  if (loading || !data) {
    return <div>Loading...</div>;
  }

  const priceConfig = {
    data: data.market_data.historical_data,
    xField: 'timestamp',
    yField: 'price',
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

  const sentimentConfig = {
    data: data.market_data.historical_data,
    xField: 'timestamp',
    yField: 'sentiment',
    point: {
      size: 5,
      shape: 'circle',
    },
    label: {
      style: {
        fill: '#aaa',
      },
    },
  };

  return (
    <div>
      <Row gutter={16}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Current Price"
              value={data.market_data.current_price}
              precision={2}
              prefix="$"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Price Change"
              value={data.market_data.price_change}
              precision={2}
              valueStyle={{ color: data.market_data.price_change >= 0 ? '#3f8600' : '#cf1322' }}
              prefix={data.market_data.price_change >= 0 ? '+' : ''}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Volume"
              value={data.market_data.volume}
              formatter={(value) => `${value.toLocaleString()}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Overall Sentiment"
              value={data.sentiment_data.overall_sentiment}
              precision={2}
              valueStyle={{ color: data.sentiment_data.overall_sentiment >= 0 ? '#3f8600' : '#cf1322' }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={12}>
          <Card title="Price History">
            <Line {...priceConfig} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Sentiment Trend">
            <Line {...sentimentConfig} />
          </Card>
        </Col>
      </Row>

      <Row style={{ marginTop: 16 }}>
        <Col span={24}>
          <Card title="Sentiment Distribution">
            <Table
              dataSource={[
                { type: 'Positive', count: data.sentiment_data.positive_count },
                { type: 'Negative', count: data.sentiment_data.negative_count },
                { type: 'Neutral', count: data.sentiment_data.neutral_count },
              ]}
              columns={[
                { title: 'Sentiment Type', dataIndex: 'type', key: 'type' },
                { title: 'Count', dataIndex: 'count', key: 'count' },
              ]}
              pagination={false}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard; 