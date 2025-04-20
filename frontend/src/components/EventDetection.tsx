import React, { useState, useEffect } from 'react';
import { Card, Timeline, Tag, Typography, Space, Button, Input } from 'antd';
import { ClockCircleOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { Search } = Input;

interface Event {
  id: string;
  type: string;
  description: string;
  timestamp: string;
  impact: number;
  confidence: number;
  source: string;
}

const EventDetection: React.FC = () => {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/events');
      setEvents(response.data);
    } catch (error) {
      console.error('Failed to fetch events:', error);
    } finally {
      setLoading(false);
    }
  };

  const getImpactColor = (impact: number) => {
    if (impact > 0.7) return 'red';
    if (impact > 0.4) return 'orange';
    return 'green';
  };

  const getImpactLabel = (impact: number) => {
    if (impact > 0.7) return 'High Impact';
    if (impact > 0.4) return 'Medium Impact';
    return 'Low Impact';
  };

  const filteredEvents = events.filter(event =>
    event.description.toLowerCase().includes(searchText.toLowerCase()) ||
    event.type.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <div>
      <Card>
        <Space direction="vertical" style={{ width: '100%' }}>
          <Title level={4}>Market Events Timeline</Title>
          <Search
            placeholder="Search events..."
            allowClear
            onChange={(e) => setSearchText(e.target.value)}
            style={{ width: 300 }}
          />
        </Space>
      </Card>

      <Card style={{ marginTop: 16 }}>
        <Timeline
          mode="left"
          items={filteredEvents.map(event => ({
            label: event.timestamp,
            children: (
              <Card size="small">
                <Space direction="vertical">
                  <Space>
                    <Tag color="blue">{event.type}</Tag>
                    <Tag color={getImpactColor(event.impact)}>
                      {getImpactLabel(event.impact)}
                    </Tag>
                    <Tag color="purple">Confidence: {(event.confidence * 100).toFixed(1)}%</Tag>
                  </Space>
                  <Text>{event.description}</Text>
                  <Text type="secondary">Source: {event.source}</Text>
                </Space>
              </Card>
            ),
          }))}
        />
      </Card>
    </div>
  );
};

export default EventDetection; 