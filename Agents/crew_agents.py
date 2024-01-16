import datetime
import sys
sys.path.append("../")
import llm.gemini_pro as gemini_pro
import tools.search as search
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from newsapi import NewsApiClient

from crewai import Agent

Finance_Analyst = Agent(
  role='The Best Indian Financial Analyst',
  goal="""Impress all customers with your financial data 
      and Indian market trends analysis auto date in 2024 for """+str(datetime.datetime.now()),
  backstory="""The most seasoned financial analyst with 
      lots of expertise in stock market analysis and investment
      strategies that is working for a super important customer.""",
  verbose=True,
  llm = gemini_pro.llm,  #using google gemini pro API
  tools=[
    search.search_tool,
  ]
)
researcher = Agent(
      role='Staff Indian Research Analyst',
      goal="""Being the best at gather, interpret data and amaze
      your customer with it relevant in 2024 for """ + str(datetime.datetime.now())+""". You can use new website like https://www.moneycontrol.com/, https://www.businesstoday.in/, https://www.livemint.com/ and https://www.indiainfoline.com/,https://www.livehindustan.com/""",
      backstory="""Known as the BEST research analyst, you're
      skilled in sifting through Indian news, Indian company announcements, 
      and Indian market sentiments. Now you're working on a super 
      important customer""",
      verbose=True,
      llm = gemini_pro.llm,
      tools=[
        search.search_tool,
        # YahooFinanceNewsTool(),
      ]
  )

Advisor=Agent(
      role='Private Investment Advisor',
      goal="""Impress your customers with full analyses over Indian stocks
      and completer investment recommendations updo data in 2024 for """ + str(datetime.datetime.now()),
      backstory="""You're the most experienced investment advisor
      and you combine various analytical insights to formulate
      strategic investment advice. You are now working for
      a super important customer you need to impress.""",
      verbose=True,
      llm = gemini_pro.llm,
      tools=[
        search.search_tool,
        # YahooFinanceNewsTool()
      ]
    )