"use client";

import { useEffect } from "react";

const groups = [
  { selector: "main > section", step: 90 },
  { selector: "#about .glass, #experience article", step: 90 },
  { selector: "#projects a.glass", step: 100 },
  { selector: ".section .grid > .glass, .section .space-y-3 > .glass", step: 80 },
  { selector: "#top .skill-node", step: 55 },
  { selector: "#contact form > *", step: 80 },
];

export function ScrollReveal() {
  useEffect(() => {
    const elements = groups.flatMap(({ selector, step }) =>
      Array.from(document.querySelectorAll<HTMLElement>(selector)).map((element, index) => {
        element.classList.add("scroll-reveal");
        element.style.setProperty("--reveal-delay", `${index * step}ms`);
        return element;
      }),
    );

    const observer = new IntersectionObserver(
      (entries) => entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      }),
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" },
    );

    elements.forEach((element) => observer.observe(element));
    return () => observer.disconnect();
  }, []);

  return null;
}
