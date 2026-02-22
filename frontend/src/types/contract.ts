export interface ContractAnalysisRequest {
  contract_text: string;
  top_k?: number;
}

export interface RelevantLawSection {
  chunk_text: string;
  // add other fields if backend returns them
}

export interface ContractAnalysisResponse {
  analysis: string;
  relevant_law_sections: RelevantLawSection[];
}
