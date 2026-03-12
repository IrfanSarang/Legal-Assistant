"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

import "./appointment.css";
import Modal from "@/componenets/Modal/Modal";
import AppointmentForm from "@/componenets/AppointmentForm/AppointmentForm";
import { useAppointments, useDeleteAppointment } from "@/hooks/useAppointment";
import AppointmentUpdate from "@/componenets/AppointmentUpdate/AppointmentUpdate";
import { Appointment } from "@/types/appointment";
import BillModal from "@/componenets/BillModal/BillModal";

const AppointmentPage: React.FC = () => {
  const [openModal, setOpenModal] = useState(false);
  const [openEditModal, setOpenEditModal] = useState(false);
  const [selectedAppointment, setSelectedAppointment] =
    useState<Appointment | null>(null);
  const [filterDate, setFilterDate] = useState("");
  const [billAppointment, setBillAppointment] = useState<Appointment | null>(
    null,
  );

  const router = useRouter();
  const { data, isLoading, isError } = useAppointments();
  const deleteAppointment = useDeleteAppointment();

  if (isLoading)
    return <div className="status-msg">Loading Appointments...</div>;
  if (isError)
    return <div className="status-msg error">Error loading data.</div>;

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Step 1: Filter out past appointments
  const upcomingData = data?.filter((appt) => {
    const apptDate = new Date(appt.date);
    apptDate.setHours(0, 0, 0, 0);
    return apptDate >= today;
  });

  // Step 2: Sort by date ascending (earliest first)
  const sortedData = upcomingData?.sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime(),
  );

  // Step 3: Apply date filter if selected
  const filteredData = filterDate
    ? sortedData?.filter((appt) => {
        const apptDate = new Date(appt.date).toLocaleDateString("en-CA");
        return apptDate === filterDate;
      })
    : sortedData;

  const handleDelete = (id: number) => {
    if (window.confirm("Are you sure you want to delete this appointment?")) {
      deleteAppointment.mutate(id);
    }
  };

  const handleDownloadPDF = () => {
    if (!filteredData || filteredData.length === 0) {
      alert("No appointments found for the selected date.");
      return;
    }

    const doc = new jsPDF();

    // ── Header ──────────────────────────────────────────────
    doc.setFontSize(18);
    doc.setTextColor(22, 101, 52);
    doc.text("Appointment Report", 14, 20);

    doc.setFontSize(11);
    doc.setTextColor(100);
    doc.text(
      filterDate
        ? `Date: ${new Date(filterDate).toLocaleDateString("en-IN", { dateStyle: "long" })}`
        : `Upcoming Appointments from ${today.toLocaleDateString("en-IN", { dateStyle: "long" })}`,
      14,
      30,
    );
    doc.text(`Total: ${filteredData.length} appointment(s)`, 14, 38);

    // ── Table ────────────────────────────────────────────────
    autoTable(doc, {
      startY: 46,
      head: [
        ["#", "Client Name", "Date & Time", "Phone", "Description", "Remark"],
      ],
      body: filteredData.map((appt, index) => [
        index + 1,
        appt.client.name,
        new Date(appt.date).toLocaleDateString("en-IN", {
          dateStyle: "medium",
        }),
        appt.client.phone,
        appt.description || "—",
        "",
      ]),
      headStyles: {
        fillColor: [22, 101, 52],
        textColor: 255,
        fontStyle: "bold",
        fontSize: 10,
      },
      bodyStyles: {
        fontSize: 9,
        textColor: 40,
        minCellHeight: 14,
      },
      alternateRowStyles: {
        fillColor: [240, 253, 244],
      },
      columnStyles: {
        0: { cellWidth: 8 },
        1: { cellWidth: 35 },
        2: { cellWidth: 38 },
        3: { cellWidth: 28 },
        4: { cellWidth: 40 },
        5: { cellWidth: 30, fillColor: [255, 255, 240] },
      },
      styles: {
        cellPadding: 4,
        lineColor: [200, 200, 200],
        lineWidth: 0.2,
      },
      margin: { left: 14, right: 14 },
    });

    // ── Signature & Stamp Section ────────────────────────────
    const pageCount = doc.getNumberOfPages();
    doc.setPage(pageCount);

    const finalY = (doc as any).lastAutoTable.finalY || 150;
    const pageHeight = doc.internal.pageSize.height;
    const pageWidth = doc.internal.pageSize.width;

    const startY =
      finalY + 20 + 60 > pageHeight - 20
        ? (() => {
            doc.addPage();
            return 30;
          })()
        : finalY + 20;

    // Divider
    doc.setDrawColor(200, 200, 200);
    doc.setLineWidth(0.3);
    doc.line(14, startY, pageWidth - 14, startY);

    // Section title
    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text("AUTHORIZED SIGNATURES", pageWidth / 2, startY + 10, {
      align: "center",
    });

    const leftX = 25;
    const rightX = pageWidth / 2 + 20;
    const lineY = startY + 42;

    // ── Left: Stamp ──────────────────────────────────────────
    doc.setFontSize(8);
    doc.setTextColor(80, 80, 80);
    doc.text("Stamp:", leftX, startY + 20);

    // Stamp box (dashed border simulation with rect)
    doc.setDrawColor(180, 180, 180);
    doc.setLineWidth(0.3);
    doc.rect(leftX, startY + 23, 60, 22);

    // Stamp label inside box
    doc.setFontSize(7);
    doc.setTextColor(180, 180, 180);
    doc.text("[ Office Stamp Here ]", leftX + 30, startY + 36, {
      align: "center",
    });

    // Label below
    doc.setFontSize(8);
    doc.setTextColor(80, 80, 80);
    doc.text("Company / Office Stamp", leftX + 30, lineY + 8, {
      align: "center",
    });

    // ── Right: Signature ─────────────────────────────────────
    doc.setFontSize(8);
    doc.setTextColor(80, 80, 80);
    doc.text("Signature:", rightX, startY + 20);

    // Signature line
    doc.setDrawColor(80, 80, 80);
    doc.setLineWidth(0.4);
    doc.line(rightX, lineY, rightX + 60, lineY);

    // Labels below signature
    doc.setFontSize(8);
    doc.setTextColor(80, 80, 80);
    doc.text("Authorized Signatory", rightX + 30, lineY + 6, {
      align: "center",
    });

    doc.setFontSize(7);
    doc.setTextColor(150);
    doc.text("Name:  ____________________", rightX, lineY + 13);
    doc.text("Designation:  ______________", rightX, lineY + 19);
    doc.text(
      `Date:  ${new Date().toLocaleDateString("en-IN", { dateStyle: "long" })}`,
      rightX,
      lineY + 25,
    );

    // ── Footer on every page ─────────────────────────────────
    for (let i = 1; i <= doc.getNumberOfPages(); i++) {
      doc.setPage(i);
      doc.setFontSize(7.5);
      doc.setTextColor(180);
      doc.line(14, pageHeight - 14, pageWidth - 14, pageHeight - 14);
      doc.text(
        `Generated on ${new Date().toLocaleDateString()} — AI Legal Assistant`,
        14,
        pageHeight - 8,
      );
      doc.text(
        `Remarks: Done  /  Cancelled  /  Pending       Page ${i} of ${doc.getNumberOfPages()}`,
        pageWidth - 14,
        pageHeight - 8,
        { align: "right" },
      );
    }

    const filename = filterDate
      ? `appointments_${filterDate}.pdf`
      : `appointments_upcoming.pdf`;
    doc.save(filename);
  };

  return (
    <main className="appointment-page">
      <header className="page-header">
        <div>
          <h1>Appointment Management</h1>
          <p>Showing upcoming appointments — past meetings are archived</p>
        </div>
        <div className="header-actions">
          <button
            className="secondary-btn"
            onClick={() => router.push("/clientDetails")}
          >
            View Clients
          </button>
          <button className="primary-btn" onClick={() => setOpenModal(true)}>
            + Add Appointment
          </button>
        </div>
      </header>

      {/* Filter + Download Bar */}
      <div className="filter-bar">
        <div className="filter-left">
          <label htmlFor="date-filter">Filter by Date:</label>
          <input
            id="date-filter"
            type="date"
            className="date-input"
            value={filterDate}
            min={today.toISOString().split("T")[0]}
            onChange={(e) => setFilterDate(e.target.value)}
          />
          {filterDate && (
            <button className="clear-btn" onClick={() => setFilterDate("")}>
              ✕ Clear
            </button>
          )}
        </div>
        <button
          className="download-btn"
          onClick={handleDownloadPDF}
          disabled={!filteredData || filteredData.length === 0}
        >
          ⬇ Download PDF
        </button>
      </div>

      <section className="appointment-section">
        <div className="table-container">
          <table className="appointment-table">
            <thead>
              <tr>
                <th>Client Name</th>
                <th>Date</th>
                <th>Contact Info</th>
                <th>Description</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredData?.map((appt) => (
                <tr key={appt.id}>
                  <td className="font-bold">{appt.client.name}</td>
                  <td>
                    {new Date(appt.date).toLocaleString([], {
                      dateStyle: "medium",
                    })}
                  </td>
                  <td>
                    <div className="contact-cell">
                      <span>{appt.client.phone}</span>
                      <small>{appt.client.email}</small>
                    </div>
                  </td>
                  <td className="description-cell">
                    {appt.description || "—"}
                  </td>
                  <td>
                    <div className="action-group">
                      <button
                        className="edit-btn"
                        onClick={() => {
                          setSelectedAppointment(appt);
                          setOpenEditModal(true);
                        }}
                      >
                        Edit
                      </button>
                      <button
                        className="delete-btn"
                        onClick={() => handleDelete(appt.id)}
                      >
                        Delete
                      </button>
                      <button
                        className="bill-btn"
                        onClick={() => setBillAppointment(appt)}
                      >
                        Generate Bill
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredData?.length === 0 && (
            <p className="no-data">
              {filterDate
                ? `No appointments on ${new Date(filterDate).toLocaleDateString()}.`
                : "No upcoming appointments scheduled."}
            </p>
          )}
        </div>
      </section>

      <Modal open={openModal} onClose={() => setOpenModal(false)}>
        <AppointmentForm onClose={() => setOpenModal(false)} />
      </Modal>

      <Modal open={openEditModal} onClose={() => setOpenEditModal(false)}>
        <AppointmentUpdate
          initialData={selectedAppointment}
          onClose={() => setOpenEditModal(false)}
        />
      </Modal>
      {billAppointment && (
        <BillModal
          appointment={billAppointment}
          onClose={() => setBillAppointment(null)}
        />
      )}
    </main>
  );
};

export default AppointmentPage;
