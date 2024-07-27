from pydantic import BaseModel
from datetime import date
from typing import List

class SaturdayLottoResult(BaseModel):
    date: date
    WinningNumber1: int
    WinningNumber2: int
    WinningNumber3: int
    WinningNumber4: int
    WinningNumber5: int
    WinningNumber6: int
    SupplementaryNumber1: int
    SupplementaryNumber2: int

class LotteryToolOutput(BaseModel):
    Results: List[SaturdayLottoResult]