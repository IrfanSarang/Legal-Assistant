"use client";
import React, { useState } from "react";
import "./appointment.css";
import Modal from "@/componenets/Modal/Modal";

const page: React.FC = () => {
  const [openModal, setOpenModal] = useState(false);
  return (
    <main className="appointment-container">
      <section className="appointemt-details">
        <h1>Appointment Details </h1>

        <div className="appointment-button">
          <button>Client Detail</button>
          <button onClick={() => setOpenModal(true)}>+ Add Appointment</button>
        </div>
      </section>
      <Modal open={openModal} onClose={() => setOpenModal(false)}>
        <h1>modal</h1>
      </Modal>

      <section className="upcomings-appointment">upcomings</section>
    </main>
  );
};

export default page;
