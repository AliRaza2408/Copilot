import React from 'react';
import { CheckCircle2 } from 'lucide-react';

export default function Header() {
  return (
    <header className="flex items-center justify-between border-b border-line pb-6">
      <div className="flex items-center gap-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-[10px] bg-primary text-xl font-bold text-accent">
          ◈
        </div>
        <div>
          <div className="text-[18px] font-extrabold leading-tight tracking-tight text-primary">
            AI MANUFACTURING DECISION COPILOT
          </div>
          <div className="mt-0.5 text-[13px] font-medium text-muted">
            Evidence-grounded sourcing intelligence
          </div>
        </div>
      </div>

      <div className="flex items-center gap-2 rounded-[20px] border border-line bg-mist px-4 py-2 text-[13px] font-semibold text-ink">
        <CheckCircle2 className="h-4 w-4 text-success" />
        SYSTEM READY
      </div>
    </header>
  );
}