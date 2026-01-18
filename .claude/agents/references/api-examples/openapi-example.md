# OpenAPI 3.1 Example: Blog API

Full example of a RESTful API specification using OpenAPI 3.1.

```yaml
openapi: 3.1.0
info:
  title: Blog API
  version: 1.0.0
  description: RESTful API for blog management
  contact:
    name: API Support
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

security:
  - bearerAuth: []

paths:
  /posts:
    get:
      summary: List all posts
      description: Retrieve a paginated list of blog posts
      tags: [Posts]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: published
          in: query
          schema:
            type: boolean
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostListResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimitExceeded'

    post:
      summary: Create a new post
      description: Create a new blog post
      tags: [Posts]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreatePostRequest'
            examples:
              basic:
                value:
                  title: "Getting Started with OpenAPI"
                  content: "OpenAPI is a specification for designing APIs..."
                  published: false
      responses:
        '201':
          description: Post created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Post'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          $ref: '#/components/responses/ValidationError'

  /posts/{postId}:
    parameters:
      - name: postId
        in: path
        required: true
        schema:
          type: string
          format: uuid

    get:
      summary: Get a post by ID
      tags: [Posts]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Post'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      summary: Update a post
      tags: [Posts]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdatePostRequest'
      responses:
        '200':
          description: Post updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Post'
        '404':
          $ref: '#/components/responses/NotFound'

    delete:
      summary: Delete a post
      tags: [Posts]
      responses:
        '204':
          description: Post deleted successfully
        '404':
          $ref: '#/components/responses/NotFound'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Post:
      type: object
      required: [id, title, content, authorId, createdAt, updatedAt]
      properties:
        id:
          type: string
          format: uuid
        title:
          type: string
          minLength: 1
          maxLength: 255
        content:
          type: string
        published:
          type: boolean
          default: false
        authorId:
          type: string
          format: uuid
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    CreatePostRequest:
      type: object
      required: [title, content]
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 255
        content:
          type: string
          minLength: 1
        published:
          type: boolean
          default: false

    UpdatePostRequest:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 255
        content:
          type: string
          minLength: 1
        published:
          type: boolean

    PostListResponse:
      type: object
      required: [data, pagination]
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Post'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      required: [page, limit, total, totalPages]
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer

    Error:
      type: object
      required: [error]
      properties:
        error:
          type: object
          required: [code, message]
          properties:
            code:
              type: string
            message:
              type: string
            details:
              type: array
              items:
                type: object

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    ValidationError:
      description: Validation error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error:
              code: "VALIDATION_ERROR"
              message: "Request validation failed"
              details:
                - field: "title"
                  message: "Title is required"

    RateLimitExceeded:
      description: Rate limit exceeded
      headers:
        X-RateLimit-Limit:
          schema:
            type: integer
        X-RateLimit-Remaining:
          schema:
            type: integer
        X-RateLimit-Reset:
          schema:
            type: integer
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```
