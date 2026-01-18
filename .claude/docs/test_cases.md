# Test Plan: InformatiK-AI Studio

## Overview

Comprehensive test strategy for InformatiK-AI Studio, a web application for AI-powered code generation similar to Bolt.new/Lovable. This platform uses Next.js 15, Supabase, and integrates multiple AI models (Claude, GPT) for intelligent code generation with real-time preview and deployment capabilities.

## Test Strategy

- **Unit Tests:** Vitest for business logic, utilities, and pure functions (80%+ coverage target)
- **Component Tests:** Vitest + Testing Library for React components and UI interactions
- **Integration Tests:** Vitest for API routes, database operations, and AI provider integration
- **E2E Tests:** Playwright for complete user flows and critical paths
- **Security Tests:** Focused scenarios for authentication, API key handling, and code execution

## Testing Framework Configuration

| Test Type | Framework | Location | Priority |
|-----------|-----------|----------|----------|
| Unit | Vitest | `*.test.ts`, `__tests__/` | P0 |
| Component | Vitest + Testing Library | `*.test.tsx` | P0 |
| Integration | Vitest | `tests/integration/` | P0 |
| E2E | Playwright | `tests/e2e/` | P1 |

---

## Epic 1: Foundation Setup

### Feature: Next.js 15 Application Bootstrap

#### Happy Paths

```gherkin
Scenario: Application starts successfully in development mode
  Given the project dependencies are installed
  And environment variables are configured
  When I run "pnpm dev"
  Then the development server should start on port 3000
  And the application should be accessible at "http://localhost:3000"
  And no console errors should be present
  And hot module replacement should be active

Scenario: Production build completes successfully
  Given all source files are valid TypeScript
  And all environment variables are set
  When I run "pnpm build"
  Then the build should complete without errors
  And the `.next` directory should contain optimized bundles
  And Server Components should be properly separated from Client Components
  And the build should generate static assets for CSS/JS

Scenario: Tailwind CSS and shadcn/ui components render correctly
  Given the application is running
  When I navigate to any page
  Then Tailwind CSS styles should be applied
  And shadcn/ui components should render with proper styling
  And no CSS conflicts should be present
  And dark mode toggle should work correctly
```

#### Validation & Edge Cases

```gherkin
Scenario: Application handles missing environment variables
  Given the `.env.local` file is missing required variables
  When I attempt to start the application
  Then the application should fail with a clear error message
  And the error should list missing environment variables
  And the application should not start partially

Scenario: TypeScript compilation catches type errors
  Given there is a type mismatch in the code
  When I run "pnpm build"
  Then the build should fail with TypeScript errors
  And the error message should indicate the file and line number
  And no JavaScript output should be generated

Scenario: Application handles invalid Tailwind configuration
  Given the `tailwind.config.ts` has syntax errors
  When I run the development server
  Then the build should fail gracefully
  And an error message should indicate the Tailwind issue
```

#### Security

```gherkin
Scenario: Environment variables are not exposed to client
  Given I have server-only secrets in `.env.local`
  When I inspect the client bundle
  Then `SUPABASE_SERVICE_ROLE_KEY` should NOT be present
  And `ANTHROPIC_API_KEY` should NOT be present
  And `OPENAI_API_KEY` should NOT be present
  And only `NEXT_PUBLIC_*` variables should be accessible

Scenario: Content Security Policy is configured
  Given the application is running
  When I inspect HTTP response headers
  Then CSP headers should be present
  And inline scripts should be restricted
  And external script sources should be whitelisted
```

---

## Epic 2: Authentication System

### Feature: User Registration and Login

#### Happy Paths

```gherkin
Scenario: User registers with email and password
  Given I am on the registration page
  When I enter "user@example.com" in the email field
  And I enter "SecureP@ss123!" in the password field
  And I enter "SecureP@ss123!" in the confirm password field
  And I click the "Sign Up" button
  Then I should see a success message
  And a verification email should be sent to "user@example.com"
  And I should be redirected to "/verify-email"

Scenario: User logs in with valid credentials
  Given I have a verified account with email "user@example.com"
  And I am on the login page
  When I enter "user@example.com" in the email field
  And I enter "SecureP@ss123!" in the password field
  And I click the "Sign In" button
  Then I should see a loading indicator
  And I should be redirected to "/dashboard"
  And the navigation should show my user profile
  And a session cookie should be set

Scenario: User logs in with OAuth (GitHub)
  Given I am on the login page
  When I click "Continue with GitHub"
  Then I should be redirected to GitHub OAuth page
  When I authorize the application
  Then I should be redirected back to the application
  And I should be logged in
  And my GitHub profile picture should be displayed
  And a session should be created in Supabase
```

#### Validation & Error Handling

```gherkin
Scenario: Registration with invalid email format
  Given I am on the registration page
  When I enter "invalid-email" in the email field
  And I enter "password123" in the password field
  And I click "Sign Up"
  Then I should see error "Please enter a valid email address"
  And the email field should have aria-invalid="true"
  And focus should remain on the email field

Scenario: Registration with weak password
  Given I am on the registration page
  When I enter "user@example.com" in the email field
  And I enter "weak" in the password field
  And I click "Sign Up"
  Then I should see error "Password must be at least 8 characters with uppercase, lowercase, number, and special character"
  And the password field should have aria-invalid="true"

Scenario: Registration with mismatched passwords
  Given I am on the registration page
  When I enter "user@example.com" in the email field
  And I enter "SecureP@ss123!" in the password field
  And I enter "DifferentPass456!" in the confirm password field
  And I click "Sign Up"
  Then I should see error "Passwords do not match"

Scenario: Login with unverified email
  Given I have registered but not verified my email
  When I attempt to log in
  Then I should see error "Please verify your email before logging in"
  And a "Resend verification email" link should be displayed

Scenario: Login with incorrect credentials
  Given I am on the login page
  When I enter "user@example.com" in the email field
  And I enter "WrongPassword" in the password field
  And I click "Sign In"
  Then I should see error "Invalid email or password"
  And the password field should be cleared
  And no session should be created

Scenario: Supabase authentication service is down
  Given the Supabase API returns a 500 error
  When I attempt to log in
  Then I should see error "Authentication service unavailable. Please try again later."
  And the form should remain enabled for retry
```

#### Edge Cases

```gherkin
Scenario: Email with leading/trailing whitespace
  Given I am on the registration page
  When I enter "  user@example.com  " in the email field
  And I complete the registration form
  And I click "Sign Up"
  Then the email should be trimmed before submission
  And registration should succeed with "user@example.com"

Scenario: User attempts multiple registrations with same email
  Given an account exists with email "user@example.com"
  When I attempt to register again with "user@example.com"
  Then I should see error "An account with this email already exists"
  And I should see a link to "Sign In instead"

Scenario: Session expires during active use
  Given I am logged in
  And my session has expired
  When I attempt to access a protected resource
  Then I should be redirected to "/login"
  And I should see message "Your session has expired. Please log in again."
  And my intended destination should be preserved for redirect after login
```

