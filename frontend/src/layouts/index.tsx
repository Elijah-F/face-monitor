import ProLayout, { DefaultFooter, PageContainer } from '@ant-design/pro-layout';
import ProCard from '@ant-design/pro-card';
import complexMenu from './complexMenu';
import React from 'react';
import { Link } from 'umi';
import './index.less';

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
    <div className="site-layout-content">{props.children}</div>
  </ProLayout>
);

export default BasicLayout;
