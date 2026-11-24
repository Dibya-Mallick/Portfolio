import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "Dibya Ayishwarja Mallick | Data & AI Portfolio", description: "Portfolio of Dibya Ayishwarja Mallick, a data professional working across analytics, BI, machine learning, and applied AI.", metadataBase: new URL("https://dibya-mallick.dev") };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