#### Security

```gherkin
Scenario: Password is hashed before storage
  Given I register a new account
  When I inspect the database
  Then the password field should NOT contain the plaintext password
  And the password should be hashed using bcrypt or similar
  And the hash should include a salt

Scenario: Session tokens are HTTPOnly and Secure
  Given I am logged in
  When I inspect browser cookies
  Then the session cookie should have HttpOnly flag
  And the session cookie should have Secure flag
  And the session cookie should have SameSite=Lax or Strict

Scenario: Brute force protection is active
  Given I am on the login page
  When I attempt to login with wrong password 5 times
  Then I should be rate limited
  And I should see error "Too many login attempts. Please try again in 15 minutes."
  And subsequent login attempts should be blocked

Scenario: OAuth state parameter prevents CSRF
  Given I initiate GitHub OAuth flow
  When I inspect the redirect URL
  Then it should contain a state parameter
  And the state should be a random, unpredictable value
  When I return from OAuth
  Then the state should be validated before creating session

Scenario: No sensitive data in URL parameters
  Given I am using the authentication system
  When I navigate through login/registration flows
  Then passwords should NEVER appear in URL parameters
  And authentication tokens should NEVER appear in URLs
  And error messages should NOT leak user enumeration data
```

### Feature: Protected Routes and Authorization

#### Happy Paths

```gherkin
Scenario: Authenticated user accesses protected route
  Given I am logged in
  When I navigate to "/dashboard"
  Then the page should load successfully
  And I should see my projects

Scenario: User logs out successfully
  Given I am logged in
  When I click the "Log Out" button
  Then my session should be terminated
  And I should be redirected to "/login"
  And I should not be able to access protected routes
  And the session cookie should be cleared
```

#### Authorization & Access Control

```gherkin
Scenario: Unauthenticated user is redirected to login
  Given I am not logged in
  When I attempt to access "/dashboard"
  Then I should be redirected to "/login"
  And the return URL should be preserved as "/dashboard"
  When I log in successfully
  Then I should be redirected back to "/dashboard"

Scenario: User cannot access another user's projects
  Given I am logged in as "user-a@example.com"
  And a project exists owned by "user-b@example.com" with ID "project-123"
  When I attempt to access "/projects/project-123"
  Then I should receive a 403 Forbidden error
  And I should see message "You do not have permission to access this project"

Scenario: User can only edit their own profile
  Given I am logged in as "user-a@example.com"
  When I attempt to update profile for "user-b@example.com"
  Then the API should return 403 Forbidden
  And the update should not be applied
```

#### Row Level Security (RLS)

```gherkin
Scenario: Database RLS policies enforce user isolation
  Given I am logged in as "user-a@example.com"
  When I query the projects table
  Then I should only see projects where user_id = my user ID
  And I should NOT see other users' projects
  And direct database queries should enforce the same policy

Scenario: Service role key bypasses RLS for admin operations
  Given I am using the service role key in a server action
  When I query the projects table
  Then I should be able to see all projects
  And I should be able to perform admin operations
  But the service role key should NEVER be exposed to the client
```

---

## Epic 3: Project Management

### Feature: Project CRUD Operations

#### Happy Paths

```gherkin
Scenario: User creates a new project
  Given I am logged in
  And I am on the dashboard
  When I click "New Project"
  And I enter "My First App" as the project name
  And I select "React" as the framework
  And I click "Create Project"
  Then a new project should be created in the database
  And the project should have a unique ID
  And I should be redirected to "/projects/{project-id}"
  And the project should appear in my dashboard
  And the created_at timestamp should be set

Scenario: User views list of projects
  Given I am logged in
  And I have 3 projects in my account
  When I navigate to "/dashboard"
  Then I should see all 3 projects listed
  And each project should display name, framework, and last modified date
  And projects should be sorted by last modified (newest first)

Scenario: User opens an existing project
  Given I have a project with ID "proj-123"
  When I click on the project in the dashboard
  Then I should be redirected to "/projects/proj-123"
  And the editor should load with the project files
  And the last opened tab should be restored

Scenario: User renames a project
  Given I am viewing project "proj-123" with name "Old Name"
  When I click the project name
  And I enter "New Name"
  And I press Enter
  Then the project name should update in the database
  And the updated_at timestamp should be updated
  And I should see a success toast "Project renamed"

Scenario: User deletes a project
  Given I have a project with ID "proj-123"
  And I am on the dashboard
  When I click the delete icon for the project
  Then I should see a confirmation dialog "Are you sure? This cannot be undone."
  When I click "Delete"
  Then the project should be removed from the database
  And all associated files should be deleted from storage
  And the project should disappear from the dashboard
  And I should see a success toast "Project deleted"
```

#### Validation & Error Handling

```gherkin
Scenario: Create project with empty name
  Given I am on the "New Project" dialog
  When I leave the project name field empty
  And I click "Create Project"
  Then I should see error "Project name is required"
  And the project should not be created

Scenario: Create project with name exceeding character limit
  Given I am on the "New Project" dialog
  When I enter a project name with 300 characters
  And I click "Create Project"
  Then I should see error "Project name must be less than 100 characters"

Scenario: Database error during project creation
  Given the database connection fails
  When I attempt to create a project
  Then I should see error "Failed to create project. Please try again."
  And no partial project data should be saved
  And the UI should remain in a state allowing retry

Scenario: User attempts to access non-existent project
  When I navigate to "/projects/non-existent-id"
  Then I should see a 404 error page
  And I should see message "Project not found"
  And I should see a link to "Return to Dashboard"

Scenario: Concurrent project updates conflict
  Given I have project "proj-123" open in two tabs
  When I rename the project to "Name A" in tab 1
  And I rename the project to "Name B" in tab 2
  Then the last write should win (optimistic locking)
  Or I should see a conflict warning "This project was updated elsewhere"
```

#### Edge Cases

```gherkin
Scenario: User has no projects
  Given I am a new user with no projects
  When I navigate to "/dashboard"
  Then I should see an empty state
  And I should see message "No projects yet. Create your first project!"
  And I should see a prominent "New Project" button

Scenario: Project name with special characters
  Given I am creating a new project
  When I enter "My-App_2024 (v1.0)" as the project name
  And I click "Create Project"
  Then the project should be created successfully
  And the name should be stored as-is
  And the name should be properly escaped in HTML rendering

Scenario: User creates 100+ projects
  Given I have 100 projects already
  When I create a new project
  Then the project should be created successfully
  And dashboard pagination should be implemented
  And I should see 20 projects per page
  And pagination controls should be displayed

Scenario: Real-time updates from other devices
  Given I have the dashboard open in browser A
  And I am logged in on browser B with the same account
  When I create a new project in browser B
  Then the new project should appear in browser A's dashboard
  And Supabase Realtime should push the update
  And no page refresh should be required
```

