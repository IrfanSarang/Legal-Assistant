import React, { useState, useEffect } from "react";
import "./ClientForm.css";
import { useCreateClients, useUpdateClients } from "@/hooks/useClients";
import { Client } from "@/types/client";

interface Props {
  initialData?: Client | null;
  onClose: () => void;
}

const ClientForm: React.FC<Props> = ({ initialData, onClose }) => {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");

  const createClient = useCreateClients();
  const updateClient = useUpdateClients();

  // 🔥 Prefill or reset form
  useEffect(() => {
    if (initialData) {
      setName(initialData.name);
      setPhone(initialData.phone);
      setEmail(initialData.email);
    } else {
      setName("");
      setPhone("");
      setEmail("");
    }
  }, [initialData]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (initialData) {
      // UPDATE
      updateClient.mutate(
        {
          id: initialData.id,
          name,
          phone,
          email,
        },
        {
          onSuccess: () => onClose(),
        },
      );
    } else {
      // CREATE
      createClient.mutate(
        { name, phone, email },
        {
          onSuccess: () => onClose(),
        },
      );
    }
  };

  const isPending = createClient.isPending || updateClient.isPending;

  return (
    <main className="client-form-container">
      <h1>{initialData ? "Update Client" : "Add Client"}</h1>

      <form className="client-form" onSubmit={handleSubmit}>
        <label>
          Name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </label>

        <label>
          Phone:
          <input
            type="text"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
          />
        </label>

        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>

        <button className="add-client-button" disabled={isPending}>
          {isPending
            ? initialData
              ? "Updating..."
              : "Adding..."
            : initialData
              ? "Update Client"
              : "Add Client"}
        </button>
      </form>
    </main>
  );
};

export default ClientForm;
