"use client";
import React, { useState } from "react";

import "./clientDetails.css";
import { useClients, useDeleteClient } from "@/hooks/useClients";
import { Client } from "@/types/client";
import Modal from "@/componenets/Modal/Modal";
import ClientForm from "@/componenets/ClientForm/ClientForm";

const page: React.FC = () => {
  const [openModal, setOpenModal] = useState(false);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const deleteClient = useDeleteClient();

  const { data, isLoading, error } = useClients();

  if (isLoading) return <p>Loading Clients...</p>;
  if (error) return <p>Error loading Error...</p>;

  const handleDelete = (id: number) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this Client? ",
    );
    if (!confirmDelete) return;

    deleteClient.mutate(id);
  };

  return (
    <main className="client-details-container">
      <h2 className="client-details-header">Client Details</h2>
      <section className="add-clients-container">
        <button
          className="add-clients"
          onClick={() => {
            setSelectedClient(null);
            setOpenModal(true);
          }}
        >
          + Add New Clients
        </button>

        <Modal open={openModal} onClose={() => setOpenModal(false)}>
          <ClientForm
            initialData={selectedClient}
            onClose={() => setOpenModal(false)}
          />
        </Modal>
      </section>
      <section className="details-container">
        {data?.map((client: Client) => (
          <div className="details-card" key={client.id}>
            <h2 className="details-card-header">{client.name}</h2>

            <div className="client-info">
              <p>
                <strong>Phone:</strong> {client.phone}
              </p>
              <p>
                <strong>Email:</strong> {client.email}
              </p>
            </div>

            <div className="details-card-actions">
              <button
                className="update-btn"
                onClick={() => {
                  setSelectedClient(client);
                  setOpenModal(true);
                }}
              >
                Update
              </button>

              <button
                className="delete-btn"
                onClick={() => handleDelete(client.id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </section>
    </main>
  );
};

export default page;
