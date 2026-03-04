"use client";

import { Button } from "@/components/ui/button";

export function HabitForm({ onSuccess }: { onSuccess?: () => void }) {
  return (
    <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
      <p className="text-sm text-slate-400">Use API POST /life/habits with title, frequency.</p>
      <Button type="submit">Save</Button>
    </form>
  );
}
