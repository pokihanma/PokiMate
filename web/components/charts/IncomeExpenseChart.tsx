"use client";

import { GlassCard } from "@/components/cards/GlassCard";

export function IncomeExpenseChart({ income, expense }: { income?: number; expense?: number }) {
  return (
    <GlassCard>
      <h3 className="text-lg font-medium mb-4">Income vs expense</h3>
      <div className="flex gap-4">
        <div className="flex-1 h-8 bg-emerald-600/80 rounded" style={{ width: `${Math.min(100, ((income ?? 0) / Math.max((income ?? 0) + (expense ?? 0), 1)) * 100)}%` }} />
        <div className="flex-1 h-8 bg-rose-600/80 rounded" style={{ width: `${Math.min(100, ((expense ?? 0) / Math.max((income ?? 0) + (expense ?? 0), 1)) * 100)}%` }} />
      </div>
      <p className="text-xs text-slate-400 mt-2">Income · Expense</p>
    </GlassCard>
  );
}