#### Security & Authorization

```gherkin
Scenario: SQL injection attempt in project name
  Given I am creating a new project
  When I enter "'; DROP TABLE projects; --" as the project name
  And I click "Create Project"
  Then the project should be created with the literal string as name
  And no SQL should be executed
  And the database should remain intact

Scenario: XSS attempt in project name
  Given I am creating a new project
  When I enter "<script>alert('xss')</script>" as the project name
  And I click "Create Project"
  Then the project should be created
  And when rendered, the HTML should be escaped
  And no script should execute

Scenario: User cannot delete another user's project
  Given a project "proj-123" owned by "user-b@example.com"
  And I am logged in as "user-a@example.com"
  When I attempt to DELETE "/api/projects/proj-123"
  Then I should receive a 403 Forbidden error
  And the project should not be deleted
```

### Feature: Dashboard and Project List

#### Happy Paths

```gherkin
Scenario: Dashboard displays project statistics
  Given I have 5 projects
  And 2 projects were modified today
  When I navigate to "/dashboard"
  Then I should see "5 Projects"
  And I should see "2 Active Today"
  And I should see total lines of code generated

Scenario: Filter projects by framework
  Given I have 3 React projects and 2 Vue projects
  When I select "React" in the framework filter
  Then I should see only the 3 React projects
  And the Vue projects should be hidden

Scenario: Search projects by name
  Given I have projects named "E-commerce App", "Blog Site", "Todo App"
  When I enter "App" in the search field
  Then I should see "E-commerce App" and "Todo App"
  And "Blog Site" should be hidden
  And search should be case-insensitive
```

#### Performance

```gherkin
Scenario: Dashboard loads quickly with many projects
  Given I have 200 projects
  When I navigate to "/dashboard"
  Then the initial page should load in under 2 seconds
  And projects should be paginated (20 per page)
  And infinite scroll or pagination should be implemented
  And database queries should use proper indexes

Scenario: Project thumbnails are optimized
  Given projects have preview screenshots
  When the dashboard loads
  Then images should be lazy-loaded
  And images should be served in WebP format
  And images should be properly sized (no oversized downloads)
```

---

## Epic 4: Chat Mode - AI Code Generation

### Feature: AI Conversation and Code Generation

#### Happy Paths

```gherkin
Scenario: User sends a message to generate code with Claude
  Given I am in a project
  And I am in "Chat Mode"
  When I enter "Create a login form with email and password fields" in the chat input
  And I click "Send"
  Then the message should appear in the chat history
  And a loading indicator should show "Claude is thinking..."
  And an API request should be sent to "/api/generate"
  And the request should use the Claude 3.5 Sonnet model
  And the response should stream back in real-time
  And generated code should be displayed with syntax highlighting
  And an "Apply to Project" button should appear

Scenario: User applies generated code to project
  Given Claude has generated a React component
  And I see the code in the chat response
  When I click "Apply to Project"
  Then a new file should be created with the generated code
  And the file should appear in the file tree
  And the file should be opened in the editor
  And I should see a success toast "Code applied successfully"

Scenario: Streaming response displays progressively
  Given I send a message requesting code generation
  When the AI starts responding
  Then I should see tokens appear progressively
  And the UI should update as each chunk arrives
  And I should not have to wait for the complete response
  And I should be able to stop generation with a "Stop" button
```

#### Multi-Model Support

```gherkin
Scenario: Fallback to GPT-4 when Claude is unavailable
  Given the Anthropic API returns a 503 error
  When I send a code generation request
  Then the system should automatically retry with GPT-4
  And I should see a notice "Using GPT-4 (Claude unavailable)"
  And the generation should complete successfully

Scenario: User manually selects AI model
  Given I am in Chat Mode
  When I click the model selector dropdown
  Then I should see options "Claude 3.5 Sonnet" and "GPT-4"
  When I select "GPT-4"
  And I send a message
  Then the request should use the GPT-4 API
  And the response should be generated by GPT-4

Scenario: Token limit is enforced per model
  Given I am using Claude 3.5 Sonnet
  When I send a request that would exceed 200k tokens
  Then I should see warning "Request exceeds token limit. Please shorten your input."
  And the request should not be sent
```

#### Validation & Error Handling

```gherkin
Scenario: User sends empty message
  Given I am in Chat Mode
  When I click "Send" without entering any text
  Then nothing should happen
  And the send button should be disabled when input is empty

Scenario: AI API returns an error
  Given the AI API returns a 500 error
  When I send a code generation request
  Then I should see error "Failed to generate code. Please try again."
  And the chat should remain in a usable state
  And I should be able to retry the request

Scenario: Network timeout during generation
  Given I send a code generation request
  And the API does not respond within 30 seconds
  Then I should see error "Request timed out. Please try again."
  And the loading state should be cleared
  And I should be able to send a new message

Scenario: AI generates invalid code
  Given the AI returns code with syntax errors
  When the code is displayed in chat
  Then syntax highlighting should still work
  And I should see a warning "Generated code may have errors"
  And I should still be able to apply it (with confirmation)

Scenario: Rate limit is reached
  Given I have sent 20 requests in the last minute
  When I attempt to send another request
  Then I should see error "Rate limit exceeded. Please wait 30 seconds."
  And the send button should be disabled temporarily
  And a countdown timer should be displayed
```

#### Edge Cases

```gherkin
Scenario: Very long conversation history
  Given I have 50+ messages in the chat history
  When I send a new message
  Then only the last 10 messages should be included in context
  And older messages should be stored but not sent to the AI
  And I should be able to scroll to view all messages

Scenario: User modifies generated code before applying
  Given Claude has generated code
  And the code is displayed in the chat
  When I edit the code directly in the chat response
  And I click "Apply to Project"
  Then the modified code should be applied
  And not the original AI-generated code

Scenario: Concurrent generation requests
  Given I send a code generation request
  And the response is still streaming
  When I send another request
  Then the first request should be cancelled
  And a new request should start
  And I should see "Previous generation stopped"

Scenario: Message with code snippets in the prompt
  Given I am in Chat Mode
  When I paste existing code into the chat input
  And I add instructions "Refactor this to use React hooks"
  And I click "Send"
  Then the AI should receive both the code and instructions
  And the AI should understand the context
  And the response should provide refactored code
```

#### Security

