"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const nav = [
  { href: "/dashboard", label: "Home" },
  { href: "/finance", label: "Finance" },
  { href: "/debt", label: "Debt" },
  { href: "/investments", label: "Invest" },
  { href: "/life", label: "Life" },
  { href: "/goals", label: "Goals" },
  { href: "/sync", label: "Sync" },
  { href: "/settings", label: "Settings" },
];

export function MobileNav() {
  const pathname = usePathname();
  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 flex items-center justify-around border-t border-slate-800 bg-slate-900/95 backdrop-blur py-2 safe-area-pb">
      {nav.slice(0, 5).map(({ href, label }) => (
        <Link
          key={href}
          href={href}
          className={cn(
            "flex flex-col items-center gap-0.5 px-2 py-1 rounded-lg text-xs font-medium",
            pathname === href || pathname.startsWith(href + "/")
              ? "text-blue-400"
              : "text-slate-500"
          )}
        >
          {label}
        </Link>
      ))}
    </nav>
  );
}
