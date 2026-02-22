"use client";

import React, { useState } from "react";
import "./Sidebar.css";
import Image from "next/image";
import Link from "next/link";

const Sidebar: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(true);
  return (
    <aside className={`sidebar ${isOpen ? "open" : "close"}`}>
      <section className="sidebar-header">
        <Image
          src="/SidebarLogo.png"
          alt="User logo"
          width={35}
          height={35}
          className={`${isOpen ? "show" : "hide"}`}
        />
        <h2 className={`sidebar-title ${isOpen ? "show" : "hide"} `}>
          Irfan Sarang
        </h2>
        <button
          className={`${isOpen ? "sidebar-button-open" : "sidebar-button-close"}`}
          onClick={() => setIsOpen((prev) => !prev)}
        >
          {`${isOpen ? "✕" : "☰"}`}
        </button>
      </section>

      <nav className="sidebar-nav">
        <Link href="/" className="sidebar-link">
          <span className="icon">📅</span>
          <span className="label">Home</span>
        </Link>

        <Link href="/appointment" className="sidebar-link">
          <span className="icon">📅</span>
          <span className="label">Appointment</span>
        </Link>

        <Link href="/legal" className="sidebar-link">
          <span className="icon">💬</span>
          <span className="label">Legal Intelligence</span>
        </Link>

        <Link href="/contract" className="sidebar-link">
          <span className="icon">📄</span>
          <span className="label">Contract Analysis</span>
        </Link>
      </nav>
    </aside>
  );
};

export default Sidebar;
