# Pokimate — Sync & security

## Encryption for backups

- **Cipher**: AES-256-GCM.
- **Key derivation**: Argon2id (preferred) or scrypt (fallback), tuned for laptop/desktop.
- **Per-backup**: Random nonce for each encryption; per-user salt for KDF (stored in manifest or derived).

## Backup format (Drive)

- **Folder**: `Pokimate_Backups` (configurable via `ASTRA_SYNC_FOLDER_NAME`).
- **Files**:
  - `backup_<timestamp>_<device_id>.enc` — encrypted DB snapshot.
  - `manifest_<timestamp>_<device_id>.json` — metadata (see below).
- **Checksum**: SHA-256 of ciphertext (in manifest or separate checksum.txt) for verify-before-decrypt.

## Manifest (JSON)

- schema_version  
- app_version  
- created_at_utc  
- device_id  
- backup_filename  
- cipher: aes-256-gcm  
- kdf: argon2id (or scrypt)  
- salt_b64  
- nonce_b64  
- ciphertext_sha256  
- db_schema_version  

## Key management

- **Web**: Cannot securely store passphrase; v1 uses backend to perform encrypt/decrypt (user enters passphrase per sync/restore).
- **Desktop**: Optional OS credential store for passphrase; else prompt each time.
- **Mobile**: Secure storage (expo-secure-store) + optional biometric gating before using tokens/keys.

## Threat model (summary)

- **Local theft**: DB and app are on device; encryption at rest for backups reduces exposure of backup files.
- **Drive exposure**: Backups are encrypted; without passphrase, files are unusable.
- **Token leakage**: Short-lived access tokens; refresh rotation; logout invalidates.
- **Audit**: All mutations logged in audit_events for debug and conflict reasoning.

## Sync flow (reminder)

1. **Upload**: Snapshot DB → derive key from passphrase (Argon2id) → encrypt (AES-256-GCM) → upload .enc + manifest → log sync_log.
2. **Restore**: List backups → user selects → download → verify SHA-256 → decrypt with passphrase → atomic replace local DB → log sync_log.

## Drive API scope

- Use `drive.file` to limit access to app-created files only.
