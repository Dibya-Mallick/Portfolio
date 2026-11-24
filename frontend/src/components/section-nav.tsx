"use client";

import { useEffect, useState } from "react";

const sections = ["top", "about", "experience", "projects", "contact"];

export function SectionNav() {
  const [active, setActive] = useState("top");

  useEffect(() => {
    let frame = 0;
    const updateActive = () => {
      const current = sections.reduce((closest, id) => {
        const element = document.getElementById(id);
        if (!element) return closest;
        const distance = Math.abs(element.getBoundingClientRect().top - 130);
        return distance < closest.distance ? { id, distance } : closest;
      }, { id: "top", distance: Number.POSITIVE_INFINITY });
      setActive(current.id);
      frame = 0;
    };
    const onScroll = () => {
      if (!frame) frame = window.requestAnimationFrame(updateActive);
    };
    updateActive();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (frame) window.cancelAnimationFrame(frame);
    };
  }, []);

  return <div className="hidden gap-6 text-sm text-[#aab4d0] md:flex md:flex-col md:gap-5">{sections.slice(1).map((item) => <a className={`section-nav-link ${active === item ? "is-active" : ""}`} key={item} href={`#${item}`}>{item}</a>)}</div>;
}
