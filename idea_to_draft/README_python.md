# Idea to Post Generation Workflow (Python)

## Overview

This Python script automates the process of transforming a simple content idea into a polished, publication-ready draft for Substack. The workflow leverages multiple AI models for different stages of content creation, mimicking a professional content production team with specialized roles.

## Workflow Architecture

### Process Flow

1. **Input**: User submits a content idea through command-line arguments
2. **Research**: Perplexity AI generates a comprehensive essay based on the idea
3. **Editorial Review**: Claude AI reviews the essay and provides editorial feedback
4. **Content Refinement**: Gemini AI implements the editorial suggestions
5. **Output**: Final draft is saved to Google Docs and a local Markdown file

## Dependencies

### External Services

| Service | Purpose | Configuration |
|---------|---------|---------------|
| OpenRouter | API gateway for accessing multiple AI models | API key required |
| Google Docs | Document storage for final drafts | OAuth2 authentication required |
| Google Drive | Storage location for Google Docs | Shared folder access required |

### AI Models (via OpenRouter)

| Model | Provider | Purpose |
|-------|----------|---------|
| Sonar Deep Research | Perplexity | Initial research and essay generation |
| Claude Sonnet 4 | Anthropic | Editorial review and feedback |
| Gemini 2.5 Pro | Google | Final draft implementation |

## Required Credentials
These must be set in a `.env` file in the same folder as the Python script.

* OPENROUTER_API_KEY: API key for OpenRouter
* GOOGLE_DRIVE_FOLDER_ID: ID of the Google Drive folder for document storage
* GOOGLE_CLIENT_ID: Client ID for Google Authentication
* GOOGLE_PROJECT_ID: Project ID for Google Authentication
* GOOGLE_CLIENT_SECRET: Client secret for Google Authentication


## Configuration

### Command Line Arguments

```
python idea_to_draft_automation.py --idea "your content idea here"
```

If no idea is provided, a default idea will be used.

### Environment Variables (.env)

```
OPENROUTER_API_KEY=your_openrouter_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_PROJECT_ID=your_google_project_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id
```

### Key Components

- **OpenRouterClient**
  - Purpose: Generic client for accessing various AI models through OpenRouter
  - Key method: `generate_completion()` - Generates text completions from specified models

- **ContentGenerator**
  - Purpose: Handles content generation using various AI models
  - Key methods:
    - `generate_research_essay()` - Uses Perplexity to create initial research
    - `generate_editorial_review()` - Uses Claude to review the essay
    - `generate_final_draft()` - Uses Gemini to implement editorial suggestions

- **GoogleDocsManager**
  - Purpose: Handles Google Docs operations
  - Key methods:
    - `create_empty_doc()` - Creates a new Google Doc
    - `update_doc_content()` - Updates a Google Doc with content

- **WorkflowOrchestrator**
  - Purpose: Orchestrates the entire workflow
  - Key method: `run_workflow()` - Executes the complete content generation process

## Output

- Google Doc with the final draft produced by the AI models, ready for human review
- Local Markdown file with the final draft (as a backup)
- The Google Doc includes the final draft produced by Gemini based on the original research by Perplexity and editorial feedback from Claude

## Pre-Requisites
- Python 3.7+
- Required Python packages (install via `pip install -r requirements.txt`):
  - requests
  - python-dotenv
  - google-api-python-client
  - google-auth-oauthlib
  - google-auth-httplib2
- OpenRouter API Key
- Google Cloud Project with Google Docs API enabled

## Usage Instructions

1. Clone the repository
2. Create a `.env` file with the required credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Run the script: `python idea_to_draft_automation.py --idea "your content idea here"`
5. Follow the Google authentication flow if prompted
6. Access your Google Drive folder to view the final document

## Troubleshooting

- **API Rate Limits**: If the workflow fails, check OpenRouter API usage limits
- **Authentication Errors**: Verify Google OAuth2 credentials are valid and have proper permissions
- **Missing Output**: Ensure the Google Drive folder ID is correct and accessible
- **Google Authentication**: If authentication fails, delete the `token.json` file and try again

## Maintenance

- **API Keys**: Rotate OpenRouter API keys periodically for security
- **OAuth Tokens**: The script will automatically refresh Google OAuth2 tokens if they expire
- **Model Updates**: Check for newer AI models periodically to improve output quality

## Costs
The costs below are approximate and may vary based on token usage:

- Perplexity Sonar Deep Research: ~$1.5 for 131k tokens output
- Claude Sonnet 4: ~$0.03 for 1.5k tokens output
- Gemini 2.5 Pro: ~$0.07 for 6k tokens outputs
