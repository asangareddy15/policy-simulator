import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
gemini_api_key = os.getenv("API_KEY")

genai.configure(api_key=gemini_api_key)


model = genai.GenerativeModel('gemini-2.5-flash')


def simulate_policy_scenario(policy, scenario):
    """Uses Gemini to simulate a policy scenario."""
    prompt = f"""
    Simulate the impacts of the following policy in this scenario:
    Policy: {policy}
    Scenario: {scenario}

    Provide a balanced analysis including:
    - Potential positive outcomes
    - Potential negative outcomes
    - Key stakeholders affected
    - Recommendations
    """

    response = model.generate_content(prompt)
    return response.text


# Main command-line loop
if __name__ == "__main__":
    print("Welcome to Policy Scenario Simulator Agent!")
    while True:
        policy = input("Enter a policy (or 'quit' to exit): ")
        if policy.lower() == 'quit':
            break
        scenario = input("Enter a scenario: ")
        result = simulate_policy_scenario(policy, scenario)
        print("\nSimulation Result:\n")
        print(result)
        print("\n---\n")

with open("results/simulations.txt", "a") as f:
    f.write(f"Policy: {policy}\nScenario: {scenario}\nResult:\n{result}\n---\n")
print("Simulation saved to results/simulations.txt")