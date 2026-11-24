"use client";

import { useEffect, useState } from "react";

type CountryCount = { country: string; visitors: number };
type AnalyticsSummary = { visitor_count: number; country_counts: CountryCount[] };

const endpoint = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
const sessionKey = "portfolio-anonymous-session";

function getSessionId() {
  const existing = window.sessionStorage.getItem(sessionKey);
  if (existing) return existing;
  const value = crypto.randomUUID();
  window.sessionStorage.setItem(sessionKey, value);
  return value;
}

export function LiveAnalytics() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    const sessionId = getSessionId();
    void fetch(`${endpoint}/api/v1/analytics/events`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        event_type: "page_view",
        page: window.location.pathname,
        session_id: sessionId,
      }),
    }).catch(() => undefined);
  }, []);

  useEffect(() => {
    const params = new URLSearchParams();
    if (startDate) params.set("start_date", startDate);
    if (endDate) params.set("end_date", endDate);
    const query = params.toString();
    void fetch(`${endpoint}/api/v1/analytics/summary${query ? `?${query}` : ""}`, { cache: "no-store" })
      .then((response) => (response.ok ? response.json() : null))
      .then((data: AnalyticsSummary | null) => data && setSummary(data))
      .catch(() => undefined);
  }, [startDate, endDate]);

  useEffect(() => {
    const refresh = window.setInterval(() => {
      const params = new URLSearchParams();
      if (startDate) params.set("start_date", startDate);
      if (endDate) params.set("end_date", endDate);
      const query = params.toString();
      void fetch(`${endpoint}/api/v1/analytics/summary${query ? `?${query}` : ""}`, { cache: "no-store" })
        .then((response) => (response.ok ? response.json() : null))
        .then((data: AnalyticsSummary | null) => data && setSummary(data))
        .catch(() => undefined);
    }, 30_000);
    return () => window.clearInterval(refresh);
  }, [startDate, endDate]);

  return (
    <section className="section border-t border-[#26345f]" aria-label="Portfolio visitor analytics">
      <div className="container">
        <div className="mb-8 flex flex-wrap items-end justify-between gap-4">
          <div><p className="eyebrow">07 / live analytics</p><h2 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">A small signal from around the world.</h2></div>
          <span className="font-mono text-xs text-emerald-300">● updating live</span>
        </div>
        <div className="grid gap-5 lg:grid-cols-[1fr_280px]">
          <div className="grid gap-4 sm:grid-cols-[.7fr_1.3fr]">
            <div className="glass rounded-2xl p-6"><p className="muted text-sm">Anonymous visitors</p><p className="mt-3 text-5xl font-bold text-cyan-300">{summary?.visitor_count ?? "—"}</p><p className="muted mt-3 text-xs">Unique browser sessions recorded</p></div>
            <div className="glass rounded-2xl p-6"><p className="muted text-sm">Visitors by country</p><div className="mt-4 grid gap-3 sm:grid-cols-2">{summary?.country_counts.length ? summary.country_counts.slice(0, 8).map((item) => <div className="flex items-center justify-between border-b border-[#26345f] pb-2 text-sm" key={item.country}><span>{item.country === "??" ? "Unknown" : item.country}</span><span className="font-mono text-cyan-300">{item.visitors}</span></div>) : <p className="muted text-sm">Collecting the first visits...</p>}</div></div>
          </div>
          <div className="glass rounded-2xl p-6"><p className="eyebrow">date slicer</p><p className="muted mt-2 text-sm">Filter the visitor summary by date.</p><div className="mt-5 grid gap-4"><label className="grid gap-2 text-xs text-[#f5f5f5]">From<input className="rounded-lg border border-[#606060] bg-[#242424] px-3 py-2 text-sm text-[#f5f5f5] outline-none focus:border-cyan-300" type="date" value={startDate} onChange={(event) => setStartDate(event.target.value)} /></label><label className="grid gap-2 text-xs text-[#f5f5f5]">To<input className="rounded-lg border border-[#606060] bg-[#242424] px-3 py-2 text-sm text-[#f5f5f5] outline-none focus:border-cyan-300" type="date" value={endDate} onChange={(event) => setEndDate(event.target.value)} /></label><button className="rounded-full border border-[#606060] px-4 py-2 text-sm font-bold hover:border-cyan-300" type="button" onClick={() => { setStartDate(""); setEndDate(""); }}>Clear dates</button></div></div>
        </div>
      </div>
    </section>
  );
}
