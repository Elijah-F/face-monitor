import React, { useState } from 'react';
import { getHistory } from '@/services/history';
import { Input, Divider } from 'antd';

const History: React.FC = () => {
  const [history, setHistory] = useState();

  return (
    <>
      <Input.Search
        placeholder="input search phone"
        enterButton
        style={{ width: 300 }}
        size="large"
        onSearch={async (phone) => {
          const data = await getHistory(phone);
        }}
      ></Input.Search>
      <Divider />
    </>
  );
};

export default History;
