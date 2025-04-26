import React from 'react';
import { Layout, Menu } from 'antd';
import { DashboardOutlined, BarChartOutlined, AlertOutlined } from '@ant-design/icons';
import Dashboard from './components/Dashboard';
import SentimentAnalysis from './components/SentimentAnalysis';
import RumorAnalysis from './components/RumorAnalysis';

const { Header, Content, Sider } = Layout;

const App: React.FC = () => {
  const [selectedMenu, setSelectedMenu] = React.useState('dashboard');

  const renderContent = () => {
    switch (selectedMenu) {
      case 'dashboard':
        return <Dashboard />;
      case 'sentiment':
        return <SentimentAnalysis />;
      case 'rumors':
        return <RumorAnalysis />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ padding: 0, background: '#fff' }}>
        <div style={{ float: 'left', width: 120, height: 31, margin: '16px 24px 16px 0', background: 'rgba(0, 0, 0, 0.2)' }} />
        <h1 style={{ color: '#001529', margin: 0, padding: '0 24px', lineHeight: '64px' }}>
          Iranian Stock Sentiment Analysis
        </h1>
      </Header>
      <Layout>
        <Sider width={200} style={{ background: '#fff' }}>
          <Menu
            mode="inline"
            defaultSelectedKeys={['dashboard']}
            style={{ height: '100%', borderRight: 0 }}
            onSelect={({ key }) => setSelectedMenu(key)}
          >
            <Menu.Item key="dashboard" icon={<DashboardOutlined />}>
              Dashboard
            </Menu.Item>
            <Menu.Item key="sentiment" icon={<BarChartOutlined />}>
              Sentiment Analysis
            </Menu.Item>
            <Menu.Item key="rumors" icon={<AlertOutlined />}>
              Rumor Analysis
            </Menu.Item>
          </Menu>
        </Sider>
        <Layout style={{ padding: '24px' }}>
          <Content
            style={{
              background: '#fff',
              padding: 24,
              margin: 0,
              minHeight: 280,
            }}
          >
            {renderContent()}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
};

export default App; 