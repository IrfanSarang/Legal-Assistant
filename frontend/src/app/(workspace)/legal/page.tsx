"use client";
import React, { useState } from "react";
import "./legal.css";
import { useAnalyseQuestion } from "@/hooks/uselegal";
import ReactMarkdown from "react-markdown";

interface ChunkResult {
  section_number: string;
  title: string;
  chunk_type: string;
  score: number;
  chunk_text: string;
}

interface LegalQueryResponse {
  question: string;
  answer: any;
  retrieved_sections: string[];
  retrieved_chunks: ChunkResult[];
}

// ✅ Safely convert any answer format to plain string
function extractAnswerText(answer: any): string {
  if (!answer) return "";

  // Already a plain string
  if (typeof answer === "string") return answer;

  // Array of content blocks — DeepSeek sometimes returns this
  if (Array.isArray(answer)) {
    return answer
      .map((item: any) => {
        if (typeof item === "string") return item;
        if (item?.text) return item.text;
        if (item?.content) {
          if (typeof item.content === "string") return item.content;
          if (Array.isArray(item.content)) {
            return item.content
              .map((c: any) => c?.text || c?.value || "")
              .join("");
          }
        }
        return "";
      })
      .filter(Boolean)
      .join("\n");
  }

  // Single object with text/content field
  if (typeof answer === "object") {
    if (answer.text) return String(answer.text);
    if (answer.content) return String(answer.content);
    if (answer.value) return String(answer.value);
    // Last resort
    return JSON.stringify(answer);
  }

  return String(answer);
}

const LegalPage: React.FC = () => {
  const [question, setQuestion] = useState("");
  const mutation = useAnalyseQuestion();
  const data = mutation.data as LegalQueryResponse | undefined;

  const handleAnalyse = () => {
    if (question.trim() === "") return;
    mutation.mutate({ query: question });
  };

  // ✅ Extract safe string from whatever answer format comes back
  const answerText = extractAnswerText(data?.answer);

  return (
    <main className="legal-container">
      <section className="legal-header">
        <h1>Legal Intelligence</h1>
        <p>RAG-based Analysis</p>
        <p>(Focused on Criminal law Domain)</p>
      </section>

      <section className="legal-main">
        {/* Input Section */}
        <section className="main-1">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Enter your legal question here..."
            rows={8}
          />
          <button onClick={handleAnalyse} disabled={mutation.isPending}>
            {mutation.isPending ? "Analysing..." : "Analyse"}
          </button>
        </section>

        {/* Output Sections */}
        <section className="main-2">
          {/* Answer Section */}
          <div className="answer-section">
            <h3>Legal Analysis</h3>

            {answerText ? (
              <div className="answer-block">
                <div className="markdown-body">
                  <ReactMarkdown>{answerText}</ReactMarkdown>
                </div>
              </div>
            ) : mutation.isPending ? (
              <p className="state-text">Analysing your query...</p>
            ) : (
              <p className="state-text">No answer yet. Ask a legal question.</p>
            )}
          </div>

          {/* Retrieved Chunks Section */}
          <div className="chunks-section">
            <h3>Retrieved Legal Sections</h3>

            {data?.retrieved_chunks && data.retrieved_chunks.length > 0 ? (
              data.retrieved_chunks.map((chunk: ChunkResult, idx: number) => (
                <div key={idx} className="chunk-block">
                  {/* Section Header */}
                  <div className="chunk-header">
                    <span className="chunk-section-badge">
                      Section {chunk.section_number}
                    </span>
                    <span className="chunk-type-badge">{chunk.chunk_type}</span>
                    <span className="chunk-score">
                      Score: {chunk.score?.toFixed(2)}
                    </span>
                  </div>

                  {/* Title */}
                  {chunk.title && <p className="chunk-title">{chunk.title}</p>}

                  {/* Chunk Text */}
                  <div className="chunk-text">
                    <ReactMarkdown>{String(chunk.chunk_text)}</ReactMarkdown>
                  </div>
                </div>
              ))
            ) : mutation.isPending ? (
              <p className="state-text">Loading sections...</p>
            ) : (
              <p className="state-text">No sections retrieved yet.</p>
            )}
          </div>
        </section>
      </section>
    </main>
  );
};

export default LegalPage;
