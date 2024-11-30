/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        white: '#FFFFFF',
        blue: '#2563EB',
        black: '#000000',
        transparent: 'transparent'
      },
      fontFamily: {
        'roboto': ['Roboto', 'sans-serif'],
        'poppins': ['Poppins', 'sans-serif'],
        'sans': ['Inter', 'sans-serif'],
      },
      borderRadius: {
        'DEFAULT': 'var(--radius)',
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
        shimmer: {
          '100%': { transform: 'translateX(100%)' },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        shimmer: 'shimmer 2s infinite',
      },
      backgroundImage: {
        'gradient-light': 'linear-gradient(to bottom right, #F3E8FF, #F9F5FF)',
        'gradient-dark': 'linear-gradient(to bottom right, #1C1C1E, #2D1F4C)',
      },
    },
  },
  plugins: [
    require('tailwindcss-animate'),
  ],
}
