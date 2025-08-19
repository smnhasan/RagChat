import ChatBox from '@/components/ChatBox'
import Link from 'next/link'
import { ArrowLeft } from 'lucide-react'

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <Link 
            href="/" 
            className="flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors"
          >
            <ArrowLeft className="h-5 w-5" />
            <span>Back to Home</span>
          </Link>
          <h1 className="text-xl font-semibold text-gray-900">RAG Chatbot</h1>
          <div className="w-24"></div> {/* Spacer for centering */}
        </div>
      </header>

      {/* Chat Interface */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <div className="flex-1 max-w-4xl mx-auto w-full px-4 py-6">
          <ChatBox />
        </div>
      </main>
    </div>
  )
}
