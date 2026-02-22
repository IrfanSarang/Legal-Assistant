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
        <Link href="/contract">Contract Analysis</Link>
      </nav>

      {/* Auth Buttons */}
      <div className="auth-buttons">
        <button>Log In</button>
        <button>Sign Up</button>
      </div>
    </header>
  );
};

export default Header;
