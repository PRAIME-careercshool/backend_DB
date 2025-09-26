from sqlalchemy.orm import Session
import models
import schemas

# 특정 ID를 가진 로그 조회
def get_log(db: Session, log_id: int):
    return db.query(models.FarmingLog).filter(models.FarmingLog.id == log_id).first()

# 특정 사용자의 모든 로그 조회
def get_logs_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.FarmingLog).filter(models.FarmingLog.user_id == user_id).offset(skip).limit(limit).all()

# 새로운 농업 일지 생성
def create_farming_log(db: Session, log: schemas.FarmingLogCreate):
    db_log = models.FarmingLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# STT 결과 및 오디오 URL 업데이트 (나중에 백엔드에서 사용)
def update_log_with_transcription(db: Session, log_id: int, audio_url: str, text: str):
    db_log = get_log(db, log_id)
    if db_log:
        db_log.audio_file_url = audio_url
        db_log.transcribed_text = text
        db.commit()
        db.refresh(db_log)
    return db_log

# 분류된 데이터 업데이트 (나중에 백엔드에서 사용)
def update_log_with_structured_data(db: Session, log_id: int, structured_data: schemas.FarmingLogBase):
    db_log = get_log(db, log_id)
    if db_log:
        update_data = structured_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_log, key, value)
        db.commit()
        db.refresh(db_log)
    return db_log
