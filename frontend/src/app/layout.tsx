import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Drama World Lab',
  description: 'AI-powered 3D drama world generation and agent simulation',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
