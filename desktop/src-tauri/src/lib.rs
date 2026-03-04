use tauri::Manager;

mod tray;
mod backend;
mod notifications;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .setup(|app| {
            let handle = app.handle().clone();
            let _tray = tray::create_tray(&handle)?;
            if let Some(window) = app.get_webview_window("main") {
                window.show().ok();
                window.set_focus().ok();
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            cmd_sync_now,
            cmd_open_app,
            cmd_ensure_backend,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

#[tauri::command]
fn cmd_sync_now() {
    // TODO: trigger sync via frontend or HTTP to backend
}

#[tauri::command]
fn cmd_open_app() {
    // Window already open
}

#[tauri::command]
fn cmd_ensure_backend() -> Result<bool, String> {
    backend::ensure_backend()
}
