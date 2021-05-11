import React, { useEffect, useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { useInterval, useTimeout } from '@/utils/hooks';
import { Popconfirm, Button, Divider, Space, Select, Card, Row, Col, notification } from 'antd';
import { PoweroffOutlined, EditOutlined, EllipsisOutlined, SettingOutlined } from '@ant-design/icons';
import useWebSocket from 'react-use-websocket';
import { useSelector } from 'umi';
import { RootState } from '@/store';

const RealTime: React.FC = () => {
  const webcamRef = useRef();
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [delay, setDelay] = useState<number>(100);
  const [span, setSpan] = useState<number>(4);
  const [monitorTime, setMonitorTime] = useState<number>(10);
  const [popVisible, setPopVisible] = useState<boolean>(false);
  const [imgSrc, setImgSrc] = useState({});
  const { userRoom, userPhone, isAdmin } = useSelector((state: RootState) => state.global);

  const { sendMessage, lastMessage } = useWebSocket(
    `ws://192.168.12.133:9527/real_time?phone=${userPhone}&room=${userRoom}`,
  );

  useInterval(
    () => {
      const imageSrc = webcamRef.current.getScreenshot();
      if (!isAdmin) {
        sendMessage(imageSrc);
      } else {
        sendMessage('admin');
      }
    },
    isPlaying ? delay : null,
  );

  const monitorFinish = () => {
    setIsPlaying(false);
    setPopVisible(false);
    sendMessage('monitor_finish');
    notification.success({ message: '监控已结束，请到后台查询结果.', duration: null });
  };

  useTimeout(monitorFinish, isPlaying ? monitorTime * 60 * 1000 : null);

  useEffect(() => {
    if (lastMessage) {
      const tmp = imgSrc;
      const lastData = JSON.parse(lastMessage.data);
      Object.keys(lastData).forEach((element) => (tmp[element] = lastData[element]));
      setImgSrc(tmp);
    }
  }, [lastMessage]);

  return (
    <>
      <Space>
        <Select
          defaultValue="4"
          onChange={(value) => {
            setSpan(Number(value));
          }}
        >
          <Select.Option value="8">疏松排列</Select.Option>
          <Select.Option value="4">紧密排列</Select.Option>
        </Select>
        <Select
          defaultValue="200"
          onChange={(value) => {
            setDelay(Number(value));
          }}
        >
          <Select.Option value="50" disabled>
            20FPS(慎用)
          </Select.Option>
          <Select.Option value="100">10FPS</Select.Option>
          <Select.Option value="200">5FPS</Select.Option>
        </Select>
        <Select
          disabled={isPlaying}
          defaultValue="60"
          onChange={(value) => {
            setMonitorTime(Number(value));
          }}
        >
          <Select.Option value="1">1min</Select.Option>
          <Select.Option value="10">10min</Select.Option>
          <Select.Option value="60">60min</Select.Option>
          <Select.Option value="90">90min</Select.Option>
        </Select>
        <Popconfirm
          title="是否提前监控结束？"
          visible={popVisible}
          onConfirm={monitorFinish}
          onCancel={() => {
            setPopVisible(false);
          }}
        >
          <Button
            type="primary"
            danger={isPlaying}
            icon={<PoweroffOutlined />}
            onClick={() => {
              if (!isPlaying) {
                // click START
                setIsPlaying(!isPlaying);
                sendMessage('monitor_begin');
              } else {
                // click STOP
                setPopVisible(true);
              }
            }}
          >
            {isPlaying ? 'STOP' : 'START'}
          </Button>
        </Popconfirm>
      </Space>
      <Divider />
      <Row gutter={[8, 8]}>
        <Col span={span}>
          <Card
            cover={<Webcam style={{ display: 'block' }} audio={false} ref={webcamRef} screenshotFormat="image/webp" />}
            actions={[
              <SettingOutlined key="setting" />,
              <EditOutlined key="edit" />,
              <EllipsisOutlined key="ellipsis" />,
            ]}
          >
            <Card.Meta title="native camerel" description="This is the description" />
          </Card>
        </Col>
        {Object.keys(imgSrc).map((element) => (
          <Col key={element} span={span}>
            <Card
              key={element}
              cover={<img src={imgSrc[element]} />}
              actions={[
                <SettingOutlined key="setting" />,
                <EditOutlined key="edit" />,
                <EllipsisOutlined key="ellipsis" />,
              ]}
            >
              <Card.Meta title={element} description="This is the description" />
            </Card>
          </Col>
        ))}
      </Row>
    </>
  );
};

export default RealTime;
