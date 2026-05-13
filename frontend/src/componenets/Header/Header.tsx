import React from "react";
import Link from "next/link";
import "./Header.css";

const Header: React.FC = () => {
  return (
    <header className="header">
      {/* Logo */}
      <div className="logo-name">
        <svg
          className="logo-icon"
          viewBox="0 0 24 24"
          width="24"
          height="24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M12 3v19" />
          <path d="M5 7h14" />
          <path d="M3 14l2-7 2 7" />
          <path d="M3 14h4" />
          <path d="M17 14l2-7 2 7" />
          <path d="M17 14h4" />
          <path d="M8 21h8" />
        </svg>
        <h1>
          <span className="logo-bold">LexAI</span>{" "}
          <span className="logo-light">Assistant</span>
        </h1>
      </div>

      {/* Navigation */}
      <nav className="header-nav">
        <Link href="/appointment">Appointment</Link>
        <Link href="/legal">Legal Intelligence</Link>
        <Link href="/contract">Clause Analysis</Link>
      </nav>

      {/*Github Button */}
      <a
        href="https://github.com/IrfanSarang/Legal-Assistant.git"
        target="_blank"
        rel="noopener noreferrer"
        className="github-btn"
      >
        GitHub
      </a>
    </header>
  );
};

export default Header;
