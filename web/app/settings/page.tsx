"use client";

import { GlassCard } from "@/components/cards/GlassCard";
import { useAuth } from "@/hooks/useAuth";

export default function SettingsPage() {
  const { user } = useAuth();
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Settings</h1>
      <GlassCard>
        <p className="text-sm text-slate-400">Profile</p>
        <p className="mt-1">{user?.username} ({user?.email}) — {user?.role}</p>
      </GlassCard>
      <GlassCard>
        <p className="text-sm text-slate-400">Seed demo data</p>
        <p className="mt-1 text-slate-300">Call POST /admin/seed-demo as admin to load demo transactions, debts, holdings, habits, goals.</p>
      </GlassCard>
    </div>
  );
}
