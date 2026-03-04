"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useAiMode } from "@/hooks/useAiMode";

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/finance", label: "Finance" },
  { href: "/debt", label: "Debt" },
  { href: "/investments", label: "Investments" },
  { href: "/life", label: "Life" },
  { href: "/goals", label: "Goals" },
  { href: "/sync", label: "Sync" },
  { href: "/ai", label: "AI Insights" },
  { href: "/settings", label: "Settings" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { isOff: aiOff } = useAiMode();
  const nav = navItems.filter((item) => item.href !== "/ai" || !aiOff);
  return (
    <aside className="hidden lg:flex flex-col w-56 border-r border-slate-800 bg-slate-900/50 p-4">
      <Link href="/dashboard" className="text-xl font-semibold text-slate-100 mb-6">
        Pokimate
      </Link>
      <nav className="flex flex-col gap-1">
        {nav.map(({ href, label }) => (
          <Link
            key={href}
            href={href}
            className={cn(
              "rounded-lg px-3 py-2 text-sm font-medium transition-colors",
              pathname === href || pathname.startsWith(href + "/")
                ? "bg-slate-700 text-white"
                : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            )}
          >
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
