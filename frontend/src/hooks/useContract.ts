import { useMutation } from "@tanstack/react-query";
import { analyzeContract } from "../api/contract";
import { QueryRequest } from "../types/contract";

export const useAnalyzeContract = () => {
  return useMutation({
    mutationFn: (payload: QueryRequest) => analyzeContract(payload),
  });
};
