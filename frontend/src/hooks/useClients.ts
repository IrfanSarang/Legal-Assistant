import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createClient,
  deleteClient,
  getClients,
  updateClient,
} from "@/api/clientApi";
import { Client, CreateClientProps } from "@/types/client";

export const useClients = () => {
  return useQuery<Client[]>({
    queryKey: ["clients"],
    queryFn: getClients,
  });
};

export const useCreateClients = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: CreateClientProps) => createClient(payload),

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["clients"] });
    },
  });
};

export const useUpdateClients = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateClient,

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["clients"] });
    },
  });
};

export const useDeleteClient = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => deleteClient(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["clients"] });
    },

    //handle errors
    onError: (error) => {
      console.error("Failed to delete client:", error);
    },
  });
};
