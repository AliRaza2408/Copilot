export default function HeroSection() {
  return (
    <section className="mx-auto max-w-[800px] text-center">
      <h1 className="text-[clamp(28px,4vw,40px)] font-extrabold leading-[1.2] tracking-tight text-primary">
        Turn manufacturing evidence into a{' '}
        <span className="text-accent">defensible supplier decision.</span>
      </h1>
      <p className="mt-4 text-[17px] leading-relaxed text-muted">
        Upload product requirements and supplier evidence to begin your sourcing analysis.
      </p>
    </section>
  );
}