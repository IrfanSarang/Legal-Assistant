import { useMutation } from "@tanstack/react-query";
import { fetchLegalAnalysis } from "@/api/legal";
import { QueryRequest, QueryResponse } from "@/types/legal";

export const useAnalyseQuestion = () => {
  return useMutation<QueryResponse, Error, QueryRequest>({
    mutationFn: fetchLegalAnalysis,
  });
};
