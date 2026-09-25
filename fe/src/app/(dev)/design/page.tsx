'use client';

import { useState } from 'react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';

const colorTokens = [
  'background',
  'foreground',
  'card',
  'card-foreground',
  'popover',
  'popover-foreground',
  'primary',
  'primary-foreground',
  'secondary',
  'secondary-foreground',
  'muted',
  'muted-foreground',
  'accent',
  'accent-foreground',
  'destructive',
  'border',
  'input',
  'ring',
] as const;

const chartTokens = [
  'chart-1',
  'chart-2',
  'chart-3',
  'chart-4',
  'chart-5',
] as const;

const typographyScale = [
  { label: 'text-4xl', className: 'text-4xl font-semibold' },
  { label: 'text-3xl', className: 'text-3xl font-semibold' },
  { label: 'text-2xl', className: 'text-2xl font-semibold' },
  { label: 'text-xl', className: 'text-xl font-medium' },
  { label: 'text-lg', className: 'text-lg font-medium' },
  { label: 'text-base', className: 'text-base' },
  { label: 'text-sm', className: 'text-sm' },
  { label: 'text-xs', className: 'text-xs' },
] as const;

const Swatch = ({ token }: { token: string }) => (
  <div className="flex flex-col gap-2">
    <div
      className="border-border h-16 w-full rounded-md border"
      style={{ backgroundColor: `var(--${token})` }}
    />
    <span className="text-muted-foreground font-mono text-xs">{token}</span>
  </div>
);

export default function DesignPreviewPage() {
  const [dialogOpen, setDialogOpen] = useState(false);

  return (
    <main className="mx-auto flex w-full max-w-4xl flex-col gap-12 px-6 py-16">
      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-semibold tracking-tight">
          Design preview
        </h1>
        <p className="text-muted-foreground">
          Dev-only page: color tokens, typography scale, and every installed
          shadcn/ui component. Not linked from production navigation.
        </p>
      </header>

      <section className="flex flex-col gap-4">
        <h2 className="text-xl font-semibold">Color tokens</h2>
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4">
          {colorTokens.map((token) => (
            <Swatch key={token} token={token} />
          ))}
        </div>
        <h3 className="text-muted-foreground text-sm font-medium">Charts</h3>
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-5">
          {chartTokens.map((token) => (
            <Swatch key={token} token={token} />
          ))}
        </div>
      </section>

      <Separator />

      <section className="flex flex-col gap-4">
        <h2 className="text-xl font-semibold">Typography</h2>
        <div className="flex flex-col gap-3">
          {typographyScale.map(({ label, className }) => (
            <div key={label} className="flex items-baseline gap-4">
              <span className="text-muted-foreground w-20 shrink-0 font-mono text-xs">
                {label}
              </span>
              <p className={className}>가나다 Aa 타이포그래피 스케일</p>
            </div>
          ))}
        </div>
      </section>

      <Separator />

      <section className="flex flex-col gap-4">
        <h2 className="text-xl font-semibold">Components</h2>

        <Card>
          <CardHeader>
            <CardTitle>Buttons</CardTitle>
            <CardDescription>Variants and sizes</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            <Button variant="default">Default</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="destructive">Destructive</Button>
            <Button variant="link">Link</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Form fields</CardTitle>
            <CardDescription>Input, label, select</CardDescription>
          </CardHeader>
          <CardContent>
            <FieldGroup>
              <Field>
                <FieldLabel htmlFor="design-name">Name</FieldLabel>
                <Input id="design-name" placeholder="Jane Doe" />
                <FieldDescription>
                  Plain label + input pairing.
                </FieldDescription>
              </Field>
              <Field>
                <Label htmlFor="design-email">Email</Label>
                <Input
                  id="design-email"
                  type="email"
                  placeholder="jane@example.com"
                />
              </Field>
              <Field>
                <FieldLabel htmlFor="design-role">Role</FieldLabel>
                <Select>
                  <SelectTrigger id="design-role" className="w-full">
                    <SelectValue placeholder="Select a role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="admin">Admin</SelectItem>
                    <SelectItem value="member">Member</SelectItem>
                    <SelectItem value="guest">Guest</SelectItem>
                  </SelectContent>
                </Select>
              </Field>
            </FieldGroup>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Dialog &amp; toast</CardTitle>
            <CardDescription>Overlay and notification patterns</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-2">
            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
              <DialogTrigger asChild>
                <Button variant="outline">Open dialog</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Example dialog</DialogTitle>
                  <DialogDescription>
                    Rendered with the shadcn Dialog component.
                  </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                  <Button onClick={() => setDialogOpen(false)}>Close</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>

            <Button
              variant="secondary"
              onClick={() =>
                toast('Example toast', {
                  description: 'Rendered with the shadcn Sonner Toaster.',
                })
              }
            >
              Show toast
            </Button>
          </CardContent>
        </Card>
      </section>
    </main>
  );
}
