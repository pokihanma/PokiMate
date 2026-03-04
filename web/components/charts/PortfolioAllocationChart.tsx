"use client";

import { GlassCard } from "@/components/cards/GlassCard";

export function PortfolioAllocationChart({ data }: { data?: { asset_class: string; pct: number }[] }) {
  return (
    <GlassCard>
      <h3 className="text-lg font-medium mb-4">Allocation</h3>
      {!data?.length ? <p className="text-sm text-slate-500">No data</p> : <ul className="space-y-1">{data.map((d) => <li key={d.asset_class} className="text-sm">{d.asset_class}: {d.pct}%</li>)}</ul>}
    </GlassCard>
  );
}
