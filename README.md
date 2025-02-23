# Create-Math
This project enables users to upload a Python-based animation script through a web interface, which then gets processed by a backend to generate a video. The generated video is then displayed back to the user in the frontend.

# Technologies

**Frontend**:
- React 18
- Monaco Editor
- Axios
- Vite

**Backend**:
- FastAPI
- Manim Community Edition
- Uvicorn
- Python 3.9

**Infrastructure**:
- Docker
- Docker Compose
- FFmpeg
- TeX Live

## Prerequisites

- Docker 20.10+
- Node.js 18+
- Python 3.9+
- Manim CE 0.17+
- FFmpeg 4.3+
- TeX Live 2022+

## Installation

### Local Development

1. **Clone Repository**
```bash
git clone https://github.com/SB3084/CREATE-MATH.git
cd create-math
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd ../frontend
npm install
```

4. **Start Services**
```bash
# Backend (in separate terminal)
cd backend && uvicorn main:app --reload

# Frontend (in separate terminal)
cd frontend && npm run dev
```

### Docker Deployment
```bash
docker-compose up --build

# Access services:
# - Frontend: http://localhost:5173
# - Backend: http://localhost:8000
```

## Project Structure

```
create-math/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── static/
│   ├── media/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Editor.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
└── docker-compose.yml
```

## Configuration

### Environment Variables

**Backend (.env)**
```ini
MANIM_QUALITY=low
MAX_RENDER_TIME=60
CLEANUP_INTERVAL=3600
```

**Frontend (.env.local)**
```ini
VITE_API_BASE=http://localhost:8000
```

## Usage

1. Access the web interface at `http://localhost:5173`
2. Write your Manim script in the editor
3. Click "Render" to start animation processing
4. View real-time status updates
5. Watch rendered animation in the preview pane

## Deployment

### Production Setup

1. **Build Containers**
```bash
docker-compose -f docker-compose.prod.yml build
```

2. **Start Services**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. **Configure Reverse Proxy (Nginx Example)**
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://frontend:5173;
    }

    location /api {
        proxy_pass http://backend:8000;
    }
}
```

## Security Considerations

- 🔒 Use HTTPS in production
- 🔑 Implement JWT authentication
- ⏱️ Add rate limiting (recommend 5 requests/minute)
- 🗑️ Regular file cleanup schedule
- 🛡️ Container isolation for rendering processes
- 📝 Input validation for scripts

**View Logs**
# Backend logs
docker logs create-math-backend-1

# Frontend logs
docker logs create-math-frontend-1
```
## Contributing ##

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License ##

MIT License - link for details - https://github.com/SB3084/Create-Math/blob/main/LICENSE

## Acknowledgments ##

- Manim Community for the animation engine
- FastAPI for the efficient backend framework
- React team for the frontend library
- Monaco Editor for the code editing component

---

## Project Maintainers ##  
[Ujjainy De]  
[Shrawani Bute] 
```

This README provides comprehensive documentation covering all aspects of the project from development to production deployment. Adjust placeholders (URLs, emails, etc.) with your actual project information. You might want to add actual architecture diagrams and screenshots for better visual documentation.
