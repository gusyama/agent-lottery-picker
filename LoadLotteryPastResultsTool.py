import csv
import os
from crewai_tools.tools.base_tool import BaseTool
from datetime import datetime
from dotenv import load_dotenv
from langchain.tools import Tool
from pathlib import Path
from pydantic import ValidationError
from pydantic.v1 import BaseModel, Field
from typing import List, Type
from SaturdayLottoResult import LotteryToolOutput



load_dotenv()

def parse_lottery_results(file_path: str) -> LotteryToolOutput:
    lottery_results = []
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            try:
                result = LotteryToolOutput(
                    date=datetime.strptime(row['Date'], '%d/%m/%Y').date(),
                    WinningNumber1=int(row['#1']),
                    WinningNumber2=int(row['#2']),
                    WinningNumber3=int(row['#3']),
                    WinningNumber4=int(row['#4']),
                    WinningNumber5=int(row['#5']),
                    WinningNumber6=int(row['#6']),
                    SupplementaryNumber1=int(row['S1']),
                    SupplementaryNumber2=int(row['S2'])
                )
                lottery_results.append(result)
            except (ValueError, ValidationError) as e:
                print(f"Error processing row: {row}, error: {e}")
                
    return lottery_results


class LoadLotteryPastResultsTool(BaseTool):
    name: str = "LoadLotteryPastResultsTool"
    description: str = (
        "Fetches all past lottery results from csv file."
    )
    return_schema: Type[BaseModel] = LotteryToolOutput
    

    def _run(self) -> LotteryToolOutput:
        file_path = os.getenv("GROQ_API_KEY")
        return parse_lottery_results(file_path)



# # Assuming the CSV file is located at 'past_lottery_results.csv'
# file_path = 'past_lottery_results.csv'

# # Create an instance of the tool
# lottery_tool = LotteryTool(file_path=file_path)

# # Execute the tool to get the list of lottery results
# results = lottery_tool.execute()

# # Print the results
# for result in results:
#     print(result)
