'use client'

import React from 'react'

export default function Loader() {
  return (
    <div className="typing-indicator">
      <span className="text-sm text-gray-600 mr-2">AI is thinking</span>
      <div className="typing-dot"></div>
      <div className="typing-dot"></div>
      <div className="typing-dot"></div>
    </div>
  )
}
