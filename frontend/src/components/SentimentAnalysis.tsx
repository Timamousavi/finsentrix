import React, { useState } from 'react';
import { Card, Input, Button, Progress, Typography, Space, Alert } from 'antd';
import { SendOutlined } from '@ant-design/icons';
import axios from 'axios';

const { TextArea } = Input;
const { Title } = Typography;

interface SentimentResult {
  sentiment: number;
  confidence: number;
  keywords: string[];
}

const SentimentAnalysis: React.FC = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SentimentResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const analyzeSentiment = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/sentiment/analyze', { text });
      setResult(response.data);
    } catch (err) {
      setError('Failed to analyze sentiment. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment: number) => {
    if (sentiment > 0.6) return '#52c41a';
    if (sentiment > 0.2) return '#faad14';
    return '#f5222d';
  };

  const getSentimentLabel = (sentiment: number) => {
    if (sentiment > 0.6) return 'Positive';
    if (sentiment > 0.2) return 'Neutral';
    return 'Negative';
  };

  return (
    <div>
      <Card>
        <Title level={4}>Enter Text for Analysis</Title>
        <TextArea
          rows={4}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to analyze sentiment..."
          style={{ marginBottom: 16 }}
        />
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={analyzeSentiment}
          loading={loading}
        >
          Analyze
        </Button>
      </Card>

      {error && (
        <Alert
          message="Error"
          description={error}
          type="error"
          showIcon
          style={{ marginTop: 16 }}
        />
      )}

      {result && (
        <Card style={{ marginTop: 16 }}>
          <Title level={4}>Analysis Results</Title>
          <Space direction="vertical" style={{ width: '100%' }}>
            <div>
              <Title level={5}>Sentiment Score</Title>
              <Progress
                percent={Math.abs(result.sentiment) * 100}
                status={result.sentiment >= 0 ? 'success' : 'exception'}
                format={() => (
                  <span style={{ color: getSentimentColor(result.sentiment) }}>
                    {getSentimentLabel(result.sentiment)} ({result.sentiment.toFixed(2)})
                  </span>
                )}
              />
            </div>

            <div>
              <Title level={5}>Confidence</Title>
              <Progress
                percent={result.confidence * 100}
                status="active"
                format={(percent) => `${percent?.toFixed(1)}%`}
              />
            </div>

            <div>
              <Title level={5}>Key Phrases</Title>
              <Space wrap>
                {result.keywords.map((keyword, index) => (
                  <Button key={index} type="dashed">
                    {keyword}
                  </Button>
                ))}
              </Space>
            </div>
          </Space>
        </Card>
      )}
    </div>
  );
};

export default SentimentAnalysis; 