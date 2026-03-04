"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { GlassCard } from "@/components/cards/GlassCard";
import { formatCurrency } from "@/lib/format";

export default function BudgetsPage() {
  const [list, setList] = useState<{ id: number; category_id: number; month: string; limit_amount: number; utilization?: { used: number; pct: number } }[]>([]);
  const month = new Date().toISOString().slice(0, 7);
  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.get<typeof list>(`/finance/budgets?month=${month}`, token).then((r) => {
      if (r.success && Array.isArray(r.data)) setList(r.data);
    });
  }, [month]);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Budgets</h1>
      <GlassCard>
        <p className="text-sm text-slate-400 mb-4">Month: {month}</p>
        {list.length === 0 ? (
          <p className="text-slate-500">No budgets. Create one from Finance.</p>
        ) : (
          <ul className="space-y-2">
            {list.map((b) => (
              <li key={b.id} className="flex justify-between items-center">
                <span>Category {b.category_id}</span>
                <span>{formatCurrency(b.limit_amount)} {b.utilization != null && `(${Math.round((b.utilization.pct || 0) * 100)}% used)`}</span>
              </li>
            ))}
          </ul>
        )}
      </GlassCard>
    </div>
  );
}
