"use client";

import { GlassCard } from "@/components/cards/GlassCard";

export function LifeTrendsChart({ data }: { data?: { date: string; mood_score?: number; sleep_hours?: number }[] }) {
  return (
    <GlassCard>
      <h3 className="text-lg font-medium mb-4">Life trends</h3>
      {!data?.length ? <p className="text-sm text-slate-500">No data</p> : <p className="text-sm text-slate-400">{data.length} days</p>}
    </GlassCard>
  );
}
