import Link from 'next/link'
import { MessageCircle, Brain, Zap, Shield } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-white">
      {/* Header */}
      <header className="py-6 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <MessageCircle className="h-8 w-8 text-primary-600" />
            <h1 className="text-2xl font-bold text-gray-900">RAG Chatbot</h1>
          </div>
          <nav className="flex space-x-6">
            <Link href="/chat" className="text-gray-600 hover:text-primary-600 transition-colors">
              Chat
            </Link>
            <Link href="/about" className="text-gray-600 hover:text-primary-600 transition-colors">
              About
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h2 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
            Intelligent Conversations
            <span className="text-primary-600 block">Powered by AI</span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Experience the next generation of chatbots with our Retrieval-Augmented Generation system. 
            Get accurate, contextual, and intelligent responses to your questions.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/chat" className="btn-primary inline-flex items-center text-lg px-8 py-3">
              <MessageCircle className="mr-2 h-5 w-5" />
              Start Chatting
            </Link>
            <Link href="/about" className="btn-secondary inline-flex items-center text-lg px-8 py-3">
              Learn More
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center p-6">
            <div className="bg-primary-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
              <Brain className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Smart Retrieval</h3>
            <p className="text-gray-600">
              Advanced retrieval system finds the most relevant information to answer your questions accurately.
            </p>
          </div>
          <div className="text-center p-6">
            <div className="bg-primary-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
              <Zap className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Lightning Fast</h3>
            <p className="text-gray-600">
              Get instant responses with our optimized processing pipeline and efficient retrieval algorithms.
            </p>
          </div>
          <div className="text-center p-6">
            <div className="bg-primary-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
              <Shield className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Reliable & Safe</h3>
            <p className="text-gray-600">
              Built with security and reliability in mind, ensuring your conversations remain private and secure.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <MessageCircle className="h-6 w-6" />
              <span className="text-lg font-semibold">RAG Chatbot</span>
            </div>
            <p className="text-gray-400">
              Powered by advanced AI technology for intelligent conversations.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
