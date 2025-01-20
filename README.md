# Serverless Task Management System

A comprehensive task management system built with AWS serverless services and React. The system enables field teams to manage tasks efficiently with features like task assignment, status tracking, and automated notifications.

## System Architecture

### Backend Services (AWS)

- **Authentication**: AWS Cognito + Lambda
- **Database**: DynamoDB
- **API**: API Gateway + Lambda
- **Notifications**: SNS
- **Monitoring**: CloudWatch (for deadline checks)
- **Deployment**: AWS Amplify

### Frontend

- React-based SPA with modern UI components
- Secure authentication with incognito mode support
- Responsive design for field team usage

## Features

- **User Authentication**

  - Secure login with Cognito
  - Role-based access control (Admin/Team Member)
  - Incognito mode for sensitive environments

- **Task Management**

  - Create and assign tasks (Admin)
  - View and update task status
  - Real-time status tracking
  - Deadline monitoring

- **Notifications**
  - Email notifications for new task assignments
  - Status update alerts
  - Deadline warning notifications
  - Customizable notification settings

## Installation

### Prerequisites

- AWS Account with appropriate permissions
- Node.js ≥ 14.x
- AWS CLI configured
- SAM CLI installed

### Backend Deployment

1. Clone the repository:

```bash
git clone <repository-url>
cd task-management-system
```

2. Install SAM CLI dependencies:

```bash
sam build
```

3. Deploy the backend:

```bash
sam deploy --guided
```

During deployment, you'll need to provide:

- Stack name
- AWS Region
- Admin email address
- Notification email source
- JWT secret key

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Install required shadcn/ui components:

```bash
npx shadcn-ui@latest add card alert button input label switch badge
```

4. Configure environment variables:

```bash
cp .env.example .env
```

Edit `.env` with your deployed backend details:

```
REACT_APP_API_URL=<your-api-endpoint>
```

5. Start the development server:

```bash
npm start
```

## API Reference

### Authentication

```http
POST /auth
```

Login endpoint for user authentication.

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

### Tasks

```http
GET /tasks
```

Retrieve tasks (filtered by user role)

```http
POST /tasks
```

Create a new task (Admin only)

**Request Body:**

```json
{
  "title": "string",
  "description": "string",
  "assignee": "string",
  "deadline": "string (ISO 8601)"
}
```

```http
PUT /tasks/{task_id}
```

Update task status

**Request Body:**

```json
{
  "status": "string (PENDING|COMPLETED)"
}
```

## Environment Variables

### Backend

```
JWT_SECRET_KEY=<your-secret-key>
USER_POOL_ID=<cognito-user-pool-id>
CLIENT_ID=<cognito-client-id>
TASKS_TABLE=<dynamodb-table-name>
TASK_NOTIFICATION_TOPIC=<sns-topic-arn>
NOTIFICATION_EMAIL_FROM=<verified-ses-email>
ADMIN_EMAIL=<admin-email-address>
```

### Frontend

```
REACT_APP_API_URL=<api-gateway-endpoint>
```

## Security Considerations

- JWT tokens for API authentication
- Role-based access control
- Incognito mode for sensitive sessions
- Secure credential handling
- AWS IAM policies for service access
- API Gateway authorization
- Data encryption in transit and at rest

## Monitoring and Maintenance

### CloudWatch Metrics

- Lambda function execution metrics
- API Gateway request metrics
- DynamoDB throughput metrics

### Logs

- Lambda function logs
- API Gateway access logs
- CloudWatch Log groups

## Scaling Considerations

- DynamoDB auto-scaling
- Lambda concurrency limits
- API Gateway throttling
- SNS message filtering
- SES sending limits

## Development

### Adding New Features

1. Create feature branch
2. Implement changes
3. Test locally
4. Deploy to staging
5. Create pull request

### Testing

```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

## Troubleshooting

Common issues and solutions:

1. Authentication Failures

   - Verify Cognito user pool settings
   - Check JWT token expiration
   - Validate user credentials

2. Task Creation Issues

   - Verify admin role permissions
   - Check DynamoDB capacity
   - Validate request payload

3. Notification Problems
   - Verify SES email verification
   - Check SNS topic permissions
   - Validate email templates

## License

MIT License - see [LICENSE](./LICENSE) file for details

## Support

For support, please contact:

- Technical issues: [Create an issue](github-issue-link)
- Usage questions: [Documentation](docs-link)
