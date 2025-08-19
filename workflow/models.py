from pydantic import BaseModel, Field
from typing import List

class Headline(BaseModel):
    """
    A single unique news headline.
    Each headline must be distinct across all categories.
    Do not repeat the same article URL or text in multiple places.
    """
    url: str = Field(
        description="The source URL of the news article. Must be unique across all headlines."
    )
    text: str = Field(
        description="The headline text of the news article. Must be unique across all headlines."
    )


class HeadlinesCategory(BaseModel):
    """
    A group of headlines that belong to a single topical category.
    Categories are only created when the user clearly expresses two or more distinct interests.
    Closely related interests (e.g., 'AI' and 'LLMs') should be merged into one category.
    Different interests (e.g., 'AI' vs. 'Trump tariffs') should be separated into different categories.
    """
    category: str = Field(
        description="The name of the category representing one distinct area of user interest."
    )
    headlines: List[Headline] = Field(
        description="A list of unique headlines relevant to this category. No duplicates within this list or across categories."
    )


class HeadlinesOutput(BaseModel):
    """
    The final structured output of relevant news headlines grouped by category.
    
    Rules:
    - Each headline must be unique across all categories (no duplicate URLs or texts).
    - Categories should only be created if the user has specified two or more distinct interests.
      - Merge closely related interests into one category.
      - Separate unrelated interests into different categories.
    - If the user has only one interest, return a single category with all unique headlines.
    """
    headlines: List[HeadlinesCategory] = Field(
        description="A list of categories containing unique, relevant news headlines. No duplicates across categories."
    )