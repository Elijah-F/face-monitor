import React, { useState } from 'react';
import { getHistory, HistoryType } from '@/services/history';
import { EditOutlined, EllipsisOutlined, SettingOutlined } from '@ant-design/icons';
import { Input, Divider, Row, Col, Card } from 'antd';
import { Bar, Pie } from '@ant-design/charts';

const History: React.FC = () => {
  const [history, setHistory] = useState<HistoryType>();

  const barConfig = {
    style: {
      height: 200,
    },
    xField: 'value',
    yField: 'index',
    seriesField: 'proportion',
    isPercent: true,
    isStack: true,
    label: {
      position: 'middle',
      content: function content(item) {
        return item.value.toFixed(2);
      },
      style: { fill: '#fff' },
    },
  };
  const pieConfig = {
    style: {
      height: 200,
    },
    appendPadding: 10,
    angleField: 'value',
    colorField: 'type',
    radius: 0.8,
    label: {
      type: 'outer',
      content: '{name} {percentage}',
    },
    interactions: [{ type: 'pie-legend-active' }, { type: 'element-active' }],
  };
  return (
    <>
      <Input.Search
        placeholder="input search phone"
        enterButton
        style={{ width: 300 }}
        size="large"
        onSearch={async (phone) => {
          const data = await getHistory(phone);
          setHistory(data);
        }}
      ></Input.Search>
      <Divider />
      <Row gutter={[16, 16]}>
        {history === undefined
          ? null
          : Object.keys(history['bar']).map((element) => {
              console.log(element);
              console.log(history['bar'][element]);
              return (
                <Col key={element} span={6}>
                  <Card
                    actions={[
                      <SettingOutlined key="setting" />,
                      <EditOutlined key="edit" />,
                      <EllipsisOutlined key="ellipsis" />,
                    ]}
                  >
                    <Bar data={history['bar'][element]} {...barConfig} />
                    <Pie data={history['pie'][element]} {...pieConfig} />
                  </Card>
                </Col>
              );
            })}
      </Row>
    </>
  );
};

export default History;
