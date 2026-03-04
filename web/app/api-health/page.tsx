"use client";

import { useState, useEffect } from "react";
import { checkApiReachable } from "@/lib/offline";
import { API_BASE } from "@/lib/constants";

export default function ApiHealthPage() {
  const [ok, setOk] = useState<boolean | null>(null);
  useEffect(() => {
    checkApiReachable().then(setOk);
  }, []);
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="rounded-2xl border border-slate-700 bg-slate-900 p-8 max-w-md w-full">
        <h1 className="text-xl font-semibold mb-4">API health</h1>
        <p className="text-sm text-slate-400">Base: {API_BASE}</p>
        <p className="mt-2">{ok === null ? "Checking…" : ok ? "OK — API reachable" : "Failed — API unreachable"}</p>
      </div>
    </div>
  );
}
