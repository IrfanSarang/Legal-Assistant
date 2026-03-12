"use client";

import React, { useState } from "react";
import jsPDF from "jspdf";
import { Appointment } from "@/types/appointment";
import "./BillModal.css";

interface BillModalProps {
  appointment: Appointment;
  onClose: () => void;
}

type PaymentMode = "Cash" | "UPI" | "Cheque" | "Bank Transfer";

const BillModal: React.FC<BillModalProps> = ({ appointment, onClose }) => {
  const [firmName, setFirmName] = useState("Irfan Associates");
  const [lawyerName, setLawyerName] = useState("Irfan Sarang");
  const [amount, setAmount] = useState("");
  const [paymentMode, setPaymentMode] = useState<PaymentMode>("Cash");
  const [generating, setGenerating] = useState(false);

  const billNumber = `BILL-${appointment.id}-${Date.now().toString().slice(-6)}`;
  const billDate = new Date().toLocaleDateString("en-IN", {
    dateStyle: "long",
  });

  const handleGenerate = () => {
    if (!amount || isNaN(Number(amount))) {
      alert("Please enter a valid amount.");
      return;
    }

    setGenerating(true);

    const doc = new jsPDF({
      orientation: "portrait",
      unit: "mm",
      format: "a4",
    });

    const pageW = doc.internal.pageSize.width;
    const pageH = doc.internal.pageSize.height;
    const halfH = pageH / 2 - 4; // ← 4mm buffer so content never bleeds
    const margin = 14;
    const contentW = pageW - margin * 2;

    [0, halfH + 4].forEach((offsetY) => {
      // ── Outer border ──────────────────────────────────────
      doc.setDrawColor(22, 101, 52);
      doc.setLineWidth(0.8);
      doc.rect(margin, offsetY + 4, contentW, halfH - 8);

      // ── Header band ───────────────────────────────────────
      doc.setFillColor(22, 101, 52);
      doc.rect(margin, offsetY + 4, contentW, 20, "F");

      // Firm name
      doc.setFontSize(13);
      doc.setTextColor(255, 255, 255);
      doc.setFont("helvetica", "bold");
      doc.text(
        firmName || "________________________",
        pageW / 2,
        offsetY + 14,
        { align: "center" },
      );

      // Receipt label
      doc.setFontSize(7.5);
      doc.setTextColor(200, 240, 200);
      doc.setFont("helvetica", "normal");
      doc.text("LEGAL SERVICE RECEIPT", pageW / 2, offsetY + 21, {
        align: "center",
      });

      // ── Bill No + Date ────────────────────────────────────
      doc.setFontSize(8);
      doc.setTextColor(80, 80, 80);
      doc.setFont("helvetica", "bold");
      doc.text(`Bill No: ${billNumber}`, margin + 4, offsetY + 30);
      doc.text(`Date: ${billDate}`, pageW - margin - 4, offsetY + 30, {
        align: "right",
      });

      // Divider
      doc.setDrawColor(230, 230, 230);
      doc.setLineWidth(0.2);
      doc.line(margin + 2, offsetY + 33, pageW - margin - 2, offsetY + 33);

      // ── Client Info ───────────────────────────────────────
      doc.setFontSize(8.5);
      doc.setTextColor(40, 40, 40);
      doc.setFont("helvetica", "bold");
      doc.text("Billed To:", margin + 4, offsetY + 39);

      doc.setFont("helvetica", "normal");
      doc.setFontSize(8.5);
      doc.text(appointment.client.name, margin + 4, offsetY + 45);
      doc.setTextColor(100);
      doc.text(`Phone: ${appointment.client.phone}`, margin + 4, offsetY + 51);
      doc.text(`Email: ${appointment.client.email}`, margin + 4, offsetY + 57);
      doc.setTextColor(80, 80, 80);
      doc.text(
        `Appointment: ${new Date(appointment.date).toLocaleDateString("en-IN", { dateStyle: "long" })}`,
        margin + 4,
        offsetY + 63,
      );
      if (appointment.description) {
        doc.text(
          `Matter: ${appointment.description}`,
          margin + 4,
          offsetY + 69,
        );
      }

      // Divider
      doc.setDrawColor(230, 230, 230);
      doc.line(margin + 2, offsetY + 73, pageW - margin - 2, offsetY + 73);

      // ── Payment Table header ───────────────────────────────
      doc.setFillColor(240, 250, 240);
      doc.rect(margin + 2, offsetY + 74, contentW - 4, 8, "F");
      doc.setFontSize(8);
      doc.setFont("helvetica", "bold");
      doc.setTextColor(22, 101, 52);
      doc.text("Description", margin + 5, offsetY + 80);
      doc.text("Mode", pageW / 2 - 8, offsetY + 80);
      doc.text("Amount (INR)", pageW - margin - 5, offsetY + 80, {
        align: "right",
      });

      // ── Payment Row ───────────────────────────────────────
      doc.setFont("helvetica", "normal");
      doc.setTextColor(40, 40, 40);
      doc.setFontSize(8);
      doc.text("Legal Consultation Fee", margin + 5, offsetY + 89);
      doc.text(paymentMode, pageW / 2 - 8, offsetY + 89);
      doc.setFont("helvetica", "bold");
      doc.text(
        `Rs. ${Number(amount).toLocaleString("en-IN")}/-`,
        pageW - margin - 5,
        offsetY + 89,
        { align: "right" },
      );

      // ── Total Row ─────────────────────────────────────────
      doc.setDrawColor(220, 220, 220);
      doc.line(margin + 2, offsetY + 93, pageW - margin - 2, offsetY + 93);
      doc.setFillColor(220, 245, 220);
      doc.rect(margin + 2, offsetY + 94, contentW - 4, 8, "F");
      doc.setFontSize(9);
      doc.setFont("helvetica", "bold");
      doc.setTextColor(22, 101, 52);
      doc.text("Total Amount Paid", margin + 5, offsetY + 100);
      doc.text(
        `Rs. ${Number(amount).toLocaleString("en-IN")}/-`,
        pageW - margin - 5,
        offsetY + 100,
        { align: "right" },
      );

      // Amount in words
      doc.setFont("helvetica", "italic");
      doc.setFontSize(7.5);
      doc.setTextColor(100);
      doc.text(
        `In words: ${amountToWords(Number(amount))} Rupees Only`,
        margin + 5,
        offsetY + 108,
      );

      // Divider
      doc.setDrawColor(220, 220, 220);
      doc.setLineWidth(0.2);
      doc.line(margin + 2, offsetY + 111, pageW - margin - 2, offsetY + 111);

      // ── Stamp (left) ──────────────────────────────────────
      doc.setDrawColor(180, 180, 180);
      doc.setLineWidth(0.3);
      doc.rect(margin + 4, offsetY + 114, 36, 16);
      doc.setFontSize(7);
      doc.setTextColor(190);
      doc.text("[ Stamp ]", margin + 22, offsetY + 123, { align: "center" });
      doc.setFontSize(6.5);
      doc.setTextColor(160);
      doc.text("Office Stamp", margin + 22, offsetY + 133, { align: "center" });

      // ── Signature (right) ─────────────────────────────────
      const sigX = pageW - margin - 58;
      doc.setDrawColor(60, 60, 60);
      doc.setLineWidth(0.4);
      doc.line(sigX, offsetY + 126, pageW - margin - 4, offsetY + 126);

      doc.setFontSize(7.5);
      doc.setFont("helvetica", "bold");
      doc.setTextColor(40, 40, 40);
      doc.text("Authorized Signatory", sigX + 27, offsetY + 130, {
        align: "center",
      });

      doc.setFont("helvetica", "normal");
      doc.setFontSize(7.5);
      doc.setTextColor(80);
      doc.text(
        lawyerName || "________________________",
        sigX + 27,
        offsetY + 135,
        { align: "center" },
      );
      doc.setFontSize(7);
      doc.setTextColor(130);
      doc.text("(Advocate / Lawyer)", sigX + 27, offsetY + 139, {
        align: "center",
      });

      // ── Green footer bar inside border ────────────────────
      doc.setFillColor(22, 101, 52);
      doc.rect(margin, offsetY + halfH - 12, contentW, 4, "F");

      // Thank you text — inside green bar
      doc.setFontSize(6.5);
      doc.setFont("helvetica", "italic");
      doc.setTextColor(200, 240, 200);
      doc.text(
        "Thank you for your trust. This is a computer generated receipt.",
        pageW / 2,
        offsetY + halfH - 9,
        { align: "center" },
      );
    });

    // ── Tear line between halves ───────────────────────────
    doc.setDrawColor(160, 160, 160);
    doc.setLineWidth(0.3);
    doc.setLineDashPattern([2, 2], 0);
    doc.line(margin, pageH / 2, pageW - margin, pageH / 2);
    doc.setLineDashPattern([], 0);
    doc.setFontSize(7);
    doc.setTextColor(160);
    doc.text("✂   Tear Here", pageW / 2, pageH / 2 - 1, { align: "center" });

    doc.save(`bill_${appointment.client.name}_${billNumber}.pdf`);
    setGenerating(false);
    onClose();
  };

  return (
    <div className="bill-overlay" onClick={onClose}>
      <div className="bill-modal" onClick={(e) => e.stopPropagation()}>
        <div className="bill-modal-header">
          <h2>Generate Bill</h2>
          <button className="bill-close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="bill-modal-body">
          {/* Client Info — read only */}
          <div className="bill-client-info">
            <span className="bill-client-name">{appointment.client.name}</span>
            <span className="bill-client-sub">
              {appointment.client.phone} · {appointment.client.email}
            </span>
            <span className="bill-client-sub">
              Appointment:{" "}
              {new Date(appointment.date).toLocaleDateString("en-IN", {
                dateStyle: "long",
              })}
            </span>
          </div>

          <div className="bill-divider" />

          {/* Firm & Lawyer */}
          <div className="bill-field">
            <label>Firm / Office Name</label>
            <input
              type="text"
              placeholder="e.g. Sharma & Associates"
              value={firmName}
              onChange={(e) => setFirmName(e.target.value)}
            />
          </div>

          <div className="bill-field">
            <label>Lawyer Name</label>
            <input
              type="text"
              placeholder="e.g. Adv. Rajesh Sharma"
              value={lawyerName}
              onChange={(e) => setLawyerName(e.target.value)}
            />
          </div>

          {/* Amount */}
          <div className="bill-field">
            <label>
              Amount (INR) <span className="required">*</span>
            </label>
            <input
              type="number"
              placeholder="e.g. 5000"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              min="0"
            />
          </div>

          {/* Payment Mode */}
          <div className="bill-field">
            <label>Mode of Payment</label>
            <div className="payment-options">
              {(
                ["Cash", "UPI", "Cheque", "Bank Transfer"] as PaymentMode[]
              ).map((mode) => (
                <button
                  key={mode}
                  className={`payment-btn ${paymentMode === mode ? "active" : ""}`}
                  onClick={() => setPaymentMode(mode)}
                >
                  {mode === "Cash" && "💵 "}
                  {mode === "UPI" && "📱 "}
                  {mode === "Cheque" && "📋 "}
                  {mode === "Bank Transfer" && "🏦 "}
                  {mode}
                </button>
              ))}
            </div>
          </div>

          {/* Bill number preview */}
          <div className="bill-preview-row">
            <span>Bill No:</span>
            <span className="bill-number-preview">{billNumber}</span>
          </div>
        </div>

        <div className="bill-modal-footer">
          <button className="bill-cancel-btn" onClick={onClose}>
            Cancel
          </button>
          <button
            className="bill-generate-btn"
            onClick={handleGenerate}
            disabled={generating || !amount}
          >
            {generating ? "Generating..." : "⬇ Generate Bill PDF"}
          </button>
        </div>
      </div>
    </div>
  );
};

