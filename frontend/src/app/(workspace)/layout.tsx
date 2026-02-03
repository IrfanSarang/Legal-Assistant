"use client";
import React from "react";
import Sidebar from "@/componenets/Sidebar/Sidebar";
import ReactQueryProvider from "@/providers/ReactQueryProvider";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="workspace">
      <Sidebar />
      <main className="content">
        <ReactQueryProvider>{children}</ReactQueryProvider>
      </main>
    </div>
  );
}
