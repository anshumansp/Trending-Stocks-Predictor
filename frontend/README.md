# Stocks Predictor Frontend

A modern, AI-powered stock prediction platform built with Next.js and Tailwind CSS.

## Features

- 🤖 AI-powered stock predictions
- 📊 Real-time market analysis
- 📈 Technical indicators and charts
- 🔒 Secure authentication with Clerk
- 🌙 Dark mode support
- 🎨 Beautiful UI with smooth animations

## Tech Stack

- Next.js 14
- TypeScript
- Tailwind CSS
- Clerk Authentication
- React Hooks
- CSS Animations

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
Create a `.env.local` file with your Clerk keys:
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_publishable_key
CLERK_SECRET_KEY=your_secret_key
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

- `/app` - Next.js app router pages and layouts
- `/components` - Reusable UI components
- `/lib` - Utility functions and shared code
- `/public` - Static assets
- `/styles` - Global styles and Tailwind configuration

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
