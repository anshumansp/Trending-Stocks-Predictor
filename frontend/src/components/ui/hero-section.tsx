'use client'

interface HeroSectionProps {
  title: string;
  subtitle: string;
  children?: React.ReactNode;
}

export function HeroSection({ title, subtitle, children }: HeroSectionProps) {
  return (
    <section className="hero">
      <div className="hero-content">
        <h1 className="hero-title">
          {title}
        </h1>
        <p className="hero-subtitle">
          {subtitle}
        </p>
        {children}
      </div>
    </section>
  );
}
