"use client";

import { formatCurrency } from "@/lib/format";

export function DebtsTable({ rows }: { rows: { id: number; name: string; remaining_balance: number; emi_monthly: number }[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-700">
            <th className="text-left py-2">Name</th>
            <th className="text-right py-2">Balance</th>
            <th className="text-right py-2">EMI</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((d) => (
            <tr key={d.id} className="border-b border-slate-800">
              <td className="py-2">{d.name}</td>
              <td className="py-2 text-right">{formatCurrency(d.remaining_balance)}</td>
              <td className="py-2 text-right">{formatCurrency(d.emi_monthly)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
