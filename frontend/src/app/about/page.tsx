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
          <h1 className="text-xl font-semibold text-gray-900">About News Reporter AI</h1>
          <div className="w-24"></div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Introduction */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
          <div className="flex items-center space-x-3 mb-6">
            <MessageCircle className="h-8 w-8 text-primary-600" />
            <h2 className="text-3xl font-bold text-gray-900">What is News Reporter AI?</h2>
          </div>
          <p className="text-lg text-gray-700 leading-relaxed mb-6">
            News Reporter AI is your go-to tool for verifying news and rumors in real-time. By leveraging advanced AI, it retrieves information from credible sources to confirm or debunk stories circulating on social media, news outlets, or other platforms. Whether you're fact-checking a viral claim or seeking clarity on recent events, News Reporter AI delivers reliable, up-to-date answers.
          </p>
          <div className="bg-primary-50 border-l-4 border-primary-600 p-6 rounded-r-lg">
            <p className="text-primary-800 font-medium">
              Stay informed with confidence—News Reporter AI ensures every response is grounded in verified information from trusted sources.
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
              <h3 className="text-lg font-semibold text-gray-900 mb-2">1. Query Analysis</h3>
              <p className="text-gray-600">
                Your question about a news event or rumor is analyzed to pinpoint key details for verification.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-green-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
                <Database className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">2. Source Retrieval</h3>
              <p className="text-gray-600">
                Relevant data is fetched from authentic news sources using advanced search techniques.
              </p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 rounded-full p-4 w-16 h-16 mx-auto mb-4">
                <Cpu className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">3. Response Generation</h3>
              <p className="text-gray-600">
                Verified information is synthesized into a clear, accurate response with source references.
              </p>
            </div>
          </div>
        </div>

        {/* Use Cases */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Use Cases</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex items-start space-x-3">
              <div className="bg-primary-100 rounded-lg p-2 mt-1">
                <MessageCircle className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Debunking Social Media Rumors</h3>
                <p className="text-gray-600">
                  Heard a viral claim on social media? Ask News Reporter AI to verify it with facts from trusted sources, such as checking if a reported celebrity event actually happened.
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-primary-100 rounded-lg p-2 mt-1">
                <Search className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Clarifying Breaking News</h3>
                <p className="text-gray-600">
                  Get accurate details on breaking news, like natural disasters or political events, to separate fact from speculation.
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-primary-100 rounded-lg p-2 mt-1">
                <Database className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Researching Current Events</h3>
                <p className="text-gray-600">
                  Need context for a recent event? News Reporter AI provides summaries and verified details, ideal for students or professionals researching topics like global summits or economic updates.
                </p>
              </div>
            </div>
            <div className="flex items-start space-x-3">
              <div className="bg-primary-100 rounded-lg p-2 mt-1">
                <Cpu className="h-5 w-5 text-primary-600" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 mb-1">Staying Informed on the Go</h3>
                <p className="text-gray-600">
                  Ask quick questions about trending topics or news updates, perfect for busy individuals wanting reliable information fast.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Disclaimer */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Disclaimer</h2>
          <p className="text-gray-600 leading-relaxed">
            While News Reporter AI strives to provide accurate and reliable information by sourcing data from credible news outlets, AI systems can occasionally make errors or misinterpret information. We strongly recommend cross-checking the provided information with the reference URLs included in our responses to ensure accuracy. News Reporter AI is a tool to assist with verification, but users should always verify critical information independently.
          </p>
        </div>

        {/* CTA */}
        <div className="text-center mt-8">
          <Link href="/chat" className="btn-primary inline-flex items-center text-lg px-8 py-3">
            <MessageCircle className="mr-2 h-5 w-5" />
            Try News Reporter AI Now
          </Link>
        </div>
      </main>
    </div>
  )
}
