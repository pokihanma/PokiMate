"use client";

import { Button } from "@/components/ui/button";

export function DebtForm({ onSuccess }: { onSuccess?: () => void }) {
  return (
    <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
      <p className="text-sm text-slate-400">Use API POST /debt with name, type, principal, interest_rate_apr, emi_monthly, etc.</p>
      <Button type="submit">Save</Button>
    </form>
  );
}
