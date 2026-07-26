import { http } from "@/lib/http";

export interface AuthUser {
  id: string;
  email: string | null;
}

export const api = {
  getMe: () => http.get<AuthUser>("/auth/me"),
};
