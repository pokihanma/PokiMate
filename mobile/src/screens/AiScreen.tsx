import { View, Text, StyleSheet } from "react-native";
import { AI_MODE } from "../lib/constants";

export default function AiScreen() {
  if (AI_MODE === "OFF") {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>AI Insights</Text>
        <Text style={styles.sub}>AI is disabled</Text>
      </View>
    );
  }
  return (
    <View style={styles.container}>
      <Text style={styles.title}>AI Insights</Text>
      <Text style={styles.sub}>Weekly summary and insights</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, backgroundColor: "#0f172a" },
  title: { fontSize: 22, fontWeight: "600", color: "#f1f5f9" },
  sub: { fontSize: 14, color: "#94a3b8", marginTop: 8 },
});
