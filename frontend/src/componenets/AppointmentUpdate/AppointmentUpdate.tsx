"use client";

import React, { useEffect, useState } from "react";
import { Appointment } from "@/types/appointment";
import { useUpdateAppointment } from "@/hooks/useAppointment";

interface Props {
  initialData?: Appointment | null;
  onClose: () => void;
}

const AppointmentUpdate: React.FC<Props> = ({ initialData, onClose }) => {
  const [date, setDate] = useState("");
  const [description, setDescription] = useState("");

  const updateAppointment = useUpdateAppointment();

  useEffect(() => {
    if (initialData) {
      setDate(initialData.date.split("T")[0]);
      setDescription(initialData.description);
    } else {
      setDate("");
      setDescription("");
    }
  }, [initialData]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!initialData) return;

    updateAppointment.mutate(
      {
        appointmentId: initialData.id,
        data: { date, description },
      },
      {
        onSuccess: () => onClose(),
        onError: (err: any) => alert("Failed to update appointment"),
      },
    );
  };
  return (
    <div className="appointment-update">
      <h2>Update Appointment</h2>

      <form onSubmit={handleSubmit}>
        <label>
          Date:
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </label>

        <label>
          Description:
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </label>

        <button type="submit">Update</button>
      </form>
    </div>
  );
};

export default AppointmentUpdate;
