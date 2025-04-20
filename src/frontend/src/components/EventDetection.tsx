import React, { useState } from 'react';
import { Card, Input, Button, Typography, Row, Col, Timeline, Tag } from 'antd';
import { Line } from '@ant-design/charts';
import axios from 'axios';

const { Title, Text } = Typography;
const { TextArea } = Input;

interface Event {
  id: string;
  type: string;
  description: string;
  timestamp: string;
  confidence: number;
  impact: string;
}

const EventDetection: React.FC = () => {
  const [text, setText] = useState('');
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(false);
  const [timeline, setTimeline] = useState<{ date: string; count: number }[]>([]);

  const detectEvents = async () => {
    if (!text.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post('/api/events/detect', { text });
      setEvents(response.data.events);
      
      // Update timeline
      const eventCounts = response.data.events.reduce((acc: { [key: string]: number }, event: Event) => {
        const date = new Date(event.timestamp).toISOString().split('T')[0];
        acc[date] = (acc[date] || 0) + 1;
        return acc;
      }, {});

      setTimeline(
        Object.entries(eventCounts).map(([date, count]) => ({
          date,
          count
        }))
      );
    } catch (error) {
      console.error('Error detecting events:', error);
    } finally {
      setLoading(false);
    }
  };

  const timelineConfig = {
    data: timeline,
    xField: 'date',
    yField: 'count',
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

  const getImpactColor = (impact: string) => {
    switch (impact.toLowerCase()) {
      case 'high':
        return 'red';
      case 'medium':
        return 'orange';
      case 'low':
        return 'green';
      default:
        return 'blue';
    }
  };

  return (
    <Card title="Event Detection">
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <TextArea
            rows={4}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to detect events..."
          />
        </Col>
        <Col span={24}>
          <Button type="primary" onClick={detectEvents} loading={loading}>
            Detect Events
          </Button>
        </Col>
        {events.length > 0 && (
          <>
            <Col span={24}>
              <Title level={4}>Detected Events</Title>
              <Timeline>
                {events.map((event) => (
                  <Timeline.Item key={event.id}>
                    <Text strong>{event.type}</Text>
                    <br />
                    <Text>{event.description}</Text>
                    <br />
                    <Tag color={getImpactColor(event.impact)}>
                      Impact: {event.impact}
                    </Tag>
                    <Tag color="blue">
                      Confidence: {(event.confidence * 100).toFixed(1)}%
                    </Tag>
                  </Timeline.Item>
                ))}
              </Timeline>
            </Col>
            <Col span={24}>
              <Title level={4}>Event Timeline</Title>
              <Line {...timelineConfig} />
            </Col>
          </>
        )}
      </Row>
    </Card>
  );
};

export default EventDetection; 