import React, { useEffect, useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { useInterval } from '@/utils/hooks';
import { Button, TimePicker, Divider, Space, Select, Card, Row } from 'antd';
import { PoweroffOutlined } from '@ant-design/icons';

const RealTime: React.FC = () => {
  const webcamRef = useRef();
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [delay, setDelay] = useState<number>(100);
  const [imgSrc, setImgSrc] = useState();
  const [ws, setWs] = useState<WebSocket | null>(null);

  useInterval(
    () => {
      const imageSrc = webcamRef.current.getScreenshot();
      setImgSrc(imageSrc);
      ws?.send(imageSrc);
    },
    isPlaying ? delay : null,
  );

  useEffect(() => {
    setWs(new WebSocket('ws://192.168.12.133:9527/real_time'));
    if (ws) {
      ws.onmessage = (evt) => {
        console.log(evt);
      };
    }
    return () => {
      ws?.close();
      setWs(null);
    };
  }, [setWs]);

  return (
    <>
      <Space>
        <TimePicker />
        <Select
          defaultValue="100"
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

      <Row>
        <Card>
          <Webcam style={{ display: 'block' }} audio={false} ref={webcamRef} screenshotFormat="image/webp" />
        </Card>
        <Card>
          <img src={imgSrc} />
        </Card>
      </Row>
    </>
  );
};

export default RealTime;
