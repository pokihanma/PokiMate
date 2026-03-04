"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { GlassCard } from "@/components/cards/GlassCard";
import { formatCurrency, formatDate } from "@/lib/format";

export default function TransactionsPage() {
  const [list, setList] = useState<{ id: number; date: string; amount: number; type: string; description: string }[]>([]);
  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.get<typeof list>("/finance/transactions", token).then((r) => {
      if (r.success && Array.isArray(r.data)) setList(r.data);
    });
  }, []);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Transactions</h1>
      <GlassCard>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left py-2">Date</th>
                <th className="text-left py-2">Type</th>
                <th className="text-left py-2">Description</th>
                <th className="text-right py-2">Amount</th>
              </tr>
            </thead>
            <tbody>
              {list.length === 0 && (
                <tr><td colSpan={4} className="py-8 text-slate-500 text-center">No transactions yet. Add your first transaction or run seed for demo data.</td></tr>
              )}
              {list.map((t) => (
                <tr key={t.id} className="border-b border-slate-800">
                  <td className="py-2">{formatDate(t.date)}</td>
                  <td className="py-2">{t.type}</td>
                  <td className="py-2">{t.description || "—"}</td>
                  <td className="py-2 text-right">{formatCurrency(t.amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>
    </div>
  );
}
