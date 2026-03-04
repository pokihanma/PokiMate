"use client";

import { useState } from "react";
import { GlassCard } from "@/components/cards/GlassCard";
import { Button } from "@/components/ui/button";

export default function ImportPage() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Import CSV</h1>
      <GlassCard>
        <p className="text-sm text-slate-400 mb-4">Upload a CSV with columns: date, amount, type, description. Map account_id and category_id via query params.</p>
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] ?? null)} className="block mb-4" />
        <Button disabled={!file} onClick={() => setResult("Use API: POST /finance/import/csv with file, account_id, category_id")}>
          Import
        </Button>
        {result && <p className="mt-4 text-sm text-slate-400">{result}</p>}
      </GlassCard>
    </div>
  );
}
