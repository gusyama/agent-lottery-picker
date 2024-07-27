import os
import time
import datetime
from crewai import Agent, Crew, Task
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class SaturdayLottoPicker():
    
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
    
    # TODO re write to OZ Saturday Lotto specifically 
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
        

    def past_result_task(self, agent, lottery='Saturday Lotto', country='Australia'):
        website=os.getenv(country.upper() + "_URL")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/{lottery}_strategy_{current_date_time}.txt"
        return Task(
            description=f"""
                Use the {website} to find all past results of {country} {lottery}, remember to ensure the order of drawn numbers are as originally picked.
                If you dont find it, search online for {country} {lottery} past drawn numbers.
                Make a list of the past results of 1 year where each line is a drawing result, and its column as: date, all drawn numbers in its original sequence with spaces between them and then the supplementary numbers
                 """,
            agent=agent,
            output_file=output_file,
            expected_output=f"Make a list of {lottery} past results of 1 year where each line is a drawing result, and its column as: date, all drawn numbers in its original sequence with spaces between them, and the supplementary numbers.",
            callback=time.sleep(5)
        )
        
    
    # TODO re write to OZ Saturday Lotto specifically 
    def result_search_task(self, agent, lottery, country):
        lottery_type=country + " " + lottery
        website=os.getenv(country.upper() + "_URL")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/{lottery_type}_past_results_{current_date_time}.txt"
        return Task(
            description=f"""
                Research to understand how {lottery_type} game works, how many winning numbers need to be picked including the supplementary number
                Research to ensure you understand how many winning numbers need to be picked per game and how many supplementary numbers to pick as well (if needed), there are lotteries such as Powerball that the supplementary number is included in the game
                You can use this website {website} to search and find the past 1 year of lottery results from {lottery_type}, which the sequence number must be in the order it was picked.
                This will preserve the probability of the number being picked together in order.
                Understand the patterns and the relationship between numbers being picked together in a specific order.
                Consider the most picked numbers and how often they get picked, such as, based on past results patterns how long in a row they get picked or how long they don't get picked
                Analize the pattern of less picked numbers and how often they dont get picked, this can increase a chance of the number being picked in case of the number has not been picked for a long period]
                Apply the knowledge acquired and specify the number which are mostly like to be picked in a sequence  
                 """,
            agent=agent,
            output_file=output_file,
            expected_output=f"Find the top 5 best strategies to win jackpot in {lottery_type} and suggest this to all agents that pick sequence number to also consider the strategy.",
            callback=time.sleep(5)
        )
        
    def implement_strategy_task(self, agent, lottery, country):
        lottery_type=country + " " + lottery
        website=os.getenv(country.upper() + "_URL")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/{lottery_type}_past_results_{current_date_time}.txt"
        return Task(
            description=f"""
                Use the top 5 best strategies to win jackpot in {lottery_type} identified for task 'result_search_task'.
                Ensure no repeting number is in the selected winning numbers and it follows the rules.
                 """,
            agent=agent,
            output_file=output_file,
            expected_output=f"Implement the top 5 strategies defined by 'result_search_task' in 5 games.",
            callback=time.sleep(5)
        )
    
    def two_hot_number_and_relationship_task(self, agent):
        rules=os.getenv("SATURDAY_LOTTO_RULES")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/saturday_hot_number_and_relationship_{current_date_time}.txt"
        return Task(
            description=f"""
                Lottery rules: {rules}
                Identify and pick 2 hot numbers not drawn recently and call them hot1 and hot2
                Identify the 2 numbers which were more frequently drawn with hot1 and pick them and call them hot1bud1 and hot1bud2
                Identify the 2 numbers which were more frequently drawn with hot2 and pick them and call them hot2bud1 and hot2bud2
                So now you have picked the 6 winning numbers
            """,
            agent=agent,
            output_file=output_file,
            expected_output=f"Pick one sequence of numbers containing 2 hot numbers and its most paired numbers, remember to be based on the past drawns",
            callback=time.sleep(5)
        )
        
        
    def two_cold_number_and_relationship_task(self, agent):
        rules=os.getenv("SATURDAY_LOTTO_RULES")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/saturday_cold_number_and_relationship_{current_date_time}.txt"
        return Task(
            description=f"""
                Lottery rules: {rules}
                Identify and pick 2 cold numbers not drawn recently and most likely to be drawn call them cold1 and cold2
                Identify the 2 numbers which were more frequently drawn with cold1 and pick them and call them cold1bud1 and cold1bud2
                Identify the 2 numbers which were more frequently drawn with cold2 and pick them and call them cold2bud1 and cold2bud2
                So now you have picked the 6 winning numbers
            """,
            agent=agent,
            output_file=output_file,
            expected_output=f"Pick one sequence of numbers containing 2 cold numbers and its most paired numbers, remember to be based on the past drawns",
            callback=time.sleep(5)
        )
        
    def hot_number_and_buddies_task(self, agent, number_games):
        rules=os.getenv("SATURDAY_LOTTO_RULES")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/saturday_hot_number_and_buddies_{current_date_time}.txt"
        return Task(
            description=f"""
                Lottery rules: {rules}
                The following steps describes how to successfully pick the sequence numbers. Remember each game will be composed of 1 hot number and its 5 mostly paired numbers.
                1. Identify and pick {number_games} hot number not drawn recently and most likely to be drawn, each of those number will be the main number of each game.
                2. Identify the 5 numbers which were more frequently drawn for each picked hot number and added them to its respective game (according to the hot number)
                3. So now you have picked the {number_games} games with 6 winning numbers each
            """,
            agent=agent,
            output_file=output_file,
            expected_output=f"{number_games} sequence of numbers containing 1 hot number and its most paired numbers, remember to be based on the past drawns",
            callback=time.sleep(5)
        )
        
    def cold_number_and_buddies_task(self, agent, number_games):
        rules=os.getenv("SATURDAY_LOTTO_RULES")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/saturday_cold_number_and_buddies_{current_date_time}.txt"
        return Task(
            description=f"""
                Lottery rules: {rules}
                The following steps describes how to successfully pick the sequence numbers. Remember each game will be composed of 1 cold number and its 5 mostly paired numbers.
                1. Identify and pick {number_games} cold number not drawn recently and most likely to be drawn, each of those number will be the main number of each game.
                2. Identify the 5 numbers which were more frequently drawn for each picked cold number and added them to its respective game (according to the cold number)
                3. So now you have picked the {number_games} games with 6 winning numbers each
            """,
            agent=agent,
            output_file=output_file,
            expected_output=f"{number_games} sequence of numbers containing 1 cold number and its most paired numbers, remember to be based on the past drawns",
            callback=time.sleep(5)
        )
        
    def pattern_and_buddies_task(self, agent):
        rules=os.getenv("SATURDAY_LOTTO_RULES")
        current_date_time = datetime.datetime.now().strftime(self.DATE_FORMAT)        
        output_file=f"output/saturday_pattern_and_buddies_{current_date_time}.txt"
        return Task(
            description=f"""
                Lottery rules: {rules}
                Identify how long in average every single number gets picked.
                Based on the fidings identify how long the number is overdue to be drawn, them pick the top 2 numbers that is in this long wait considering its average to be picked up, call them as wait1 and wait2
                Identify the 2 numbers which were more frequently drawn with wait1 and pick them 
                Identify the 2 numbers which were more frequently drawn with wait2 and pick them 
                So now you have picked the 6 winning numbers
            """,
            agent=agent,
            output_file=output_file,
            expected_output=f"Pick one sequence of numbers containing the top 2 number identified and its most paired numbers, remember to be based on the past drawns",
            callback=time.sleep(5)
        )
    
    # TODO re write to OZ Saturday Lotto specifically 
    def sequence_reviewer_task(self, agent, lottery, country, number_of_sequence):
        lottery_type=country + " " + lottery
        rules=os.getenv(lottery_type.upper() + "_RULES")
        return Task(
            description=f"""
                Ensure there are {number_of_sequence} games picked for {lottery_type} and each game has the required sequence number.
                Check all picked games against {lottery_type} rules and ensure they are all valid games.
                Ensure the strategy is well implemented and numbers make sense.
                Ensure there are {number_of_sequence} games.
                Ensure each game have the correct picked numbers.
                Ensure {number_of_sequence} games were picked and {rules}.
                Ensure the sequence is made of either 3 evens and 3 odds numbers or 4 evens and 2 odds or 2 evens and 4 odds.
                Ensure that each game the sum of the number of the game falls within the calculated range of 56 to 220
                Ensure the sequence game numbers are different and a single number do not repeat more than 4 times within all games, otherwise ask the agent to pick another sequence.
            """,
            agent=agent,
            expected_output=f"Ensure games are valid against its rules, and a perfect strategy for picking the numbers were applied",
            callback=time.sleep(5)
        )
    
    