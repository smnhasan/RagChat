# News Reporter AI Frontend

A modern, responsive chatbot interface built with Next.js, React, and TypeScript. This frontend connects to the News Reporter AI backend to provide a seamless experience for verifying news and rumors using credible sources in real-time.

## Features

- 🎨 **Modern UI/UX**: Intuitive, clean, and responsive design powered by Tailwind CSS.
- 💬 **Real-time News Verification**: Ask about rumors or recent events and get instant, verified responses.
- 🤖 **AI-Powered Responses**: Integrates with a Retrieval-Augmented Generation (RAG) backend to deliver accurate answers from trusted sources.
- 📱 **Mobile Responsive**: Optimized for seamless use across all device sizes.
- ⚡ **High Performance**: Built with Next.js for fast page loads and efficient state management.
- 🎯 **TypeScript**: Ensures type safety throughout the application.
- 🔄 **Conversation Continuity**: Maintains chat context for a natural user experience.
- 🎭 **Accessible Design**: Follows accessibility best practices for inclusivity.

## Project Structure

```
frontend/
├── public/                   # Static assets
├── src/
│   ├── app/                  # Next.js App Router pages
│   │   ├── about/            # About page with project details
│   │   ├── chat/             # Chat page for interacting with the AI
│   │   ├── globals.css       # Global styles
│   │   ├── layout.tsx        # Root layout
│   │   └── page.tsx          # Home page
│   ├── components/           # Reusable React components
│   │   ├── ChatBox.tsx       # Main chat interface
│   │   ├── MessageBubble.tsx # Individual message component
│   │   └── Loader.tsx        # Loading animation
│   └── services/             # API service layer
│       └── api.ts            # Backend API integration
├── package.json
├── tailwind.config.js        # Tailwind CSS configuration
├── tsconfig.json             # TypeScript configuration
├── next.config.js            # Next.js configuration
├── postcss.config.js         # PostCSS configuration
└── README.md
```

## Getting Started

### Prerequisites

- Node.js 18.0 or higher
- npm or yarn package manager
- A running News Reporter AI backend (see backend README for setup)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/smnhasan/RagChat.git
   cd frontend
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set Up Environment Variables**:
   ```bash
   cp .env.example .env.local
   ```

   Edit `.env.local` to configure the backend API URL:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Start the Development Server**:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Available Scripts

- `npm run dev` - Starts the development server
- `npm run build` - Builds the application for production
- `npm run start` - Starts the production server
- `npm run lint` - Runs ESLint for code quality checks

## Backend Integration

The frontend connects to the News Reporter AI backend, expected to run on `http://localhost:8000` (configurable via `NEXT_PUBLIC_API_URL`). The following endpoints are required:

### Required API Endpoints

#### POST `/api/chat`
Sends a user query to verify news or rumors.

**Request:**
```json
{
  "message": "Is the recent political scandal true?",
  "user_id": "user123",
  "session_id": "session_abc"
}
```

**Response:**
```json
{
  "response": "Verified response based on credible sources",
  "sources": ["https://trusted-news-source.com/article1", "https://another-source.com/report"],
  "confidence": 0.90,
  "session_id": "session_abc"
}
```

#### GET `/api/health`
Checks the backend's health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-21T13:40:00Z"
}
```

## Customization

### Styling

The application uses Tailwind CSS for styling. Customize the following:

- **Colors**: Update the color palette in `tailwind.config.js`.
- **Global Styles**: Modify styles in `src/app/globals.css`.
- **Responsive Design**: Adjust breakpoints and spacing for different screen sizes.

### API Configuration

The API client is defined in `src/services/api.ts`:

- **Base URL**: Set via `NEXT_PUBLIC_API_URL` environment variable.
- **Timeout**: Configured to 30 seconds (adjustable).
- **Headers**: Uses JSON content type with optional authentication headers.

### Components

#### ChatBox (`src/components/ChatBox.tsx`)
The main chat interface, featuring:
- Message history with user and bot messages
- Input form for querying news or rumors
- Loading states for streaming responses
- Error handling for failed requests

#### MessageBubble (`src/components/MessageBubble.tsx`)
Renders individual messages with:
- User vs. bot styling
- Timestamps
- Responsive design

#### Loader (`src/components/Loader.tsx`)
Displays an animated indicator during response streaming.

## Environment Variables

| Variable              | Description                     | Default                  |
|-----------------------|---------------------------------|--------------------------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL            | `http://localhost:8000`  |

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Submit a pull request with a detailed description.

## Performance Considerations

- **Code Splitting**: Leverages Next.js for automatic code splitting.
- **Lazy Loading**: Components load on-demand for faster initial rendering.
- **Bundle Optimization**: Monitor bundle size with `npm run build` and minimize heavy imports.

## Deployment

### Vercel (Recommended)

1. Connect the repository to Vercel.
2. Configure environment variables in the Vercel dashboard.
3. Deploy automatically on pushes to the main branch.

### Other Platforms

Build the application:
```bash
npm run build
```

The `out` folder contains static files ready for deployment.

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Verify the backend server is running on the specified port.
   - Check `NEXT_PUBLIC_API_URL` in `.env.local`.
   - Ensure CORS is properly configured on the backend.

2. **Build Errors**
   - Clear Next.js cache: `rm -rf .next`.
   - Reinstall dependencies: `rm -rf node_modules && npm install`.

3. **TypeScript Errors**
   - Run type checking: `npx tsc --noEmit`.
   - Validate import paths and type definitions.

