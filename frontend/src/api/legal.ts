import { QueryRequest, QueryResponse } from "@/types/legal";
import axiosInstance from "@/lib/axiosInstance";

const API_URL = "/api/v1/legal/query";

export const fetchLegalAnalysis = async (
  payload: QueryRequest,
): Promise<QueryResponse> => {
  const res = await axiosInstance.post<QueryResponse>(API_URL, payload);
  return res.data;
};
