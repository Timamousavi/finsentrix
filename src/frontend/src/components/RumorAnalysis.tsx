import React, { useState } from 'react';
import { Card, Input, Button, Typography, Row, Col, Progress, Tag, Alert } from 'antd';
import { Line } from '@ant-design/charts';
import axios from 'axios';

const { Title, Text } = Typography;
const { TextArea } = Input;

interface Rumor {
  id: string;
  text: string;
  confidence: number;
  spread_score: number;
  key_phrases: string[];
  timestamp: string;
  verdict: string;
}

interface ApiResponse {
  rumors: Rumor[];
}

const RumorAnalysis: React.FC = () => {
  const [text, setText] = useState('');
  const [rumors, setRumors] = useState<Rumor[]>([]);
  const [loading, setLoading] = useState(false);
  const [spreadData, setSpreadData] = useState<{ time: string; score: number }[]>([]);

  const analyzeRumor = async () => {
    if (!text.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post<ApiResponse>('/api/rumors/detect', { text });
      const rumorData = response.data.rumors;
      setRumors(rumorData);
      
      // Update spread data
      const spreadScores = rumorData.map((rumor) => ({
        time: new Date(rumor.timestamp).toISOString(),
        score: rumor.spread_score
      }));
      setSpreadData(spreadScores);
    } catch (error) {
      console.error('Error analyzing rumor:', error);
    } finally {
      setLoading(false);
    }
  };

  const spreadConfig = {
    data: spreadData,
    xField: 'time',
    yField: 'score',
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

  const getVerdictColor = (verdict: string) => {
    switch (verdict.toLowerCase()) {
      case 'likely manipulation':
        return 'red';
      case 'potential rumor':
        return 'orange';
      case 'unlikely':
        return 'green';
      default:
        return 'blue';
    }
  };

  return (
    <Card title="Rumor Analysis">
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <TextArea
            rows={4}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to analyze for rumors..."
          />
        </Col>
        <Col span={24}>
          <Button type="primary" onClick={analyzeRumor} loading={loading}>
            Analyze Rumor
          </Button>
        </Col>
        {rumors.length > 0 && (
          <>
            <Col span={24}>
              <Title level={4}>Rumor Analysis Results</Title>
              {rumors.map((rumor) => (
                <Card key={rumor.id} style={{ marginBottom: 16 }}>
                  <Row gutter={[16, 16]}>
                    <Col span={24}>
                      <Text strong>Text:</Text>
                      <Text>{rumor.text}</Text>
                    </Col>
                    <Col span={24}>
                      <Text strong>Confidence:</Text>
                      <Progress percent={rumor.confidence * 100} />
                    </Col>
                    <Col span={24}>
                      <Text strong>Spread Score:</Text>
                      <Progress percent={rumor.spread_score * 100} status="active" />
                    </Col>
                    <Col span={24}>
                      <Text strong>Key Phrases:</Text>
                      <div style={{ marginTop: 8 }}>
                        {rumor.key_phrases.map((phrase, index) => (
                          <Tag key={index} color="blue">{phrase}</Tag>
                        ))}
                      </div>
                    </Col>
                    <Col span={24}>
                      <Alert
                        message="Verdict"
                        description={rumor.verdict}
                        type={rumor.verdict.toLowerCase().includes('manipulation') ? 'error' : 
                              rumor.verdict.toLowerCase().includes('potential') ? 'warning' : 'success'}
                        showIcon
                      />
                    </Col>
                  </Row>
                </Card>
              ))}
            </Col>
            <Col span={24}>
              <Title level={4}>Spread Analysis</Title>
              <Line {...spreadConfig} />
            </Col>
          </>
        )}
      </Row>
    </Card>
  );
};

export default RumorAnalysis; 