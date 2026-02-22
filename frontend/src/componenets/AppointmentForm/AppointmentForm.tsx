"use client";

import React, { useState } from "react";
import "./AppointmentForm.css";
import { useQuery } from "@tanstack/react-query";
import axiosInstance from "@/lib/axiosInstance";
import { Client } from "@/types/client";
import { useCreateAppointment } from "@/hooks/useAppointment";

interface Props {
  onClose: () => void;
}

const AppointmentForm: React.FC<Props> = ({ onClose }) => {
  const [clientId, setClientId] = useState("");
  const [date, setDate] = useState("");
  const [description, setDescription] = useState("");

  const createAppointment = useCreateAppointment();

  const {
    data: clients,
    isLoading,
    isError,
  } = useQuery<Client[]>({
    queryKey: ["clients"],
    queryFn: async () => {
      const res = await axiosInstance.get("/api/v1/clients");
      return res.data;
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    createAppointment.mutate(
      {
        client_id: Number(clientId),
        date: new Date(date).toISOString(),
        description,
      },
      {
        onSuccess: () => onClose(),
      },
    );
  };

  return (
    <div className="modal-overlay">
      <main className="appointment-form-container">
        <div className="form-header">
          <h2>📅 Schedule Appointment</h2>
          <button className="close-x" onClick={onClose}>
            ✕
          </button>
        </div>

        <form className="appointment-form" onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="client">Client Name</label>
            <select
              id="client"
              value={clientId}
              onChange={(e) => setClientId(e.target.value)}
              required
              disabled={isLoading}
            >
              <option value="">
                {isLoading ? "Loading clients..." : "Select a Client"}
              </option>
              {clients?.map((client) => (
                <option key={client.id} value={client.id}>
                  {client.name}
                </option>
              ))}
            </select>
            {isError && (
              <span className="error-text">Failed to load clients.</span>
            )}
          </div>

          <div className="input-group">
            <label htmlFor="date">Appointment Date</label>
            <input
              id="date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
            />
          </div>

          <div className="input-group">
            <label htmlFor="desc">Description / Notes</label>
            <textarea
              id="desc"
              placeholder="Case details, meeting agenda..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="cancel-btn" onClick={onClose}>
              Cancel
            </button>
            <button
              type="submit"
              className="submit-btn"
              disabled={createAppointment.isPending}
            >
              {createAppointment.isPending
                ? "Scheduling..."
                : "Confirm Schedule"}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default AppointmentForm;
