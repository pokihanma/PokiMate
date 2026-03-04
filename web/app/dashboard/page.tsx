"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { KpiCard } from "@/components/cards/KpiCard";
import { GlassCard } from "@/components/cards/GlassCard";
import { formatCurrency, formatPercent } from "@/lib/format";
import { useOfflineQueue } from "@/hooks/useOfflineQueue";

export default function DashboardPage() {
  const [summary, setSummary] = useState<{
    month: string;
    income_total: number;
    expense_total: number;
    savings_rate: number;
  } | null>(null);
  const [debtSummary, setDebtSummary] = useState<{ total_balance: number; total_emi: number; debt_stress_index: number } | null>(null);
  const [healthScore, setHealthScore] = useState<number | null>(null);
  const { isOffline } = useOfflineQueue();

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    const month = new Date().toISOString().slice(0, 7);
    api.get<{ month: string; income_total: number; expense_total: number; savings_rate: number }>(`/finance/summary?month=${month}`, token).then((r) => {
      if (r.success && r.data) setSummary(r.data);
    });
    api.get<{ total_balance: number; total_emi: number; debt_stress_index: number }>("/debt/summary", token).then((r) => {
      if (r.success && r.data) setDebtSummary(r.data);
    });
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
      </div>
      {isOffline && (
        <div className="rounded-lg bg-amber-900/30 border border-amber-700/50 px-4 py-2 text-sm text-amber-200">
          You are offline. Data may be cached.
        </div>
      )}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          title="Net worth (proxy)"
          value={summary ? formatCurrency(summary.income_total - summary.expense_total) : "—"}
          sub={summary ? `${summary.month}` : "Load summary"}
        />
        <KpiCard
          title="Savings rate"
          value={summary ? formatPercent(summary.savings_rate) : "—"}
          sub={summary?.month}
        />
        <KpiCard
          title="Debt balance"
          value={debtSummary ? formatCurrency(debtSummary.total_balance) : "—"}
          sub={debtSummary ? `EMI: ${formatCurrency(debtSummary.total_emi)}` : undefined}
        />
        <KpiCard
          title="Financial health"
          value={healthScore != null ? `${healthScore}` : "—"}
          sub="0–100"
        />
      </div>
      <GlassCard>
        <h2 className="text-lg font-medium mb-4">Monthly overview</h2>
        {summary ? (
          <div className="grid gap-4 sm:grid-cols-2">
            <p className="text-sm text-slate-400">Income: {formatCurrency(summary.income_total)}</p>
            <p className="text-sm text-slate-400">Expense: {formatCurrency(summary.expense_total)}</p>
          </div>
        ) : (
          <p className="text-sm text-slate-500">Loading… or add transactions and run seed for demo data.</p>
        )}
      </GlassCard>
    </div>
  );
}
