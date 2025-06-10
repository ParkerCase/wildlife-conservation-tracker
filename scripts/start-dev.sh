#!/bin/bash
echo "🚀 Starting WildGuard AI in development mode..."

# Start backend
cd backend
python src/api/app.py &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ Platform started!"
echo "📊 Dashboard: http://localhost:3000"
echo "🔗 API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
