import { useState } from "react";
import { View, TextInput, Text, Pressable, StyleSheet } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { apiPost } from "../lib/api";
import { setTokens } from "../lib/auth";
import { useStore } from "../store/state";

export default function LoginScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigation = useNavigation();
  const setUser = useStore((s) => s.setUser);

  async function login() {
    setError("");
    const r = await apiPost<{ access_token: string; user: { id: number; email: string; username: string; role: string } }>(
      "/auth/login",
      { email, password },
      ""
    );
    if (r.success && r.data) {
      await setTokens(r.data.access_token, r.data.user);
      setUser(r.data.user);
      (navigation as { reset: (o: object) => void }).reset({ index: 0, routes: [{ name: "Main" }] });
    } else {
      setError((r as { error?: string }).error || "Login failed");
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Pokimate</Text>
      <TextInput style={styles.input} placeholder="Email" value={email} onChangeText={setEmail} autoCapitalize="none" placeholderTextColor="#64748b" />
      <TextInput style={styles.input} placeholder="Password" value={password} onChangeText={setPassword} secureTextEntry placeholderTextColor="#64748b" />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <Pressable style={styles.button} onPress={login}>
        <Text style={styles.buttonText}>Sign in</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", padding: 24, backgroundColor: "#0f172a" },
  title: { fontSize: 24, fontWeight: "600", color: "#f1f5f9", marginBottom: 24 },
  input: { borderWidth: 1, borderColor: "#475569", borderRadius: 8, padding: 12, marginBottom: 12, color: "#f1f5f9" },
  error: { color: "#f87171", marginBottom: 8 },
  button: { backgroundColor: "#2563eb", borderRadius: 8, padding: 14, alignItems: "center", marginTop: 8 },
  buttonText: { color: "#fff", fontWeight: "600" },
});
