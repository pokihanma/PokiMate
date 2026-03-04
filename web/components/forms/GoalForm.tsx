"use client";

import { Button } from "@/components/ui/button";

export function GoalForm({ onSuccess }: { onSuccess?: () => void }) {
  return (
    <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
      <p className="text-sm text-slate-400">Use API POST /goals with type, title, target_date, target_value.</p>
      <Button type="submit">Save</Button>
    </form>
  );
}
