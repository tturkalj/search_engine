from sqlalchemy import Column, DateTime, Integer, Boolean, MetaData, UnicodeText, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from search_engine_app.helper import now


class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, nullable=False, default=now())


class Document(BaseModel):
    name = Column(UnicodeText, nullable=False)
    text = Column(UnicodeText, nullable=False)

class DocumentWord(BaseModel):
    document_id = Column(ForeignKey(''))
