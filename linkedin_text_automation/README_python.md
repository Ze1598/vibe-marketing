# Python LinkedIn Content Automation Script

## Overview
This repository contains a Python script that replicates the n8n workflow functionality for automating the research, creation, and distribution of LinkedIn posts focused on marketing use cases for n8n and AI. The script leverages multiple data sources, AI models, and human oversight to generate high-quality content.

## Workflow Architecture

```
Data Collection → Content Processing → AI Research → Content Generation → Human Review → Google Drive Upload
```

### Key Components

1. **Data Collection**
   - YouTube videos and transcripts via Apify API
   - Twitter/X content via Apify API
   - Implemented in the `APIClient` class

2. **AI Processing**
   - Research synthesis using Claude 3.7 Sonnet
   - Content generation using Perplexity Sonar
   - Structured output formatting
   - Implemented in the `AIProcessor` class

3. **Human Oversight**
   - Interactive review and approval step before distribution
   - Quality control checkpoint
   - Implemented in the `HumanReview` class
   - Can be bypassed with `--skip-review` flag

4. **Output**
   - Google Drive storage of finalized LinkedIn posts
   - Structured document formatting
   - Implemented in the `GoogleDriveUploader` class

## Setup Requirements

### Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### API Keys
To use this script, you'll need to configure the following API keys:
- Apify API key (for YouTube and Twitter scraping)
- OpenRouter API key (for AI models)
- Google Drive API credentials

Set these as environment variables or modify the CONFIG dictionary in the script:
```bash
export APIFY_API_KEY="your_apify_api_key"
export OPENROUTER_API_KEY="your_openrouter_api_key"
export GOOGLE_DRIVE_FOLDER_ID="your_folder_id"
```

### Google Drive Setup
1. Create a project in the Google Cloud Console
2. Enable the Google Drive API
3. Create OAuth 2.0 credentials
4. Download the credentials as `credentials.json` and place in the same directory as the script

## Usage

### Basic Usage
Run the script with default settings:
```bash
python linkedin_content_automation.py
```

### Skip Human Review
To bypass the human review step:
```bash
python linkedin_content_automation.py --skip-review
```

### Configuration
Edit the CONFIG dictionary in the script to customize:
- Search queries for YouTube
- Twitter username to scrape
- Maximum number of results to process
- Google Drive folder ID for output

## Script Structure

The script is organized into modular classes:

1. **APIClient**: Handles API requests to external services
2. **ContentProcessor**: Processes and transforms content from various sources
3. **AIProcessor**: Handles AI processing using OpenRouter API
4. **DocumentFormatter**: Formats content for Google Docs
5. **GoogleDriveUploader**: Handles uploading content to Google Drive
6. **HumanReview**: Handles human review of generated content
7. **WorkflowOrchestrator**: Orchestrates the entire workflow

## Customization

The script can be customized by:
- Modifying search queries and parameters in the CONFIG dictionary
- Adjusting AI prompts in the AIProcessor class
- Changing the output format in the DocumentFormatter class
- Extending the WorkflowOrchestrator to add additional steps

## Maintenance

- Regularly check API endpoints for changes
- Update AI model selections as new models become available
- Review and refine prompts to maintain content quality
