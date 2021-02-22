import { notification } from 'antd';

export default (description: any, title = '错误') => {
  notification.error({ description: String(description), message: title, duration: null });
  console.log(description);
};
