import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Table } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import { Line } from '@ant-design/charts';

interface SentimentData {
  date: string;
  value: number;
}

interface Analysis {
  id: string;
  text: string;
  sentiment: number;
  timestamp: string;
}

const Dashboard: React.FC = () => {
  const [sentimentData, setSentimentData] = useState<SentimentData[]>([]);
  const [recentAnalyses, setRecentAnalyses] = useState<Analysis[]>([]);

  useEffect(() => {
    // Fetch sentiment data
    fetch('/api/sentiment/trends')
      .then(response => response.json())
      .then(data => setSentimentData(data));

    // Fetch recent analyses
    fetch('/api/analyses/recent')
      .then(response => response.json())
      .then(data => setRecentAnalyses(data));
  }, []);

  const columns = [
    {
      title: 'Text',
      dataIndex: 'text',
      key: 'text',
      ellipsis: true,
    },
    {
      title: 'Sentiment',
      dataIndex: 'sentiment',
      key: 'sentiment',
      render: (value: number) => (
        <span style={{ color: value >= 0 ? '#52c41a' : '#f5222d' }}>
          {value.toFixed(2)}
        </span>
      ),
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
    },
  ];

  const config = {
    data: sentimentData,
    xField: 'date',
    yField: 'value',
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

  return (
    <div>
      <Row gutter={16}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Analyses"
              value={1128}
              prefix={<ArrowUpOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Average Sentiment"
              value={0.65}
              precision={2}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Events Detected"
              value={42}
              prefix={<ArrowUpOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Rumors Analyzed"
              value={18}
              prefix={<ArrowDownOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginTop: 16 }}>
        <Col span={12}>
          <Card title="Sentiment Trend">
            <Line {...config} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Recent Analyses">
            <Table
              dataSource={recentAnalyses}
              columns={columns}
              size="small"
              pagination={{ pageSize: 5 }}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard; 