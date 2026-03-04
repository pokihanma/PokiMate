import { View, Text, StyleSheet } from "react-native";

export default function FinanceScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Finance</Text>
      <Text style={styles.sub}>Transactions, budgets, recurring</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, backgroundColor: "#0f172a" },
  title: { fontSize: 22, fontWeight: "600", color: "#f1f5f9" },
  sub: { fontSize: 14, color: "#94a3b8", marginTop: 8 },
});
