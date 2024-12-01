interface SectionTitleProps {
  children: React.ReactNode;
}

export const SectionTitle = ({ children }: SectionTitleProps) => (
  <h2 className="text-2xl font-bold mb-4 text-gray-900">{children}</h2>
);
