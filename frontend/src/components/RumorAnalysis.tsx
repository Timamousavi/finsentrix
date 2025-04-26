import React, { useState } from 'react';
import { Card, Input, Button, Table, Typography, message, List } from 'antd';
import axios from 'axios';

const { TextArea } = Input;
const { Title } = Typography;

interface Rumor {
  id: string;
  text: string;
  sentiment: string;
  confidence: number;
  timestamp: string;
  impact: number;
}

const RumorAnalysis: React.FC = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [rumors, setRumors] = useState<Rumor[]>([]);

  const analyzeRumor = async () => {
    if (!text.trim()) {
      message.error('Please enter a rumor to analyze');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/analyze/rumors', {
        text: text,
      });
      setRumors([...rumors, response.data]);
      setText('');
      message.success('Rumor analyzed successfully');
    } catch (error) {
      console.error('Error analyzing rumor:', error);
      message.error('Failed to analyze rumor');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: 'Rumor',
      dataIndex: 'text',
      key: 'text',
    },
    {
      title: 'Sentiment',
      dataIndex: 'sentiment',
      key: 'sentiment',
    },
    {
      title: 'Confidence',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (value: number) => `${(value * 100).toFixed(2)}%`,
    },
    {
      title: 'Impact',
      dataIndex: 'impact',
      key: 'impact',
      render: (value: number) => (
        <span style={{ color: value >= 0 ? '#3f8600' : '#cf1322' }}>
          {value >= 0 ? '+' : ''}{value.toFixed(2)}%
        </span>
      ),
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
    },
  ];

  return (
    <div>
      <Card>
        <Title level={4}>Market Rumor Analysis</Title>
        <TextArea
          rows={4}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter a market rumor to analyze..."
          style={{ marginBottom: 16 }}
        />
        <Button type="primary" onClick={analyzeRumor} loading={loading}>
          Analyze Rumor
        </Button>
      </Card>

      <Card style={{ marginTop: 16 }}>
        <Title level={4}>Recent Rumors</Title>
        <Table
          dataSource={rumors}
          columns={columns}
          rowKey="id"
          pagination={{ pageSize: 5 }}
        />
      </Card>
    </div>
  );
};

export default RumorAnalysis; 