import request from '../utils/request';

export interface HistoryItem {
  smile_rate: number;
  lost_face_rate: number;
  speak: number;
}

export interface HistoryType {
  job_id: HistoryItem;
}

export async function getHistory(phone: string): Promise<HistoryType> {
  const { data } = await request.get(`/history?phone=${phone}`);
  return data;
}
