from dotenv import load_dotenv
import os
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()
gemini_api_key = os.getenv("API_KEY")

genai.configure(api_key=gemini_api_key)


model = genai.GenerativeModel('gemini-2.5-flash')


def simulate_policy_scenario(policy_context, scenario):
    """Uses Gemini to simulate a policy scenario with extracted context."""
    if not policy_context or not scenario:
        return "Error: Policy context and scenario cannot be empty."
    prompt = f"""
    Based on the following policy context:
    {policy_context}

    Simulate the impacts in this scenario:
    Scenario: {scenario}

    Provide a balanced analysis including:
    - Potential positive outcomes
    - Potential negative outcomes
    - Key stakeholders affected
    - Recommendations
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}. Please check your API key or try again."


if __name__ == "__main__":
    print("Welcome to Policy Scenario Simulator Agent!")
    while True:
        choice = input(
            "Enter '1' for manual policy input, '2' for PDF file, '3' for URL (YouTube or webpage) (or 'quit' to exit): ")
        if choice.lower() == 'quit':
            break
        policy_context = ""
        if choice == '1':
            policy_context = input("Enter the policy: ")
        elif choice == '2':
            pdf_path = input("Enter the local PDF file path: ")
            try:
                reader = PdfReader(pdf_path)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() or ''
                policy_context = text[:5000]  # Limit length
            except Exception as e:
                print(f"Error extracting from PDF: {str(e)}")
                continue
        elif choice == '3':
            url = input("Enter the URL: ")
            url_type = input("Enter type ('youtube' or 'webpage'): ").lower()
            try:
                if url_type == 'youtube':
                    video_id = url.split('v=')[-1].split('&')[0]
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    policy_context = ' '.join([entry['text'] for entry in transcript])[:5000]
                elif url_type == 'webpage':
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    policy_context = ' '.join([p.text for p in soup.find_all('p')])[:5000]
                else:
                    print("Invalid URL type. Choose 'youtube' or 'webpage'.")
                    continue
            except Exception as e:
                print(f"Error extracting from URL: {str(e)}")
                continue
        else:
            print("Invalid choice. Please enter '1', '2', '3', or 'quit'.")
            continue

        if policy_context:
            print("\nExtracted Policy Context Preview:\n")
            print(policy_context[:500])  # Show preview
        scenario = input("Enter a scenario: ")
        result = simulate_policy_scenario(policy_context, scenario)
        print("\nSimulation Result:\n")
        print(result)
        print("\n---\n")