import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Switch, Button, Typography, message, Select } from 'antd';
import axios from 'axios';
import { useLanguage } from '../contexts/LanguageContext';

const { Title } = Typography;
const { Option } = Select;

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
  const { language, setLanguage, t } = useLanguage();

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await axios.get('/api/settings');
      form.setFieldsValue(response.data);
    } catch (error) {
      console.error('Failed to fetch settings:', error);
      message.error(t('settings', 'loadError'));
    }
  };

  const handleSave = async (values: Settings) => {
    setLoading(true);
    try {
      await axios.post('/api/settings', values);
      message.success(t('settings', 'settingsSaved'));
    } catch (error) {
      console.error('Failed to save settings:', error);
      message.error(t('settings', 'settingsError'));
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageChange = (value: 'en' | 'fa') => {
    setLanguage(value);
  };

  return (
    <div style={{ direction: language === 'fa' ? 'rtl' : 'ltr' }}>
      <Card>
        <Title level={4}>{t('settings', 'title')}</Title>
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
            label={t('settings', 'language')}
            name="language"
            initialValue={language}
          >
            <Select onChange={handleLanguageChange}>
              <Option value="en">English</Option>
              <Option value="fa">فارسی</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label={t('settings', 'apiKey')}
            name="apiKey"
            rules={[{ required: true, message: t('settings', 'apiKeyMessage') }]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            label={t('settings', 'enableNotifications')}
            name="enableNotifications"
            valuePropName="checked"
          >
            <Switch />
          </Form.Item>

          <Form.Item
            label={t('settings', 'sentimentThreshold')}
            name="sentimentThreshold"
            rules={[{ required: true, message: t('settings', 'sentimentThresholdMessage') }]}
          >
            <Input type="number" min={0} max={1} step={0.1} />
          </Form.Item>

          <Form.Item
            label={t('settings', 'eventConfidenceThreshold')}
            name="eventConfidenceThreshold"
            rules={[{ required: true, message: t('settings', 'eventConfidenceMessage') }]}
          >
            <Input type="number" min={0} max={1} step={0.1} />
          </Form.Item>

          <Form.Item
            label={t('settings', 'rumorSpreadThreshold')}
            name="rumorSpreadThreshold"
            rules={[{ required: true, message: t('settings', 'rumorSpreadMessage') }]}
          >
            <Input type="number" min={0} max={1} step={0.1} />
          </Form.Item>

          <Form.Item
            label={t('settings', 'dataRetention')}
            name="dataRetentionDays"
            rules={[{ required: true, message: t('settings', 'dataRetentionMessage') }]}
          >
            <Input type="number" min={1} max={365} />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              {t('settings', 'saveSettings')}
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default Settings; 