import React, { useState, useEffect } from 'react';
import { Card, Table, Tag, Typography, Space, Button, Input, Progress } from 'antd';
import { SearchOutlined, AlertOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { Search } = Input;

interface Rumor {
  id: string;
  text: string;
  type: string;
  spreadScore: number;
  confidence: number;
  sources: string[];
  timestamp: string;
  status: 'active' | 'verified' | 'debunked';
}

const RumorAnalysis: React.FC = () => {
  const [rumors, setRumors] = useState<Rumor[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');

  useEffect(() => {
    fetchRumors();
  }, []);

  const fetchRumors = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/rumors');
      setRumors(response.data);
    } catch (error) {
      console.error('Failed to fetch rumors:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'orange';
      case 'verified':
        return 'green';
      case 'debunked':
        return 'red';
      default:
        return 'default';
    }
  };

  const columns = [
    {
      title: 'Rumor',
      dataIndex: 'text',
      key: 'text',
      ellipsis: true,
      render: (text: string) => <Text>{text}</Text>,
    },
    {
      title: 'Type',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => <Tag color="blue">{type}</Tag>,
    },
    {
      title: 'Spread Score',
      dataIndex: 'spreadScore',
      key: 'spreadScore',
      render: (score: number) => (
        <Progress
          percent={score * 100}
          size="small"
          status={score > 0.7 ? 'exception' : score > 0.4 ? 'normal' : 'success'}
        />
      ),
    },
    {
      title: 'Confidence',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (confidence: number) => (
        <Progress
          percent={confidence * 100}
          size="small"
          status="active"
          format={(percent) => `${percent?.toFixed(1)}%`}
        />
      ),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </Tag>
      ),
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Rumor) => (
        <Space>
          <Button type="link" onClick={() => handleVerify(record.id)}>
            Verify
          </Button>
          <Button type="link" danger onClick={() => handleDebunk(record.id)}>
            Debunk
          </Button>
        </Space>
      ),
    },
  ];

  const handleVerify = async (id: string) => {
    try {
      await axios.post(`/api/rumors/${id}/verify`);
      fetchRumors();
    } catch (error) {
      console.error('Failed to verify rumor:', error);
    }
  };

  const handleDebunk = async (id: string) => {
    try {
      await axios.post(`/api/rumors/${id}/debunk`);
      fetchRumors();
    } catch (error) {
      console.error('Failed to debunk rumor:', error);
    }
  };

  const filteredRumors = rumors.filter(rumor =>
    rumor.text.toLowerCase().includes(searchText.toLowerCase()) ||
    rumor.type.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <div>
      <Card>
        <Space direction="vertical" style={{ width: '100%' }}>
          <Title level={4}>Rumor Analysis</Title>
          <Search
            placeholder="Search rumors..."
            allowClear
            onChange={(e) => setSearchText(e.target.value)}
            style={{ width: 300 }}
          />
        </Space>
      </Card>

      <Card style={{ marginTop: 16 }}>
        <Table
          columns={columns}
          dataSource={filteredRumors}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>
    </div>
  );
};

export default RumorAnalysis; 