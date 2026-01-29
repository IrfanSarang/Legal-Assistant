import React from "react";
import "./appointment.css";

const page: React.FC = () => {
  const appointmentDetails = [
    {
      id: "1",
      client_id: "3515",
      name: "Anurag Dubey",
      time: "17:00",
      date: "01-01-2026",
      description: "This meeting is related to property dispute",
    },
  ];

  return (
    <main className="appointment-container">
      <section className="appointemt-details">
        <h1>Appointment Details </h1>

        <div className="appointment-button">
          <button>Client Detail</button>
          <button>+ Add Appointment</button>
        </div>
      </section>

      <section className="upcomings-appointment">upcomings</section>
    </main>
  );
};

export default page;
