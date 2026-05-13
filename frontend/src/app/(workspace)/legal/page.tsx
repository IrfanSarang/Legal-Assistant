"use client";
import React, { useState } from "react";

import { useAnalyseQuestion } from "@/hooks/uselegal";
import ReactMarkdown from "react-markdown";
import "./legal.css";

const LegalPage: React.FC = () => {
  const [question, setQuestion] = useState("");
  const mutation = useAnalyseQuestion();

  const handleAnalyse = () => {
    if (question.trim() === "") return;
    mutation.mutate({ query: question });
  };

  const answerText = mutation.data?.answer ?? "";

  return (
    <main className="legal-container">
      <header className="legal-header">
        <div className="header-badge">AI Legal Intelligence</div>
        <h1>Criminal Law Analysis</h1>
        <p>Grounded insights based on the BNS 2023 legal framework.</p>
      </header>

      <section className="legal-main">
        {/* Input Section */}
        <div className="main-1">
          <div className="input-group">
            <label htmlFor="legal-query">Describe the scenario or ask a question</label>
            <textarea
              id="legal-query"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., What are the legal implications of...?"
              rows={8}
            />
          </div>
          
          <button 
            className={`analyse-btn ${mutation.isPending ? 'loading' : ''}`}
            onClick={handleAnalyse} 
            disabled={mutation.isPending}
          >
            {mutation.isPending ? (
              <>
                <span className="spinner"></span>
                Analysing...
              </>
            ) : (
              "Generate Analysis"
            )}
          </button>

          {mutation.isError && (
            <div className="error-message">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {mutation.error?.message ?? "Analysis failed. Please check your connection."}
            </div>
          )}
        </div>

        {/* Output Section */}
        <div className="main-2">
          <div className="answer-section">
            <div className="answer-header">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>
              </svg>
              <h3>Legal Analysis Result</h3>
            </div>

            <div className="answer-content">
              {answerText ? (
                <div className="answer-block">
                  <div className="markdown-body">
                    <ReactMarkdown>{answerText}</ReactMarkdown>
                  </div>
                </div>
              ) : mutation.isPending ? (
                <div className="state-text loading-state">
                  <div className="shimmer"></div>
                  <p>Searching legal database and generating response...</p>
                </div>
              ) : (
                <div className="state-text empty-state">
                  <p>Your analysis will appear here after you submit a query.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>
    </main>
  );
};

export default LegalPage;
