import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Switch, Button, Typography, message } from 'antd';
import axios from 'axios';

const { Title } = Typography;

interface Settings {
  apiKey: string;
  enableNotifications: boolean;
  sentimentThreshold: number;
  eventConfidenceThreshold: number;
  rumorSpreadThreshold: number;
  dataRetentionDays: number;
}

const Settings: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get('/api/settings');
      form.setFieldsValue(response.data);
    } catch (error) {
      console.error('Failed to fetch settings:', error);
      message.error('Failed to load settings');
    }
  };

  const handleSave = async (values: Settings) => {
    setLoading(true);
    try {
      await axios.post('/api/settings', values);
      message.success('Settings saved successfully');
    } catch (error) {
      console.error('Failed to save settings:', error);
      message.error('Failed to save settings');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Card>
        <Title level={4}>Application Settings</Title>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSave}
          initialValues={{
            enableNotifications: true,
            sentimentThreshold: 0.5,
            eventConfidenceThreshold: 0.7,
            rumorSpreadThreshold: 0.6,
            dataRetentionDays: 30,
          }}
        >
          <Form.Item
            label="API Key"
            name="apiKey"
            rules={[{ required: true, message: 'Please input your API key!' }]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            label="Enable Notifications"
            name="enableNotifications"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            label="Sentiment Threshold"
            name="sentimentThreshold"
            rules={[{ required: true, message: 'Please input sentiment threshold!' }]}
          >
            <Input type="number" min={0} max={1} step={0.1} />
          </Form.Item>

          <Form.Item
            label="Event Confidence Threshold"
            name="eventConfidenceThreshold"
            rules={[{ required: true, message: 'Please input event confidence threshold!' }]}
          >
            <Input type="number" min={0} max={1} step={0.1} />
          </Form.Item>

          <Form.Item
            label="Rumor Spread Threshold"
            name="rumorSpreadThreshold"
            rules={[{ required: true, message: 'Please input rumor spread threshold!' }]}
          >
            <Input type="number" min={0} max={1} step={0.1} />
          </Form.Item>

          <Form.Item
            label="Data Retention (Days)"
            name="dataRetentionDays"
            rules={[{ required: true, message: 'Please input data retention days!' }]}
          >
            <Input type="number" min={1} max={365} />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              Save Settings
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Settings; 