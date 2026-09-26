import type { Metadata } from 'next';
import { Geist_Mono, Noto_Sans_KR, Noto_Serif_KR } from 'next/font/google';
import { AppProviders } from './providers';
import './globals.css';

// Korean-friendly font available via next/font/google without manual
// downloads. Swap for Pretendard (self-hosted) once brand fonts are decided.
const notoSansKr = Noto_Sans_KR({
  variable: '--font-sans',
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
});

const notoSerifKr = Noto_Serif_KR({
  variable: '--font-serif',
  subsets: ['latin'],
  weight: ['700', '900'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'Korean Saju · 여덟 글자로 읽는 나',
  description: '태어난 순간의 네 기둥으로 타고난 성향과 흐름을 읽는 한국 사주.',
};

export default function RootLayout({ children }: LayoutProps<'/'>) {
  return (
    <html
      lang="ko"
      className={`${notoSansKr.variable} ${notoSerifKr.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col">
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
