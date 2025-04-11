#!/bin/bash

# Set environment variables
export DATABASE_URL="postgresql://user:pass@ep-fragrant-block-a7lnk03h-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
export RAPIDAPI_KEY="placeholder"

echo "Starting PriceByte locally..."
echo "DATABASE_URL set to: $DATABASE_URL"
echo "RAPIDAPI_KEY set"

# Start backend in background
echo "Starting backend..."
cd backend
./gradlew bootRun &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 10

# Start frontend
echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Services started. Backend PID: $BACKEND_PID, Frontend PID: $FRONTEND_PID"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8080"
echo "Press Ctrl+C to stop"

# Wait for interrupt
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait