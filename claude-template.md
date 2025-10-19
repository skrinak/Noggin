# Project Name

> **Setup Instructions:** Copy this template to your project as `.claude/claude.md`. Replace all `[bracketed-values]` with actual values. Update AWS account IDs, profile names, resource names, and API endpoints. Delete this note when done.

## Overview
Brief description of project purpose.

**Tech Stack:** React + TypeScript frontend, AWS Lambda + API Gateway backend, DynamoDB

**CRITICAL: Backend and frontend deployed to SEPARATE AWS accounts**
- Backend Account: `[backend-profile-name]` (ID: 123456789012)
- Frontend Account: `[frontend-profile-name]` (ID: 987654321098)

## Infrastructure

### CloudFormation Templates (IaC)
```
infrastructure/cloudformation/
├── backend-stack.yaml      # Lambda, API Gateway, DynamoDB
├── cognito-stack.yaml      # Auth (User Pool, Identity Pool)
├── eventbridge-stack.yaml  # Event Bus, Rules
└── frontend-stack.yaml     # S3, CloudFront, Route53
```

**ALWAYS update CloudFormation templates when making infrastructure changes.**

### Key Resources
**Backend (backend account):**
- API Gateway: [api-id] → Lambda handlers
- DynamoDB: `users` (PK: userId), `items` (PK: id, SK: timestamp)
- Cognito: User Pool [pool-id], Identity Pool [identity-pool-id]
- EventBridge: Default bus, rules → Lambda/SQS targets

**Frontend (frontend account):**
- S3: `[bucket-name]-[stage]` → static build files
- CloudFront: [distribution-id] → S3 origin, custom domain

## File Structure
```
project-root/
├── frontend/src/           # React app (components, hooks, services, types)
├── backend/src/            # Lambda (handlers, services, models, types)
├── infrastructure/cloudformation/  # All IaC templates
└── shared/                 # Shared types
```

## Commands

### Development
```bash
# Frontend
npm run dev                # Localhost:3000
npm run build              # Production build
npm test                   # Run tests

# Backend (ALWAYS use --profile)
npm run deploy:dev -- --profile [backend-profile-name]
npm run logs -- --profile [backend-profile-name]
npm run test:api           # Local API tests (no AWS)

# CloudFormation
aws cloudformation validate-template \
  --template-body file://infrastructure/cloudformation/[stack].yaml \
  --profile [backend-profile-name]
```

### Deployment

**Backend:**
```bash
# 1. Validate + deploy infrastructure (if changed)
aws cloudformation deploy \
  --template-file infrastructure/cloudformation/backend-stack.yaml \
  --stack-name backend-[dev|prod] \
  --capabilities CAPABILITY_IAM \
  --profile [backend-profile-name] \
  --region us-west-2

# 2. Deploy Lambda code
npm run deploy:[dev|prod] -- --profile [backend-profile-name]

# 3. Check logs
aws logs tail /aws/lambda/[function-name] --follow --profile [backend-profile-name]
```

**Frontend:**
```bash
# 1. Build
npm run build

# 2. Deploy to S3
aws s3 sync dist/ s3://[bucket-name] --delete --profile [frontend-profile-name]

# 3. Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id [dist-id] \
  --paths "/*" \
  --profile [frontend-profile-name]
```

## Environment Variables

**Frontend (.env):**
```
VITE_API_ENDPOINT=https://api.example.com
VITE_AWS_REGION=us-west-2
VITE_COGNITO_USER_POOL_ID=
VITE_COGNITO_CLIENT_ID=
```

**Backend (Lambda env vars):**
```
STAGE=dev|prod
DATABASE_TABLE_NAME=users
AWS_REGION=us-west-2
```

## API Endpoints
- Dev: `https://dev-api.example.com`
- Prod: `https://api.example.com`

[Document key endpoints here]

---

## Notes for Claude Code

### Infrastructure Changes Workflow

**When adding/modifying infrastructure:**
1. Read existing CloudFormation template: `infrastructure/cloudformation/[stack].yaml`
2. Update CloudFormation template with new resources
3. Validate: `aws cloudformation validate-template --template-body file://...`
4. Write application code
5. Deploy template + code

**Example - Adding Lambda:**
- Read `backend-stack.yaml` → Update with new Lambda resource → Write handler code → Deploy

### AWS Account Rules

**CRITICAL: Always specify correct AWS profile**
- Backend work: `--profile [backend-profile-name]`
- Frontend work: `--profile [frontend-profile-name]`
- Verify account: `aws sts get-caller-identity --profile [profile-name]`

❌ Never mix profiles (backend resources in frontend account or vice versa)

### Development Workflow

**Before starting:**
1. Read CloudFormation templates to understand existing infrastructure
2. Read test files to understand expected behavior
3. Grep for similar functionality to avoid duplication
4. Check if changes affect both frontend AND backend

**While coding:**
1. Run `npm run test:watch`
2. Check CloudWatch logs when Lambda fails
3. Verify correct AWS profile before AWS commands
4. Test locally before deploying

**Before committing:**
```bash
npm test                 # Must pass
npm run lint             # Must pass
npm run build            # Must succeed
```

**After infrastructure changes:**
```bash
aws cloudformation validate-template --template-body file://[template] --profile [profile]
```

### Common Issues - Quick Fix

**Lambda 500 error:**
```bash
aws logs tail /aws/lambda/[function] --follow --profile [backend-profile-name]
```

**CORS error:**
- Check API Gateway CORS config
- Verify allowed origins match frontend domain
- Check OPTIONS preflight returns 200

**Cognito auth failing:**
- Verify User Pool ID and Client ID in frontend .env
- Check token expiry (60 min default)
- Verify callback URLs match exactly

**CloudFront stale content:**
```bash
aws cloudfront create-invalidation --distribution-id [id] --paths "/*" --profile [frontend-profile-name]
```

**EventBridge not triggering:**
- Verify event pattern matches exactly
- Check target Lambda has EventBridge permissions
- Check CloudWatch Logs for target Lambda

### Key AWS Service Configs

**Cognito (backend account):**
- User Pool: MFA optional, email verification required
- Client: SRP auth, 60min tokens, OAuth code grant
- Location: `infrastructure/cloudformation/cognito-stack.yaml`

**EventBridge (backend account):**
- Use for service decoupling (not direct Lambda calls)
- Include correlation IDs in events
- Use DLQ for failed events
- Location: `infrastructure/cloudformation/eventbridge-stack.yaml`

**CloudFront (frontend account):**
- Origin: S3 bucket (React build)
- Cache: index.html (5min), /static/* (1yr)
- Error responses: 403/404 → 200 (SPA routing)
- Location: `infrastructure/cloudformation/frontend-stack.yaml`

### Critical Don'ts

❌ Create AWS resources without updating CloudFormation
❌ Deploy without running tests
❌ Mix backend/frontend AWS profiles
❌ Hardcode values (use env vars)
❌ Skip reading existing code before implementing
❌ Deploy to prod without testing in dev
❌ Forget CORS when adding API endpoints
