import streamlit as st
from crewai import Task, Crew
import Agents.crew_agents as agents
import datetime



# Create tasks for your agents
task1 = Task(
    description="""Conduct a comprehensive analysis of {Topic} share price up to date in 2024 for """ + str(datetime.datetime.now()) +""". You can use new website like https://www.moneycontrol.com/, https://www.businesstoday.in/, https://www.livemint.com/ and https://www.indiainfoline.com/,https://www.livehindustan.com/
    Identify key trends and follow latest news. Provide actionable insights.
    Your final answer MUST be a full indian stock analysis report""",
    agent=agents.researcher
)

task2 = Task(
    description="""Conduct a thorough analysis of the stock's financial
        health and market performance. 
        This includes examining key financial metrics such as
        P/E ratio, EPS growth, revenue trends, and 
        debt-to-equity ratio. 
        Also, analyze the {Topic} stock's performance in comparison 
        to its industry peers and overall market trends in 2024 for """ + str(datetime.datetime.now()) + """. You can use new website like https://www.moneycontrol.com/, https://www.businesstoday.in/, https://www.livemint.com/ and https://www.indiainfoline.com/,https://www.livehindustan.com/
        

        Your final report MUST expand on the summary provided
        but now including a clear assessment of the stock's
        financial standing, its strengths and weaknesses, 
        and how it fares against its competitors in the current
        market scenario.

        Make sure to use the most recent data possible.""",
    agent=agents.Finance_Analyst
)

task3 = Task(description=f"""
        Review and synthesize the analyses provided by the
        Financial Analyst and the Research Analyst.
        Combine these insights to form a comprehensive
        investment recommendation. 
        
        You MUST Consider all aspects, including financial
        health, market sentiment, and qualitative data from
        EDGAR filings.

        Make sure to include a section that shows insider 
        trading activity, and upcoming events like earnings.

        Your final answer MUST be a recommendation for your
        customer. It should be a full super detailed report, providing a 
        clear investment stance and strategy with supporting evidence.
        Make it pretty and well formatted for your customer.
      """,
      agent=agents.Advisor)


# Instantiate your crew with a sequential process
crew = Crew(
    agents=[agents.researcher, agents.Finance_Analyst, agents.Advisor],
    tasks=[task1, task2, task3],
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

