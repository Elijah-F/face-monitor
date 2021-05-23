import React, { useState } from 'react';
import { Upload, message, Row, Col } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import { Pie } from '@ant-design/charts';

const { Dragger } = Upload;

const VideoFlow: React.FC = () => {
  const [resp, setResp] = useState();

  const pieConfig = {
    style: {
      height: 300,
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
      <Dragger
        name="video"
        action="http://192.168.12.133:8998/api/video_flow"
        onChange={(info) => {
          const { status } = info.file;
          if (status !== 'uploading') {
            console.log(info.file, info.fileList);
          }
          if (status === 'done') {
            message.success(`${info.file.name} file uploaded successfully.`);
            setResp(info.file.response);
          } else if (status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
          }
        }}
      >
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">Click or drag file to this area to upload</p>
        <p className="ant-upload-hint">
          Support for a single or bulk upload. Strictly prohibit from uploading company data or other band files
        </p>
      </Dragger>
      {resp === undefined ? null : <Pie data={resp['pie']} {...pieConfig} />}
      {resp === undefined
        ? null
        : Object.keys(resp['image']).map((element) => {
            return (
              <Row gutter={[16, 16]} key={element}>
                {resp['image'][element].map((ele) => {
                  return (
                    <Col span={4}>
                      <img width="100%" src={ele} key={ele} />
                    </Col>
                  );
                })}
              </Row>
            );
          })}
    </>
  );
};

export default VideoFlow;
