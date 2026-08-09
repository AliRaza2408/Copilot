import React from 'react';
import UploadBox from './UploadBox';

export default function ChallengePack({ onUploadSuccess }) {
  return (
    <section className="mx-auto w-full max-w-[640px] overflow-hidden rounded-card border border-line bg-white shadow-card">
      <div className="border-b border-line bg-frost px-8 py-5">
        <span className="text-xs font-bold uppercase tracking-[0.08em] text-secondary">
          Challenge Pack
        </span>
      </div>
      
      <div className="p-8">
        <UploadBox onUploadSuccess={onUploadSuccess} />
      </div>
    </section>
  );
}