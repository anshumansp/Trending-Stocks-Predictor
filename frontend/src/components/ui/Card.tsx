interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export const Card = ({ children, className = '' }: CardProps) => (
  <div className={`bg-white p-6 rounded-lg shadow-lg ${className}`}>
    {children}
  </div>
);