```gherkin
Scenario: API keys are never exposed to client
  Given I am using the chat feature
  When I inspect network requests in DevTools
  Then I should NOT see the ANTHROPIC_API_KEY
  And I should NOT see the OPENAI_API_KEY
  And all AI requests should go through server routes

Scenario: User input is sanitized before sending to AI
  Given I enter a message with malicious content
  When the message is sent to the AI API
  Then it should be sanitized to prevent prompt injection
  And the AI should not be able to execute unintended actions

Scenario: Generated code is not auto-executed
  Given the AI generates JavaScript code
  When the code is displayed in chat
  Then it should NOT be automatically executed
  And eval() should NOT be used
  And the code should only run if user explicitly applies it to preview

Scenario: AI responses are validated before display
  Given the AI API returns a response
  When the response is received
  Then it should be validated as proper JSON
  And malicious content should be escaped
  And XSS attempts in the response should be prevented

Scenario: Cost tracking and limits
  Given I have a free tier account
  When I send multiple expensive requests
  Then my token usage should be tracked
  And I should see a warning at 80% of my limit
  And I should be blocked at 100% with message "Monthly limit reached"
```

### Feature: Chat History and Context Management

#### Happy Paths

```gherkin
Scenario: Chat history is persisted per project
  Given I am in project "proj-123"
  And I have a conversation with 10 messages
  When I close the project and reopen it
  Then all 10 messages should be restored
  And the chat scroll position should be at the bottom

Scenario: User clears chat history
  Given I have a conversation with multiple messages
  When I click "Clear Chat History"
  Then I should see confirmation "Clear all messages? This cannot be undone."
  When I confirm
  Then all messages should be deleted
  And the chat should show an empty state

Scenario: Export chat history
  Given I have a conversation with code generation
  When I click "Export Chat"
  Then a markdown file should be downloaded
  And it should contain all messages with timestamps
  And code blocks should be properly formatted
```

---

## Epic 5: Editor Mode - Monaco Integration

### Feature: Code Editor with Monaco

#### Happy Paths

```gherkin
Scenario: Monaco Editor loads and displays file content
  Given I am in a project with a file "src/App.tsx"
  When I click the file in the file tree
  Then Monaco Editor should load
  And the file content should be displayed
  And syntax highlighting for TypeScript should be active
  And line numbers should be visible

Scenario: User edits code and saves manually
  Given I have a file open in the editor
  When I modify the code
  And I press Ctrl+S (or Cmd+S on Mac)
  Then the file should be saved to Supabase Storage
  And I should see a success indicator "Saved"
  And the modified timestamp should update

Scenario: Auto-save triggers after inactivity
  Given I have a file open in the editor
  When I make changes
  And I stop typing for 2 seconds
  Then the file should be auto-saved
  And I should see a subtle "Auto-saved" indicator
  And the indicator should fade after 2 seconds

Scenario: Syntax highlighting works for multiple languages
  Given I open "index.html"
  Then I should see HTML syntax highlighting
  When I open "styles.css"
  Then I should see CSS syntax highlighting
  When I open "script.js"
  Then I should see JavaScript syntax highlighting
  When I open "App.tsx"
  Then I should see TypeScript/JSX syntax highlighting
```

#### Multi-Tab Support

```gherkin
Scenario: User opens multiple files in tabs
  Given I am in the editor
  When I click "src/App.tsx" in the file tree
  Then a tab should open for "App.tsx"
  When I click "src/utils.ts" in the file tree
  Then a second tab should open for "utils.ts"
  And both tabs should be visible in the tab bar
  And the active tab should be "utils.ts"

Scenario: User switches between tabs
  Given I have "App.tsx" and "utils.ts" open in tabs
  And "utils.ts" is active
  When I click the "App.tsx" tab
  Then the editor should switch to "App.tsx" content
  And the "App.tsx" tab should be highlighted as active

Scenario: User closes a tab
  Given I have "App.tsx" open
  When I click the close icon (X) on the tab
  Then the tab should close
  And if I have unsaved changes, I should see a confirmation
  And the next tab should become active (or editor shows empty state)

Scenario: Tab shows unsaved indicator
  Given I have a file open
  When I make changes without saving
  Then the tab should show a dot or asterisk indicator
  And the tab title should show "* App.tsx"
  When I save the file
  Then the indicator should disappear
```

#### Editor Features

```gherkin
Scenario: IntelliSense provides autocomplete suggestions
  Given I am editing a TypeScript file
  When I type "React." and pause
  Then I should see autocomplete suggestions
  And suggestions should include "useState", "useEffect", etc.
  And I should be able to navigate suggestions with arrow keys
  And pressing Tab or Enter should apply the suggestion

Scenario: Error markers show TypeScript errors
  Given I am editing a TypeScript file
  When I write code with a type error: "const x: number = 'string';"
  Then I should see a red squiggly underline
  And hovering should show error tooltip
  And the error should appear in the problems panel

Scenario: Code formatting with Prettier
  Given I have unformatted code in the editor
  When I press Shift+Alt+F (or format command)
  Then the code should be formatted according to Prettier rules
  And indentation should be consistent
  And the formatting should match project .prettierrc

Scenario: Find and replace in editor
  Given I have a file open with the word "oldName" appearing 5 times
  When I press Ctrl+F
  And I search for "oldName"
  Then all 5 occurrences should be highlighted
  When I press Ctrl+H and enter "newName" as replacement
  And I click "Replace All"
  Then all 5 occurrences should be replaced

Scenario: Go to definition works
  Given I have a TypeScript project
  And I have a function "calculateTotal" defined in "utils.ts"
  And I use it in "App.tsx"
  When I Ctrl+Click on "calculateTotal" in "App.tsx"
  Then the editor should open "utils.ts"
  And the cursor should jump to the function definition
```

#### File Operations

```gherkin
Scenario: Create new file from editor
  Given I am in the editor
  When I right-click on a folder in the file tree
  And I select "New File"
  And I enter "Button.tsx"
  And I press Enter
  Then a new file should be created in Supabase Storage
  And the file should open in a new tab
  And the file should be empty

Scenario: Rename file from editor
  Given I have a file "OldName.tsx"
  When I right-click the file in the file tree
  And I select "Rename"
  And I enter "NewName.tsx"
  And I press Enter
  Then the file should be renamed in storage
  And any open tabs should update to "NewName.tsx"
  And import statements should be updated (if applicable)

Scenario: Delete file from editor
  Given I have a file "Unused.tsx"
  When I right-click the file in the file tree
  And I select "Delete"
  Then I should see confirmation "Delete Unused.tsx?"
  When I confirm
  Then the file should be deleted from storage
  And the tab should close if open
  And the file should disappear from the file tree
```

#### Edge Cases

