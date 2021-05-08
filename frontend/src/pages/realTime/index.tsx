import React, { useEffect, useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { useInterval } from '@/utils/hooks';
import { Button, Divider, Space, Select, Card, Row, Col } from 'antd';
import { PoweroffOutlined, EditOutlined, EllipsisOutlined, SettingOutlined } from '@ant-design/icons';
import useWebSocket from 'react-use-websocket';
import { useSelector } from 'umi';
import { RootState } from '@/store';

const RealTime: React.FC = () => {
  const webcamRef = useRef();
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [delay, setDelay] = useState<number>(100);
  const [span, setSpan] = useState<number>(4);
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
          <Select.Option value="4">紧密排列</Select.Option>
          <Select.Option value="8">疏松排列</Select.Option>
        </Select>
        <Select
          defaultValue="200"
          onChange={(value) => {
            setDelay(Number(value));
          }}
        >
          <Select.Option value="200">5FPS</Select.Option>
          <Select.Option value="100">10FPS</Select.Option>
          <Select.Option value="50" disabled>
            20FPS(慎用)
          </Select.Option>
        </Select>
        <Button
          type="primary"
          danger={isPlaying}
          icon={<PoweroffOutlined />}
          onClick={() => {
            setIsPlaying(!isPlaying);
          }}
        >
          {isPlaying ? 'STOP' : 'START'}
        </Button>
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
