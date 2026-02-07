import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";
import {
  createAppointment,
  deleteAppointment,
  getAppointments,
  updateAppointment,
} from "@/api/appointment";
import {
  Appointment,
  CreateAppointmentProps,
  UpdateAppointmentVariables,
} from "@/types/appointment";

//Read appointments
export const useAppointments = () => {
  return useQuery<Appointment[]>({
    queryKey: ["appointments"],
    queryFn: getAppointments,
  });
};

//Update appointment
export const useUpdateAppointment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ appointmentId, data }: UpdateAppointmentVariables) =>
      updateAppointment(appointmentId, data),

    onSuccess: () => {
      // refresh appointment list
      queryClient.invalidateQueries({ queryKey: ["appointments"] });
    },
  });
};

//Delete appointment
export const useDeleteAppointment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (appointmentId: number) => deleteAppointment(appointmentId),

    onSuccess: () => {
      // refresh appointment list
      queryClient.invalidateQueries({ queryKey: ["appointments"] });
    },
    //handle errors
    onError: (error) => {
      console.error("Failed to delete appointment:", error);
    },
  });
};

//Create Appointment
export const useCreateAppointment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateAppointmentProps) => createAppointment(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["appointments"] });
    },
  });
};