// ── Amount to words helper ──────────────────────────────────
function amountToWords(amount: number): string {
  const ones = [
    "",
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Eleven",
    "Twelve",
    "Thirteen",
    "Fourteen",
    "Fifteen",
    "Sixteen",
    "Seventeen",
    "Eighteen",
    "Nineteen",
  ];
  const tens = [
    "",
    "",
    "Twenty",
    "Thirty",
    "Forty",
    "Fifty",
    "Sixty",
    "Seventy",
    "Eighty",
    "Ninety",
  ];

  if (amount === 0) return "Zero";

  function convertHundreds(n: number): string {
    if (n > 99)
      return ones[Math.floor(n / 100)] + " Hundred " + convertHundreds(n % 100);
    if (n > 19)
      return tens[Math.floor(n / 10)] + (n % 10 ? " " + ones[n % 10] : "");
    return ones[n];
  }

  function convert(n: number): string {
    if (n >= 10000000)
      return (
        convert(Math.floor(n / 10000000)) + " Crore " + convert(n % 10000000)
      );
    if (n >= 100000)
      return convert(Math.floor(n / 100000)) + " Lakh " + convert(n % 100000);
    if (n >= 1000)
      return convert(Math.floor(n / 1000)) + " Thousand " + convert(n % 1000);
    return convertHundreds(n);
  }

  return convert(Math.floor(amount)).trim();
}

export default BillModal;
