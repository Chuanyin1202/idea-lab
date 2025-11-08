import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'TourneyFlow - Esports Tournament Management',
  description: '為電競賽事主辦方打造的一站式管理平台',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-TW">
      <body>{children}</body>
    </html>
  )
}
