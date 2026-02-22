"use client";
import React, { useState } from "react";

import "./clientDetails.css";
import { useClients, useDeleteClient } from "@/hooks/useClients";
import { Client } from "@/types/client";
import Modal from "@/componenets/Modal/Modal";
import ClientForm from "@/componenets/ClientForm/ClientForm";

const ClientDetailsPage: React.FC = () => {
  const [openModal, setOpenModal] = useState(false);
  const [selectedClient, setSelectedClient] = useState<Client | null>(null);
  const deleteClient = useDeleteClient();

  const { data, isLoading, error } = useClients();

  if (isLoading) return <div className="status-msg">Loading Clients...</div>;
  if (error)
    return <div className="status-msg error">Error loading clients.</div>;

  const handleDelete = (id: number) => {
    if (window.confirm("Are you sure you want to delete this client?")) {
      deleteClient.mutate(id);
    }
  };

  const handleOpenAddModal = () => {
    setSelectedClient(null);
    setOpenModal(true);
  };

  const handleOpenEditModal = (client: Client) => {
    setSelectedClient(client);
    setOpenModal(true);
  };

  return (
    <main className="client-details-container">
      <header className="client-header-section">
        <div>
          <h1>Client Directory</h1>
          <p>Manage contact information for your legal cases</p>
        </div>
        <button className="add-clients-btn" onClick={handleOpenAddModal}>
          + Add New Client
        </button>
      </header>

      <section className="clients-grid">
        {data?.map((client: Client) => (
          <div className="client-card" key={client.id}>
            <div className="client-card-header">
              <div className="avatar">{client.name.charAt(0)}</div>
              <h3>{client.name}</h3>
            </div>

            <div className="client-card-body">
              <div className="info-row">
                <span className="icon">📞</span>
                <span>{client.phone}</span>
              </div>
              <div className="info-row">
                <span className="icon">✉️</span>
                <span className="email-text">{client.email}</span>
              </div>
            </div>

            <div className="client-card-footer">
              <button
                className="update-btn"
                onClick={() => handleOpenEditModal(client)}
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

      {data?.length === 0 && <p className="no-data">No clients found.</p>}

      <Modal open={openModal} onClose={() => setOpenModal(false)}>
        <ClientForm
          initialData={selectedClient}
          onClose={() => setOpenModal(false)}
        />
      </Modal>
    </main>
  );
};

export default ClientDetailsPage;
