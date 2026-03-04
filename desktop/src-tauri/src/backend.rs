use std::net::TcpStream;
use std::process::{Child, Command, Stdio};
use std::sync::Mutex;

const PORT: u16 = 8000;

fn is_backend_running() -> bool {
    TcpStream::connect(("127.0.0.1", PORT)).is_ok()
}

pub fn ensure_backend() -> Result<bool, String> {
    if is_backend_running() {
        return Ok(true);
    }
    // Try to spawn backend from sibling backend/ directory
    let backend_path = std::env::current_exe()
        .ok()
        .and_then(|p| p.parent().map(|p| p.to_path_buf()))
        .and_then(|p| p.parent().map(|p| p.join("backend")))
        .ok_or_else(|| "Could not resolve backend path".to_string())?;

    let python = which::which("python").or_else(|_| which::which("python3")).map_err(|e| e.to_string())?;
    let mut child = Command::new(python)
        .args(["-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", &PORT.to_string()])
        .current_dir(backend_path)
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
        .map_err(|e| e.to_string())?;

    std::thread::sleep(std::time::Duration::from_secs(2));
    if is_backend_running() {
        Ok(true)
    } else {
        let _ = child.kill();
        Err("Backend failed to start".to_string())
    }
}
