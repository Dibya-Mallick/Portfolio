"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useState } from "react";

const roles = ["Data Analyst", "Analytics Engineer", "Data Engineer", "Data Scientist"];
const ROLE_DURATION = 1500;

export function RoleRotator() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const timer = window.setInterval(() => setIndex((current) => (current + 1) % roles.length), ROLE_DURATION);
    return () => window.clearInterval(timer);
  }, []);

  return (
    <span className="role-rotator" aria-live="polite">
      <AnimatePresence initial={false} mode="wait">
        <motion.span
          key={roles[index]}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          className="role-rotator__word"
          exit={{ opacity: 0, y: -10, filter: "blur(4px)" }}
          initial={{ opacity: 0, y: 10, filter: "blur(4px)" }}
          transition={{ duration: 0.45, ease: "easeOut" }}
        >
          {roles[index]}
        </motion.span>
      </AnimatePresence>
    </span>
  );
}
