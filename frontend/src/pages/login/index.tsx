import React from 'react';
import { useHistory } from 'umi';
import { message, notification, Modal } from 'antd';
import ProForm, { ProFormText, ProFormCaptcha } from '@ant-design/pro-form';
import { MobileOutlined, MailOutlined, TagsOutlined } from '@ant-design/icons';
import { login, register } from '@/services/login';
import { useDispatch } from 'react-redux';

export interface LoginData {
  phone: string;
  captcha: string;
  room: string;
}

const Login: React.FC = () => {
  const dispatch = useDispatch();
  const history = useHistory();

  const onFinishHandler = async (value: LoginData) => {
    const resp = await login(value.phone, value.room);
    if (resp.code === -100) {
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
    if (resp.code === 100) {
      notification.success({
        message: '房间已经存在，加入成功!',
      });
    }
    if (resp.code === 0) {
      notification.success({
        message: '房间创建成功!',
        description: '您已经成为该房间管理员!',
      });
    }
    dispatch({ type: 'global/setUserPhone', payload: value.phone });
    dispatch({ type: 'global/setRoom', payload: value.room });
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
        <ProFormText
          fieldProps={{ size: 'large', prefix: <TagsOutlined /> }}
          name="room"
          placeholder="请输入房间号"
          rules={[
            { required: true, message: '请输入五位房间号!' },
            { pattern: /^\d{5}$/, message: '不合法的房间号!' },
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
