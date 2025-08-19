'use client'

import React from 'react'
import { User, Bot } from 'lucide-react'
import clsx from 'clsx'

interface MessageBubbleProps {
  message: string
  isBot: boolean
  timestamp: Date
}

export default function MessageBubble({ message, isBot, timestamp }: MessageBubbleProps) {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className={clsx(
      'flex items-start space-x-3 max-w-4xl',
      isBot ? 'justify-start' : 'justify-end flex-row-reverse space-x-reverse'
    )}>
      {/* Avatar */}
      <div className={clsx(
        'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
        isBot 
          ? 'bg-primary-100 text-primary-600' 
          : 'bg-gray-700 text-white'
      )}>
        {isBot ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
      </div>

      {/* Message Content */}
      <div className={clsx(
        'flex flex-col',
        isBot ? 'items-start' : 'items-end'
      )}>
        <div className={clsx(
          'message-bubble',
          isBot ? 'bot-message' : 'user-message'
        )}>
          <p className="text-sm leading-relaxed whitespace-pre-wrap">
            {message}
          </p>
        </div>
        
        {/* Timestamp */}
        <span className="text-xs text-gray-400 mt-1 px-2">
          {formatTime(timestamp)}
        </span>
      </div>
    </div>
  )
}
