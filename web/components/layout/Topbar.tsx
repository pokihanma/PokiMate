"use client";

import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";
import { Button } from "@/components/ui/button";

export function Topbar() {
  const { user, logout } = useAuth();
  return (
    <header className="sticky top-0 z-10 flex h-14 items-center justify-between border-b border-slate-800 bg-slate-900/80 backdrop-blur px-4 lg:px-8">
      <div className="flex items-center gap-4">
        <span className="text-sm text-slate-400">
          {new Date().toLocaleString("en-IN", { month: "long", year: "numeric" })}
        </span>
      </div>
      <div className="flex items-center gap-2">
        <Link href="/sync">
          <Button variant="ghost" size="sm">Sync</Button>
        </Link>
        {user ? (
          <div className="flex items-center gap-2">
            <span className="text-sm text-slate-400">{user.username}</span>
            <Button variant="ghost" size="sm" onClick={() => logout()}>Logout</Button>
          </div>
        ) : (
          <Link href="/login">
            <Button size="sm">Login</Button>
          </Link>
        )}
      </div>
    </header>
  );
}
