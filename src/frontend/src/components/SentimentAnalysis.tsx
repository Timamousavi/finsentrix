import React, { useState } from 'react';
import { Card, Input, Button, Typography, Row, Col, Progress } from 'antd';
import { Line } from '@ant-design/charts';
import axios from 'axios';

const { Title, Text } = Typography;
const { TextArea } = Input;

interface SentimentScores {
  positive: number;
  negative: number;
  neutral: number;
}

const SentimentAnalysis: React.FC = () => {
  const [text, setText] = useState('');
  const [sentiment, setSentiment] = useState<SentimentScores | null>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<{ timestamp: string; score: number }[]>([]);

  const analyzeSentiment = async () => {
    if (!text.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post('/api/sentiment/analyze', { text });
      setSentiment(response.data.sentiment);
      
      // Update history
      const score = response.data.sentiment.positive - response.data.sentiment.negative;
      setHistory(prev => [...prev, {
        timestamp: new Date().toISOString(),
        score
      }].slice(-10)); // Keep last 10 entries
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
    } finally {
      setLoading(false);
    }
  };

  const sentimentConfig = {
    data: history,
    xField: 'timestamp',
    yField: 'score',
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
    <Card title="Sentiment Analysis">
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <TextArea
            rows={4}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to analyze sentiment..."
          />
        </Col>
        <Col span={24}>
          <Button type="primary" onClick={analyzeSentiment} loading={loading}>
            Analyze
          </Button>
        </Col>
        {sentiment && (
          <>
            <Col span={24}>
              <Title level={4}>Sentiment Scores</Title>
              <Row gutter={16}>
                <Col span={8}>
                  <Text>Positive</Text>
                  <Progress percent={sentiment.positive * 100} status="success" />
                </Col>
                <Col span={8}>
                  <Text>Negative</Text>
                  <Progress percent={sentiment.negative * 100} status="exception" />
                </Col>
                <Col span={8}>
                  <Text>Neutral</Text>
                  <Progress percent={sentiment.neutral * 100} />
                </Col>
              </Row>
            </Col>
            <Col span={24}>
              <Title level={4}>Sentiment Trend</Title>
              <Line {...sentimentConfig} />
            </Col>
          </>
        )}
      </Row>
    </Card>
  );
};

export default SentimentAnalysis; 