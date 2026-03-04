"use client";

import { GlassCard } from "@/components/cards/GlassCard";

export default function DebtSimulatorPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Debt simulator</h1>
      <GlassCard>
        <p className="text-slate-400">Use API: POST /debt/simulate?s=avalanche or ?s=snowball with body as_of_date, extra_payment_monthly. Chart payoff schedule here.</p>
      </GlassCard>
    </div>
  );
}
