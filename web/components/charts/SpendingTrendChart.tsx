"use client";

import { GlassCard } from "@/components/cards/GlassCard";

export function SpendingTrendChart({ data }: { data?: { month: string; amount: number }[] }) {
  return (
    <GlassCard>
      <h3 className="text-lg font-medium mb-4">Spending trend</h3>
      {!data?.length ? <p className="text-sm text-slate-500">No data</p> : <div className="h-48 flex items-end gap-1">{data.map((d, i) => <div key={d.month} className="flex-1 bg-blue-600/80 rounded-t min-h-[2px]" style={{ height: `${Math.max(2, (d.amount / Math.max(...data.map((x) => x.amount))) * 100)}%` }} title={`${d.month}: ${d.amount}`} />)}</div>}
    </GlassCard>
  );
}