```gherkin
Scenario: Large file (>1MB) opens with warning
  Given I have a file larger than 1MB
  When I attempt to open it
  Then I should see a warning "This file is large and may impact performance"
  And I should have options to "Open Anyway" or "Cancel"
  When I click "Open Anyway"
  Then the file should open with features potentially limited

Scenario: Binary file is not editable
  Given I have an image file "logo.png"
  When I click it in the file tree
  Then I should see a preview of the image
  And I should NOT see the Monaco editor
  And I should see message "Binary file - Preview only"

Scenario: Editor recovers from crash
  Given I am editing a file
  And the browser tab crashes or is force-closed
  When I reopen the project
  Then any unsaved changes should be recovered from localStorage
  And I should see a notification "Recovered unsaved changes"

Scenario: Keyboard shortcuts are customizable
  Given I am in editor settings
  When I navigate to "Keyboard Shortcuts"
  Then I should see a list of all shortcuts
  And I should be able to customize them
  And changes should persist across sessions

Scenario: Multiple users edit the same file (conflict)
  Given user A and user B have the same file open
  When user A saves changes
  And user B also makes changes and saves
  Then user B should see a conflict warning
  And I should have options to "Keep Mine", "Use Theirs", or "Merge"
```

#### Performance

```gherkin
Scenario: Editor loads quickly for typical files
  Given I have a TypeScript file with 500 lines
  When I open the file
  Then the editor should render in under 500ms
  And syntax highlighting should be complete in under 1 second
  And typing should feel responsive (<50ms latency)

Scenario: Editor handles very long lines
  Given I have a file with lines longer than 1000 characters
  When I scroll horizontally
  Then scrolling should be smooth
  And rendering should not cause lag

Scenario: Syntax highlighting is debounced for performance
  Given I am typing quickly in the editor
  When I type continuously
  Then syntax highlighting should update smoothly
  And highlighting should not block typing
```

#### Security

```gherkin
Scenario: File path traversal is prevented
  Given I attempt to create a file with path "../../../etc/passwd"
  When I submit the file creation
  Then I should see error "Invalid file path"
  And no file should be created outside the project directory

Scenario: Code execution is sandboxed (not in editor itself)
  Given I write malicious code in the editor
  When I save the file
  Then the code should be stored as text
  And it should NOT be executed on the server
  And it should only run in the sandboxed preview
```

---

## Epic 6: Preview System

### Feature: Live Preview with Sandboxed iframe

#### Happy Paths

```gherkin
Scenario: Preview updates when code changes
  Given I have a React component open in the editor
  When I modify the JSX
  And I save the file
  Then the preview iframe should reload
  And I should see the updated component
  And the preview should update within 2 seconds

Scenario: Hot Module Replacement works for React
  Given I have HMR configured
  When I change a component's styling
  And I save
  Then the preview should update without full page reload
  And component state should be preserved
  And I should see the style change instantly

Scenario: Preview handles multiple entry points
  Given my project has "index.html" as entry
  When I open the preview
  Then the preview should load "index.html"
  And all linked CSS/JS should be loaded
  And the application should function correctly

Scenario: User toggles preview panel visibility
  Given the preview is visible
  When I click "Hide Preview"
  Then the preview panel should collapse
  And the editor should expand to full width
  When I click "Show Preview"
  Then the preview should reappear
```

#### Console Output Integration

```gherkin
Scenario: Console logs appear in integrated console
  Given I have code that logs to console: "console.log('Hello');"
  When the preview runs
  Then I should see "Hello" in the integrated console panel
  And console.error should appear in red
  And console.warn should appear in yellow
  And console.info should appear in blue

Scenario: Runtime errors are displayed in console
  Given I have code that throws an error
  When the preview runs
  Then I should see the error in the console
  And the error should include stack trace
  And the line number should be clickable
  And clicking should jump to the error in the editor

Scenario: User clears console output
  Given the console has multiple messages
  When I click the "Clear Console" button
  Then all messages should be removed
  And the console should be empty
```

#### Error Handling

```gherkin
Scenario: Preview handles syntax errors gracefully
  Given I have invalid JavaScript in my code
  When the preview attempts to run
  Then I should see an error overlay in the preview
  And the error message should explain the syntax issue
  And the error should not crash the preview iframe

Scenario: Preview handles network errors
  Given the preview tries to fetch a non-existent resource
  When the fetch fails
  Then I should see a network error in the console
  And the preview should remain functional
  And I should see error "Failed to load resource: 404"

Scenario: Preview times out for infinite loops
  Given I have code with an infinite loop
  When the preview tries to run
  Then the preview should detect the loop
  And I should see a warning "Script execution timed out"
  And the preview should be terminated safely

Scenario: Preview handles missing dependencies
  Given my code imports a package that doesn't exist
  When the preview tries to run
  Then I should see error "Cannot find module 'missing-package'"
  And the error should suggest installing the package
```

#### Edge Cases

```gherkin
Scenario: Preview works with multiple HTML pages
  Given I have "index.html" and "about.html"
  When I navigate to "about.html" in the preview
  Then the preview should load "about.html"
  And navigation should work within the preview

Scenario: Preview handles large assets
  Given my project includes large images
  When the preview loads
  Then images should be lazy-loaded where appropriate
  And I should see loading indicators
  And the preview should remain responsive

Scenario: Preview preserves state during code changes
  Given I have a form with user input in the preview
  When I make a CSS change in the editor
  And HMR updates the preview
  Then the form input should be preserved
  And I should not lose my entered data

Scenario: User resizes preview panel
  Given the preview is in split view with the editor
  When I drag the divider to resize
  Then the preview should resize smoothly
  And the layout should be responsive
  And the resize should persist across sessions
```

#### Security (Critical)

```gherkin
Scenario: Preview iframe is sandboxed
  Given the preview is running
  When I inspect the iframe element
  Then it should have sandbox attributes
  And sandbox should include "allow-scripts allow-same-origin"
  And the iframe should NOT have access to parent window
  And cross-origin isolation should be enforced

Scenario: Preview cannot access localStorage of parent
  Given I run code in the preview that accesses localStorage
  When the code executes
  Then it should access preview's own localStorage
  And it should NOT access the editor's localStorage
  And data should be isolated

Scenario: Preview cannot make arbitrary network requests
  Given the preview tries to make a fetch to an external API
  When the request is made
  Then it should be subject to CORS policies
  And sensitive requests should be blocked
  And CSP headers should be enforced

Scenario: XSS in preview is contained
  Given I write code with XSS payload: "<img src=x onerror=alert(1)>"
  When the preview renders
  Then the XSS should execute in the sandboxed iframe
  And it should NOT affect the parent application
  And it should NOT steal authentication tokens

Scenario: Preview cannot execute Node.js code on server
  Given I write code that attempts to use 'fs' or 'process'
  When the preview runs
  Then it should throw an error "Module not found"
  And no server-side code should execute
  And the sandbox should only run browser-compatible code
```

#### Performance

```gherkin
Scenario: Preview loads quickly for small projects
  Given I have a simple HTML/CSS/JS project
  When I open the preview
  Then the preview should load in under 1 second
  And the page should be interactive in under 2 seconds

Scenario: Preview handles large bundles efficiently
  Given my project has a 5MB JavaScript bundle
  When the preview loads
  Then I should see a loading indicator
  And the bundle should be loaded progressively
  And I should see meaningful progress updates
```

