"use client";

import { useState } from "react";
import { useAnalyzeContract } from "../../../hooks/useContract";

export default function ContractPage() {
  const [contractText, setContractText] = useState("");

  const { mutate, data, isPending } = useAnalyzeContract();

  const handleAnalyze = () => {
    mutate({
      contract_text: contractText,
    });
  };

  return (
    <div>
      <h1>Contract Analysis</h1>

      <textarea
        value={contractText}
        onChange={(e) => setContractText(e.target.value)}
        placeholder="Paste contract here..."
        rows={10}
      />

      <button onClick={handleAnalyze} disabled={isPending}>
        {isPending ? "Analyzing..." : "Analyze"}
      </button>

      {data && (
        <div>
          <h2>Analysis</h2>
          <p>{data.analysis}</p>

          <h3>Relevant Law Sections</h3>
          {data.relevant_law_sections.map((law, index) => (
            <p key={index}>{law.chunk_text}</p>
          ))}
        </div>
      )}
    </div>
  );
}
