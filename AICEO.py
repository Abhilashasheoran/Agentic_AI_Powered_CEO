# ai_ceo_app.py

import os
import streamlit as st
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool as LangchainTool

# 🧠 1. Set your Gemini API Key here (REQUIRED)
os.environ["GOOGLE_API_KEY"] = "your-gemini-api-key"  # 🔑 Replace this

# 🧠 2. Load Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key="AIzaSyBooWQhuxQJOWA5JGKF_SQceLi9mGczM",
    convert_system_message_to_human=True,
    temperature=0.5
)

# 🛠 3. Define simulated tools
def simulate_gmail_action(input: str) -> str:
    return f"📧 (Simulated) Sent email with content: {input}"

def simulate_calendar_event(input: str) -> str:
    return f"📅 (Simulated) Scheduled calendar event: {input}"

def simulate_slack_post(input: str) -> str:
    return f"💬 (Simulated) Posted to Slack: {input}"

def simulate_notion_update(input: str) -> str:
    return f"📘 (Simulated) Updated Notion database with: {input}"

def simulate_web_search(input: str) -> str:
    return f"🔍 (Simulated) Searched the web for: '{input}' and found relevant results."

# 🔧 4. Wrap tools
tools = [
    LangchainTool(name="SendEmail", func=simulate_gmail_action, description="Simulate sending an email"),
    LangchainTool(name="ScheduleEvent", func=simulate_calendar_event, description="Simulate scheduling event"),
    LangchainTool(name="PostToSlack", func=simulate_slack_post, description="Simulate posting to Slack"),
    LangchainTool(name="UpdateNotion", func=simulate_notion_update, description="Simulate updating Notion"),
    LangchainTool(name="WebSearch", func=simulate_web_search, description="Simulate searching the web"),
]

# 🤖 5. Initialize agent
agent = create_react_agent(llm, tools)

# 🎨 6. Streamlit UI
st.set_page_config(page_title="🧠 AI CEO Agent", page_icon="🤖")
st.title("🤖 AI-Powered CEO Assistant")
st.markdown("Type a command for your AI CEO. For example:")
st.code("Schedule team meeting, send email to dev team, and post reminder to Slack.")

user_input = st.text_area("📥 Enter your instruction", height=150)

if st.button("▶️ Run AI CEO Agent"):
    if not user_input.strip():
        st.warning("Please enter a valid instruction.")
    else:
        with st.spinner("AI CEO is processing..."):
            input_message = {"role": "user", "content": user_input}
            result = ""
            for step in agent.stream({"messages": [input_message]}, stream_mode="values"):
                last_message = step["messages"][-1]
                result += f"\n✅ {last_message.content}\n"
            st.success("Done!")
            st.markdown("### 📤 Output")
            st.code(result.strip())
