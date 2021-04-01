import React from 'react';
import { Layout } from 'antd';
import ProLayout, { DefaultFooter } from '@ant-design/pro-layout';

const { Header, Footer, Content } = Layout;

const SimpleLayout: React.FC = (props) => {
  return (
    <ProLayout
      title="Face Monitor"
      layout="top"
      footerRender={() => <DefaultFooter copyright="2021, fufuzhao. All right reserved." links={[]} />}
    >
      {props.children}
    </ProLayout>
  );
};

export default SimpleLayout;
