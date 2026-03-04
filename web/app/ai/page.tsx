"use client";

import { useState } from "react";
import { useAiMode } from "@/hooks/useAiMode";
import { getWeeklySummary } from "@/lib/ai";
import { InsightCard } from "@/components/cards/InsightCard";
import { Button } from "@/components/ui/button";

export default function AiPage() {
  const { isOff } = useAiMode();
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (isOff) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold">AI Insights</h1>
        <p className="text-slate-400">AI is disabled (AI_MODE=OFF).</p>
      </div>
    );
  }

  async function loadSummary() {
    setLoading(true);
    const r = await getWeeklySummary();
    setLoading(false);
    if (r.success && r.data) setSummary(r.data.summary);
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">AI Insights</h1>
      <Button onClick={loadSummary} disabled={loading}>{loading ? "Loading…" : "Generate weekly summary"}</Button>
      {summary && (
        <InsightCard title="Weekly summary" defaultOpen={true}>
          {summary}
        </InsightCard>
      )}
    </div>
  );
}
