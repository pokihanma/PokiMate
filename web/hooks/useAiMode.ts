"use client";

import { AI_MODE } from "@/lib/constants";

export function useAiMode() {
  const isOff = AI_MODE === "OFF";
  const isLight = AI_MODE === "LIGHT";
  const isFull = AI_MODE === "FULL";
  return { isOff, isLight, isFull, mode: AI_MODE };
}
