'use client'

import { Logo } from "./ui/logo"
import Link from "next/link"
import { Github, Twitter, Linkedin } from "lucide-react"

const footerLinks = [
  {
    title: "Product",
    links: [
      { name: "Features", href: "#features" },
      { name: "Pricing", href: "#pricing" },
      { name: "API", href: "#api" },
    ],
  },
  {
    title: "Resources",
    links: [
      { name: "Documentation", href: "#docs" },
      { name: "Blog", href: "#blog" },
      { name: "Support", href: "#support" },
    ],
  },
  {
    title: "Company",
    links: [
      { name: "About", href: "#about" },
      { name: "Careers", href: "#careers" },
      { name: "Contact", href: "#contact" },
    ],
  },
  {
    title: "Legal",
    links: [
      { name: "Privacy", href: "#privacy" },
      { name: "Terms", href: "#terms" },
      { name: "Security", href: "#security" },
    ],
  },
]

const socialLinks = [
  {
    name: "GitHub",
    href: "https://github.com",
    icon: Github,
  },
  {
    name: "Twitter",
    href: "https://twitter.com",
    icon: Twitter,
  },
  {
    name: "LinkedIn",
    href: "https://linkedin.com",
    icon: Linkedin,
  },
]

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="border-t border-black/20 bg-white">
      <div className="mx-auto max-w-7xl px-4 py-12">
        {/* Top section with logo and social links */}
        <div className="flex flex-col items-start justify-between gap-y-12 pb-8 md:flex-row md:items-center">
          <div>
            <Logo />
            <p className="mt-4 max-w-xs text-sm text-black/70">
              Advanced stock market predictions powered by artificial intelligence
            </p>
          </div>
          <div className="flex space-x-6">
            {socialLinks.map((item) => {
              const Icon = item.icon
              return (
                <a
                  key={item.name}
                  href={item.href}
                  className="text-black/70 hover:text-black transition-colors"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <span className="sr-only">{item.name}</span>
                  <Icon className="h-6 w-6" />
                </a>
              )
            })}
          </div>
        </div>

        {/* Links grid */}
        <div className="grid grid-cols-2 gap-8 pt-8 md:grid-cols-4">
          {footerLinks.map((group) => (
            <div key={group.title}>
              <h3 className="text-sm font-semibold text-black">{group.title}</h3>
              <ul className="mt-4 space-y-3">
                {group.links.map((link) => (
                  <li key={link.name}>
                    <Link
                      href={link.href}
                      className="text-sm text-black/70 hover:text-black transition-colors"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom section with copyright */}
        <div className="mt-12 pt-8 border-t border-black/20">
          <p className="text-sm text-black/70 text-center">
            &copy; {currentYear} StockAI. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
