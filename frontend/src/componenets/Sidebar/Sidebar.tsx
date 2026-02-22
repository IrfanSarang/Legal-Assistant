"use client";

import React, { useState } from "react";
import Link from "next/link";
import "./Sidebar.css";

const Sidebar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <aside className={`sidebar ${isOpen ? "open" : "closed"}`}>
      <div className="sidebar-header">
        {isOpen && <h2 className="sidebar-title">Features</h2>}
        <button
          className="toggle-btn"
          onClick={() => setIsOpen((prev) => !prev)}
          aria-label="Toggle Sidebar"
        >
          {isOpen ? "✕" : "☰"}
        </button>
      </div>

      <nav className="sidebar-nav">
        <SidebarItem href="/" icon="🏠" label="Home" isOpen={isOpen} />
        <SidebarItem
          href="/appointment"
          icon="📅"
          label="Appointment"
          isOpen={isOpen}
        />
        <SidebarItem
          href="/legal"
          icon="⚖️"
          label="Legal Intelligence"
          isOpen={isOpen}
        />
        <SidebarItem
          href="/contract"
          icon="📄"
          label="Contract Analysis"
          isOpen={isOpen}
        />
      </nav>
    </aside>
  );
};

interface ItemProps {
  href: string;
  icon: string;
  label: string;
  isOpen: boolean;
}

const SidebarItem = ({ href, icon, label, isOpen }: ItemProps) => (
  <Link href={href} className="sidebar-link" title={!isOpen ? label : ""}>
    <span className="icon">{icon}</span>
    {isOpen && <span className="label">{label}</span>}
  </Link>
);

export default Sidebar;
