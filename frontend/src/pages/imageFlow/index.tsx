import React from 'react';
import { useState } from 'react';
import { Upload, Timeline, Divider, message } from 'antd';
import { InboxOutlined, ClockCircleOutlined } from '@ant-design/icons';

const { Dragger } = Upload;

const ImageFlow: React.FC = () => {
  const [imageList, setImageList] = useState<any[]>([]);

  return (
    <>
      <Dragger
        name="image"
        action="http://192.168.12.133:8998/api/image_flow"
        listType="picture-card"
        multiple={true}
        fileList={imageList}
        onChange={(info: any) => {
          const { status } = info.file;
          if (status === 'done') {
            message.success(`${info.file.name} file uploaded successfully.`);
          } else if (status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
          }
          setImageList([...info.fileList]);
        }}
      >
        <p className="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p className="ant-upload-text">Click or drag file to this area to upload</p>
        <p className="ant-upload-hint">Support for a single or bulk upload. Please carefully upload private data.</p>
      </Dragger>

      <Divider orientation="left"></Divider>

      <Timeline mode="alternate">
        <Timeline.Item dot={<ClockCircleOutlined style={{ fontSize: '16px' }} />}>
          The analysis results are shown below.
        </Timeline.Item>

        {imageList.map((val, index) => {
          let colorList = ['red', 'green', 'orange', 'blue'];
          if (val.status == 'done') {
            return (
              <Timeline.Item color={colorList[index % colorList.length]} key={val.uid}>
                {val.name} {val.response.job_id}
              </Timeline.Item>
            );
          }
        })}
      </Timeline>
    </>
  );
};

export default ImageFlow;
