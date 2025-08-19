import Link from 'next/link'
import { ArrowLeft, MessageCircle, Database, Cpu, Search } from 'lucide-react'

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
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
          <h1 className="text-xl font-semibold text-gray-900">About RAG Chatbot</h1>
          <div className="w-24"></div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Introduction */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
          <div className="flex items-center space-x-3 mb-6">
            <MessageCircle className="h-8 w-8 text-primary-600" />
            <h2 className="text-3xl font-bold text-gray-900">What is RAG?</h2>
          </div>
          <p className="text-lg text-gray-700 leading-relaxed mb-6">
            RAG (Retrieval-Augmented Generation) is an advanced AI technique that combines the power of 
            information retrieval with natural language generation. Instead of relying solely on 
            pre-trained knowledge, our chatbot can access and retrieve relevant information from 
            external knowledge bases to provide more accurate and up-to-date responses.
          </p>
          <div className="bg-primary-50 border-l-4 border-primary-600 p-6 rounded-r-lg">
            <p className="text-primary-800 font-medium">
              Our RAG system ensures that every response is grounded in reliable, retrievable information, 
              making conversations more accurate and contextually relevant.
            </p>
          </div>
        </div>

        {/* How it Works */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
                <Search className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">1. Query Processing</h3>
              <p className="text-gray-600">
                Your question is analyzed and converted into a format optimized for information retrieval.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-green-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
                <Database className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">2. Information Retrieval</h3>
              <p className="text-gray-600">
                Relevant documents and data are retrieved from our knowledge base using advanced search algorithms.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
                <Cpu className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">3. Response Generation</h3>
              <p className="text-gray-600">
                The retrieved information is used to generate a comprehensive and accurate response.
              </p>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Key Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex items-start space-x-3">
              <div className="bg-primary-100 rounded-lg p-2 mt-1">
                <MessageCircle className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Natural Conversations</h3>
                <p className="text-gray-600">Engage in natural, flowing conversations with context awareness.</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-primary-100 rounded-lg p-2 mt-1">
                <Database className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Knowledge Grounding</h3>
                <p className="text-gray-600">Every response is backed by reliable, retrievable information.</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-primary-100 rounded-lg p-2 mt-1">
                <Search className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Smart Search</h3>
                <p className="text-gray-600">Advanced search algorithms find the most relevant information quickly.</p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-primary-100 rounded-lg p-2 mt-1">
                <Cpu className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Real-time Processing</h3>
                <p className="text-gray-600">Fast, efficient processing for immediate responses.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Technology Stack */}
        <div className="bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Technology Stack</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="font-semibold text-gray-900 mb-1">Frontend</div>
              <div className="text-sm text-gray-600">Next.js, React, TypeScript</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="font-semibold text-gray-900 mb-1">Styling</div>
              <div className="text-sm text-gray-600">Tailwind CSS</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="font-semibold text-gray-900 mb-1">Icons</div>
              <div className="text-sm text-gray-600">Lucide React</div>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="font-semibold text-gray-900 mb-1">HTTP Client</div>
              <div className="text-sm text-gray-600">Axios</div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center mt-8">
          <Link href="/chat" className="btn-primary inline-flex items-center text-lg px-8 py-3">
            <MessageCircle className="mr-2 h-5 w-5" />
            Try the Chatbot Now
          </Link>
        </div>
      </main>
    </div>
  )
}
