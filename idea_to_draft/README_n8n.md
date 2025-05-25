# Idea to Post Generation Workflow

## Overview

This n8n workflow automates the process of transforming a simple content idea into a polished, publication-ready draft for Substack. The workflow leverages multiple AI models for different stages of content creation, mimicking a professional content production team with specialized roles.

## Workflow Architecture

![Workflow Diagram](workflow.png)

### Process Flow

1. **Input**: User submits a content idea through a chat interface
2. **Research**: Perplexity AI generates a comprehensive essay based on the idea
3. **Editorial Review**: Claude AI reviews the essay and provides editorial feedback
4. **Content Refinement**: Gemini AI implements the editorial suggestions
5. **Output**: Final draft is saved to Google Docs

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

1. **OpenRouter API**
   - Used by: All AI model nodes

2. **Google Docs OAuth2**
   - Used by: Google Docs nodes

## Configuration

### Chat Trigger

- Type: `@n8n/n8n-nodes-langchain.chatTrigger`
- Purpose: Entry point for user to submit content ideas
- Webhook ID: `bd5cbd88-9403-46ca-88b6-56257a3c6cee`

### AI Model Nodes

- **Perplexity Research**
  - Model: perplexity/sonar-deep-research
  - Task: Generate initial research and essay
  - Prompt: Write an essay about `{{ $json.chatInput }}`

- **Claude Revision**
  - Model: anthropic/claude-sonnet-4
  - Task: Produce an editorial review of the research
  - Prompt: Write an editorial revision of the text below. I will review your feedback and edit the text to make it ready to post on Substack. `{{ $json.output }}`

- **Gemini Drafting**
  - Model: google/gemini-2.5-pro-preview
  - Task: Generate final draft by combining the reseach results with the editorial review feedback
  - Prompt: I have attached both my original essay and the editorial review by a colleague. Implement the editorial review so the text is ready to publish on Substack. P.S. I am happy for the output to be multiple posts as suggested by the editor if you agree with the need for it. ### Original Essay `{{ $('Perplexity Research').item.json.output }}` ### Editorial Review `{{ $('Claude Revision').item.json.output }}`

### Google Docs Integration

- **Create New Doc Empty**
  - Create a blank Google Doc to write into
  - Document naming convention: `Draft YYYY-MM-DD HH-MM-SS`

- **Save Draft in Doc**
  - Operation: Update document with final content from Gemini

## Output

- Google Doc with the final draft produced by the AI models in this workflow, ready for human review.
- The Doc will include any additional from Gemini from the revisions it did over the original draft by Perplexity. This is good to see the changes and the context of the original draft.

## Pre-Requisites
- n8n Account
- OpenRouter API Key
- Google Docs Project
    - Google Docs API Enabled
    - n8n's callback URL whitelisted (https://oauth.n8n.cloud/oauth2/callback)

## Usage Instructions

1. Access the n8n workflow dashboard
2. Import the JSON workflow
3. Configure the credentials for OpenRouter and Google Docs (these nodes will have an error icon in the workflow)
4. Locate and activate the "Idea to Post Generation" workflow
5. Use the chat interface to submit your content idea
6. Wait for the workflow to process (typically takes 2-5 minutes depending on content length)
7. Access your Google Drive folder to view the final document

## Troubleshooting

- **API Rate Limits**: If the workflow fails, check OpenRouter API usage limits
- **Authentication Errors**: Verify Google OAuth2 credentials are valid and have proper permissions
- **Missing Output**: Ensure the Google Drive folder ID is correct and accessible

## Maintenance

- **API Keys**: Rotate OpenRouter API keys periodically for security
- **OAuth Tokens**: Refresh Google OAuth2 tokens if they expire
- **Model Updates**: Check for newer AI models periodically to improve output quality

## Costs
The costs below are the highest costs paid during personal tests:

- Perplexity Sonar Deep Research: ~$1.5 for 131k tokens output
- Claude Sonnet 4: ~$0.03 for 1.5k tokens output
- Gemini 2.5 Pro: ~$0.07 for 6k tokens outputs