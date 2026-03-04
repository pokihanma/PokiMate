"use client";

import { GlassCard } from "@/components/cards/GlassCard";

export function DebtPayoffChart({ schedule }: { schedule?: { month: string; balance: number }[] }) {
  return (
    <GlassCard>
      <h3 className="text-lg font-medium mb-4">Debt payoff</h3>
      {!schedule?.length ? <p className="text-sm text-slate-500">No schedule</p> : <p className="text-sm text-slate-400">{schedule.length} months</p>}
    </GlassCard>
  );
}
