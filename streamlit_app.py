# streamlit_app.py
import os
import openai
import streamlit as st
from dotenv import load_dotenv

# Load OpenAI API key from environment
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load prompts from files
def load_prompt(agent_name):
    try:
        with open(f"prompts/{agent_name}_prompt.md", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Prompt not found."

# Route query to correct agent
def route_agent(query):
    q = query.lower()
    if any(k in q for k in ["wage", "termination", "overtime", "employment", "leave"]):
        return "LaborLawAgent"
    elif any(k in q for k in ["discrimination", "harassment", "disability", "human rights"]):
        return "HumanRightsAgent"
    elif any(k in q for k in ["helmet", "safety", "injury", "ppe", "hazard"]):
        return "SafetyAgent"
    else:
        return "BingSearchTool"

# Ask OpenAI GPT-4
def ask_openai(prompt, query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Contoso HR Copilot")
st.title("🤖 Contoso HR Copilot")
st.markdown("Ask compliance questions about labor laws, human rights, and workplace safety.")

user_query = st.text_input("🔍 Your question:")

if user_query:
    agent = route_agent(user_query)
    
    if agent == "BingSearchTool":
        st.info("This may be a recent issue. Please verify via official sites or search below.")
        st.markdown(f"[🔗 Bing Search](https://www.bing.com/search?q={user_query.replace(' ', '+')})")

