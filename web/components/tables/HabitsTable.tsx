"use client";

export function HabitsTable({ rows }: { rows: { id: number; title: string; frequency: string }[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-700">
            <th className="text-left py-2">Habit</th>
            <th className="text-left py-2">Frequency</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((h) => (
            <tr key={h.id} className="border-b border-slate-800">
              <td className="py-2">{h.title}</td>
              <td className="py-2">{h.frequency}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
