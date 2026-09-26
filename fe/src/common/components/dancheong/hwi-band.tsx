import { useId } from 'react';

const SCALES = [
  { r: 20, fill: '#2F4FA3' },
  { r: 17, fill: '#7E9BDB' },
  { r: 15, fill: '#FFFDF7' },
  { r: 14, fill: '#E4572E' },
  { r: 11, fill: '#F08A4B' },
  { r: 9, fill: '#FFFDF7' },
  { r: 8, fill: '#4BB39A' },
  { r: 5.5, fill: '#9AD8C4' },
  { r: 3.5, fill: '#F4B63A' },
];

type HwiBandProps = {
  /** 휘 띠 아래에 점 띠를 붙인다 */
  withDots?: boolean;
  className?: string;
};

/** 조선 단청의 휘(暈) 띠 — 겹겹이 쌓인 반원 비늘 무늬. 장식용. */
export function HwiBand({ withDots = true, className }: HwiBandProps) {
  const id = useId().replace(/:/g, '');
  const height = withDots ? 42 : 30;

  return (
    <svg
      aria-hidden="true"
      className={className}
      width="100%"
      height={height}
      preserveAspectRatio="none"
    >
      <defs>
        <pattern
          id={`hwi-${id}`}
          width="40"
          height="30"
          patternUnits="userSpaceOnUse"
        >
          <rect width="40" height="30" fill="#2E6B5E" />
          {[0, 20, 40].map((cx) => (
            <g key={cx}>
              {SCALES.map(({ r, fill }) => (
                <circle key={r} cx={cx} cy="30" r={r} fill={fill} />
              ))}
            </g>
          ))}
        </pattern>
        <pattern
          id={`dots-${id}`}
          width="18"
          height="12"
          patternUnits="userSpaceOnUse"
        >
          <rect width="18" height="12" fill="#2E6B5E" />
          <circle cx="9" cy="6" r="4.2" fill="#F2A38E" />
          <circle cx="9" cy="6" r="2.4" fill="#E4572E" />
          <circle cx="9" cy="6" r="0.9" fill="#F4B63A" />
        </pattern>
      </defs>
      <rect width="100%" height="30" fill={`url(#hwi-${id})`} />
      {withDots && (
        <rect y="30" width="100%" height="12" fill={`url(#dots-${id})`} />
      )}
    </svg>
  );
}
