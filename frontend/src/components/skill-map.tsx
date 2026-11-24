"use client";

import { useMemo, useState } from "react";

type SkillNode = {
  id: string;
  label: string;
  x: number;
  y: number;
  radius: number;
  color: string;
  evidence: string;
};

const nodes: SkillNode[] = [
  { id: "sql", label: "SQL", x: 255, y: 178, radius: 31, color: "#2f62d8", evidence: "Used across revenue assurance, campaign analysis, data marts, and 11M+ taxi records." },
  { id: "powerbi", label: "Power BI", x: 410, y: 244, radius: 28, color: "#7540df", evidence: "Used for churn, retention, taxi operations, and executive KPI dashboards." },
  { id: "python", label: "Python", x: 148, y: 116, radius: 27, color: "#244db7", evidence: "Used across analytics automation, predictive modelling, NLP, and data workflows." },
  { id: "postgresql", label: "PostgreSQL", x: 112, y: 218, radius: 24, color: "#0b8a71", evidence: "Used to build operational pipelines, campaign analysis queries, and service-wise data marts." },
  { id: "dax", label: "DAX", x: 465, y: 145, radius: 22, color: "#f29c18", evidence: "Used to define business metrics and measures in Power BI reporting." },
  { id: "modelling", label: "Data Modelling", x: 350, y: 90, radius: 23, color: "#3d8df0", evidence: "Used to structure analytical models, retention views, and reusable reporting layers." },
  { id: "pandas", label: "Pandas", x: 55, y: 88, radius: 20, color: "#4a86df", evidence: "Used for cleaning, transformation, exploratory analysis, and feature preparation." },
  { id: "ml", label: "ML", x: 67, y: 300, radius: 22, color: "#8d54ef", evidence: "Used for churn prediction, segmentation, score prediction, and model evaluation." },
  { id: "nlp", label: "NLP", x: 190, y: 307, radius: 20, color: "#13b887", evidence: "Used for text classification and the Romanized Bangla notification thesis." },
  { id: "fastapi", label: "FastAPI", x: 300, y: 310, radius: 23, color: "#0b9e9e", evidence: "Used in Snap-a-Store and this portfolio backend for typed APIs and workflows." },
  { id: "pipelines", label: "Pipelines", x: 440, y: 42, radius: 19, color: "#579ef3", evidence: "Used for incremental loading, service monitoring, and reporting automation." },
  { id: "ab", label: "A/B Testing", x: 415, y: 320, radius: 17, color: "#e7a01a", evidence: "Used with Python for landing-page conversion analysis and statistical comparison." },
];

const links = [
  ["sql", "powerbi"], ["sql", "modelling"], ["sql", "pipelines"],
  ["powerbi", "dax"], ["powerbi", "modelling"],
  ["python", "pandas"], ["python", "ml"], ["python", "nlp"], ["python", "fastapi"], ["python", "ab"],
  ["postgresql", "pipelines"], ["ml", "nlp"], ["fastapi", "pipelines"],
] as const;

export function SkillMap() {
  const [active, setActive] = useState<string | null>(null);
  const nodeById = useMemo(() => new Map(nodes.map((node) => [node.id, node])), []);
  const connected = (id: string) => !active || id === active || links.some(([from, to]) => (from === active && to === id) || (to === active && from === id));

  return (
    <div className="skill-map" aria-label="Interactive skill map">
      <div className="skill-map__header"><span className="eyebrow">capability map</span><span className="muted text-xs">hover a node to trace the chain</span></div>
      <svg viewBox="0 0 520 360" role="img" aria-labelledby="skill-map-title skill-map-description">
        <title id="skill-map-title">Skills connected across projects and professional work</title>
        <desc id="skill-map-description">Bubble size represents demonstrated depth of use. Lines show skills used together.</desc>
        <g className="skill-map__links">{links.map(([from, to]) => { const source = nodeById.get(from)!; const target = nodeById.get(to)!; const isActive = Boolean(active) && connected(from) && connected(to); return <line key={`${from}-${to}`} className={isActive ? "skill-link is-visible" : "skill-link is-hidden"} x1={source.x} y1={source.y} x2={target.x} y2={target.y} />; })}</g>
        <g>{nodes.map((node) => <g className={`skill-node ${connected(node.id) ? "is-visible" : "is-dimmed"}`} key={node.id} onMouseEnter={() => setActive(node.id)} onMouseLeave={() => setActive(null)} onFocus={() => setActive(node.id)} onBlur={() => setActive(null)} role="button" tabIndex={0} aria-label={node.label}><circle cx={node.x} cy={node.y} r={node.radius + 8} className="skill-node__halo" /><circle cx={node.x} cy={node.y} r={node.radius} fill={node.color} className="skill-node__bubble" /><text x={node.x + node.radius + 10} y={node.y + 5} className="skill-node__label">{node.label}</text></g>)}</g>
      </svg>
      <div className="skill-map__legend"><span><i className="skill-map__legend-dot" /> deeper demonstrated use</span><span><i className="skill-map__legend-line" /> shared workflow</span></div>
    </div>
  );
}
