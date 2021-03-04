import axios from 'axios';

export const request = axios.create({
  baseURL: 'http:127.0.0.1:9527',
});

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
