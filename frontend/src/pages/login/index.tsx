import { RootState } from '@/store';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Form } from 'antd';

const Login: React.FC = () => {
  const dispatch = useDispatch();
  const userName = useSelector((state: RootState) => state.global.userName);
  const [mode, setMode] = useState('login');
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    setVisible(userName === '');
  }, [userName]);

  return <h1>loginj alxi</h1>;
};

export default Login;
