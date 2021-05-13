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

export interface ImageHistoryType {
  smile: string[];
  face: string[];
  sleepy: string[];
  speak: string[];
}

export async function getHistory(phone: string): Promise<HistoryType> {
  const { data } = await request.get(`/history?phone=${phone}`);
  return data;
}

export async function getImageHistory(job_id: string): Promise<ImageHistoryType> {
  const { data } = await request.get(`/image_history?job_id=${job_id}`);
  return data;
}
