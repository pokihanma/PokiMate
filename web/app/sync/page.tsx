"use client";

import { useState, useEffect } from "react";
import { getSyncStatus, uploadBackup, listBackups } from "@/lib/sync";
import { GlassCard } from "@/components/cards/GlassCard";
import { Button } from "@/components/ui/button";

export default function SyncPage() {
  const [status, setStatus] = useState<{ last_sync: string | null; backup_count: number; drive_connected: boolean } | null>(null);
  const [passphrase, setPassphrase] = useState("");
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    getSyncStatus().then((r) => {
      if (r.success && r.data) setStatus(r.data);
    });
  }, []);

  async function handleUpload() {
    if (!passphrase) return;
    setUploading(true);
    setMessage(null);
    const r = await uploadBackup(passphrase);
    setUploading(false);
    if (r.success && r.data) {
      setMessage(`Uploaded: ${r.data.backup_id}`);
      getSyncStatus().then((res) => res.success && res.data && setStatus(res.data));
    } else setMessage((r as { error?: string }).error || "Upload failed");
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Sync</h1>
      <GlassCard>
        <p className="text-sm text-slate-400 mb-4">Manual encrypted backup to Google Drive (when configured).</p>
        {status && (
          <p className="text-sm mb-2">Last sync: {status.last_sync ?? "Never"} · Backups: {status.backup_count} · Drive: {status.drive_connected ? "Connected" : "Not configured"}</p>
        )}
        <div className="flex gap-2 items-center flex-wrap">
          <input
            type="password"
            placeholder="Passphrase"
            value={passphrase}
            onChange={(e) => setPassphrase(e.target.value)}
            className="rounded-lg border border-slate-600 bg-slate-800 px-3 py-2 text-sm"
          />
          <Button onClick={handleUpload} disabled={uploading || !passphrase}>{uploading ? "Uploading…" : "Sync now"}</Button>
        </div>
        {message && <p className="mt-2 text-sm text-slate-400">{message}</p>}
      </GlassCard>
    </div>
  );
}
