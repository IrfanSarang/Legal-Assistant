"use client";

import React, { use, useState } from "react";
import { useRouter } from "next/navigation";

import "./appointment.css";
import Modal from "@/componenets/Modal/Modal";
import AppointmentForm from "@/componenets/AppointmentForm/AppointmentForm";
import { useAppointments, useDeleteAppointment } from "@/hooks/useAppointment";
import AppointmentUpdate from "@/componenets/AppointmentUpdate/AppointmentUpdate";
import { Appointment } from "@/types/appointment";

const AppointmentPage: React.FC = () => {
  const [openModal, setOpenModal] = useState(false);
  const [openEditModal, setOpenEditModal] = useState(false);
  const [selectedAppointment, setSelectedAppointment] =
    useState<Appointment | null>(null);

  const router = useRouter();
  const { data, isLoading, isError } = useAppointments();
  const deleteAppointment = useDeleteAppointment();

  if (isLoading)
    return <div className="status-msg">Loading Appointments...</div>;
  if (isError)
    return <div className="status-msg error">Error loading data.</div>;

  const handleDelete = (id: number) => {
    if (window.confirm("Are you sure you want to delete this appointment?")) {
      deleteAppointment.mutate(id);
    }
  };

  return (
    <main className="appointment-page">
      <header className="page-header">
        <div>
          <h1>Appointment Management</h1>
          <p>Manage your client schedules and case meetings</p>
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

      <section className="appointment-section">
        <div className="table-container">
          <table className="appointment-table">
            <thead>
              <tr>
                <th>Client Name</th>
                <th>Date </th>
                <th>Contact Info</th>
                <th>Description</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {data?.map((appt) => (
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
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {data?.length === 0 && (
            <p className="no-data">No appointments scheduled.</p>
          )}
        </div>
      </section>

      {/* Modals */}
      <Modal open={openModal} onClose={() => setOpenModal(false)}>
        <AppointmentForm onClose={() => setOpenModal(false)} />
      </Modal>

      <Modal open={openEditModal} onClose={() => setOpenEditModal(false)}>
        <AppointmentUpdate
          initialData={selectedAppointment}
          onClose={() => setOpenEditModal(false)}
        />
      </Modal>
    </main>
  );
};

export default AppointmentPage;
