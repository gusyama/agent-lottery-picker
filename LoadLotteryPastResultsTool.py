import csv
import os
from crewai_tools.tools.base_tool import BaseTool
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, ValidationError
from pydantic.fields import ClassVar
from typing import List, Type
from SaturdayLottoResult import SaturdayLottoResult, LotteryToolOutput


load_dotenv()


class Task(BaseModel):
    expected_output: dict  # Add the expected_output field
    output_pydantic: BaseModel  # Ensure output_pydantic is a subclass of BaseModel


def parse_lottery_results(file_path: str) -> LotteryToolOutput:
    lottery_results = []
    
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        
        current_date = datetime.now().date()
        
        for row in reader:
            try:
                result_date = datetime.strptime(row['Date'], '%d/%m/%y').date()
        
                # Calculate the date 1 year ago from the current date
                one_year_ago = current_date - timedelta(days=365)
                
                if result_date < one_year_ago:
                    break  # Exit the loop if the result date is more than 1 year ago
        
                result = SaturdayLottoResult(
                    date = result_date,
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
    return_schema: ClassVar[Type[SaturdayLottoResult]] = SaturdayLottoResult
    

    def _run(self) -> LotteryToolOutput:
        file_path = os.getenv("LOTTERY_PAST_RESULTS_PATH")
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
