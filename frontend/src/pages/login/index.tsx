import React from 'react';
import { message } from 'antd';
import ProForm, { ProFormText, ProFormCaptcha } from '@ant-design/pro-form';
import { MobileOutlined, MailOutlined } from '@ant-design/icons';

const Login: React.FC = () => {
  return (
    <div style={{ width: 330, margin: 'auto' }}>
      <ProForm
        onFinish={async () => {
          // await waitTime(2000);
          message.success('提交成功');
        }}
        submitter={{
          searchConfig: { submitText: '登录' },
          render: (_, dom) => dom.pop(),
          submitButtonProps: { size: 'large', style: { width: '100%' } },
        }}
      >
        <h1 style={{ textAlign: 'center' }}>
          <img
            style={{ height: '44px', marginRight: 16 }}
            alt="logo"
            src="https://gw.alipayobjects.com/zos/rmsportal/KDpgvguMpGfqaHPjicRK.svg"
          />
          注意力监测系统
        </h1>
        <div style={{ marginTop: 12, textAlign: 'center', marginBottom: 40 }}>
          旨在提供轻量、便携和易于操作的监控系统！
        </div>
        <ProFormText
          fieldProps={{ size: 'large', prefix: <MobileOutlined /> }}
          name="phone"
          placeholder="请输入手机号"
          rules={[
            { required: true, message: '请输入手机号!' },
            { pattern: /^1\d{10}$/, message: '不合法的手机号格式!' },
          ]}
        />
        <ProFormCaptcha
          fieldProps={{ size: 'large', prefix: <MailOutlined /> }}
          captchaProps={{ size: 'large' }}
          phoneName="phone"
          name="captcha"
          rules={[{ required: true, message: '请输入验证码' }]}
          placeholder="请输入验证码"
          onGetCaptcha={async (phone) => {
            // await waitTime(1000);
            message.success(`手机号 ${phone} 验证码发送成功!`);
          }}
        />
      </ProForm>
    </div>
  );
};

export default Login;
