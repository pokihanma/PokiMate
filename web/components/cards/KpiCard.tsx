"use client";

import { GlassCard } from "./GlassCard";

export function KpiCard({
  title,
  value,
  sub,
  trend,
}: {
  title: string;
  value: string | number;
  sub?: string;
  trend?: "up" | "down" | "neutral";
}) {
  return (
    <GlassCard>
      <p className="text-sm text-slate-400 font-medium">{title}</p>
      <p className="text-3xl font-semibold tracking-tight mt-1">{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-1">{sub}</p>}
      {trend && (
        <p className={cn("text-xs mt-1", trend === "up" && "text-emerald-400", trend === "down" && "text-rose-400", trend === "neutral" && "text-slate-400")}>
          {trend === "up" ? "↑" : trend === "down" ? "↓" : "→"}
        </p>
      )}
    </GlassCard>
  );
}

function cn(...a: (string | boolean | undefined)[]) {
  return a.filter(Boolean).join(" ");
}
