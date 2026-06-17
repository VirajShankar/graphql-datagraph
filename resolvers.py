from fastapi import Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List

engine = create_engine("postgresql://user:password@localhost/db")
Session = sessionmaker(bind=engine)
session = Session()

class MicrosoftRepo:
    def __init__(self, id):
        self.id = id

    @classmethod
    def get(cls, id):
        repo = session.query(cls).get(id)
        if repo is None:
            raise HTTPException(status_code=404, detail="Microsoft repo not found")
        return repo

    @classmethod
    def get_list(cls):
        return session.query(cls).all()

def get_microsoft_repos_query(session=Depends(session)):
    repos = session.query(MicrosoftRepo).all()
    return [{"id": repo.id} for repo in repos]

async def get_microsoft_repos(id: int = None):
    if id is not None:
        return await MicrosoftRepo.get(id)
    return get_microsoft_repos_query()
