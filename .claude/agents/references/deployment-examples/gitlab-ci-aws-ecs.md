# GitLab CI + AWS ECS Deployment

Full example of a CI/CD pipeline for AWS ECS deployment.

## GitLab CI Configuration

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - security
  - deploy

variables:
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  AWS_REGION: us-east-1

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE

test:unit:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm run test:unit
  coverage: '/Statements\s+:\s+(\d+\.\d+)%/'

test:integration:
  stage: test
  image: node:20
  services:
    - postgres:15
  variables:
    POSTGRES_DB: test_db
    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/test_db
  script:
    - npm ci
    - npm run test:integration

security:sast:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config auto --json -o gl-sast-report.json
  artifacts:
    reports:
      sast: gl-sast-report.json

security:secrets:
  stage: security
  image: zricethezav/gitleaks:latest
  script:
    - gitleaks detect --source . --verbose --redact

deploy:staging:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/cloud-deploy/aws-base:latest
  script:
    - aws ecs update-service --cluster staging-cluster --service app-service --force-new-deployment
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy:production:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/cloud-deploy/aws-base:latest
  script:
    - aws ecs update-service --cluster production-cluster --service app-service --force-new-deployment
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual
```

## Dockerfile (Multi-stage)

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./

USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

## AWS ECS Task Definition

```json
{
  "family": "app-service",
  "taskRoleArn": "arn:aws:iam::123456789:role/ecsTaskRole",
  "executionRoleArn": "arn:aws:iam::123456789:role/ecsTaskExecutionRole",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "name": "app",
      "image": "${DOCKER_IMAGE}",
      "cpu": 256,
      "memory": 512,
      "essential": true,
      "portMappings": [
        { "containerPort": 3000, "protocol": "tcp" }
      ],
      "environment": [
        { "name": "NODE_ENV", "value": "production" }
      ],
      "secrets": [
        { "name": "DATABASE_URL", "valueFrom": "arn:aws:ssm:us-east-1:123456789:parameter/db-url" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/app-service",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512"
}
```
