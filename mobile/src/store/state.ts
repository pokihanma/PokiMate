import { create } from "zustand";

type User = { id: number; email: string; username: string; role: string } | null;

interface AppState {
  user: User;
  setUser: (u: User) => void;
}

export const useStore = create<AppState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
}));
