# FinSentrix Frontend

The frontend application for FinSentrix, built with React, TypeScript, and modern web technologies.

## Technology Stack

- React 18
- TypeScript
- Material-UI (MUI)
- React Query for API data fetching
- React Router for navigation
- Chart.js for data visualization
- i18next for internationalization

## Project Structure

```
frontend/
├── src/
│   ├── api/           # API integration and services
│   ├── components/    # Reusable UI components
│   ├── contexts/      # React contexts for state management
│   ├── hooks/         # Custom React hooks
│   ├── layouts/       # Page layouts and templates
│   ├── locales/       # Internationalization files
│   ├── pages/         # Page components
│   ├── styles/        # Global styles and theme
│   ├── types/         # TypeScript type definitions
│   └── utils/         # Utility functions
├── public/            # Static assets
└── tests/            # Test files
```

## Setup Instructions

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm start
   ```

3. Build for production:
   ```bash
   npm run build
   ```

4. Run tests:
   ```bash
   npm test
   ```

## Development Guidelines

- Follow the established project structure
- Use TypeScript for all new code
- Write unit tests for components and utilities
- Follow the Material-UI theming system
- Support both English and Persian languages
- Ensure responsive design for all screen sizes

## Features

- Real-time sentiment analysis dashboard
- Historical sentiment trends visualization
- Market analysis tools
- Multi-language support (English/Persian)
- Dark/Light theme support
- Responsive design
- Interactive charts and graphs
- User authentication and authorization
- API integration with backend services

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_VERSION=$npm_package_version
```

## Available Scripts

- `npm start` - Start development server
- `npm test` - Run tests
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier 