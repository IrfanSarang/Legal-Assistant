"use client";

import { useState } from "react";
import { useAnalyzeContract } from "../../../hooks/useContract";
import "./contract.css";

export default function ContractPage() {
  const [contractText, setContractText] = useState("");
  const { mutate, data, isPending } = useAnalyzeContract();

  const handleAnalyze = () => {
    if (!contractText.trim()) return;
    mutate({ contract_text: contractText });
  };

  return (
    <main className="contract-container">
      <header className="contract-header">
        <h1>Contract Analysis</h1>
        <p>AI-Powered Risk & Compliance Review</p>
        <p>(Focused on contract law act 1872)</p>
      </header>

      <div className="contract-grid">
        {/* Input Section */}
        <section className="contract-input-panel">
          <textarea
            value={contractText}
            onChange={(e) => setContractText(e.target.value)}
            placeholder="Paste your contract clause here.."
            rows={20}
          />
          <button
            className="analyze-btn"
            onClick={handleAnalyze}
            disabled={isPending}
          >
            {isPending ? "Processing..." : "Analyze Contract"}
          </button>
        </section>

        {/* Results Section */}
        <section className="contract-results-panel">
          {!data && !isPending && (
            <div className="empty-state">
              <p>Upload or paste a contract to see the legal breakdown.</p>
            </div>
          )}

          {isPending && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Extracting legal insights...</p>
            </div>
          )}

          {data && (
            <div className="analysis-content">
              <div className="analysis-card primary">
                <h2>
                  <span className="icon">⚖️</span> Legal Analysis
                </h2>
                <div className="analysis-text">{data.analysis}</div>
              </div>

              <div className="analysis-card secondary">
                <h3>Relevant Law Sections</h3>
                <div className="law-list">
                  {data.relevant_law_sections.map((law, index) => (
                    <div key={index} className="law-item">
                      <span className="check">✔</span>
                      <p>{law.chunk_text}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
