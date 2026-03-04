"use client";

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { GlassCard } from "@/components/cards/GlassCard";

export default function HabitsPage() {
  const [list, setList] = useState<{ id: number; title: string; frequency: string }[]>([]);
  useEffect(() => {
    const token = getToken();
    if (!token) return;
    api.get<typeof list>("/life/habits", token).then((r) => {
      if (r.success && Array.isArray(r.data)) setList(r.data);
    });
  }, []);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Habits</h1>
      <GlassCard>
        {list.length === 0 ? (
          <p className="text-slate-500">No habits. Add one or run seed.</p>
        ) : (
          <ul className="space-y-2">
            {list.map((h) => (
              <li key={h.id}>{h.title} ({h.frequency})</li>
            ))}
          </ul>
        )}
      </GlassCard>
    </div>
  );
}
