"use client"

import { Award, Code, Users } from "lucide-react"

export default function About() {
  return (
    <div className="space-y-16">
      {/* About Hero */}
      <section className="text-center space-y-6">
        <h1 
          className="text-5xl font-bold bg-gradient-to-r from-royal-200 to-royal-400 text-transparent bg-clip-text animate-fade-in"
        >
          About AI Stocks Predictor
        </h1>
        <p 
          className="text-xl text-royal-200 max-w-3xl mx-auto animate-fade-in-delayed"
        >
          Building the future of stock trading with AI-powered predictions
        </p>
      </section>

      {/* Mission Section */}
      <section className="bg-gradient-to-br from-royal-900/50 to-black/50 p-12 rounded-lg border border-royal-700/30">
        <div className="max-w-4xl mx-auto space-y-6">
          <h2 className="text-3xl font-bold text-royal-200 animate-fade-in">Our Mission</h2>
          <p className="text-lg text-royal-300 animate-fade-in-delayed">
            To democratize advanced stock analysis by providing sophisticated AI-powered tools through an intuitive cloud platform. 
            We believe in making professional-grade financial analysis accessible to everyone, from individual investors to large institutions.
          </p>
        </div>
      </section>

      {/* Values Section */}
      <section className="grid md:grid-cols-3 gap-8">
        {[
          {
            icon: Code,
            title: "Innovation",
            description: "Pushing the boundaries of what's possible with AI and cloud technology"
          },
          {
            icon: Award,
            title: "Excellence",
            description: "Committed to delivering the highest quality analysis and insights"
          },
          {
            icon: Users,
            title: "User-Centric",
            description: "Building tools that empower users to make better investment decisions"
          }
        ].map((value, index) => (
          <div
            key={value.title}
            className="p-6 rounded-lg bg-gradient-to-br from-royal-900/50 to-black/50 border border-royal-700/30 animate-fade-in-up"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <value.icon className="w-12 h-12 text-royal-400 mb-4" />
            <h3 className="text-xl font-semibold mb-2 text-royal-200">{value.title}</h3>
            <p className="text-royal-300">{value.description}</p>
          </div>
        ))}
      </section>

      {/* Technology Stack */}
      <section className="space-y-8">
        <h2 className="text-3xl font-bold text-royal-200 animate-fade-in">Our Technology Stack</h2>
        <div className="grid md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-royal-200">Cloud Infrastructure</h3>
            <ul className="list-disc list-inside text-royal-300 space-y-2">
              <li>Amazon Web Services (AWS)</li>
              <li>Serverless Architecture</li>
              <li>Container Orchestration</li>
              <li>Auto-scaling Infrastructure</li>
            </ul>
          </div>
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-royal-200">AI & Analytics</h3>
            <ul className="list-disc list-inside text-royal-300 space-y-2">
              <li>Claude AI Integration</li>
              <li>Real-time Data Processing</li>
              <li>Machine Learning Models</li>
              <li>Advanced Analytics Engine</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="text-center space-y-8">
        <h2 className="text-3xl font-bold text-royal-200 animate-fade-in">Built by Experts</h2>
        <p className="text-lg text-royal-300 max-w-3xl mx-auto animate-fade-in-delayed">
          Our team combines expertise in cloud architecture, artificial intelligence, and financial markets 
          to deliver a platform that sets new standards in stock analysis and market intelligence.
        </p>
      </section>
    </div>
  )
}
