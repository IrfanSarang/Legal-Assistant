import React from "react";
import Link from "next/link";
import "./Header.css";

const Header: React.FC = () => {
  return (
    <header className="header">
      {/* Logo */}
      <div className="logo-name">
        <h1>AI Legal Assistant</h1>
      </div>

      {/* Navigation */}
      <nav>
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
        Github
      </a>
    </header>
  );
};

export default Header;
