"use client";

import { useState, useEffect, useCallback } from "react";
import { getToken, getUser, clearAuth, setTokens, User } from "@/lib/auth";
import { api } from "@/lib/api";

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const t = getToken();
    const u = getUser();
    if (t && u) setUser(u);
    setLoading(false);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const res = await api.post<{
      access_token: string;
      refresh_token: string;
      expires_in: number;
      user: User;
    }>("/auth/login", { email, password });
    if (res.success && res.data) {
      setTokens(res.data.access_token, res.data.refresh_token, res.data.user);
      setUser(res.data.user);
      return { success: true as const };
    }
    return { success: false as const, error: (res as { error: string }).error };
  }, []);

  const logout = useCallback(() => {
    clearAuth();
    setUser(null);
  }, []);

  return { user, loading, login, logout, isAuthenticated: !!user };
}