---

## Epic 7: Deployment Integration

### Feature: Deploy to Vercel

#### Happy Paths

```gherkin
Scenario: User connects Vercel account
  Given I am in a project
  And I have not connected Vercel
  When I click "Deploy"
  Then I should be prompted to "Connect Vercel Account"
  When I click "Connect"
  Then I should be redirected to Vercel OAuth
  When I authorize the application
  Then I should be redirected back
  And my Vercel account should be linked
  And I should see my Vercel teams/organizations

Scenario: User deploys project to Vercel for the first time
  Given I have connected my Vercel account
  And I am in a project that has not been deployed
  When I click "Deploy to Vercel"
  Then I should see deployment configuration options
  And I should select a Vercel team
  And I should specify environment variables (if any)
  When I click "Start Deployment"
  Then a deployment should be triggered via Vercel API
  And I should see deployment progress updates
  And I should see "Building..." status
  When the deployment completes
  Then I should see "Deployment Successful"
  And I should see the deployment URL (e.g., "my-app.vercel.app")
  And I should be able to click to open the deployed site

Scenario: User re-deploys with updates
  Given my project is already deployed to Vercel
  When I make changes to the code
  And I click "Re-deploy"
  Then a new deployment should be triggered
  And the deployment should use the latest code from the project
  And I should see the new deployment URL (could be production or preview)

Scenario: Deployment progress is tracked in real-time
  Given a deployment is in progress
  When I am on the deployment page
  Then I should see real-time status updates
  And I should see logs streaming from Vercel
  And I should see stages: "Queued", "Building", "Deploying", "Ready"
  And I should see build duration
```

#### Validation & Error Handling

```gherkin
Scenario: Deployment fails due to build errors
  Given my project has a TypeScript error
  When I attempt to deploy
  Then the deployment should start
  And the build should fail
  And I should see error logs from Vercel
  And the error should indicate the file and line number
  And the deployment status should be "Failed"
  And I should see a "View Logs" button

Scenario: Deployment fails due to missing environment variables
  Given my project requires NEXT_PUBLIC_API_KEY
  And I have not configured it in Vercel
  When the deployment runs
  Then the build should fail with error "Missing environment variable: NEXT_PUBLIC_API_KEY"
  And I should see a suggestion to add it in project settings

Scenario: Vercel API is unavailable
  Given the Vercel API returns a 503 error
  When I attempt to deploy
  Then I should see error "Vercel is currently unavailable. Please try again later."
  And the deployment should not be started
  And I should be able to retry

Scenario: User's Vercel quota is exceeded
  Given I have exceeded my Vercel deployment limit
  When I attempt to deploy
  Then I should see error "Deployment quota exceeded. Please upgrade your Vercel plan."
  And a link to Vercel dashboard should be provided

Scenario: OAuth token expires during deployment
  Given my Vercel OAuth token has expired
  When a deployment is triggered
  Then I should see error "Vercel authentication expired"
  And I should be prompted to re-authenticate
  And I should be able to re-connect without losing progress
```

#### Edge Cases

```gherkin
Scenario: User has multiple Vercel teams
  Given I am connected to Vercel with 3 teams
  When I start a deployment
  Then I should see a dropdown to select the team
  And I should be able to choose which team to deploy under

Scenario: Deployment history is maintained
  Given I have deployed 5 times
  When I navigate to "Deployment History"
  Then I should see all 5 deployments listed
  And each should show timestamp, status, and URL
  And I should be able to click to view details or logs

Scenario: User cancels a deployment in progress
  Given a deployment is currently building
  When I click "Cancel Deployment"
  Then the deployment should be cancelled via Vercel API
  And I should see status "Cancelled"
  And no URL should be generated

Scenario: Project name conflicts with existing Vercel project
  Given I have a Vercel project named "my-app"
  And I try to deploy a new project also named "my-app"
  When the deployment starts
  Then I should see error "Project name already exists"
  And I should be prompted to choose a different name
```

#### Security (Critical)

```gherkin
Scenario: Vercel OAuth token is stored securely
  Given I have connected my Vercel account
  When I inspect the database
  Then the OAuth token should be encrypted at rest
  And the token should NOT be accessible via client-side code
  And the token should be stored with user-specific RLS policies

Scenario: Vercel API calls use user's token (not global)
  Given I am deploying a project
  When the deployment API call is made
  Then it should use MY Vercel OAuth token
  And NOT a shared service token
  And I should only be able to deploy to my own Vercel account

Scenario: Deployment does not expose API keys
  Given my project uses ANTHROPIC_API_KEY
  When I deploy to Vercel
  Then the API key should be set as a Vercel environment variable
  And it should NOT be included in the build output
  And it should NOT be visible in client-side bundles

Scenario: Malicious code in project is sandboxed on Vercel
  Given I deploy a project with malicious code
  When the deployment runs
  Then the build should run in Vercel's sandboxed environment
  And it should NOT affect the InformatiK-AI platform
  And it should NOT access other users' deployments

Scenario: Rate limiting prevents abuse
  Given I attempt to trigger 100 deployments in 1 minute
  When I make the requests
  Then I should be rate limited
  And I should see error "Too many deployment requests. Please wait."
  And subsequent requests should be blocked temporarily
```

#### Performance

```gherkin
Scenario: Deployment status is polled efficiently
  Given a deployment is in progress
  When the UI polls for status updates
  Then polling should occur every 5 seconds
  And polling should stop when deployment completes
  And polling should use exponential backoff on errors

Scenario: Large projects deploy within reasonable time
  Given my project has 100 files and 10MB bundle
  When I deploy
  Then the deployment should complete within 5 minutes
  And I should see progress updates throughout
```

### Feature: Deployment Settings and Management

#### Happy Paths

```gherkin
Scenario: User configures custom domain
  Given my project is deployed to Vercel
  When I navigate to deployment settings
  And I enter "myapp.com" as custom domain
  And I click "Add Domain"
  Then the domain should be added via Vercel API
  And I should see DNS configuration instructions
  And Vercel should verify domain ownership

Scenario: User configures environment variables for deployment
  Given I am setting up deployment
  When I navigate to "Environment Variables"
  And I add key "NEXT_PUBLIC_API_URL" with value "https://api.example.com"
  And I click "Save"
  Then the environment variable should be saved to Vercel
  And it should be available in the deployed build
  And changes should trigger re-deployment warning

Scenario: User rolls back to previous deployment
  Given I have 3 successful deployments
  And the latest deployment has a bug
  When I navigate to deployment history
  And I click "Rollback" on deployment #2
  Then Vercel should set deployment #2 as active
  And the production URL should serve the rolled-back version
  And I should see success message "Rolled back to deployment #2"
```

---

## Coverage Matrix

