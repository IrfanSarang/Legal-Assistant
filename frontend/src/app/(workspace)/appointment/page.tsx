"use client";

import React, { use, useState } from "react";
import { useRouter } from "next/navigation";

import "./appointment.css";
import Modal from "@/componenets/Modal/Modal";
import AppointmentForm from "@/componenets/AppointmentForm/AppointmentForm";
import { useAppointments, useDeleteAppointment } from "@/hooks/useAppointment";
import AppointmentUpdate from "@/componenets/AppointmentUpdate/AppointmentUpdate";
import { Appointment } from "@/types/appointment";

const page: React.FC = () => {
  const [openModal, setOpenModal] = useState(false);
  const [openEditModal, setOpenEditModal] = useState(false);
  const deleteAppointment = useDeleteAppointment();
  const [selectedAppointment, setSelectedAppointment] =
    useState<Appointment | null>(null);
  const router = useRouter();
  const { data, isLoading, isError } = useAppointments();
  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (isError) {
    return <p>Error loading appointments.</p>;
  }

  const handleDelete = (id: number) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this appointment? ",
    );
    if (!confirmDelete) return;
    deleteAppointment.mutate(id);
  };

  return (
    <main className="appointment-container">
      <section className="appointemt-details">
        <h1>Appointment Details </h1>

        <div className="appointment-button">
          <button
            onClick={() => {
              router.push("/clientDetails");
            }}
          >
            Client Detail
          </button>
          <button onClick={() => setOpenModal(true)}>+ Add Appointment</button>
        </div>

        <Modal open={openModal} onClose={() => setOpenModal(false)}>
          <AppointmentForm onClose={() => setOpenModal(false)} />
        </Modal>

        <section className="appointment-list">
          <h2>Appointments</h2>

          {data?.length === 0 && <p>No appointments found</p>}

          <div className="appointment-grid">
            {data?.map((appt) => (
              <div key={appt.id} className="appointment-card">
                <h3>{appt.client.name}</h3>

                <p>
                  <b>Date:</b> {new Date(appt.date).toLocaleString()}
                </p>
                <p>
                  <b>Phone:</b> {appt.client.phone}
                </p>
                <p>
                  <b>Email:</b> {appt.client.email}
                </p>

                {appt.description && (
                  <p>
                    <b>Note:</b> {appt.description}
                  </p>
                )}

                <button
                  onClick={() => {
                    setSelectedAppointment(appt);
                    setOpenEditModal(true);
                  }}
                >
                  Edit
                </button>
                <button onClick={() => handleDelete(appt.id)}>Delete</button>
              </div>
            ))}
          </div>
        </section>
        <Modal open={openEditModal} onClose={() => setOpenEditModal(false)}>
          <AppointmentUpdate
            initialData={selectedAppointment}
            onClose={() => setOpenEditModal(false)}
          />
        </Modal>
      </section>
    </main>
  );
};

export default page;
