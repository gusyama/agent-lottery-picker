import os
import time
import datetime
from crewai import Agent, Crew, Task
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from LotteryPicker import LotteryPicker
from SaturdayLottoPicker import SaturdayLottoPicker



# Setup Crew
lotto_type = 'Saturday Lotto'
country = 'Australia'
lottery = SaturdayLottoPicker()
agent=lottery.lottery_expert_agent()
DATE_FORMAT="%m%d%Y-%H%M%S"
current_date_time = datetime.datetime.now().strftime(DATE_FORMAT)

crew = Crew(
    agents=[
        agent
    ],
    tasks=[
        lottery.past_result_task(agent),
        lottery.result_search_task(agent, lotto_type, country),
        # lottery.implement_strategy_task(agent, lotto_type, country),
        # lottery.two_hot_number_and_relationship_task(agent),
        # lottery.two_cold_number_and_relationship_task(agent),
        lottery.hot_number_and_buddies_task(agent, 2),
        lottery.cold_number_and_buddies_task(agent, 2),
        lottery.pattern_and_buddies_task(agent),
        lottery.sequence_reviewer_task(agent, lotto_type, country, 5),  
    ],
    output_log_file=f"output/saturday_lotto_{current_date_time}.txt"
    #max_rpm=29
)



# lottery_type="Saturday Lotto"
# country="Australia"
# number_of_games="3"

# # Setup Crew
# lottery = LotteryPicker()
# agent=lottery.lottery_expert_agent()

# crew = Crew(
#     agents=[
#         agent
#     ],
#     tasks=[
#         lottery.result_search_task(agent, lottery_type, country),
#         lottery.pick_sequence_task(agent, lottery_type, country, number_of_games),
#         lottery.sequence_reviewer_task(agent, lottery_type, country, number_of_games)       
#     ],
#     #max_rpm=29
# )

# Kick off the crew
start_time = time.time()


results = crew.kickoff()

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Crew kickoff took {elapsed_time} seconds.")
print("Crew usage", crew.usage_metrics)