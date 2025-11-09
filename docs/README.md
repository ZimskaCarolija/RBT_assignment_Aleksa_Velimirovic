# API Documentation

## OpenAPI/Swagger Specification

This folder contains the complete OpenAPI 3.0 specification for the Vacation Management System API.

### Files

- **`openapi.yaml`** - Complete OpenAPI 3.0 specification document

### Viewing the Documentation

There are several ways to view and interact with the OpenAPI documentation:

#### 1. Swagger UI (Recommended)

You can use Swagger UI to view and test the API interactively:

**Option A: Online Swagger Editor**
1. Go to [https://editor.swagger.io/](https://editor.swagger.io/)
2. Click "File" → "Import file"
3. Select `openapi.yaml` from this folder
4. The documentation will be rendered with an interactive interface

**Option B: Local Swagger UI (using Docker)**
```bash
docker run -p 8080:8080 -e SWAGGER_JSON=/openapi.yaml -v $(pwd)/docs:/openapi swaggerapi/swagger-ui
```
Then open [http://localhost:8080](http://localhost:8080)

**Option C: Using Swagger UI via npm**
```bash
npx swagger-ui-serve docs/openapi.yaml
```

#### 2. Redoc

Redoc provides a beautiful, responsive documentation interface:

**Option A: Online Redoc**
1. Go to [https://redocly.github.io/redoc/](https://redocly.github.io/redoc/)
2. Paste the contents of `openapi.yaml` or upload the file

**Option B: Local Redoc (using Docker)**
```bash
docker run -p 8080:80 -v $(pwd)/docs:/usr/share/nginx/html/api -e SPEC_URL=api/openapi.yaml redocly/redoc
```

#### 3. Postman

You can import the OpenAPI specification into Postman:

1. Open Postman
2. Click "Import"
3. Select "File" tab
4. Choose `openapi.yaml`
5. Postman will generate a collection with all endpoints

#### 4. VS Code Extension

If you use VS Code, install the "OpenAPI (Swagger) Editor" extension:
- Extension ID: `42Crunch.vscode-openapi`
- Open `openapi.yaml` in VS Code
- Use the preview feature to view the documentation

### API Overview

The Vacation Management System API provides the following main features:

#### 1. User Management (`/users`)
- Create, read, update, and delete users
- List users with pagination and filtering
- Role-based access control

#### 2. Vacation Management (`/vacation`)
- Create and manage vacation records
- Check for overlapping vacation periods
- View vacation summaries (entitled, used, available days)
- Manage vacation entitlements per year
- List vacation records with date range filtering

#### 3. Import Operations (`/import`)
- Bulk import users from CSV
- Bulk import vacation records from CSV
- Bulk import vacation entitlements from CSV

#### 4. Health Check (`/health`)
- Simple health check endpoint (no authentication required)

### Authentication

All endpoints (except `/health`) require Basic Authentication:

1. Format: `Authorization: Basic base64(email:password)`
2. Example:
   - Email: `user@example.com`
   - Password: `password123`
   - Encoded: `dXNlckBleGFtcGxlLmNvbTpwYXNzd29yZDEyMw==`
   - Header: `Authorization: Basic dXNlckBleGFtcGxlLmNvbTpwYXNzd29yZDEyMw==`

### Authorization Levels

- **Public**: No authentication required (`/health`)
- **Authenticated**: Requires valid user credentials
- **Admin**: Requires admin role (import endpoints)
- **Admin or Owner**: Requires admin role OR the user must be accessing their own data (most user and vacation endpoints)

### Response Format

All API responses follow a consistent format:

**Success Response:**
```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "status_code": 200
}
```

**Error Response:**
```json
{
  "success": false,
  "data": null,
  "error": "Error message here",
  "status_code": 400
}
```

### Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

### Examples

#### Creating a User

```bash
curl -X POST http://localhost:5000/users \
  -H "Authorization: Basic dXNlckBleGFtcGxlLmNvbTpwYXNzd29yZDEyMw==" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "password123",
    "full_name": "John Doe"
  }'
```

#### Creating a Vacation Record

```bash
curl -X POST http://localhost:5000/vacation/users/1/create \
  -H "Authorization: Basic dXNlckBleGFtcGxlLmNvbTpwYXNzd29yZDEyMw==" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-07-01",
    "end_date": "2025-07-05",
    "note": "Summer vacation"
  }'
```

#### Getting Vacation Summary

```bash
curl -X GET "http://localhost:5000/vacation/users/1/summary?year=2025" \
  -H "Authorization: Basic dXNlckBleGFtcGxlLmNvbTpwYXNzd29yZDEyMw=="
```

### CSV Import Format

#### Users Import
```csv
email,password,full_name
user1@example.com,password123,User One
user2@example.com,password456,User Two
```

#### Vacation Records Import
```csv
user_id,start_date,end_date,note
1,2025-07-01,2025-07-05,Summer vacation
1,2025-12-20,2025-12-31,Winter vacation
```

#### Entitlements Import
```csv
user_id,year,total_days
1,2025,25
2,2025,30
```

### Validation Rules

#### User Creation/Update
- Email must be valid and unique
- Password must be at least 6 characters
- Full name is optional (max 255 characters)

#### Vacation Records
- End date must be after or equal to start date
- Period must not overlap with existing records
- User must have sufficient available vacation days
- Note is optional (max 500 characters)

#### Entitlements
- Year must be between 1900 and 2100
- Each user can have only one entitlement per year
- Total days must be a positive integer

### Pagination

List endpoints support pagination with the following query parameters:
- `page`: Page number (default: 1, minimum: 1)
- `per_page`: Items per page (default: 20, minimum: 1, maximum: 100)

### Date Formats

All dates should be in ISO 8601 format: `YYYY-MM-DD`
- Example: `2025-07-01`

All timestamps are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- Example: `2025-01-01T10:00:00Z`

### Support

For questions or issues, please contact:
- Email: velimirovicaleksa001@gmail.com

### License

MIT License - see the main project README for details.

