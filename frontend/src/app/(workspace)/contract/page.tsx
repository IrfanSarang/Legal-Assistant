"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
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
          {/* Empty state */}
          {!data && !isPending && (
            <div className="empty-state">
              <p>Answer Section</p>
            </div>
          )}

          {/* Loading state */}
          {isPending && (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Extracting legal insights...</p>
            </div>
          )}

          {/* Results */}
          {data && (
            <div className="analysis-content">
              {/* FIX 1: ReactMarkdown renders ** bold, ## headers etc */}
              <div className="analysis-card primary">
                <h2>⚖️ Legal Analysis</h2>
                <div className="analysis-text markdown-body">
                  <ReactMarkdown>{data.analysis}</ReactMarkdown>
                </div>
              </div>

              {/* FIX 2: correct keys — section/title/content/score */}
              <div className="analysis-card secondary">
                <h3>📚 Relevant Law Sections</h3>
                <div className="law-list">
                  {data.relevant_law_sections?.map(
                    (law: any, index: number) => (
                      <div key={index} className="law-item">
                        <span className="check">✔</span>
                        <div className="law-item-body">
                          <div className="law-item-header">
                            <span className="law-section-badge">
                              Section {law.section}
                            </span>
                          </div>
                          <p className="law-title">{law.title}</p>
                          <p className="law-content">{law.content}</p>
                        </div>
                      </div>
                    ),
                  )}
                </div>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
