from sqlalchemy import create_engine, Integer, String, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped


engine = create_engine(url="sqlite:///chatdata.db", echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# TODO:implement db to store chat messages

### MODEL ###
class Base(DeclarativeBase): pass

class Chat(Base):
        __tablename__ = "chat"
        
        id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
        message: Mapped[str] = mapped_column(Text)
        user_id: Mapped[str] = mapped_column(String)
        message_id: Mapped[str] = mapped_column(String)
        channel_id: Mapped[str] = mapped_column(String)
        
Base.metadata.create_all(bind=engine)