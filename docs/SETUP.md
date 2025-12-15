# Setup Guide

## Quick Start with Docker (Recommended)

This is the fastest way to get AI Drama World Lab running.

### Prerequisites
- Docker Engine 20.10 or later
- Docker Compose 2.0 or later
- At least 4GB of available RAM
- Modern web browser with WebGL support

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yutuknown/ai-drama-world-lab.git
cd ai-drama-world-lab
```

2. **Start the application**
```bash
./start.sh
```

Or manually:
```bash
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

4. **Stop the application**
```bash
docker-compose down
```

## Local Development Setup

For development without Docker.

### Backend Setup

#### Prerequisites
- Python 3.10 or later
- pip package manager

#### Steps

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the backend**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000

### Frontend Setup

#### Prerequisites
- Node.js 18.0 or later
- npm package manager

#### Steps

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Set environment variables**
Create a `.env.local` file:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. **Run the development server**
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Production Deployment

### Build for Production

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend
```bash
cd frontend
npm run build
npm start
```

### Docker Production Build

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### Environment Variables

#### Backend
- `PYTHONUNBUFFERED=1` - Disable Python output buffering

#### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)
- `NODE_ENV` - Environment (development/production)

## Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use, modify `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change host port
  
  frontend:
    ports:
      - "3001:3000"  # Change host port
```

### Docker Build Fails

1. Clear Docker cache:
```bash
docker-compose down -v
docker system prune -a
```

2. Rebuild:
```bash
docker-compose up --build
```

### Backend Import Errors

Ensure you're in the correct directory and virtual environment is activated:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend Build Errors

Clear cache and reinstall:
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

### WebGL Not Working

- Update your graphics drivers
- Try a different browser (Chrome/Firefox recommended)
- Check browser WebGL support: https://get.webgl.org/

## System Requirements

### Minimum
- CPU: 2 cores
- RAM: 4GB
- Storage: 2GB free space
- OS: Linux, macOS, or Windows 10+

### Recommended
- CPU: 4+ cores
- RAM: 8GB+
- GPU: Any with WebGL 2.0 support
- Storage: 5GB free space (for episodes)

## Performance Tips

1. **Reduce simulation FPS** if experiencing lag
2. **Limit number of agents** (start with 1-2)
3. **Use smaller scenes** for better performance
4. **Close other browser tabs** to free up resources

## Next Steps

After setup, see:
- [README.md](README.md) - Full documentation
- [docs/API.md](docs/API.md) - API reference
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
