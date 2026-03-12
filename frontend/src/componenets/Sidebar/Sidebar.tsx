"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import "./Sidebar.css";

const Sidebar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(true);
  const [mounted, setMounted] = useState(false);
  const pathname = usePathname();

  // Read saved state on mount
  useEffect(() => {
    const saved = localStorage.getItem("sidebar-open");
    if (saved !== null) {
      setIsOpen(saved === "true");
    }
    setMounted(true);
  }, []);

  // Persist state on change
  const handleToggle = () => {
    setIsOpen((prev) => {
      localStorage.setItem("sidebar-open", String(!prev));
      return !prev;
    });
  };

  // Prevent hydration mismatch — render nothing until mounted
  if (!mounted) return null;

  return (
    <aside className={`sidebar ${isOpen ? "open" : "closed"}`}>
      <div className="sidebar-header">
        {isOpen && <h2 className="sidebar-title">Features</h2>}
        <button
          className="toggle-btn"
          onClick={handleToggle}
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
          label="Clause Analysis"
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

const SidebarItem = ({ href, icon, label, isOpen }: ItemProps) => {
  const pathname = usePathname();
  const isActive = pathname === href;

  return (
    <Link
      href={href}
      className={`sidebar-link ${isActive ? "active" : ""}`}
      title={!isOpen ? label : ""}
    >
      <span className="icon">{icon}</span>
      {isOpen && <span className="label">{label}</span>}
    </Link>
  );
};

export default Sidebar;
