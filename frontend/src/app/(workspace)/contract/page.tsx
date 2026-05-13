"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { useAnalyzeContract } from "../../../hooks/useContract";
import "./contract.css";

export default function ContractPage() {
  const [query, setQuery] = useState("");
  const { mutate, data, isPending } = useAnalyzeContract();

  const handleAnalyze = () => {
    if (!query.trim()) return;
    mutate({ query });
  };

  return (
    <main className="contract-container">
      <header className="contract-header">
        <div className="header-badge">Contract Intelligence</div>
        <h1>Contract Law Assistant</h1>
        <p>Strategic analysis and clause review powered by AI.</p>
        <span className="sub-note">Grounding: Contract Law & Precedents</span>
      </header>

      <div className="contract-grid">
        {/* LEFT PANEL */}
        <section className="contract-input-panel">
          <div className="input-group">
            <label htmlFor="contract-query">Clause or Question</label>
            <textarea
              id="contract-query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., Analyze the termination clause for potential risks..."
            />
          </div>
          <button
            className={`analyze-btn ${isPending ? 'loading' : ''}`}
            onClick={handleAnalyze}
            disabled={isPending}
          >
            {isPending ? (
              <>
                <span className="spinner"></span>
                Processing...
              </>
            ) : "Analyze Contract"}
          </button>
        </section>

        {/* RIGHT PANEL */}
        <section className="contract-results-panel">
          <div className="panel-header">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            <h3>Legal Insights</h3>
          </div>

          <div className="panel-content">
            {/* Empty state */}
            {!data && !isPending && (
              <div className="state-text empty-state">
                <p>Submit a clause to begin the analysis.</p>
              </div>
            )}

            {/* Loading state */}
            {isPending && (
              <div className="state-text loading-state">
                <div className="shimmer"></div>
                <p>Extracting legal insights and reviewing precedents...</p>
              </div>
            )}

            {/* Result */}
            {data && (
              <div className="analysis-content">
                <div className="analysis-card-premium">
                  <div className="card-accent"></div>
                  <div className="analysis-text markdown-body">
                    <ReactMarkdown>{data.answer}</ReactMarkdown>
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>
      </div>
    </main>
  );
}
