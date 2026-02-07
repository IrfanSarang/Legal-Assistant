import { Client, CreateClientProps, UpdateClientProps } from "@/types/client";
import axiosInstance from "../lib/axiosInstance";

const BASE_URL = "/api/v1/clients/";

// READ
export const getClients = async (): Promise<Client[]> => {
  const response = await axiosInstance.get(BASE_URL);
  return response.data;
};

// CREATE
export const createClient = async (
  payload: CreateClientProps,
): Promise<Client> => {
  const response = await axiosInstance.post(BASE_URL, payload);
  return response.data;
};

// UPDATE
export const updateClient = async (
  payload: UpdateClientProps,
): Promise<Client> => {
  const { id, ...data } = payload;
  const response = await axiosInstance.put(`${BASE_URL}${id}`, data);
  return response.data;
};

// DELETE
export const deleteClient = async (id: number): Promise<void> => {
  await axiosInstance.delete(`${BASE_URL}${id}`);
};
