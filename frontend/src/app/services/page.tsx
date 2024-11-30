'use client';

import { BarChart2, Brain, Cloud, Lock, Search, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import Link from "next/link"

const services = [
  {
    title: "AI Stock Predictions",
    description: "Get accurate stock predictions powered by advanced AI models",
    icon: Brain,
    features: [
      "Machine learning-based predictions",
      "Pattern recognition",
      "Market trend analysis",
      "Risk assessment"
    ]
  },
  {
    title: "Real-time Analysis",
    description: "Analyze market data in real-time for instant insights",
    icon: BarChart2,
    features: [
      "Live market data",
      "Technical indicators",
      "Sentiment analysis",
      "Price alerts"
    ]
  },
  {
    title: "Market Research",
    description: "Comprehensive market research and company analysis",
    icon: Search,
    features: [
      "Company fundamentals",
      "Industry analysis",
      "Competitor tracking",
      "News sentiment"
    ]
  },
  {
    title: "Portfolio Management",
    description: "Advanced tools for portfolio optimization and tracking",
    icon: Cloud,
    features: [
      "Portfolio tracking",
      "Risk management",
      "Performance analytics",
      "Rebalancing suggestions"
    ]
  },
  {
    title: "Secure Trading",
    description: "Enterprise-grade security for your trading activities",
    icon: Lock,
    features: [
      "Encrypted data",
      "Secure authentication",
      "Transaction monitoring",
      "Compliance checks"
    ]
  },
  {
    title: "Trading Automation",
    description: "Automate your trading strategies with AI",
    icon: Zap,
    features: [
      "Strategy automation",
      "Backtesting",
      "Custom alerts",
      "API integration"
    ]
  }
]

export default function Services() {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center space-y-6">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-royal-200 to-royal-400 text-transparent bg-clip-text animate-fade-in">
          Our Services
        </h1>
        <p className="text-xl text-royal-200 max-w-3xl mx-auto animate-fade-in-delayed">
          Comprehensive AI-powered stock analysis and prediction services
        </p>
      </section>

      {/* Services Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {services.map((service, index) => (
          <div
            key={service.title}
            className="p-6 rounded-lg border border-royal-800 bg-black/50 backdrop-blur-sm hover:border-royal-600 transition-colors animate-fade-in-up"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <service.icon className="h-12 w-12 text-royal-400 mb-4" />
            <h3 className="text-xl font-semibold mb-2 text-royal-200">{service.title}</h3>
            <p className="text-royal-300 mb-4">{service.description}</p>
            <ul className="space-y-2">
              {service.features.map((feature) => (
                <li key={feature} className="text-royal-400 text-sm flex items-center">
                  <div className="w-1.5 h-1.5 rounded-full bg-royal-400 mr-2" />
                  {feature}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </section>

      {/* CTA Section */}
      <section className="text-center space-y-6">
        <h2 className="text-3xl font-bold text-royal-200 animate-fade-in">
          Ready to Start Trading Smarter?
        </h2>
        <p className="text-xl text-royal-300 max-w-2xl mx-auto animate-fade-in-delayed">
          Join us and experience the power of AI-driven stock predictions
        </p>
        <div className="animate-fade-in-delayed">
          <Link href="/dashboard">
            <Button size="lg" className="bg-royal-600 hover:bg-royal-700">
              Get Started Now
            </Button>
          </Link>
        </div>
      </section>
    </div>
  )
}
