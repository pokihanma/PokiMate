"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { GlassCard } from "@/components/cards/GlassCard";
import { formatCurrency, formatDate } from "@/lib/format";

export default function RecurringPage() {
  const [list, setList] = useState<{ id: number; title: string; amount: number; next_due_date: string; frequency: string }[]>([]);
  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.get<typeof list>("/finance/recurring", token).then((r) => {
      if (r.success && Array.isArray(r.data)) setList(r.data);
    });
  }, []);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Recurring</h1>
      <GlassCard>
        {list.length === 0 ? (
          <p className="text-slate-500">No recurring rules.</p>
        ) : (
          <ul className="space-y-2">
            {list.map((r) => (
              <li key={r.id} className="flex justify-between items-center">
                <span>{r.title} ({r.frequency})</span>
                <span>{formatCurrency(r.amount)} — next {formatDate(r.next_due_date)}</span>
              </li>
            ))}
          </ul>
        )}
      </GlassCard>
    </div>
  );
}
