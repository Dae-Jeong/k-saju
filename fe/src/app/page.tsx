import { HwiBand } from '@/common/components/dancheong/hwi-band';

const PILLARS = [
  { han: '丁', label: '시주', color: 'text-fire' },
  { han: '甲', label: '일주', color: 'text-wood' },
  { han: '辛', label: '월주', color: 'text-metal' },
  { han: '庚', label: '연주', color: 'text-metal' },
];

export default function Welcome() {
  return (
    <div className="flex flex-1 flex-col">
      <header className="mx-auto flex w-full max-w-5xl items-center justify-between px-6 py-4">
        <span className="font-serif text-lg font-black tracking-wide">
          SERVICE
        </span>
        <span className="text-muted-foreground text-xs">서비스 준비 중</span>
      </header>
      <HwiBand />

      <main className="mx-auto grid w-full max-w-5xl flex-1 grid-cols-1 items-center gap-12 px-6 py-16 md:grid-cols-[1.2fr_1fr]">
        <section className="flex min-w-0 flex-col gap-5">
          <span className="text-muted-foreground text-xs tracking-[0.16em]">
            KOREAN SAJU · 사주
          </span>
          <h1 className="font-serif text-4xl leading-tight font-black md:text-6xl">
            여덟 글자로
            <br />
            읽는 나
          </h1>
          <p className="text-muted-foreground max-w-md text-base leading-relaxed">
            태어난 순간의 네 기둥으로 타고난 성향과 흐름을 읽어요. 곧 무료로 내
            사주를 볼 수 있어요.
          </p>
          <div className="flex flex-wrap items-center gap-3">
            <span className="bg-primary text-primary-foreground rounded-xl px-6 py-3.5 text-base font-bold">
              곧 열려요
            </span>
            <span className="text-muted-foreground text-sm">
              가입 없이 무료 · 한국어 / English
            </span>
          </div>
        </section>

        <section
          aria-label="예시 아키타입 카드"
          className="bg-card border-line min-w-0 overflow-hidden rounded-2xl border"
        >
          <HwiBand withDots={false} />
          <div className="flex flex-col items-center gap-2 px-6 py-8 text-center">
            <span className="text-muted-foreground text-xs tracking-[0.14em]">
              예시 · 아키타입
            </span>
            <span className="text-wood font-serif text-7xl leading-none font-black">
              甲
            </span>
            <span className="font-serif text-xl font-bold">갑목 · 큰 나무</span>
            <span className="text-muted-foreground text-xs tracking-[0.14em]">
              YANG WOOD · THE GREAT TREE
            </span>
            <div className="mt-4 grid w-full grid-cols-4 gap-2">
              {PILLARS.map(({ han, label, color }) => (
                <div
                  key={label}
                  className="bg-background border-line rounded-lg border py-2"
                >
                  <div className={`font-serif text-2xl font-black ${color}`}>
                    {han}
                  </div>
                  <div className="text-muted-foreground text-[11px]">
                    {label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-secondary text-muted-foreground px-6 py-6 text-[11px] leading-relaxed">
        <div className="mx-auto max-w-5xl">
          <div className="text-foreground font-bold">Service (가칭)</div>
          <div>Korean Saju · 곧 만나요.</div>
        </div>
      </footer>
    </div>
  );
}
