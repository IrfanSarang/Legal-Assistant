export interface Appointment {
  id: number;
  date: string;
  description: string;

  client: {
    clientId: number;
    name: string;
    phone: string;
    email: string;
  };
}

export interface UpdateAppointmentProps {
  date: string;
  description: string;
}

export interface UpdateAppointmentVariables {
  appointmentId: number;
  data: UpdateAppointmentProps;
}

export interface DeleteAppointmentProps {
  appointmentId: number;
}

export interface CreateAppointmentProps {
  date: string;
  description: string;
  client_id: number;
}
