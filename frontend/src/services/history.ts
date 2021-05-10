import request from '../utils/request';

export interface HistoryBarItem {
  index: string;
  proportion: string;
  value: number;
}
export interface HistoryPieItem {
  type: string;
  value: number;
}

export interface HistoryType {
  bar: any;
  pie: any;
  job_date: any;
}

export async function getHistory(phone: string): Promise<HistoryType> {
  const { data } = await request.get(`/history?phone=${phone}`);
  return data;
}
