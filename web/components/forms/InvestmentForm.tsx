"use client";

import { Button } from "@/components/ui/button";

export function InvestmentForm({ onSuccess }: { onSuccess?: () => void }) {
  return (
    <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
      <p className="text-sm text-slate-400">Use API POST /investments/holdings with type, asset_name, units, avg_cost, current_price.</p>
      <Button type="submit">Save</Button>
    </form>
  );
}
