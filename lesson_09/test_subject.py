import random
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Subject(Base):
    __tablename__ = "subject"

    subject_id = Column(Integer, primary_key=True)
    subject_title = Column(String)
    deleted_at = Column(DateTime, nullable=True)


def generate_test_id():
    """Генерирует случайный ID вне диапазона существующих (1–15)."""
    return random.randint(100000, 999999)


def hard_delete_subject(session, subject_id):
    """Удаляем тестовую строку через ORM (cleanup)."""
    subject = session.query(Subject).filter_by(subject_id=subject_id).first()
    if subject is not None:
        session.delete(subject)
        session.commit()


def test_add_subject(db_session):
    """Создаём предмет и проверяем его наличие в БД."""
    subject_id = generate_test_id()

    try:
        subject = Subject(
            subject_id=subject_id,
            subject_title="QA Test Subject"
        )
        db_session.add(subject)
        db_session.commit()

        result = db_session.query(Subject).filter_by(
            subject_id=subject_id
        ).first()

        assert result is not None
        assert result.subject_title == "QA Test Subject"
        assert result.deleted_at is None
    finally:
        hard_delete_subject(db_session, subject_id)


def test_update_subject(db_session):
    """Создаём, обновляем название, сверяем с БД."""
    subject_id = generate_test_id()

    try:
        subject = Subject(
            subject_id=subject_id,
            subject_title="Old QA Title"
        )
        db_session.add(subject)
        db_session.commit()

        subject.subject_title = "Updated QA Title"
        db_session.commit()

        updated = db_session.query(Subject).filter_by(
            subject_id=subject_id
        ).first()

        assert updated.subject_title == "Updated QA Title"
        assert updated.deleted_at is None
    finally:
        hard_delete_subject(db_session, subject_id)


def test_soft_delete_subject(db_session):
    """Помечаем deleted_at, для мягкого удаления, проверяем скрытие из выборки."""
    subject_id = generate_test_id()

    try:
        subject = Subject(
            subject_id=subject_id,
            subject_title="Subject For Soft Delete"
        )
        db_session.add(subject)
        db_session.commit()

        # Ставим метку времени
        subject.deleted_at = datetime.now()
        db_session.commit()

        # Запись находится в БД
        all_rows = db_session.query(Subject).filter_by(
            subject_id=subject_id
        ).all()
        assert len(all_rows) == 1
        assert all_rows[0].deleted_at is not None

        # Скрыта из выборки
        active = db_session.query(Subject).filter_by(
            subject_id=subject_id,
            deleted_at=None
        ).first()
        assert active is None
    finally:
        hard_delete_subject(db_session, subject_id)