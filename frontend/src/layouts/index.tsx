import ProLayout, { DefaultFooter } from '@ant-design/pro-layout';
import complexMenu from './complexMenu';
import React from 'react';
import { Link } from 'umi';
import './index.css';

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
