import os
import time
import datetime
from crewai import Agent, Crew, Task
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class LotteryPicker():
    
    DATE_FORMAT="%m%d%Y-%H%M%S"
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-8b-8192" 
            #model="lama3-70b-8192"
            #model="mixtral-8x7b-32768"
            #model="gemma-7b-it"
            #model="whisper-large-v3"
        )
    
    def lottery_expert_agent(self):
        return Agent(
            role="Lottery Expert",
            goal=f"""
                Lottery expert goals:
                Understand the patterns and the relationship between numbers being picked together in a specific order.
                Consider the most picked numbers and how often they get picked, such as, based on past results patterns how long in a row they get picked or how long they don't get picked
                Analize the pattern of less picked numbers and how often they dont get picked, this can increase a chance of the number being picked in case of the number has not been picked for a long period]
                Apply the knowledge acquired and specify the number which are mostly like to be picked in a sequence                
                """,
            backstory="""
                You are a lottery expert who is a expert in mathematics, statistics and probabilities
                You are also a master in machine learning, AI who loves analize data (lottery results) to find patterns and relationship between numbers
                
                """,
            verbose=True,
            llm=self.llm
        )
    
    def result_search_task(self, agent, lottery, country):
        lottery_type=country + " " + lottery
        website=os.getenv(country.upper() + "_URL")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/{lottery_type}_strategy_{current_date_time}.txt"
        return Task(
            description=f"""
                Research to understand how {lottery_type} game works, how many winning numbers need to be picked including the supplementary number
                Research to ensure you understand how many winning numbers need to be picked per game and how many supplementary numbers to pick as well (if needed), there are lotteries such as Powerball that the supplementary number is included in the game
                You can use this website {website} to search and find all past lottery results from {lottery_type}, which the sequence number must be in the order it was picked.
                This will preserve the probability of the number being picked together in order.
                Understand the patterns and the relationship between numbers being picked together in a specific order.
                Consider the most picked numbers and how often they get picked, such as, based on past results patterns how long in a row they get picked or how long they don't get picked
                Analize the pattern of less picked numbers and how often they dont get picked, this can increase a chance of the number being picked in case of the number has not been picked for a long period]
                Apply the knowledge acquired and specify the number which are mostly like to be picked in a sequence  
                 """,
            agent=agent,
            output_file=output_file,
            expected_output=f"Find all past {lottery_type} results preserving its original picked number sequence.",
            callback=time.sleep(5)
        )
    
    def pick_sequence_task(self, agent, lottery, country, number_of_sequence):
        lottery_type=country + " " + lottery
        rules=os.getenv(lottery_type.upper() + "_RULES")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/{lottery_type}_winning_numbers_{current_date_time}.txt"
        return Task(
            description=f"""
                Reasearch and understand all rules for {lottery_type}, this includes the weight of the extra number, how many balls to be picked, the difference between picked numbers and drawn numbers.
                Understand all rules and odds of {lottery_type}, this includes the odds of winning and the prizes.
                Analyse all past lottery results from {lottery_type}, which the sequence number must be in the order it was picked.
                This will preserve the probability of the number being picked together in order.
                Research to understand how {lottery_type} game works, how many numbers need to be picked per game including the extra number.
                Research to ensure and understand how many numbers need to be picked per game and how many extra numbers to pick as well, there are lotteries such as Powerball that the extra number is included in the game
                Carefully pick {number_of_sequence} games and {rules}
            """,
            agent=agent,
            output_file=output_file,
            expected_output=f"Pick {number_of_sequence} sequence numbers considering all patterns and rules from past drawn numbers",
            callback=time.sleep(5)
        )
        
    def sequence_reviewer_task(self, agent, lottery, country, number_of_sequence):
        lottery_type=country + " " + lottery
        rules=os.getenv(lottery_type.upper() + "_RULES")
        return Task(
            description=f"""
                Ensure there are {number_of_sequence} games picked for {lottery_type} and each game has the required sequence number.
                Check all picked games against {lottery_type} rules and ensure they are all valid games.
                Ensure the strategy is well implemented and numbers make sense.
                Ensure there are {number_of_sequence} games
                Ensure each game have the correct picked numbers
                Ensure {number_of_sequence} games were picked and {rules}.  
            """,
            agent=agent,
            expected_output=f"Ensure games are valid against its rules, and a perfect strategy for picking the numbers were applied",
            callback=time.sleep(5)
        )
    
    