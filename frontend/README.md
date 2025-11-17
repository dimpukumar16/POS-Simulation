# POS Simulator Frontend

React-based frontend for the POS Simulator application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure the API endpoint:
   - Edit `src/api/config.js` to set the backend URL (default: http://localhost:5000)

3. Start the development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Features

- Login page with username/password or PIN
- Product scanning and search
- Shopping cart management
- Checkout with multiple payment methods
- Receipt viewing
- Sales and inventory reports
- Admin dashboard
- Manager override dialogs

## Project Structure

```
src/
├── components/        # Reusable UI components
├── pages/            # Page components
├── api/              # API client functions
├── stores/           # Zustand state management
├── utils/            # Utility functions
└── App.jsx           # Main application component
```

## Quick Start

The frontend connects to the backend API at `http://localhost:5000` by default.

### Default Login Credentials

- **Cashier**: username: `cashier`, password: `cashier123`, PIN: `3333`
- **Manager**: username: `manager`, password: `manager123`, PIN: `2222`
- **Admin**: username: `admin`, password: `admin123`, PIN: `1111`

## Technologies

- React 18
- Vite (build tool)
- TailwindCSS (styling)
- Axios (HTTP client)
- Zustand (state management)
- React Router (routing)
