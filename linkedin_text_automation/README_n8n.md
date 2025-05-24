# n8n LinkedIn Content Automation Workflow

## Overview
This repository contains an n8n workflow designed to automate the research, creation, and distribution of LinkedIn posts focused on marketing use cases for n8n and AI. The workflow leverages multiple data sources, AI models, and human oversight to generate high-quality content.

## Workflow Architecture

```
Trigger → Research Collection → AI Analysis → Content Generation → Human Review → Storage
```

### Key Components

1. **Data Collection**
   - YouTube videos and transcripts via Apify API
   - Twitter/X content via Apify API

2. **AI Processing**
   - Research synthesis using Claude 3.7 Sonnet
   - Content generation using Perplexity Sonar
   - Structured output formatting

3. **Human Oversight**
   - Review and approval step before distribution
   - Quality control checkpoint

4. **Output**
   - Google Drive storage of finalized LinkedIn posts
   - Structured document formatting

## Setup Requirements

### API Keys
To use this workflow, you'll need to configure the following API keys:
- Apify API key (for YouTube and Twitter scraping)
- OpenRouter API key (for AI models)
- Google Drive API credentials

### n8n Configuration
1. Import the `n8n_workflow.json` file into your n8n instance
2. Configure the necessary credentials
3. Update API keys in the HTTP Request nodes
4. Set the Google Drive folder ID to your preferred destination

## Usage

1. Trigger the workflow via the webhook or chat interface
2. Monitor the research collection process
3. Review the AI-generated content when prompted
4. Approve or reject the content for distribution
5. Access the final LinkedIn posts in the specified Google Drive folder

## Workflow Details

For a complete step-by-step breakdown of the workflow, refer to the detailed documentation file.

## Customization

The workflow can be customized by:
- Modifying search queries in the YouTube and Twitter nodes
- Adjusting the AI prompts for different content styles
- Changing the output format in the Code nodes
- Updating the Google Drive destination

## Maintenance

- Regularly check API endpoints for changes
- Update AI model selections as new models become available
- Review and refine prompts to maintain content quality

## License

[Your license information here]
