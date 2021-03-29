import { RootState } from '@/store';
import { Modal } from 'antd';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Form } from 'antd';

const LoginForm: React.FC = () => {
  return <h1>登陆</h1>;
};

const RegisterForm: React.FC = () => {
  return (
    <Form>
      <Form.Item></Form.Item>
      <Form.Item></Form.Item>
      <Form.Item></Form.Item>
    </Form>
  );
};

const Login: React.FC = () => {
  const dispatch = useDispatch();
  const userName = useSelector((state: RootState) => state.global.userName);
  const [mode, setMode] = useState('login');
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    setVisible(userName === '');
  }, [userName]);

  return (
    <Modal
      title={`${mode}`}
      visible={visible}
      onOk={() => dispatch({ type: 'global/setUserName', payload: 'myname' })}
      footer={null}
    >
      {(() => {
        return mode === 'login' ? <LoginForm /> : <RegisterForm />;
      })()}
    </Modal>
  );
};

export default Login;
