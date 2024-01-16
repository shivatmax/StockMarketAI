import streamlit as st
from crewai import Task, Crew
import Agents.crew_agents as agents



# Create tasks for your agents
task1 = Task(
    description="""Conduct a comprehensive analysis of {Topic} share price up to date in 2024.
    Identify key trends and follow latest news. Provide actionable insights.
    Your final answer MUST be a full indian stock analysis report""",
    agent=agents.researcher
)

task2 = Task(
    description="""Using the insights provided, develop an engaging blog
    post that highlights that should i buy or sell {Topic} share.
    Your post should be informative yet accessible, catering to a indian stock market audience.
    Make it with statistics, numbers and graphs.
    Format: - Introduction(About company) - Body[all with graphs and statistical numbers][promoter percentage,individual investor percentage,past 1 year high, past 1 year low, 1 month high, 1 month low, 1 day high, 1 day low, volume, positive report, negtive report,good news,bad news target price, stop loss price] - Conclusion[buy or sell]""",
    agent=agents.writer
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[agents.researcher, agents.writer],
    tasks=[task1, task2],
    verbose=2,  # You can set it to 1 or 2 for different logging levels
)
st.title("AI Stock Market Blog Writer")
st.write("Welcome to the AI Stock Blog Writer!")
# Get user input for the topic
topic = st.text_input("Enter the topic:")

# Check if the topic is provided
if topic:
    # Update the task descriptions with the user-provided topic
    task1.description = task1.description.format(Topic=topic)
    task2.description = task2.description.format(Topic=topic)
    if st.button("Generate stock Blog"): 
       result = crew.kickoff()
       st.subheader("Market Result")
       st.write(result)
else:
    st.write("Please enter a topic to start the CrewAI tasks.")

