import { useMutation } from "@tanstack/react-query";
import { analyzeContract } from "../api/contract";
import { ContractAnalysisRequest } from "../types/contract";

export const useAnalyzeContract = () => {
  return useMutation({
    mutationFn: (payload: ContractAnalysisRequest) => analyzeContract(payload),
  });
};
