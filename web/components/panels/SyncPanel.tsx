"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

export function SyncPanel({ lastSync, backupCount }: { lastSync?: string | null; backupCount?: number }) {
  return (
    <div className="rounded-2xl border border-slate-700/50 bg-slate-900/60 p-4">
      <p className="text-sm text-slate-400">Last sync: {lastSync ?? "Never"} · Backups: {backupCount ?? 0}</p>
      <Link href="/sync" className="inline-block mt-2">
        <Button size="sm">Sync now</Button>
      </Link>
    </div>
  );
}
