# Todo App - Frontend

A modern React frontend for managing todo items integrated with the FastAPI backend.

## Location
`/workspaces/LangChain-Tuts/project/module-2/sandbox/todo_list/frontend`

## Features
- **List Tasks**: View all tasks with status indicators, timestamps, and filter by completion status (All, Active, Completed).
- **Create Tasks**: Add new tasks with title (required) and description (optional).
- **Edit Tasks**: Update existing tasks (title, description, completed status) via an edit modal.
- **Toggle Completion**: Toggle task completion status with a single click.
- **Delete Tasks**: Remove tasks with confirmation modal.
- **Backend Health Check**: Real-time connection status indicator for the FastAPI backend (`http://localhost:8000`).
- **User Feedback & Errors**: Toast notifications for operations and detailed error banners for failed network/validation operations.

## Tech Stack
- **Framework**: React 18
- **Build Tool**: Vite
- **Icons**: Lucide React
- **Styling**: CSS with modern custom variables, responsive flex/grid layouts

## How to Run

### Prerequisites
1. Ensure Node.js (v18+) and npm are installed.
2. Ensure the FastAPI backend is running at `http://localhost:8000`.

### Instructions
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser at the provided URL (e.g. `http://localhost:3000`).

### Build for Production
To build the application for production:
```bash
npm run build
```
To preview the production build locally:
```bash
npm run preview
```
