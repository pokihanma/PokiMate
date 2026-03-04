"use client";

import { useState, useEffect } from "react";
import { checkApiReachable } from "@/lib/offline";

export function useOfflineQueue() {
  const [isReachable, setIsReachable] = useState(true);

  useEffect(() => {
    let mounted = true;
    checkApiReachable().then((ok) => {
      if (mounted) setIsReachable(ok);
    });
    const t = setInterval(() => {
      checkApiReachable().then((ok) => {
        if (mounted) setIsReachable(ok);
      });
    }, 30000);
    return () => {
      mounted = false;
      clearInterval(t);
    };
  }, []);

  return { isReachable, isOffline: !isReachable };
}
