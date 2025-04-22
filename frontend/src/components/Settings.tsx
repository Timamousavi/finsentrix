import React, { useState, useEffect } from 'react';
import { Form, Input, Switch, Button, message, InputNumber, Select } from 'antd';
import Card from 'antd/es/card';
import Typography from 'antd/es/typography';
import { useLanguage } from '../contexts/LanguageContext';
import axios from 'axios';

const { Title } = Typography;
const { Password } = Input;

interface Settings {
  apiKey: string;
  enableNotifications: boolean;
  sentimentThreshold: number;
  eventConfidenceThreshold: number;
  language: 'en' | 'fa';
}

const SettingsComponent: React.FC = () => {
  const [form] = Form.useForm<Settings>();
  const { language, setLanguage, t } = useLanguage();
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
        <Title level={2}>{t('settings', 'title')}</Title>
        <Form<Settings>
          form={form}
          layout="vertical"
          initialValues={{
            enableNotifications: true,
            sentimentThreshold: 0.5,
            eventConfidenceThreshold: 0.7,
            language: language,
          }}
          onFinish={handleSave}
        >
          <Form.Item
            label={t('settings', 'language')}
            name="language"
          >
            <Select
              value={language}
              onChange={handleLanguageChange}
              options={[
                { value: 'en', label: t('settings', 'english') },
                { value: 'fa', label: t('settings', 'persian') }
              ]}
            />
          </Form.Item>

          <Form.Item
            label={t('settings', 'apiKey')}
            name="apiKey"
            rules={[
              { required: true, message: t('settings', 'apiKeyRequired') }
            ]}
          >
            <Password />
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
            rules={[
              { required: true, message: t('settings', 'thresholdRequired') }
            ]}
          >
            <InputNumber min={0} max={1} step={0.1} />
          </Form.Item>

          <Form.Item
            label={t('settings', 'eventConfidenceThreshold')}
            name="eventConfidenceThreshold"
            rules={[
              { required: true, message: t('settings', 'thresholdRequired') }
            ]}
          >
            <InputNumber min={0} max={1} step={0.1} />
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

export default SettingsComponent; 