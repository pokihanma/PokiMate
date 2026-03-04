"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { GlassCard } from "@/components/cards/GlassCard";

export default function FinancePage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Finance</h1>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Link href="/finance/transactions">
          <GlassCard className="hover:border-slate-600 transition-colors cursor-pointer">
            <p className="font-medium">Transactions</p>
            <p className="text-sm text-slate-400 mt-1">View and manage transactions</p>
          </GlassCard>
        </Link>
        <Link href="/finance/budgets">
          <GlassCard className="hover:border-slate-600 transition-colors cursor-pointer">
            <p className="font-medium">Budgets</p>
            <p className="text-sm text-slate-400 mt-1">Monthly budgets by category</p>
          </GlassCard>
        </Link>
        <Link href="/finance/recurring">
          <GlassCard className="hover:border-slate-600 transition-colors cursor-pointer">
            <p className="font-medium">Recurring</p>
            <p className="text-sm text-slate-400 mt-1">Recurring bills</p>
          </GlassCard>
        </Link>
        <Link href="/finance/import">
          <GlassCard className="hover:border-slate-600 transition-colors cursor-pointer">
            <p className="font-medium">Import</p>
            <p className="text-sm text-slate-400 mt-1">CSV import</p>
          </GlassCard>
        </Link>
      </div>
    </div>
  );
}
