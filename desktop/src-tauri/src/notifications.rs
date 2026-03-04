// Desktop notifications: budget exceeded, upcoming recurring, goal milestone
// Use tauri::api::notification when needed
#[allow(dead_code)]
pub fn notify_budget_exceeded(category: &str) {
    // Notification::new(env!("CARGO_PKG_NAME")).body(format!("Budget exceeded: {}", category)).show();
}

#[allow(dead_code)]
pub fn notify_upcoming_recurring(title: &str, amount: &str) {
    // Notification::new(env!("CARGO_PKG_NAME")).body(format!("Upcoming: {} - {}", title, amount)).show();
}

#[allow(dead_code)]
pub fn notify_goal_milestone(title: &str) {
    // Notification::new(env!("CARGO_PKG_NAME")).body(format!("Goal milestone: {}", title)).show();
}
