"use client"

import * as React from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <button
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="relative inline-flex items-center justify-center 
                rounded-full p-2 w-10 h-10
                bg-white/20 dark:bg-charcoal/20 
                backdrop-blur-sm
                border border-royal-purple/20 dark:border-soft-lavender/20
                hover:bg-royal-purple/10 dark:hover:bg-soft-lavender/10
                transform transition-all duration-300
                hover:scale-110 active:scale-95
                group"
      aria-label="Toggle theme"
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all duration-300
                     dark:-rotate-90 dark:scale-0 
                     text-royal-purple dark:text-soft-lavender
                     group-hover:text-royal-purple/80 dark:group-hover:text-soft-lavender/80" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all duration-300
                      dark:rotate-0 dark:scale-100 
                      text-royal-purple dark:text-soft-lavender
                      group-hover:text-royal-purple/80 dark:group-hover:text-soft-lavender/80" />
      <span className="sr-only">Toggle theme</span>
    </button>
  )
}
