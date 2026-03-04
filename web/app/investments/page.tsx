"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { GlassCard } from "@/components/cards/GlassCard";
import { formatCurrency } from "@/lib/format";

export default function InvestmentsPage() {
  const [list, setList] = useState<{ id: number; asset_name: string; type: string; units: number; current_price: number }[]>([]);
  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.get<typeof list>("/investments/holdings", token).then((r) => {
      if (r.success && Array.isArray(r.data)) setList(r.data);
    });
  }, []);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Investments</h1>
      <GlassCard>
        {list.length === 0 ? (
          <p className="text-slate-500">No holdings. Add one or run seed.</p>
        ) : (
          <ul className="space-y-2">
            {list.map((h) => (
              <li key={h.id} className="flex justify-between items-center">
                <span>{h.asset_name} ({h.type})</span>
                <span>{h.units} × {formatCurrency(h.current_price)}</span>
              </li>
            ))}
          </ul>
        )}
      </GlassCard>
    </div>
  );
}
