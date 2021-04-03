import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { useInterval } from '@/utils/hooks';
import { Button } from 'antd';

const RealTime: React.FC = () => {
  const webcamRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [delay, setDelay] = useState<number>(500);

  useInterval(
    () => {
      const imageSrc = webcamRef.current.getScreenshot();
      // TODO: send imageSrc to backend using sigle connect
    },
    isPlaying ? delay : null,
  );

  return (
    <>
      <Button
        type="primary"
        onClick={() => {
          setIsPlaying(true);
        }}
      >
        开始
      </Button>
      <Button
        type="primary"
        onClick={() => {
          setIsPlaying(false);
        }}
      >
        结束
      </Button>
      <Webcam style={{ display: 'block' }} audio={false} ref={webcamRef} screenshotFormat="image/webp" />
    </>
  );
};

export default RealTime;
