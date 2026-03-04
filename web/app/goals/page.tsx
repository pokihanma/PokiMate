"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { GlassCard } from "@/components/cards/GlassCard";
import { formatCurrency, formatDate } from "@/lib/format";

export default function GoalsPage() {
  const [list, setList] = useState<{ id: number; title: string; target_date: string; progress_value: number | null; target_value: number | null; status: string }[]>([]);
  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.get<typeof list>("/goals", token).then((r) => {
      if (r.success && Array.isArray(r.data)) setList(r.data);
    });
  }, []);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Goals</h1>
      <GlassCard>
        {list.length === 0 ? (
          <p className="text-slate-500">No goals. Add one or run seed.</p>
        ) : (
          <ul className="space-y-2">
            {list.map((g) => (
              <li key={g.id} className="flex justify-between items-center">
                <span>{g.title} — {formatDate(g.target_date)}</span>
                <span>{g.progress_value != null && g.target_value != null ? `${formatCurrency(g.progress_value)} / ${formatCurrency(g.target_value)}` : g.status}</span>
              </li>
            ))}
          </ul>
        )}
      </GlassCard>
    </div>
  );
}
