"use client";

import React from "react";
import "./AppointmentForm.css";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import axiosInstance from "@/lib/axiosInstance";
import { Client } from "@/types/client";
import { useCreateAppointment } from "@/hooks/useAppointment";

interface Props {
  onClose: () => void;
}

const AppointmentForm: React.FC<Props> = ({ onClose }) => {
  const [clientId, setClientId] = React.useState("");
  const [date, setDate] = React.useState("");
  const [description, setDescription] = React.useState("");

  const createAppointment = useCreateAppointment();

  // Fetch clients
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

  // Handle form submit
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
    <main className="appointment-form-container">
      <h1>Schedule Appointments</h1>

      <form className="appointment-form" onSubmit={handleSubmit}>
        <label>
          Client Name:
          <select
            name="clientId"
            onChange={(e) => setClientId(e.target.value)}
            required
          >
            <option value="">Select Client</option>

            {isLoading && <option>Loading...</option>}
            {isError && <option>Error loading clients</option>}

            {clients?.map((client) => (
              <option key={client.id} value={client.id}>
                {client.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Date:
          <input
            type="date"
            name="date"
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </label>

        <label>
          Description:
          <textarea
            name="description"
            onChange={(e) => setDescription(e.target.value)}
          />
        </label>

        <button type="submit">Add</button>
      </form>
    </main>
  );
};

export default AppointmentForm;
