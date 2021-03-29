import ProLayout, { DefaultFooter } from '@ant-design/pro-layout';
import { SmileOutlined, CrownOutlined, RadarChartOutlined } from '@ant-design/icons';
import Login from './Login';
import React from 'react';
import { Link } from 'umi';

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

const BasicLayout: React.FC = (props) => (
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
    footerRender={() => <DefaultFooter copyright="2021, fufuzhao. All right reserved" links={[]} />}
  >
    <Login />
    <div style={{ minHeight: 280, padding: 24, background: '#fff' }}>{props.children}</div>
  </ProLayout>
);

export default BasicLayout;
