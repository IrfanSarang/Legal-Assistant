export interface QueryRequest {
  query: string;
  top_k?: number;
}

export interface ChunkResponse {
  section_number: string;
  title: string;
  chunk_index: number;
  chunk_text: string;
  illustrations: string[];
  explanations: string[];
  provisos: string[];
}

export interface QueryResponse {
  question: string;
  answer: string;
  retrieved_chunks: ChunkResponse[];
}
