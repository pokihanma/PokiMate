"use client";

import { formatCurrency } from "@/lib/format";

export function InvestmentsTable({ rows }: { rows: { id: number; asset_name: string; type: string; units: number; current_price: number }[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-700">
            <th className="text-left py-2">Asset</th>
            <th className="text-left py-2">Type</th>
            <th className="text-right py-2">Units</th>
            <th className="text-right py-2">Price</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((h) => (
            <tr key={h.id} className="border-b border-slate-800">
              <td className="py-2">{h.asset_name}</td>
              <td className="py-2">{h.type}</td>
              <td className="py-2 text-right">{h.units}</td>
              <td className="py-2 text-right">{formatCurrency(h.current_price)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
