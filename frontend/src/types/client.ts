export interface Client {
  id: number;
  name: string;
  phone: string;
  email: string;
}

export interface CreateClientProps {
  name: string;
  phone: string;
  email: string;
}
export interface UpdateClientProps extends CreateClientProps {
  id: number;
}
