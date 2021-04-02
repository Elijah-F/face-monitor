import axios from 'axios';

const request = axios.create({
  baseURL: 'http://192.168.12.133:8998/api',
});

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

export default request;
