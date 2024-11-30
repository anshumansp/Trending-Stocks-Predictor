export function Logo({ className = "" }) {
  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      <svg
        width="32"
        height="32"
        viewBox="0 0 32 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="text-black"
      >
        <path
          d="M16 2L2 9L16 16L30 9L16 2Z"
          fill="currentColor"
          fillOpacity="0.2"
        />
        <path
          d="M2 23L16 30L30 23V9L16 16L2 9V23Z"
          fill="currentColor"
          fillOpacity="0.4"
        />
        <path
          d="M16 16L2 9V23L16 30V16Z"
          fill="currentColor"
          fillOpacity="0.8"
        />
      </svg>
      <span className="text-xl font-bold text-black">
        StockAI
      </span>
    </div>
  );
}
