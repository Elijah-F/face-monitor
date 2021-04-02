import ProLayout, { DefaultFooter } from '@ant-design/pro-layout';
import { SmileOutlined, CrownOutlined, RadarChartOutlined, UserOutlined } from '@ant-design/icons';
import React, { useEffect } from 'react';
import { Link, useHistory, useSelector, useLocation } from 'umi';
import LoginLayout from './LoginLayout';
import { RootState } from '@/store';
import { Avatar } from 'antd';

const complexMenu = [
  {
    path: '/realTime',
    name: 'Real Time',
    icon: <SmileOutlined />,
  },
  {
    path: '/videoFlow',
    name: 'Video Flow',
    icon: <RadarChartOutlined />,
  },
  {
    path: '/imageFlow',
    name: 'Image Flow',
    icon: <CrownOutlined />,
  },
];

const BasicLayout: React.FC = (props) => {
  const userPhone = useSelector((state: RootState) => state.global.userPhone);
  const history = useHistory();
  const location = useLocation();

  // first login in, then balabala...
  useEffect(() => {
    if (userPhone === '') {
      history.push('/login');
    }
  }, [userPhone]);

  if (location.pathname === '/login' || location.pathname === '/register') {
    return <LoginLayout>{props.children}</LoginLayout>;
  }
  return (
    <ProLayout
      title="Face Monitor"
      layout="top"
      menuDataRender={() => complexMenu}
      menuItemRender={(item: any, dom: React.ReactNode) => {
        const { render, path } = item;
        if (render) {
          return render(dom);
        }
        return <Link to={path}>{dom}</Link>;
      }}
      footerRender={() => <DefaultFooter copyright="2021, fufuzhao. All right reserved." links={[]} />}
      rightContentRender={() => <Avatar icon={<UserOutlined />} style={{ marginRight: 30 }} />}
    >
      <div style={{ minHeight: 280, padding: 24, background: '#fff' }}>{props.children}</div>
    </ProLayout>
  );
};

export default BasicLayout;
