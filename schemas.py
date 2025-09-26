from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 기본 스키마
class FarmingLogBase(BaseModel):
    user_id: str
    cultivation_area: Optional[str] = None
    crop: Optional[str] = None
    task: Optional[str] = None
    pesticide: Optional[str] = None
    fertilizer: Optional[str] = None
    memo: Optional[str] = None
    audio_file_url: Optional[str] = None
    transcribed_text: Optional[str] = None

# 로그 생성을 위한 스키마
class FarmingLogCreate(FarmingLogBase):
    pass

# DB에서 읽어올 때 (API 응답) 사용될 스키마
class FarmingLog(FarmingLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
