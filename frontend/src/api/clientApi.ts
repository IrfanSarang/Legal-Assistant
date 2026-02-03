import { Client, CreateClientProps, UpdateClientProps } from "@/types/client";
import axiosInstance from "../lib/axiosInstance";

// READ
export const getClients = async (): Promise<Client[]> => {
  const response = await axiosInstance.get("/api/clients/");
  return response.data;
};

// CREATE
export const createClient = async (
  payload: CreateClientProps,
): Promise<Client> => {
  const response = await axiosInstance.post("/api/clients/", payload);
  return response.data;
};

// UPDATE
export const updateClient = async (
  payload: UpdateClientProps,
): Promise<Client> => {
  const { id, ...data } = payload;
  const response = await axiosInstance.put(`/api/clients/${id}`, data);
  return response.data;
};

// DELETE
export const deleteClient = async (id: number): Promise<void> => {
  await axiosInstance.delete(`/api/clients/${id}`);
};
