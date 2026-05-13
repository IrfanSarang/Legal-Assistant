import axiosInstance from "../lib/axiosInstance";
import { QueryRequest, QueryResponse } from "../types/contract";

const BASE_URL = "/api/v1/contract/analyse";

export const analyzeContract = async (
  payload: QueryRequest,
): Promise<QueryResponse> => {
  const { data } = await axiosInstance.post(BASE_URL, payload);
  return data;
};
