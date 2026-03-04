import { View, Text, Pressable, StyleSheet } from "react-native";
import { useNavigation } from "@react-navigation/native";

export default function LifeScreen() {
  const nav = useNavigation();
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Life</Text>
      <Pressable style={styles.button} onPress={() => nav.navigate("Habits" as never)}>
        <Text style={styles.buttonText}>Habits</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, backgroundColor: "#0f172a" },
  title: { fontSize: 22, fontWeight: "600", color: "#f1f5f9" },
  button: { backgroundColor: "#2563eb", borderRadius: 8, padding: 12, marginTop: 16, alignItems: "center" },
  buttonText: { color: "#fff", fontWeight: "600" },
});
