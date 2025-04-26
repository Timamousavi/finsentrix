import React, { useState } from 'react';
import { Card, Input, Button, Table, Typography, message } from 'antd';
import axios from 'axios';

const { TextArea } = Input;
const { Title } = Typography;

interface SentimentResult {
  text: string;
  sentiment: string;
  confidence: number;
  details: {
    positive: number;
    negative: number;
    neutral: number;
  };
}

const SentimentAnalysis: React.FC = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SentimentResult | null>(null);

  const analyzeSentiment = async () => {
    if (!text.trim()) {
      message.error('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/analyze', {
        text: text,
      });
      setResult(response.data);
      message.success('Analysis completed successfully');
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
      message.error('Failed to analyze sentiment');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
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
  ];

  const dataSource = result
    ? [
        {
          key: '1',
          sentiment: result.sentiment,
          confidence: result.confidence,
        },
      ]
    : [];

  return (
    <div>
      <Card>
        <Title level={4}>Text Sentiment Analysis</Title>
        <TextArea
          rows={4}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter Persian text to analyze..."
          style={{ marginBottom: 16 }}
        />
        <Button type="primary" onClick={analyzeSentiment} loading={loading}>
          Analyze Sentiment
        </Button>
      </Card>

      {result && (
        <Card style={{ marginTop: 16 }}>
          <Title level={4}>Analysis Results</Title>
          <Table
            dataSource={dataSource}
            columns={columns}
            pagination={false}
            style={{ marginBottom: 16 }}
          />
          <Title level={5}>Detailed Sentiment Breakdown</Title>
          <Table
            dataSource={[
              {
                key: '1',
                type: 'Positive',
                value: result.details.positive,
              },
              {
                key: '2',
                type: 'Negative',
                value: result.details.negative,
              },
              {
                key: '3',
                type: 'Neutral',
                value: result.details.neutral,
              },
            ]}
            columns={[
              {
                title: 'Type',
                dataIndex: 'type',
                key: 'type',
              },
              {
                title: 'Value',
                dataIndex: 'value',
                key: 'value',
                render: (value: number) => `${(value * 100).toFixed(2)}%`,
              },
            ]}
            pagination={false}
          />
        </Card>
      )}
    </div>
  );
};

export default SentimentAnalysis; 