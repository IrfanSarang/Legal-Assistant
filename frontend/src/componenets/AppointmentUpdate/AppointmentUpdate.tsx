"use client";

import React, { useEffect, useState } from "react";
import { Appointment } from "@/types/appointment";
import { useUpdateAppointment } from "@/hooks/useAppointment";

import "./AppointmentUpdate.css";
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
      setDate(initialData.date ? initialData.date.split("T")[0] : "");
      setDescription(initialData.description || "");
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
        onError: () => alert("Failed to update appointment"),
      },
    );
  };

  if (!initialData) return null;

  return (
    <div className="update-form-container">
      <div className="update-header">
        <h2>Refine Appointment</h2>
        <p>
          Updating schedule for: <strong>{initialData.client.name}</strong>
        </p>
      </div>

      <form className="update-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="update-date">New Date</label>
          <input
            id="update-date"
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </div>

        <div className="input-group">
          <label htmlFor="update-desc">Updated Description</label>
          <textarea
            id="update-desc"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add new notes..."
            rows={4}
            required
          />
        </div>

        <div className="update-actions">
          <button type="button" className="cancel-btn" onClick={onClose}>
            Discard
          </button>
          {/* Restored the Save Button */}
          <button
            type="submit"
            className="save-btn"
            disabled={updateAppointment.isPending}
          >
            {updateAppointment.isPending ? "Saving..." : "Save Changes"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AppointmentUpdate;
