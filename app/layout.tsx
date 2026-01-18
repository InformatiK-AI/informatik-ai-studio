/**
 * ABOUTME: Root layout with providers
 * RESPONSIBILITY: Wrap entire app with global providers and styles
 * DEPENDENCIES: Tailwind CSS, global.css
 */
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'InformatiK-AI Studio',
  description: 'AI-powered software generation platform',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
