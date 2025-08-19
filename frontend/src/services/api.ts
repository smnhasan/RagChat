import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
  // Disable CORS preflight for simple requests
  withCredentials: false,
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token')
      }
    }
    return Promise.reject(error)
  }
)

export interface ChatRequest {
  query: string
}

export interface ChatResponse {
  query: string
  answer: string
}

export interface HealthResponse {
  status: string
  timestamp: string
}

// Regular chat API function (non-streaming)
export const sendMessage = async (query: string): Promise<ChatResponse> => {
  try {
    console.log('Sending message to:', `${API_BASE_URL}/api/chat`)
    console.log('Payload:', { query })
    
    const payload: ChatRequest = {
      query
    }

    const response = await apiClient.post<ChatResponse>('/chat', payload)
    console.log('Response received:', response.data)
    return response.data
  } catch (error: any) {
    console.error('Full error object:', error)
    console.error('Error response:', error.response)
    console.error('Error message:', error.message)
    console.error('Error code:', error.code)
    
    // Return a default error response
    if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
      throw new Error('Unable to connect to the server. Please check if the backend is running.')
    }
    
    if (error.response?.status === 500) {
      throw new Error('Server error occurred. Please try again later.')
    }
    
    throw new Error(error.response?.data?.message || error.message || 'Failed to send message')
  }
}

// Streaming chat API function using SSE
export const sendMessageStream = async (
  query: string, 
  onToken: (token: string) => void,
  onComplete: () => void,
  onError: (error: string) => void
): Promise<void> => {
  try {
    const url = `${API_BASE_URL}/api/chat/stream?query=${encodeURIComponent(query)}`
    
    // Create EventSource for SSE
    const eventSource = new EventSource(url)
    
    eventSource.onmessage = (event) => {
      const data = event.data
      
      // Check if streaming is complete
      if (data === '[DONE]') {
        eventSource.close()
        onComplete()
        return
      }
      
      // Send token to callback
      onToken(data)
    }
    
    eventSource.onerror = (error) => {
      console.error('EventSource error:', error)
      eventSource.close()
      onError('Streaming connection error occurred')
    }
    
  } catch (error: any) {
    console.error('Error starting stream:', error)
    onError(error.message || 'Failed to start streaming')
  }
}

// WebSocket chat function
export class WebSocketChat {
  private ws: WebSocket | null = null
  private onMessage: ((message: string) => void) | null = null
  private onError: ((error: string) => void) | null = null
  private onConnect: (() => void) | null = null
  private onDisconnect: (() => void) | null = null

  constructor() {
    this.ws = null
  }

  connect(
    onMessage: (message: string) => void,
    onError: (error: string) => void,
    onConnect?: () => void,
    onDisconnect?: () => void
  ): void {
    this.onMessage = onMessage
    this.onError = onError
    this.onConnect = onConnect
    this.onDisconnect = onDisconnect

    try {
      const wsUrl = API_BASE_URL.replace('http://', 'ws://').replace('https://', 'wss://')
      this.ws = new WebSocket(`${wsUrl}/api/ws/chat`)

      this.ws.onopen = () => {
        console.log('WebSocket connected')
        this.onConnect?.()
      }

      this.ws.onmessage = (event) => {
        this.onMessage?.(event.data)
      }

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        this.onError?.('WebSocket connection error')
      }

      this.ws.onclose = () => {
        console.log('WebSocket disconnected')
        this.onDisconnect?.()
      }
    } catch (error: any) {
      console.error('Error creating WebSocket:', error)
      this.onError?.(error.message || 'Failed to create WebSocket connection')
    }
  }

  sendMessage(message: string): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(message)
    } else {
      console.error('WebSocket is not connected')
      this.onError?.('WebSocket is not connected')
    }
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN
  }
}

// Health check function
export const checkHealth = async (): Promise<HealthResponse> => {
  try {
    const response = await apiClient.get<HealthResponse>('/health')
    return response.data
  } catch (error) {
    console.error('Health check failed:', error)
    throw error
  }
}

// Utility function to generate session ID
const generateSessionId = (): string => {
  return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now()
}

// Export the configured axios instance for custom requests
export { apiClient }
