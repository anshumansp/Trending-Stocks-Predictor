'use client'

import { Button } from "@/components/ui/button"
import { ArrowRight, BarChart2, LineChart, TrendingUp, Shield } from "lucide-react"
import Link from "next/link"

export default function Home() {
  return (
    <main className="flex-1">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            AI-Powered Stock Market
            <br />
            Predictions & Analysis
          </h1>
          <p className="hero-subtitle">
            Make informed investment decisions with our advanced AI algorithms and real-time market analysis.
            Get accurate predictions and comprehensive insights for your portfolio.
          </p>
          <div className="flex items-center justify-center gap-4">
            <Link href="/stock-predictor">
              <Button className="btn-primary">
                Try Stock Predictor
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="section bg-background-subtle">
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">95%</div>
            <div className="stat-label">Prediction Accuracy</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">10K+</div>
            <div className="stat-label">Active Users</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">24/7</div>
            <div className="stat-label">Market Monitoring</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">500+</div>
            <div className="stat-label">Supported Stocks</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="section">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title text-center">Powerful Features</h2>
          <p className="section-subtitle text-center">
            Everything you need to make smart investment decisions
          </p>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
            <div className="feature-card">
              <div className="feature-icon">
                <BarChart2 className="h-5 w-5" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Real-time Analysis</h3>
              <p className="text-neutral-600">
                Get instant insights with real-time market data and AI-powered analysis
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">
                <LineChart className="h-5 w-5" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Price Predictions</h3>
              <p className="text-neutral-600">
                Advanced ML models predict future stock prices with high accuracy
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">
                <TrendingUp className="h-5 w-5" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Trend Detection</h3>
              <p className="text-neutral-600">
                Identify market trends and patterns before they become obvious
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="section bg-background-subtle">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="section-title text-center">About Our Platform</h2>
          <p className="section-subtitle text-center">
            We combine cutting-edge AI technology with comprehensive market data to provide
            you with the most accurate stock predictions and analysis
          </p>
          
          <div className="grid md:grid-cols-2 gap-12 mt-12">
            <div className="space-y-6">
              <h3 className="text-2xl font-semibold">Why Choose Us?</h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <Shield className="h-6 w-6 text-primary flex-shrink-0" />
                  <div>
                    <p className="font-medium">Advanced AI Technology</p>
                    <p className="text-neutral-600">State-of-the-art machine learning models trained on vast market data</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <Shield className="h-6 w-6 text-primary flex-shrink-0" />
                  <div>
                    <p className="font-medium">Real-time Updates</p>
                    <p className="text-neutral-600">Instant market data and predictions updated in real-time</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <Shield className="h-6 w-6 text-primary flex-shrink-0" />
                  <div>
                    <p className="font-medium">Expert Analysis</p>
                    <p className="text-neutral-600">Comprehensive insights from financial experts and AI analysis</p>
                  </div>
                </li>
              </ul>
            </div>
            
            <div className="space-y-6">
              <h3 className="text-2xl text-neutral-900 font-semibold">Our Mission</h3>
              <p className="text-neutral-600">
                We're on a mission to democratize stock market analysis and make professional-grade
                investment tools accessible to everyone. Our platform combines the power of artificial
                intelligence with user-friendly interfaces to help you make better investment decisions.
              </p>
              <p className="text-neutral-600">
                Whether you're a seasoned investor or just starting out, our tools provide the insights
                you need to navigate the market with confidence.
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
