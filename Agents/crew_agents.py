import sys
sys.path.append("../")
import llm.gemini_pro as gemini_pro
import tools.search as search

from crewai import Agent

researcher = Agent(
  role='Senior indian stock-market Research Analyst',
  goal='Uncover cutting-edge Daily indian stock Trends',
  backstory="""You work at a leading indian stock-market Organisation.
  Your expertise lies in identifying emerging trends like when to buy or sel and at what price.
  You have a knack for dissecting complex data and presenting
  actionable insights.""",
  verbose=True,
  allow_delegation=False,
  llm = gemini_pro.llm,  #\using google gemini pro API
  tools=[
        search.search_tool
      ]
)


writer = Agent(
  role='Finance and indian stock-market Content Strategist',
  goal='Craft compelling content on indian stock-market and latest news',
  backstory="""You are most profitable trader and read new related to finance everyday.""",
  verbose=True,
  allow_delegation=False,
  llm = gemini_pro.llm,  #using google gemini pro API
  tools=[
    search.search_tool
  ]
)