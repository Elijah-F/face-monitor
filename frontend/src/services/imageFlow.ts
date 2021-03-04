import { request } from '../utils/request';

export async function updateImages() {
  const payload = {};
  const { data } = await request.post('/image_flow/update', JSON.stringify(payload));
  return data;
}
