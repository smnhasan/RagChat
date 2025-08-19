# RAG Chatbot Frontend

A modern, responsive chatbot interface built with Next.js, React, and TypeScript. This frontend connects to a RAG (Retrieval-Augmented Generation) backend to provide intelligent, context-aware conversations.

## Features

- 🎨 **Modern UI/UX**: Clean, responsive design with Tailwind CSS
- 💬 **Real-time Chat**: Instant messaging with typing indicators
- 🤖 **RAG Integration**: Connects to backend RAG system for intelligent responses
- 📱 **Mobile Responsive**: Works seamlessly on all device sizes
- ⚡ **Fast Performance**: Optimized with Next.js and efficient state management
- 🎯 **TypeScript**: Full type safety throughout the application
- 🔄 **Session Management**: Maintains conversation context
- 🎭 **Accessible**: Built with accessibility best practices

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **State Management**: React Hooks (useState, useEffect)

## Project Structure

```
frontend/
├── public/                   # Static assets
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── about/          # About page
│   │   ├── chat/           # Chat page
│   │   ├── globals.css     # Global styles
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Home page
│   ├── components/          # Reusable React components
│   │   ├── ChatBox.tsx     # Main chat interface
│   │   ├── MessageBubble.tsx # Individual message component
│   │   └── Loader.tsx      # Loading animation
│   └── services/           # API service layer
│       └── api.ts          # Backend API integration
├── package.json
├── tailwind.config.js      # Tailwind CSS configuration
├── tsconfig.json          # TypeScript configuration
├── next.config.js         # Next.js configuration
├── postcss.config.js      # PostCSS configuration
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18.0 or higher
- npm or yarn package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rag-chatbot/frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
```

Edit `.env.local` and configure your backend API URL:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. Start the development server:
```bash
npm run dev
# or
yarn dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Backend Integration

The frontend expects a RAG backend server running on `http://localhost:8000` (configurable via environment variables) with the following endpoints:

### Required API Endpoints

#### POST `/api/chat`
Send a message to the chatbot.

**Request:**
```json
{
  "message": "Your question here",
  "user_id": "user123",
  "session_id": "session_abc"
}
```

**Response:**
```json
{
  "response": "Bot response here",
  "sources": ["source1.pdf", "source2.txt"],
  "confidence": 0.85,
  "session_id": "session_abc"
}
```

#### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-19T10:30:00Z"
}
```

## Customization

### Styling

The application uses Tailwind CSS for styling. Key customization points:

- **Colors**: Modify the color palette in `tailwind.config.js`
- **Components**: Custom component styles in `src/app/globals.css`
- **Layout**: Responsive breakpoints and spacing

### API Configuration

The API client is configured in `src/services/api.ts`:

- **Base URL**: Set via `NEXT_PUBLIC_API_URL` environment variable
- **Timeout**: Default 30 seconds (configurable)
- **Headers**: JSON content type with optional authentication

### Components

#### ChatBox (`src/components/ChatBox.tsx`)
Main chat interface with:
- Message history
- Input form
- Loading states
- Error handling

#### MessageBubble (`src/components/MessageBubble.tsx`)
Individual message component with:
- User/bot differentiation
- Timestamp display
- Responsive layout

#### Loader (`src/components/Loader.tsx`)
Animated typing indicator for bot responses.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a pull request

## Performance Considerations

- **Code Splitting**: Next.js automatically splits code for optimal loading
- **Image Optimization**: Use Next.js Image component for images
- **Lazy Loading**: Components load only when needed
- **Bundle Size**: Monitor with `npm run build` and optimize imports

## Deployment

### Vercel (Recommended)

1. Connect your repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Other Platforms

Build the application:
```bash
npm run build
```

The `out` folder contains the static files ready for deployment.

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure backend server is running on the correct port
   - Check `NEXT_PUBLIC_API_URL` environment variable
   - Verify CORS settings on backend

2. **Build Errors**
   - Clear Next.js cache: `rm -rf .next`
   - Clear node_modules: `rm -rf node_modules && npm install`

3. **TypeScript Errors**
   - Run type checking: `npx tsc --noEmit`
   - Check import paths and type definitions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check existing documentation
- Review the troubleshooting section