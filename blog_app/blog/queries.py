from typing import List

from pydantic import BaseModel

from blog.models import Article


class ListArticlesQuery(BaseModel):
    def execute(self) -> List[Article]:
        return Article.list()


class GetArticleByIDQuery(BaseModel):
    id: str

    def execute(self) -> Article:
        return Article.get_by_id(self.id)
