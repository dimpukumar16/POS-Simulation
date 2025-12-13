# POS Simulator - Docker Deployment Guide

## Quick Start with Docker

### Prerequisites
- Docker Desktop or Docker Engine (v20.10+)
- Docker Compose (v2.0+)

### Running the Application

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pos_simulator
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - PostgreSQL database on port 5432
   - Backend API on port 5000
   - Frontend on port 5173

3. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000/api
   - API Health: http://localhost:5000/api/health

4. **Default credentials**
   - **Admin**: username: `admin`, password: `admin123`, PIN: `1111`
   - **Manager**: username: `manager`, password: `manager123`, PIN: `2222`
   - **Cashier**: username: `cashier`, password: `cashier123`, PIN: `3333`

### Managing Services

**View logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Stop services**
```bash
docker-compose down
```

**Stop and remove volumes (data will be lost)**
```bash
docker-compose down -v
```

**Rebuild after code changes**
```bash
docker-compose up -d --build
```

**Restart a specific service**
```bash
docker-compose restart backend
```

### Database Access

**Connect to PostgreSQL**
```bash
docker exec -it pos_db psql -U postgres -d pos_db
```

**Run database migrations** (if needed)
```bash
docker exec -it pos_backend python init_db.py
```

### Troubleshooting

**Backend not connecting to database**
```bash
# Check if database is healthy
docker-compose ps

# Restart database
docker-compose restart db

# Check backend logs
docker-compose logs backend
```

**Port already in use**
```bash
# Change ports in docker-compose.yml
# For example, change frontend port:
ports:
  - "3000:5173"  # Access on localhost:3000 instead
```

**Reset everything**
```bash
docker-compose down -v
docker-compose up -d --build
```

### Production Deployment

For production, update `docker-compose.yml`:

1. **Set strong secrets**
   ```yaml
   environment:
     - SECRET_KEY=<generate-strong-random-key>
     - JWT_SECRET_KEY=<generate-strong-random-jwt-key>
   ```

2. **Use production database**
   ```yaml
   environment:
     - DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```

3. **Build optimized frontend**
   ```dockerfile
   # In frontend/Dockerfile
   FROM node:20-alpine as build
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci
   COPY . .
   RUN npm run build

   FROM nginx:alpine
   COPY --from=build /app/dist /usr/share/nginx/html
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

4. **Use environment-specific compose files**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<strong-password>
POSTGRES_DB=pos_db

# Backend
SECRET_KEY=<your-secret-key>
JWT_SECRET_KEY=<your-jwt-secret>
FLASK_ENV=production

# Frontend
VITE_API_BASE_URL=http://localhost:5000/api
```

### Backup and Restore

**Backup database**
```bash
docker exec pos_db pg_dump -U postgres pos_db > backup.sql
```

**Restore database**
```bash
docker exec -i pos_db psql -U postgres pos_db < backup.sql
```

### Performance Tuning

**Increase database resources**
```yaml
services:
  db:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

**Enable PostgreSQL connection pooling**
```yaml
services:
  db:
    command: postgres -c max_connections=100 -c shared_buffers=256MB
```

## CI/CD Integration

GitHub Actions workflow is configured in `.github/workflows/ci.yml`:
- Runs tests on every push/PR
- Builds Docker images
- Runs security scans
- Deploys on merge to main (configure deployment steps)

### Manual CI Steps

**Run tests locally**
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

**Build images locally**
```bash
docker build -t pos-backend:latest ./backend
docker build -t pos-frontend:latest ./frontend
```

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Verify service health: `docker-compose ps`
3. Review PROJECT_SPEC.md for architecture details
4. Check API_DOCUMENTATION.md for API references
