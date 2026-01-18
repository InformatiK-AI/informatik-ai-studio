<!-- mixin-version: 1.0.0 -->
<!-- mixin-id: common-commands -->
<!-- last-updated: 2026-01-17 -->

## Common Commands

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/{{ANALYZER_SCRIPT}} .
python scripts/{{TOOL_SCRIPT}} --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```
