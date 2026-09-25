import Link from 'next/link';

import { Button } from '@/components/ui/button';

export default function Home() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center gap-4 p-16 text-center">
      <h1 className="text-3xl font-semibold tracking-tight">App</h1>
      <p className="text-muted-foreground max-w-md">
        Frontend scaffold. See the design token and component preview at{' '}
        <code className="bg-muted rounded px-1.5 py-0.5 font-mono text-sm">
          /design
        </code>
        .
      </p>
      <Button asChild>
        <Link href="/design">View design preview</Link>
      </Button>
    </main>
  );
}
