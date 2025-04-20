import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import {
  DashboardOutlined,
  BarChartOutlined,
  AlertOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import { Link } from 'react-router-dom';

// Components
import Dashboard from './components/Dashboard';
import SentimentAnalysis from './components/SentimentAnalysis';
import EventDetection from './components/EventDetection';
import RumorAnalysis from './components/RumorAnalysis';
import Settings from './components/Settings';

const { Header, Sider, Content } = Layout;

const App: React.FC = () => {
  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider width={200} theme="light">
          <div className="logo" style={{ height: 32, margin: 16, background: 'rgba(0, 0, 0, 0.2)' }} />
          <Menu
            mode="inline"
            defaultSelectedKeys={['1']}
            style={{ height: '100%', borderRight: 0 }}
          >
            <Menu.Item key="1" icon={<DashboardOutlined />}>
              <Link to="/">Dashboard</Link>
            </Menu.Item>
            <Menu.Item key="2" icon={<BarChartOutlined />}>
              <Link to="/sentiment">Sentiment Analysis</Link>
            </Menu.Item>
            <Menu.Item key="3" icon={<AlertOutlined />}>
              <Link to="/events">Event Detection</Link>
            </Menu.Item>
            <Menu.Item key="4" icon={<AlertOutlined />}>
              <Link to="/rumors">Rumor Analysis</Link>
            </Menu.Item>
            <Menu.Item key="5" icon={<SettingOutlined />}>
              <Link to="/settings">Settings</Link>
            </Menu.Item>
          </Menu>
        </Sider>
        <Layout>
          <Header style={{ background: '#fff', padding: 0 }} />
          <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 280 }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/sentiment" element={<SentimentAnalysis />} />
              <Route path="/events" element={<EventDetection />} />
              <Route path="/rumors" element={<RumorAnalysis />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </Router>
  );
};

export default App; 