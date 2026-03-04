"use client";

import { cn } from "@/lib/utils";

export function GlassCard({
  className,
  children,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-slate-700/50 bg-slate-900/60 backdrop-blur-md shadow-lg p-4 sm:p-6",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}
