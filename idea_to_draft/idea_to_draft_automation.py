import os
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime
import argparse
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload

# Parse command line arguments at the global scope
parser = argparse.ArgumentParser(description='Idea to Draft Automation')
parser.add_argument('--idea', type=str, help='The idea to generate content from')

# Parse arguments and make them available as global variables
args = parser.parse_args()
RESEARCH_IDEA = args.idea

if not RESEARCH_IDEA:
    RESEARCH_IDEA = "japanese sports manga as a medium to discuss deep psychological topics in a more accessible format"

# Load environment variables from .env file
load_dotenv()

# Configuration - Replace with your actual API keys and credentials
CONFIG = {
    "openrouter_api_key": os.environ.get("OPENROUTER_API_KEY"),
    "google_drive_folder_id": os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
}

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/docs']


class OpenRouterClient:
    """Generic OpenRouter API client for accessing various AI models"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def generate_completion(self, 
                           model: str, 
                           system_prompt: str, 
                           user_prompt: str, 
                           temperature: float = 0.7,
                           max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate a completion using the specified model
        
        Args:
            model: The OpenRouter model identifier
            system_prompt: The system prompt to set context
            user_prompt: The user prompt containing the main request
            temperature: Controls randomness (0-1)
            max_tokens: Maximum tokens to generate (optional)
            
        Returns:
            Dictionary containing the response or error information
        """
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
            
        try:
            response = requests.post(self.base_url, json=payload, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            return {
                "success": True,
                "content": content,
                "model": model,
                "raw_response": result
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error calling OpenRouter API: {str(e)}"
            if hasattr(e, 'response') and e.response:
                error_msg += f" - Status code: {e.response.status_code}"
                error_msg += f" - Response: {e.response.text}"
                
            print(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "content": "",
                "model": model
            }


class ContentGenerator:
    """Handles content generation using various AI models"""
    
    def __init__(self, openrouter_client: OpenRouterClient):
        self.client = openrouter_client
        
    def generate_research_essay(self, idea: str) -> Dict[str, Any]:
        """Generate a research essay using Perplexity Sonar Deep Research"""
        system_prompt = "You are a professional researcher and writer specializing in creating comprehensive, well-structured essays."
        
        user_prompt = f"""
        Write an essay about {idea}
        
        Please create a comprehensive, well-researched essay that explores this topic in depth.
        Include relevant facts, analysis, and insights.
        Structure the essay with clear sections and a logical flow.
        """
        
        response = self.client.generate_completion(
            model="perplexity/sonar-deep-research",
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.7
        )
        
        return {
            "success": response["success"],
            "research_essay": response["content"],
            "timestamp": datetime.now().isoformat()
        }
        
    def generate_editorial_review(self, essay_content: str) -> Dict[str, Any]:
        """Generate an editorial review using Claude Sonnet"""
        system_prompt = "You are an experienced editor for Substack publications. Your job is to provide constructive feedback on essays to make them publication-ready."
        
        user_prompt = f"""
        Write an editorial revision of the text below. I will review your feedback and edit the text to make it ready to post on Substack.

        {essay_content}
        """
        
        response = self.client.generate_completion(
            model="anthropic/claude-sonnet-4",
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.5
        )
        
        return {
            "success": response["success"],
            "editorial_review": response["content"],
            "timestamp": datetime.now().isoformat()
        }
        
    def generate_final_draft(self, essay_content: str, editorial_review: str) -> Dict[str, Any]:
        """Generate a final draft using Gemini Pro"""
        system_prompt = "You are a professional content writer who specializes in creating publication-ready content for Substack."
        
        user_prompt = f"""
        I have attached both my original essay and the editorial review by a colleague. Implement the editorial review so the text is ready to publish on Substack.

        P.S. I am happy for the output to be multiple posts as suggested by the editor if you agree with the need for it.


        ### Original Essay

        {essay_content}


        ### Editorial Review

        {editorial_review}
        """
        
        response = self.client.generate_completion(
            model="google/gemini-2.5-pro-preview",
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3
        )
        
        return {
            "success": response["success"],
            "final_draft": response["content"],
            "timestamp": datetime.now().isoformat()
        }


class GoogleDocsManager:
    """Handles Google Docs operations"""
    
    def __init__(self):
        self.credentials = self._get_credentials()
        if self.credentials:
            self.drive_service = build('drive', 'v3', credentials=self.credentials)
            self.docs_service = build('docs', 'v1', credentials=self.credentials)
        else:
            self.drive_service = None
            self.docs_service = None
        
    def _get_credentials(self) -> Optional[Credentials]:
        """Get or refresh Google API credentials"""
        # Allow insecure local host for development
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        
        # Define paths
        client_secrets_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client_secrets.json')
        token_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')
        
        # Check if client_secrets.json exists, if not, create it
        if not os.path.exists(client_secrets_file):
            print("client_secrets.json not found. Creating it from environment variables...")
            try:
                client_config = {
                    "installed": {
                        "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
                        "project_id": os.environ.get("GOOGLE_PROJECT_ID", ""),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
                        "redirect_uris": ["http://localhost"]
                    }
                }
                
                if not client_config["installed"]["client_id"] or not client_config["installed"]["client_secret"]:
                    print("Google OAuth credentials not found in environment variables.")
                    print("Please set GOOGLE_CLIENT_ID, GOOGLE_PROJECT_ID, and GOOGLE_CLIENT_SECRET in your .env file.")
                    print("Skipping Google Docs integration.")
                    return None
                
                with open(client_secrets_file, 'w') as f:
                    json.dump(client_config, f)
                print(f"Created client_secrets.json at {client_secrets_file}")
            except Exception as e:
                print(f"Error creating client_secrets.json: {e}")
                print("Skipping Google Docs integration.")
                return None
        
        # Check if token.json exists
        creds = None
        if os.path.exists(token_path):
            try:
                with open(token_path, 'r') as token_file:
                    creds = Credentials.from_authorized_user_info(json.load(token_file), SCOPES)
            except Exception as e:
                print(f"Error loading token.json: {e}")
                # Continue with authentication flow
        
        # If no valid credentials or they're expired, run the auth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing credentials: {e}")
                    # Continue with authentication flow
            else:
                try:
                    print("\nAuthenticating Google account...")
                    print("A browser window will open for authentication...")
                    
                    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                    creds = flow.run_local_server(port=8080)
                    
                    # Save the credentials for the next run
                    with open(token_path, 'w') as token:
                        token.write(creds.to_json())
                    print(f"Authentication successful. Token saved to {token_path}")
                except Exception as e:
                    print(f"Authentication failed: {e}")
                    print("Skipping Google Docs integration.")
                    return None
        
        return creds
    
    def create_empty_doc(self, title: str, folder_id: str) -> Dict[str, Any]:
        """Create an empty Google Doc in the specified folder"""
        if not self.drive_service:
            print("Google Drive service not initialized. Skipping document creation.")
            return {
                "success": False,
                "error": "Google Drive service not initialized"
            }
            
        try:
            file_metadata = {
                'name': title,
                'mimeType': 'application/vnd.google-apps.document',
                'parents': [folder_id]
            }
            
            file = self.drive_service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            return {
                "success": True,
                "doc_id": file.get('id'),
                "title": title
            }
            
        except Exception as e:
            print(f"Error creating Google Doc: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def update_doc_content(self, doc_id: str, content: str) -> Dict[str, Any]:
        """Update the content of a Google Doc"""
        if not self.docs_service:
            print("Google Docs service not initialized. Skipping document update.")
            return {
                "success": False,
                "error": "Google Docs service not initialized"
            }
            
        try:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1
                        },
                        'text': content
                    }
                }
            ]
            
            result = self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            return {
                "success": True,
                "doc_id": doc_id,
                "update_result": result
            }
            
        except Exception as e:
            print(f"Error updating Google Doc: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


class WorkflowOrchestrator:
    """Orchestrates the entire workflow"""
    
    def __init__(self):
        self.openrouter_client = OpenRouterClient(CONFIG["openrouter_api_key"])
        self.content_generator = ContentGenerator(self.openrouter_client)
        self.docs_manager = GoogleDocsManager()
    
    def run_workflow(self, idea_text: str) -> None:
        """Run the complete workflow"""
        print("Starting Idea to Draft automation workflow...")
        
        # 1. Generate research essay
        print("Generating research essay using Perplexity...")
        research_result = self.content_generator.generate_research_essay(idea_text)
        
        if not research_result["success"]:
            print("Failed to generate research essay. Workflow terminated.")
            return
            
        # 2. Generate editorial review
        print("Generating editorial review using Claude...")
        editorial_result = self.content_generator.generate_editorial_review(
            research_result["research_essay"]
        )
        
        if not editorial_result["success"]:
            print("Failed to generate editorial review. Workflow terminated.")
            return
            
        # 3. Generate final draft
        print("Generating final draft using Gemini...")
        draft_result = self.content_generator.generate_final_draft(
            research_result["research_essay"],
            editorial_result["editorial_review"]
        )
        
        if not draft_result["success"]:
            print("Failed to generate final draft. Workflow terminated.")
            return
            
        # 4. Combine all content for review
        combined_content = {
            "research_essay": research_result["research_essay"],
            "editorial_review": editorial_result["editorial_review"],
            "final_draft": draft_result["final_draft"]
        }
            
        # 5. Create Google Doc if Google Docs integration is available
        print("Creating Google Doc...")
        doc_result = self.docs_manager.create_empty_doc(
            f"Draft {datetime.now().strftime('%Y-%m-%d %H-%M-%S')}",
            CONFIG["google_drive_folder_id"]
        )
        
        print("Saving content to local file.")
        self._save_to_local_file(draft_result["final_draft"])
            
        # 6. Update Google Doc with content
        print("Saving draft to Google Doc...")
        update_result = self.docs_manager.update_doc_content(
            doc_result["doc_id"],
            draft_result["final_draft"]
        )
        
        if update_result["success"]:
            print(f"Workflow completed successfully!")
            print(f"Document created: https://docs.google.com/document/d/{doc_result['doc_id']}/edit")
    
    def _save_to_local_file(self, content: str) -> None:
        """Save content to a local file as fallback"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"draft_{timestamp}.md"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Content saved to local file: {filepath}")
        except Exception as e:
            print(f"Error saving to local file: {e}")


def main():
    """Main function to run the workflow"""
    orchestrator = WorkflowOrchestrator()
    orchestrator.run_workflow(RESEARCH_IDEA)


if __name__ == "__main__":
    main()