| Epic | Feature Area | Unit Tests | Integration Tests | E2E Tests | Security Tests | Priority |
|------|--------------|------------|-------------------|-----------|----------------|----------|
| **1. Foundation** | Next.js Setup | ✓ | ✓ | ✓ | ✓ | P0 |
| | Environment Config | ✓ | ✓ | - | ✓ | P0 |
| | Tailwind/shadcn | ✓ | - | ✓ | - | P1 |
| **2. Authentication** | Registration/Login | ✓ | ✓ | ✓ | ✓ | P0 |
| | OAuth (GitHub) | - | ✓ | ✓ | ✓ | P0 |
| | Protected Routes | ✓ | ✓ | ✓ | ✓ | P0 |
| | Session Management | ✓ | ✓ | ✓ | ✓ | P0 |
| | RLS Policies | ✓ | ✓ | - | ✓ | P0 |
| **3. Project Mgmt** | CRUD Operations | ✓ | ✓ | ✓ | ✓ | P0 |
| | Dashboard | ✓ | ✓ | ✓ | - | P1 |
| | Realtime Updates | - | ✓ | ✓ | - | P1 |
| **4. Chat Mode** | AI Generation | ✓ | ✓ | ✓ | ✓ | P0 |
| | Streaming | ✓ | ✓ | ✓ | - | P0 |
| | Multi-Model | ✓ | ✓ | ✓ | - | P1 |
| | Token Management | ✓ | ✓ | - | ✓ | P0 |
| **5. Editor** | Monaco Integration | ✓ | - | ✓ | - | P0 |
| | File Operations | ✓ | ✓ | ✓ | ✓ | P0 |
| | Multi-Tab | ✓ | - | ✓ | - | P1 |
| | Auto-save | ✓ | ✓ | ✓ | - | P1 |
| | IntelliSense | - | - | ✓ | - | P2 |
| **6. Preview** | Sandboxed iframe | ✓ | ✓ | ✓ | ✓ | P0 |
| | HMR | ✓ | - | ✓ | - | P1 |
| | Console Integration | ✓ | - | ✓ | - | P1 |
| | Error Handling | ✓ | ✓ | ✓ | ✓ | P0 |
| **7. Deployment** | Vercel Integration | ✓ | ✓ | ✓ | ✓ | P0 |
| | OAuth Flow | - | ✓ | ✓ | ✓ | P0 |
| | Build Process | ✓ | ✓ | ✓ | - | P0 |
| | Env Variables | ✓ | ✓ | ✓ | ✓ | P0 |
| | Deployment History | ✓ | ✓ | ✓ | - | P1 |

## Non-Functional Requirements

### Performance Criteria

| Metric | Target | Test Method |
|--------|--------|-------------|
| Dashboard Load Time | < 2s | Lighthouse, Playwright |
| Editor Open Time | < 500ms | Performance API |
| Preview Update Time | < 2s | Custom timing |
| AI Response TTFB | < 3s | API monitoring |
| Build Time (typical) | < 30s | CI measurements |
| Deploy Time | < 5min | Vercel API logs |

### Accessibility Criteria

| Requirement | WCAG Level | Test Method |
|-------------|------------|-------------|
| Keyboard Navigation | AA | Manual + axe-core |
| Screen Reader Support | AA | NVDA/JAWS testing |
| Color Contrast | AAA | axe-core |
| Focus Management | AA | Playwright tests |
| ARIA Labels | AA | axe-core + manual |

### Security Requirements

| Area | Requirement | Validation |
|------|-------------|------------|
| Authentication | Supabase Auth + RLS | Integration tests |
| API Keys | Never exposed to client | Code review + tests |
| XSS Prevention | All user input escaped | Security tests |
| CSRF Protection | Tokens on mutations | Integration tests |
| Sandbox Isolation | iframe with sandbox attr | E2E tests |
| Rate Limiting | 20 req/min for AI, 5/5min for deploy | Load tests |
| Token Storage | HTTPOnly, Secure cookies | Browser inspection |

### Browser Compatibility

| Browser | Min Version | Test Coverage |
|---------|-------------|---------------|
| Chrome | 120+ | Full (Playwright) |
| Firefox | 120+ | Full (Playwright) |
| Safari | 16+ | Smoke tests |
| Edge | 120+ | Smoke tests |

---

## Test Implementation Guidelines

### Unit Test Structure (Vitest)

```typescript
// Example: lib/ai/providers/anthropic.test.ts

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { generateCode } from './anthropic';

describe('Anthropic AI Provider', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('generateCode', () => {
    it('should generate code successfully with valid prompt', async () => {
      // Arrange
      const prompt = 'Create a button component';
      const mockResponse = { code: 'export default function Button() {}' };

      // Act
      const result = await generateCode(prompt);

      // Assert
      expect(result.ok).toBe(true);
      expect(result.data).toContain('function Button');
    });

    it('should handle API errors gracefully', async () => {
      // Arrange
      vi.mocked(anthropicClient).mockRejectedValue(new Error('API Error'));

      // Act
      const result = await generateCode('test');

      // Assert
      expect(result.ok).toBe(false);
      expect(result.error.message).toContain('API Error');
    });

    it('should enforce token limits', async () => {
      // Arrange
      const longPrompt = 'a'.repeat(300000);

      // Act
      const result = await generateCode(longPrompt);

      // Assert
      expect(result.ok).toBe(false);
      expect(result.error.code).toBe('TOKEN_LIMIT_EXCEEDED');
    });
  });
});
```

### Integration Test Structure (Vitest)

```typescript
// Example: tests/integration/api/projects.test.ts

import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createClient } from '@supabase/supabase-js';
import { createProject, getProjects } from '@/app/actions/projects';

describe('Projects API Integration', () => {
  let supabase;
  let testUser;

  beforeAll(async () => {
    // Setup test database
    supabase = createClient(process.env.TEST_SUPABASE_URL, process.env.TEST_KEY);
    testUser = await createTestUser();
  });

  afterAll(async () => {
    // Cleanup
    await deleteTestUser(testUser.id);
  });

  it('should create project and enforce RLS', async () => {
    // Act
    const project = await createProject({ name: 'Test Project' }, testUser.id);

    // Assert
    expect(project).toBeDefined();
    expect(project.user_id).toBe(testUser.id);

    // Verify RLS - another user cannot access
    const otherUser = await createTestUser();
    const projects = await getProjects(otherUser.id);
    expect(projects).not.toContainEqual(expect.objectContaining({ id: project.id }));
  });
});
```

### E2E Test Structure (Playwright)

