"use client";

import { useState, useCallback } from "react";
import { getToken } from "@/lib/auth";

type Status = "idle" | "loading" | "success" | "error";

export function useApi<T>() {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<Status>("idle");

  const run = useCallback(async (fn: (token: string) => Promise<{ success: boolean; data?: T; error?: string }>) => {
    const token = getToken();
    if (!token) {
      setError("Not authenticated");
      setStatus("error");
      return;
    }
    setStatus("loading");
    setError(null);
    const result = await fn(token);
    if (result.success && result.data !== undefined) {
      setData(result.data);
      setStatus("success");
    } else {
      setError((result as { error?: string }).error || "Request failed");
      setStatus("error");
    }
  }, []);

  return { data, error, status, run };
}
