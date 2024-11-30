"use client"

import { SignInButton, SignedIn, SignedOut, UserButton } from "@clerk/nextjs"
import Link from "next/link"
import { Button } from "./ui/button"
import { usePathname } from "next/navigation"
import { Logo } from "./ui/logo"

export default function Navbar() {
  const pathname = usePathname()

  const isActive = (path: string) => {
    return pathname === path ? "text-black font-medium" : "text-black/70 hover:text-black transition-colors"
  }

  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-blue/20">
      <div className="container mx-auto">
        <div className="flex items-center justify-between h-16 px-4">
          {/* Logo */}
          <Link href="/" className="flex items-center">
            <Logo />
          </Link>

          {/* Navigation Links */}
          <div className="flex items-center space-x-8">
            <Link href="/" className={isActive("/")}>
              Home
            </Link>
            <Link href="/stock-predictor" className={isActive("/stock-predictor")}>
              Stock Predictor
            </Link>
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-4">
            <SignedIn>
              <UserButton 
                afterSignOutUrl="/"
                appearance={{
                  elements: {
                    avatarBox: "w-8 h-8 rounded-full ring-2 ring-blue/20"
                  }
                }}
              />
            </SignedIn>
            <SignedOut>
              <SignInButton mode="modal">
                <Button className="btn-primary">
                  Sign In
                </Button>
              </SignInButton>
            </SignedOut>
          </div>
        </div>
      </div>
    </nav>
  )
}
