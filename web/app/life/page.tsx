"use client";

import Link from "next/link";
import { GlassCard } from "@/components/cards/GlassCard";
import { Button } from "@/components/ui/button";

export default function LifePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Life</h1>
      <Link href="/life/habits">
        <Button>Habits</Button>
      </Link>
      <GlassCard>
        <p className="text-slate-400">Daily metrics (sleep, work, exercise, mood) and weekly summary. Use API: GET /life/metrics, POST /life/metrics, GET /life/summary.</p>
      </GlassCard>
    </div>
  );
}
