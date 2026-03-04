"use client";

import { useState } from "react";
import { GlassCard } from "./GlassCard";
import { cn } from "@/lib/utils";

export function InsightCard({
  title,
  children,
  defaultOpen = true,
}: {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <GlassCard>
      <button
        type="button"
        className="w-full flex items-center justify-between text-left"
        onClick={() => setOpen((o) => !o)}
      >
        <span className="text-lg font-medium">{title}</span>
        <span className={cn("transition-transform", open && "rotate-180")}>▼</span>
      </button>
      {open && <div className="mt-4 text-sm text-slate-300">{children}</div>}
    </GlassCard>
  );
}
