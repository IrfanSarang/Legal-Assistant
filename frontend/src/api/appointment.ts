import axiosInstance from "@/lib/axiosInstance";
import {
  Appointment,
  CreateAppointmentProps,
  UpdateAppointmentProps,
} from "@/types/appointment";

const BASE_URL = "/api/v1/appointments/";

export const getAppointments = async (): Promise<Appointment[]> => {
  const response = await axiosInstance.get(BASE_URL);
  return response.data;
};

export const updateAppointment = async (
  appointmentId: number,
  data: UpdateAppointmentProps,
): Promise<Appointment> => {
  const response = await axiosInstance.put(`${BASE_URL}${appointmentId}`, data);
  return response.data;
};

export const deleteAppointment = async (
  appointmentId: number,
): Promise<void> => {
  await axiosInstance.delete(`${BASE_URL}${appointmentId}`);
};

export const createAppointment = async (
  payload: CreateAppointmentProps,
): Promise<Appointment> => {
  const response = await axiosInstance.post(BASE_URL, payload);
  return response.data;
};
