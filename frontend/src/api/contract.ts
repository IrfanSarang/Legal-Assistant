import axiosInstance from "../lib/axiosInstance";
import {
  ContractAnalysisRequest,
  ContractAnalysisResponse,
} from "../types/contract";

const BASE_URL = "/api/v1/contract/analyze";

export const analyzeContract = async (
  payload: ContractAnalysisRequest,
): Promise<ContractAnalysisResponse> => {
  const { data } = await axiosInstance.post(BASE_URL, payload);
  return data;
};
