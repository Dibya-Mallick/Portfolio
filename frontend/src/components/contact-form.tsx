"use client";

import { FormEvent, useState } from "react";

const endpoint = `${process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"}/api/v1/contact`;

export function ContactForm() {
  const [status, setStatus] = useState<"idle" | "sending" | "success" | "error">("idle");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus("sending");
    const form = new FormData(event.currentTarget);
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(form.entries())),
      });
      if (!response.ok) throw new Error("Request failed");
      event.currentTarget.reset();
      setStatus("success");
    } catch {
      setStatus("error");
    }
  }

  return (
    <form className="mt-8 grid gap-3" onSubmit={submit}>
      <div className="grid gap-3 sm:grid-cols-2">
        <input className="rounded-xl border border-[#606060] bg-[#242424] px-4 py-3 text-sm outline-none focus:border-cyan-300" name="name" placeholder="Your name" required maxLength={120} />
        <input className="rounded-xl border border-[#606060] bg-[#242424] px-4 py-3 text-sm outline-none focus:border-cyan-300" name="email" type="email" placeholder="Your email" required maxLength={254} />
      </div>
      <input className="rounded-xl border border-[#606060] bg-[#242424] px-4 py-3 text-sm outline-none focus:border-cyan-300" name="subject" placeholder="Subject (optional)" maxLength={180} />
      <textarea className="min-h-32 rounded-xl border border-[#606060] bg-[#242424] px-4 py-3 text-sm outline-none focus:border-cyan-300" name="message" placeholder="Tell me a little about what you are working on..." required maxLength={5000} />
      <input className="hidden" name="website" tabIndex={-1} autoComplete="off" aria-hidden="true" />
      <div className="flex flex-wrap items-center gap-4"><button className="rounded-full bg-cyan-300 px-6 py-3 font-bold text-[#00072d] disabled:opacity-50" disabled={status === "sending"} type="submit">{status === "sending" ? "Sending..." : "Send message"}</button>{status === "success" && <span className="text-sm text-emerald-300">Message sent—thank you.</span>}{status === "error" && <span className="text-sm text-rose-300">Could not send. Please try again or email directly.</span>}</div>
    </form>
  );
}
