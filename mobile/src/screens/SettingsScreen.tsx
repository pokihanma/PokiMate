import { View, Text, Pressable, StyleSheet } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { clearAuth } from "../lib/auth";
import { useStore } from "../store/state";

export default function SettingsScreen() {
  const setUser = useStore((s) => s.setUser);
  const nav = useNavigation();

  async function logout() {
    await clearAuth();
    setUser(null);
    (nav as { reset: (o: object) => void }).reset({ index: 0, routes: [{ name: "Login" }] });
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Settings</Text>
      <Pressable style={styles.button} onPress={logout}>
        <Text style={styles.buttonText}>Logout</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, backgroundColor: "#0f172a" },
  title: { fontSize: 22, fontWeight: "600", color: "#f1f5f9" },
  button: { backgroundColor: "#475569", borderRadius: 8, padding: 12, marginTop: 16, alignItems: "center" },
  buttonText: { color: "#fff", fontWeight: "600" },
});
