import os
import shutil
import time
import streamlit as st
from crewai import Task, Crew
import Agents.crew_agents as agents
import datetime
from clear_pycache import clear_pycache
import tools.bingimage as bi
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Add image to Streamlit app
image_path = "images/stock4-remove.png"
st.image(image_path, use_column_width=True, caption="Stocky AI", width=500)

# Add custom CSS styles
st.markdown(
    """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #FFCCCC;
    }
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .title {
        font-size: 36px;
        color: #3366ff;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 24px;
        color: #666666;
        margin-bottom: 10px;
    }
    .button {
        background-color: #3366ff;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create tasks for your agents
task2 = Task(
    description="""Conduct a thorough analysis of the {Topic} share price up to """
    + str(datetime.datetime.now().date())
    + """. 
        This includes examining key financial metrics such as
        P/E ratio, EPS growth, revenue trends, and 
        debt-to-equity ratio. 
        
        Also, analyze the stock's performance in comparison 
        to its industry peers and overall market trends in india.

        Your final report MUST expand on the summary provided
        but now including a clear assessment of the stock's
        financial standing, its strengths and weaknesses, 
        and how it fares against its competitors in the current
        market scenario in india.
        
        Also make sure to return the All Stock information.

        Make sure to use the most recent data possible.
      """,
    agent=agents.Finance_Analyst,
)

task1 = Task(
    description="""Collect and summarize recent news articles, press
        releases, and market analyses related to the {Topic} stock price in india and
        its industry to the date """
    + str(datetime.datetime.now().date())
    + """.You can use new website like https://www.moneycontrol.com/, https://www.businesstoday.in/, https://www.livemint.com/ and https://www.indiainfoline.com/,https://www.livehindustan.com/
        Pay special attention to any significant events, market
        sentiments, and analysts' opinions. Also include upcoming 
        events like earnings and others.
  
        Your final answer MUST be a report that includes a
        comprehensive summary of the latest news, any notable
        shifts in indian market sentiment, and potential impacts on 
        the stock.
        
        Also make sure to return the All Stock information.
        
        Make sure to use the most recent data possible.""",
    agent=agents.Finance_researcher,
)


task3 = Task(
    description=f"""
        Review and synthesize the analyses provided by the
        Financial Analyst and the Research Analyst.
        Combine these insights to form a comprehensive
        investment recommendation. 
        
        You MUST Consider all aspects, including Recent News,Upcoming Events,Potential Impacts on the Stock,Key financial
        health and metrics, market sentiment, and qualitative data from
        EDGAR filings with statistics, percentages, prices and numbers.
       
        YOU MUST ADD new line charater '\ n' to the end of every full stop '.'
       
        Make sure to include a section that shows insider 
        trading activity, and upcoming events like earnings.
        
        YOU MUST ADD new line charater '\ n' to the end of every full stop '.'

        Your final answer MUST be a recommendation with rating out of 10 for your
        customer.
        It should be a full super detailed report, providing a 
        clear investment stance and strategy with supporting evidence.
        
        YOU MUST ADD new line charater '\ n' to the end of every full stop '.'
        
        Your Final Answer MUST be a detailed report with bullet points that includes all aspects, including Recent News, 
        Negative News, Positive News, Upcoming Events, Potential Impacts on the Stock, Key financial
        health and metrics, market sentiment, and qualitative data with statistics, percentages, prices and numbers.
        
        Make it pretty and well formatted for your customer.
        
        YOU MUST ADD new line charater '\ n' to the end of every full stop '.'
      """,
    agent=agents.investment_Advisor,
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[
        agents.Finance_Analyst,
        agents.Finance_researcher,
        agents.investment_Advisor,
    ],
    tasks=[task1, task2, task3],
    verbose=False,  # You can set it to 1 or 2 for different logging levels
)

# Add custom styling to the app
st.markdown("<h1 class='title'>Stocky AI!!</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Hi !! I'm Stocky, the AI Stock Researcher and Analyst! 😄</p>", unsafe_allow_html=True)

# Get user input for the topic
topic = st.text_input("Enter the Name of Company")

# Check if the topic is provided
if topic:
    logo = bi.CompanyLogo(topic)
    company_logo = str(logo)

    time.sleep(1)

    # Update the task descriptions with the user-provided topic
    task1.description = task1.description.format(Topic=topic)
    task2.description = task2.description.format(Topic=topic)

    col1, col2, col3 = st.columns([1, 0.5, 1])
    with col1:
        st.image(company_logo, caption=topic + " Company", width=200)
    with col2:
        st.write("")
    with col3:
        st.write("")
        st.write("")
        a = st.button(f"Generate {topic} stock report", key="generate_report")
        st.write("")
        # 
    if a:
        with st.spinner(f"Generating {topic} stock report..."):
            result = crew.kickoff()

            st.markdown("<h2 class='subtitle'>Stock Report</h2>", unsafe_allow_html=True)
            t1 = result.replace("**", " ")
            text1 = t1.replace(" *", "•")
            st.write(text1)
            time.sleep(2)

            print(text1)

            # Create a PDF canvas
            from reportlab.lib.units import inch
            c = canvas.Canvas(f"{topic}_stock_report.pdf", pagesize=letter)
            c.setPageSize((15 * inch, 11.7 * inch))

            w, h = letter
            c.drawImage(company_logo, x=100, y=h - 50, width=100, height=75)

            # Write the result text below the company logo
            c.setFont("Helvetica", 8)
            text = c.beginText(20, h - 60)
            text.textLines(str(text1))
            c.drawText(text)
            c.showPage()
            # Save and close the PDF canvas
            c.save()

            def openfile(topic):
                with open(f"{topic}_stock_report.pdf", "rb") as file:
                    return file.read()

            # Provide a download button for the PDF file
            st.download_button(
                label="Download Stock Report",
                data=openfile(topic),
                file_name=f"{topic}_stock_report.pdf",
                mime="application/pdf"
            )

            def clear_images_folder():
                folder_path = "images/company"
                shutil.rmtree(folder_path)

            clear_images_folder()
            time.sleep(10)
            os.remove(f"{topic}_stock_report.pdf")
            clear_pycache()
else:
    st.write("Please enter a Company Name to generate a stock report. Like Tata Motors")
