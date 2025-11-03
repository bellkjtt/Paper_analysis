/**
 * Root layout component
 * Single Responsibility: Application shell and global configuration
 */

import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '논문 분석 시스템',
  description: 'Gemini Flash 2.5 기반 학술 논문 분석',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
