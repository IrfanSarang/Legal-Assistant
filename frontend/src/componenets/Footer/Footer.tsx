import React from "react";
import Link from "next/link";
import "./Footer.css";

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="footer-inner">
        {/* Left — Logo & description */}
        <div className="footer-brand">
          <h3>
            <span className="footer-logo-bold">LexAI</span>{" "}
            <span className="footer-logo-light">Assistant</span>
          </h3>
          <p>AI-powered legal research and case management.</p>
        </div>

        {/* Center — Quick links */}
        <div className="footer-links">
          <h4>Quick Links</h4>
          <Link href="/appointment">Appointments</Link>
          <Link href="/legal">Legal Intelligence</Link>
          <Link href="/contract">Clause Analysis</Link>
        </div>

        {/* Right — Contact */}
        <div className="footer-contact">
          <h4>Connect</h4>
          <a
            href="https://github.com/IrfanSarang/Legal-Assistant.git"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub Repository
          </a>
          <span>Built with Next.js & FastAPI</span>
        </div>
      </div>

      {/* Bottom strip */}
      <div className="footer-bottom">
        <p>© 2026 AI Legal Assistant. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
