"use client";

import { InsightCard } from "@/components/cards/InsightCard";

export function AiInsightsPanel({ summary, cachedAt }: { summary?: string; cachedAt?: string | null }) {
  return (
    <InsightCard title="AI Insights" defaultOpen={true}>
      {cachedAt && <p className="text-xs text-slate-500 mb-2">Last generated: {cachedAt}</p>}
      {summary ?? "Generate summary from AI page."}
    </InsightCard>
  );
}
