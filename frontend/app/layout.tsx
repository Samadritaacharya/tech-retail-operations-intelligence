import type { Metadata } from 'next'
import './globals.css'
export const metadata:Metadata={title:'Retail Operations Intelligence — Action Command Center',description:'Interactive commerce operations intelligence for checkout, fulfillment, returns, support, inventory, campaigns, and accountable action.'}
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="en"><body>{children}</body></html>}
