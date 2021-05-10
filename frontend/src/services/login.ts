import request from '../utils/request';

export interface BasicResp {
  code: number;
  message: string;
}

export interface HistoryType {
  smile_rate: number;
  lost_face_rate: number;
}

export async function login(phone: string, room: string): Promise<BasicResp> {
  const { data } = await request.post('/login', { phone, room });
  return data;
}

export async function register(phone: string): Promise<BasicResp> {
  const { data } = await request.post('/register', { phone });
  return data;
}

export async function getHistory(phone: string): Promise<HistoryType> {
  const { data } = await request.get(`/history?phone=${phone}`);
  return data;
}
