import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import LoginScreen from "../screens/LoginScreen";
import DashboardScreen from "../screens/DashboardScreen";
import FinanceScreen from "../screens/FinanceScreen";
import DebtScreen from "../screens/DebtScreen";
import DebtSimulatorScreen from "../screens/DebtSimulatorScreen";
import InvestmentsScreen from "../screens/InvestmentsScreen";
import LifeScreen from "../screens/LifeScreen";
import HabitsScreen from "../screens/HabitsScreen";
import GoalsScreen from "../screens/GoalsScreen";
import SettingsScreen from "../screens/SettingsScreen";
import SyncScreen from "../screens/SyncScreen";
import AiScreen from "../screens/AiScreen";

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function MainTabs() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false, tabBarStyle: { backgroundColor: "#0f172a" }, tabBarActiveTintColor: "#60a5fa" }}>
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Finance" component={FinanceScreen} />
      <Tab.Screen name="Debt" component={DebtScreen} />
      <Tab.Screen name="Invest" component={InvestmentsScreen} />
      <Tab.Screen name="Life" component={LifeScreen} />
      <Tab.Screen name="Goals" component={GoalsScreen} />
      <Tab.Screen name="Sync" component={SyncScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
}

export function RootNavigator() {
  return (
    <Stack.Navigator screenOptions={{ contentStyle: { backgroundColor: "#0f172a" }, headerStyle: { backgroundColor: "#1e293b" }, headerTintColor: "#f1f5f9" }}>
      <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
      <Stack.Screen name="Main" component={MainTabs} />
      <Stack.Screen name="DebtSimulator" component={DebtSimulatorScreen} />
      <Stack.Screen name="Habits" component={HabitsScreen} />
      <Stack.Screen name="Ai" component={AiScreen} />
    </Stack.Navigator>
  );
}
