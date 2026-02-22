"use client";
import React, { useState } from "react";
import "./legal.css";
import { useAnalyseQuestion } from "@/hooks/uselegal";

const LegalPage: React.FC = () => {
  const [question, setQuestion] = useState("");
  const mutation = useAnalyseQuestion();

  const handleAnalyse = () => {
    if (question.trim() === "") return;
    mutation.mutate({ query: question, top_k: 3 });
  };

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
            <h3>Answer</h3>
            {mutation.data?.answer ? (
              Array.isArray(mutation.data.answer) ? (
                mutation.data.answer.map((item: any, idx: number) => (
                  <div key={idx} className="answer-block">
                    <p>{item.text}</p>
                    {item.annotations && item.annotations.length > 0 && (
                      <ul>
                        {item.annotations.map((anno: string, i: number) => (
                          <li key={i}>{anno}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                ))
              ) : (
                <p>{mutation.data.answer}</p>
              )
            ) : mutation.isPending ? (
              <p>Loading answer...</p>
            ) : (
              <p>No answer yet.</p>
            )}
          </div>

          {/* Retrieved Chunks Section */}
          <div className="chunks-section">
            <h3>Retrieved Chunks</h3>
            {mutation.data?.retrieved_chunks &&
            mutation.data.retrieved_chunks.length > 0 ? (
              mutation.data.retrieved_chunks.map((chunk: any, idx: number) => (
                <div key={idx} className="chunk-block">
                  <p>
                    <strong>Section {chunk.section_number}</strong>
                    {chunk.title && `: ${chunk.title}`}
                  </p>
                  <p>{chunk.chunk_text}</p>

                  {chunk.illustrations && chunk.illustrations.length > 0 && (
                    <div>
                      <strong>Illustrations:</strong>
                      <ul>
                        {chunk.illustrations.map((illu: string, i: number) => (
                          <li key={i}>{illu}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {chunk.explanations && chunk.explanations.length > 0 && (
                    <div>
                      <strong>Explanations:</strong>
                      <ul>
                        {chunk.explanations.map((exp: string, i: number) => (
                          <li key={i}>{exp}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {chunk.provisos && chunk.provisos.length > 0 && (
                    <div>
                      <strong>Provisos:</strong>
                      <ul>
                        {chunk.provisos.map((prov: string, i: number) => (
                          <li key={i}>{prov}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))
            ) : mutation.isPending ? (
              <p>Loading chunks...</p>
            ) : (
              <p>No chunks retrieved.</p>
            )}
          </div>
        </section>
      </section>
    </main>
  );
};

export default LegalPage;
