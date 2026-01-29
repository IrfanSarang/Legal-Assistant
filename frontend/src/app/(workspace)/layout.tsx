"use client";
import React from "react";
import Sidebar from "@/componenets/Sidebar/Sidebar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="workspace">
      <Sidebar />
      <main className="content">{children}</main>
    </div>
  );
}
