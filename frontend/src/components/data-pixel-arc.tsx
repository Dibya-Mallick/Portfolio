"use client";

import { useEffect, useRef } from "react";

type DataPixelArcProps = { background?: string; baseColor?: string; accentColor?: string; highlight?: string };

const hexToRgb = (hex: string) => {
  const value = hex.replace("#", "");
  const normalized = value.length === 3 ? value.split("").map((part) => part + part).join("") : value;
  const number = Number.parseInt(normalized, 16);
  return { r: (number >> 16) & 255, g: (number >> 8) & 255, b: number & 255 };
};

export function DataPixelArc({ background = "#1b1b1b", baseColor = "#f29c18", accentColor = "#6b4510", highlight = "#fff1d6" }: DataPixelArcProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext("2d");
    if (!canvas || !context) return;
    const base = hexToRgb(baseColor), accent = hexToRgb(accentColor), bright = hexToRgb(highlight);
    let frame = 0, width = 0, height = 0, dpr = 1;
    const pointer = { x: 0.52, y: 0.48 };
    let target = { ...pointer };
    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2); width = rect.width; height = rect.height;
      canvas.width = Math.floor(width * dpr); canvas.height = Math.floor(height * dpr); context.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    const onPointerMove = (event: PointerEvent) => { target = { x: event.clientX / window.innerWidth, y: event.clientY / window.innerHeight }; };
    const render = (time: number) => {
      pointer.x += (target.x - pointer.x) * 0.04; pointer.y += (target.y - pointer.y) * 0.04;
      context.fillStyle = background; context.fillRect(0, 0, width, height);
      const spacing = Math.max(7, Math.min(11, width / 150)), columns = Math.ceil(width / spacing), rows = Math.ceil(height / spacing);
      const arcX = width * (0.5 + (pointer.x - 0.5) * 0.12), arcY = height * 0.98, radius = Math.max(width * 0.54, 420), pulse = time * 0.00055;
      for (let row = 0; row < rows; row += 1) for (let column = 0; column < columns; column += 1) {
        const x = column * spacing + spacing * 0.5, y = row * spacing + spacing * 0.5;
        const arcStrength = Math.max(0, 1 - Math.abs(Math.hypot(x - arcX, y - arcY) - radius) / (height * 0.3));
        const wave = (Math.sin(column * 0.24 + pulse * 3.2 + row * 0.08) + 1) / 2;
        const hoverStrength = Math.max(0, 1 - Math.hypot(x - width * pointer.x, y - height * pointer.y) / 240);
        const strength = Math.min(1, arcStrength * 0.72 + hoverStrength * 0.25 + wave * 0.08);
        if (strength < 0.035) continue;
        const color = strength > 0.72 ? bright : strength > 0.34 ? base : accent;
        context.fillStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${Math.min(0.82, 0.08 + strength * 0.72)})`;
        const size = Math.max(2, spacing * (0.42 + strength * 0.2)); context.fillRect(x - size / 2, y - size / 2, size, size);
      }
      frame = requestAnimationFrame(render);
    };
    resize(); window.addEventListener("resize", resize); window.addEventListener("pointermove", onPointerMove, { passive: true }); frame = requestAnimationFrame(render);
    return () => { cancelAnimationFrame(frame); window.removeEventListener("resize", resize); window.removeEventListener("pointermove", onPointerMove); };
  }, [accentColor, background, baseColor, highlight]);

  return <canvas ref={canvasRef} aria-hidden="true" className="data-pixel-arc" />;
}
