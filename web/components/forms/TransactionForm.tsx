"use client";

import { Button } from "@/components/ui/button";

export function TransactionForm({ onSuccess }: { onSuccess?: () => void }) {
  return (
    <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
      <p className="text-sm text-slate-400">Use API POST /finance/transactions or add fields (date, amount, type, account_id, category_id, description).</p>
      <Button type="submit">Save</Button>
    </form>
  );
}
