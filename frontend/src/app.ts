import { notification } from 'antd';

const notifyError = (description: any, title = 'dva create error!') => {
  notification.error({ description: String(description), message: title, duration: null });
  console.log(description);
};

// docs: https://umijs.org/zh-CN/plugins/plugin-dva
export const dva = {
  config: {
    // namespacePrefixWarning: false,
    onError(err: Error) {
      notifyError(err.message);
    },
  },
};
