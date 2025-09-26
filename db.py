from sqlalchemy import create_engine, Integer, String, Text, Enum 
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped


engine = create_engine(url="sqlite:///chatdata.db", echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


### MODEL ###
class Base(DeclarativeBase): pass

class Chat(Base):
        __tablename__ = "chat"
        
        id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
        message: Mapped[str] = mapped_column(Text)
        user_id: Mapped[str] = mapped_column(String)
        role: Mapped[str] = mapped_column(String) #Enum(enums=["ai", "human", "user", "system"]))
        message_id: Mapped[str] = mapped_column(String)
        channel_id: Mapped[str] = mapped_column(String)
        
Base.metadata.create_all(bind=engine)