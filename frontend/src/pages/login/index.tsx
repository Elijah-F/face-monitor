import React from 'react';
import { useHistory } from 'umi';
import { message, Button, Modal } from 'antd';
import ProForm, { ProFormText, ProFormCaptcha } from '@ant-design/pro-form';
import { MobileOutlined, MailOutlined } from '@ant-design/icons';
import { login, register } from '@/services/login';
import { useDispatch } from 'react-redux';

export interface LoginData {
  phone: string;
  captcha: string;
}

const Login: React.FC = () => {
  const dispatch = useDispatch();
  const history = useHistory();

  const onFinishHandler = async (value: LoginData) => {
    const resp = await login(value.phone);
    if (resp.code !== 0) {
      Modal.confirm({
        title: 'Account is not existed!',
        content: 'Account is not existed! Whether to register with the current phone number?',
        cancelText: 'cancel',
        okText: 'register',
        cancelButtonProps: { danger: true },
        okButtonProps: { ghost: true },
        onOk: async () => {
          const resp = await register(value.phone);
          if (resp.code !== 0) {
            message.error(resp.message);
            return;
          }
          message.info('register success!');
        },
      });
      return;
    }
    dispatch({ type: 'global/setUserPhone', payload: value.phone });
    history.push('/realTime');
  };

  return (
    <div style={{ width: 330, margin: 'auto' }}>
      <ProForm
        onFinish={onFinishHandler}
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
            message.success(`手机号 ${phone} 验证码发送成功!`);
          }}
        />
      </ProForm>
    </div>
  );
};

export default Login;
