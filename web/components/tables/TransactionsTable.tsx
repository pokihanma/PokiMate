"use client";

import { formatCurrency, formatDate } from "@/lib/format";

export function TransactionsTable({ rows }: { rows: { id: number; date: string; type: string; description: string; amount: number }[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-700">
            <th className="text-left py-2">Date</th>
            <th className="text-left py-2">Type</th>
            <th className="text-left py-2">Description</th>
            <th className="text-right py-2">Amount</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((t) => (
            <tr key={t.id} className="border-b border-slate-800">
              <td className="py-2">{formatDate(t.date)}</td>
              <td className="py-2">{t.type}</td>
              <td className="py-2">{t.description || "—"}</td>
              <td className="py-2 text-right">{formatCurrency(t.amount)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
