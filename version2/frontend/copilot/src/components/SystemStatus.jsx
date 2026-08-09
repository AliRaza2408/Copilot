import React from 'react';
import { CheckCircle2, Clock, CircleDashed } from 'lucide-react';

const STATUSES = {
  backend:  { label: 'Backend',        text: 'Connected',        icon: CheckCircle2, color: 'text-success' },
  ai:       { label: 'AI Engine',      text: 'Ready',            icon: Clock,         color: 'text-warning' },
  waiting:  { label: 'Evidence Store', text: 'Waiting',          icon: CircleDashed,  color: 'text-muted' },
  received: { label: 'Evidence Store', text: 'Documents Received', icon: CheckCircle2, color: 'text-success' },
};

export default function SystemStatus({ evidenceReceived }) {
  const evidenceStatus = evidenceReceived ? STATUSES.received : STATUSES.waiting;
  const statuses = [STATUSES.backend, STATUSES.ai, evidenceStatus];

  return (
    <section className="mx-auto w-full max-w-[640px]">
      <div className="mb-4 text-xs font-bold uppercase tracking-[0.08em] text-muted">
        System Status
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {statuses.map(({ label, text, icon: Icon, color }) => (
          <div
            key={label}
            className="rounded-card border border-line bg-white p-5 shadow-card"
          >
            <div className="mb-3 text-sm font-semibold text-ink">{label}</div>
            <div className="flex items-center gap-2 text-[13px] font-medium text-ink">
              <Icon className={`h-4 w-4 ${color}`} />
              {text}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}