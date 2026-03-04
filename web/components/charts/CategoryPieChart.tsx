"use client";

import { GlassCard } from "@/components/cards/GlassCard";

export function CategoryPieChart({ data }: { data?: { category: string; amount: number }[] }) {
  return (
    <GlassCard>
      <h3 className="text-lg font-medium mb-4">By category</h3>
      {!data?.length ? <p className="text-sm text-slate-500">No data</p> : <ul className="space-y-1">{data.map((d) => <li key={d.category} className="text-sm">{d.category}: {d.amount}</li>)}</ul>}
    </GlassCard>
  );
}
