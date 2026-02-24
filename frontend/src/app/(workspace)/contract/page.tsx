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
        <h1>Clause Analysis</h1>
        <p>Rag-powered analysis</p>
        <p className="sub-note">(Focused on Contract Law Act 1872)</p>
      </header>

      <div className="contract-grid">
        {/* LEFT PANEL */}
        <section className="contract-input-panel">
          <textarea
            value={contractText}
            onChange={(e) => setContractText(e.target.value)}
            placeholder="Paste your contract clause here..."
          />

          <button
            className="analyze-btn"
            onClick={handleAnalyze}
            disabled={isPending}
          >
            {isPending ? "Processing..." : "Analyze Contract"}
          </button>
        </section>

        {/* RIGHT PANEL */}
        <section className="contract-results-panel">
          {!data && !isPending && (
            <div className="empty-state">
              <p>Answer Section</p>
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
                <h2>⚖️ Legal Analysis</h2>
                <div className="analysis-text">{data.analysis}</div>
              </div>

              <div className="analysis-card secondary">
                <h3>Relevant Law Sections</h3>
                <div className="law-list">
                  {data.relevant_law_sections?.map((law, index) => (
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
