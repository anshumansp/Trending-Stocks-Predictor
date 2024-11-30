'use client'

import { LucideIcon } from 'lucide-react';

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
}

export function FeatureCard({ icon: Icon, title, description }: FeatureCardProps) {
  return (
    <div className="feature-card">
      <div className="feature-icon">
        <Icon className="h-5 w-5" />
      </div>
      <h3 className="font-semibold text-lg mb-2">{title}</h3>
      <p className="text-neutral-600">{description}</p>
    </div>
  );
}
