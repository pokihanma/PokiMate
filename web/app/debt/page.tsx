"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { GlassCard } from "@/components/cards/GlassCard";
import { formatCurrency } from "@/lib/format";
import { Button } from "@/components/ui/button";

export default function DebtPage() {
  const [list, setList] = useState<{ id: number; name: string; remaining_balance: number; emi_monthly: number }[]>([]);
  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.get<typeof list>("/debt/list", token).then((r) => {
      if (r.success && Array.isArray(r.data)) setList(r.data);
    });
  }, []);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Debt</h1>
      <Link href="/debt/simulator">
        <Button>Simulator</Button>
      </Link>
      <GlassCard>
        {list.length === 0 ? (
          <p className="text-slate-500">No debts. Add one or run seed.</p>
        ) : (
          <ul className="space-y-2">
            {list.map((d) => (
              <li key={d.id} className="flex justify-between items-center">
                <span>{d.name}</span>
                <span>Balance: {formatCurrency(d.remaining_balance)} / EMI: {formatCurrency(d.emi_monthly)}</span>
              </li>
            ))}
          </ul>
        )}
      </GlassCard>
    </div>
  );
}
