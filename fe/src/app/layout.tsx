import type { Metadata } from 'next';
import { Geist_Mono, Noto_Sans_KR } from 'next/font/google';
import { AppProviders } from './providers';
import './globals.css';

// Korean-friendly font available via next/font/google without manual
// downloads. Swap for Pretendard (self-hosted) once brand fonts are decided.
const notoSansKr = Noto_Sans_KR({
  variable: '--font-sans',
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'App',
  description: 'Project scaffold',
};

export default function RootLayout({ children }: LayoutProps<'/'>) {
  return (
    <html
      lang="ko"
      className={`${notoSansKr.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col">
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
