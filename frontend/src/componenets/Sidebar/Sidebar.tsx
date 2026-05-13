"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import "./Sidebar.css";

/* ── SVG Icons (16×16 white stroke) ──────── */
const icons: Record<string, React.ReactNode> = {
  home: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  ),
  calendar: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  ),
  scales: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 3v19" />
      <path d="M5 7h14" />
      <path d="M3 14l2-7 2 7" />
      <path d="M3 14h4" />
      <path d="M17 14l2-7 2 7" />
      <path d="M17 14h4" />
      <path d="M8 22h8" />
    </svg>
  ),
  fileSearch: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <circle cx="11.5" cy="14.5" r="2.5" />
      <line x1="13.3" y1="16.3" x2="15" y2="18" />
    </svg>
  ),
};

const navItems = [
  { href: "/", icon: "home", label: "Home" },
  { href: "/appointment", icon: "calendar", label: "Appointments" },
  { href: "/legal", icon: "scales", label: "Legal Intelligence" },
  { href: "/contract", icon: "fileSearch", label: "Clause Analysis" },
];

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
      {/* ── Header ───────────────────────────── */}
      <div className="sidebar-header">
        {isOpen && (
          <div className="sidebar-brand">
            <span className="sidebar-pulse" />
            <span className="sidebar-title">LexAI</span>
          </div>
        )}
        <button
          className="toggle-btn"
          onClick={handleToggle}
          aria-label="Toggle Sidebar"
        >
          {isOpen ? (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          ) : (
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          )}
        </button>
      </div>

      {/* ── Navigation ───────────────────────── */}
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`sidebar-link ${isActive ? "active" : ""}`}
              title={!isOpen ? item.label : ""}
            >
              <span className="sidebar-icon">{icons[item.icon]}</span>
              {isOpen && <span className="sidebar-label">{item.label}</span>}
              {!isOpen && <span className="sidebar-tooltip">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {/* ── Bottom Profile ───────────────────── */}
      <div className="sidebar-bottom">
        <div className="sidebar-profile">
          <div className="sidebar-avatar">LA</div>
          {isOpen && (
            <div className="sidebar-profile-info">
              <span className="sidebar-profile-name">Legal Admin</span>
              <span className="sidebar-profile-role">Administrator</span>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
