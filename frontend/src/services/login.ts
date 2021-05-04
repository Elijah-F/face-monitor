import request from '../utils/request';

export interface BasicResp {
  code: number;
  message: string;
}

export async function login(phone: string, room: string): Promise<BasicResp> {
  const { data } = await request.post('/login', { phone, room });
  return data;
}

export async function register(phone: string): Promise<BasicResp> {
  const { data } = await request.post('/register', { phone });
  return data;
}