```typescript
// Example: tests/e2e/chat-mode.spec.ts

import { test, expect } from '@playwright/test';

test.describe('Chat Mode - AI Code Generation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'TestPass123!');
    await page.click('button:has-text("Sign In")');
    await page.waitForURL('/dashboard');
  });

  test('should generate code with Claude and apply to project', async ({ page }) => {
    // Open project
    await page.click('text=My Project');
    await page.waitForURL(/\/projects\/.+/);

    // Switch to Chat Mode
    await page.click('text=Chat Mode');

    // Send message
    await page.fill('[placeholder="Describe what you want to build..."]',
      'Create a login form with email and password');
    await page.click('button:has-text("Send")');

    // Wait for AI response
    await expect(page.locator('text=Claude is thinking')).toBeVisible();
    await expect(page.locator('code')).toBeVisible({ timeout: 30000 });

    // Apply to project
    await page.click('button:has-text("Apply to Project")');

    // Verify file created
    await expect(page.locator('text=LoginForm.tsx')).toBeVisible();
    await expect(page.locator('text=Code applied successfully')).toBeVisible();
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API failure
    await page.route('**/api/generate', route =>
      route.fulfill({ status: 500, body: 'Internal Server Error' })
    );

    // Attempt generation
    await page.fill('[placeholder="Describe what you want to build..."]', 'test');
    await page.click('button:has-text("Send")');

    // Verify error handling
    await expect(page.locator('text=Failed to generate code')).toBeVisible();
  });
});
```

### Component Test Structure (Testing Library)

```typescript
// Example: components/editor/code-editor.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import CodeEditor from './code-editor';

describe('CodeEditor Component', () => {
  it('should render Monaco editor with file content', async () => {
    const mockFile = { name: 'App.tsx', content: 'function App() {}' };

    render(<CodeEditor file={mockFile} />);

    await waitFor(() => {
      expect(screen.getByRole('textbox')).toBeInTheDocument();
    });
  });

  it('should trigger auto-save after 2 seconds of inactivity', async () => {
    const onSave = vi.fn();
    const mockFile = { name: 'test.ts', content: 'const x = 1;' };

    render(<CodeEditor file={mockFile} onSave={onSave} />);

    // Simulate typing
    const editor = screen.getByRole('textbox');
    fireEvent.change(editor, { target: { value: 'const x = 2;' } });

    // Wait for auto-save debounce
    await waitFor(() => expect(onSave).toHaveBeenCalled(), { timeout: 3000 });
    expect(onSave).toHaveBeenCalledWith(expect.objectContaining({
      content: 'const x = 2;'
    }));
  });

  it('should show unsaved indicator when file is modified', async () => {
    const mockFile = { name: 'test.ts', content: 'const x = 1;' };

    render(<CodeEditor file={mockFile} />);

    const editor = screen.getByRole('textbox');
    fireEvent.change(editor, { target: { value: 'const x = 2;' } });

    await waitFor(() => {
      expect(screen.getByText(/unsaved/i)).toBeInTheDocument();
    });
  });
});
```

---

## CI/CD Test Integration

### GitHub Actions Workflow

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: pnpm test -- --coverage
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json

  integration-tests:
    runs-on: ubuntu-latest
    env:
      TEST_SUPABASE_URL: ${{ secrets.TEST_SUPABASE_URL }}
      TEST_SUPABASE_KEY: ${{ secrets.TEST_SUPABASE_KEY }}
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: pnpm test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: npx playwright install --with-deps
      - run: pnpm build
      - run: pnpm test:e2e
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## Test Execution Commands

```bash
# Unit Tests
pnpm test                           # Run all unit tests
pnpm test -- --watch                # Watch mode
pnpm test -- --coverage             # With coverage
pnpm test -- --ui                   # Vitest UI mode

# Integration Tests
pnpm test:integration               # Run integration tests
pnpm test:integration -- --watch    # Watch mode

# E2E Tests
pnpm test:e2e                       # Run all E2E tests (headless)
pnpm test:e2e -- --ui               # Playwright UI mode
pnpm test:e2e -- --headed           # Run with browser visible
pnpm test:e2e -- --project=chromium # Run on specific browser

# Component Tests
pnpm test -- --grep="Component"     # Run only component tests

# Coverage
pnpm test:coverage                  # Generate coverage report
open coverage/index.html            # View coverage report

# Lint and Type Check (should run before tests)
pnpm lint                           # ESLint
pnpm type-check                     # TypeScript
```

---

## Test Data Management

### Test User Accounts

| Email | Password | Role | Purpose |
|-------|----------|------|---------|
| test@example.com | TestPass123! | User | General testing |
| admin@example.com | AdminPass123! | Admin | Admin feature testing |
| oauth-test@github.com | N/A | User | OAuth flow testing |

### Test Projects

| Name | Framework | Files | Purpose |
|------|-----------|-------|---------|
| Empty Project | React | 0 | New project testing |
| Small Project | React | 5 | Quick operations |
| Large Project | Next.js | 100+ | Performance testing |
| Error Project | React | Invalid | Error handling |

### Mock Data

- **AI Responses**: Pre-recorded Claude/GPT responses for consistent testing
- **Vercel API**: Mock deployment responses for offline testing
- **Supabase**: Test database with seeded data

---

## Success Criteria

### Coverage Targets

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: All critical API routes and database operations
- **E2E Tests**: All happy paths and critical user flows
- **Security Tests**: All authentication, authorization, and API key handling scenarios

### Quality Gates

- [ ] All tests pass in CI
- [ ] Coverage thresholds met
- [ ] No security vulnerabilities detected
- [ ] Performance budgets met
- [ ] Accessibility tests pass (axe-core)
- [ ] No TypeScript errors
- [ ] No ESLint warnings

### Definition of Done

A feature is considered complete when:

1. Implementation is finished
2. All unit tests written and passing (80%+ coverage)
3. Integration tests cover API and database interactions
4. E2E tests cover user flows
5. Security scenarios tested (if applicable)
6. Code reviewed and approved
7. Documentation updated
8. `/acceptance-validator` confirms all criteria met

---

## Notes for Implementation

- **Test First**: Where possible, write tests before implementation (TDD)
- **Mock External APIs**: Always mock Anthropic, OpenAI, and Vercel APIs in tests
- **Isolate Tests**: Each test should be independent and not rely on execution order
- **Use Test Database**: Never test against production Supabase instance
- **Security Focus**: Given the nature of code execution and API key handling, security tests are P0
- **Performance Monitoring**: Track test execution time and optimize slow tests
- **Flaky Tests**: Fix or quarantine within 24 hours - do not merge with flaky tests

---

## Related Skills

After implementing this test strategy, use:

| Skill | Purpose |
|-------|---------|
| `/acceptance-validator` | Validate that implementation meets all acceptance criteria |
| `/code-reviewer` | Review test code for completeness and quality |
| `/security-scanning-hooks` | Setup automated security scanning in CI/CD |

---

**End of Test Plan**

This test plan provides comprehensive coverage for all 7 Epics of the InformatiK-AI Studio project, with specific focus on the technology stack (Next.js 15, Supabase, Monaco, AI providers) and critical security requirements (API key handling, sandboxed code execution, authentication).
