"""Tools for the Tool Use Workflow."""

from typing import cast
from langchain_core.tools import tool as langchain_tool


@langchain_tool
def search_database(query: str) -> list[dict[str, str | int]]:
    """Fake tool that would search a database of books using the query

    Args:
        query: The query to search the database for
    Returns:
        A list of dictionaries with the title and author of the books.
        Properties:
            title: The title of the book
            author: The author of the book
            copies: The number of copies of the book in the database
    """
    print(f"{'-' * 10} Tool called - Searching database for: {query} {'-' * 10}")
    fake_results: list[dict[str, str | int]] = [
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "copies": 10},
        {"title": "1984", "author": "George Orwell", "copies": 5},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "copies": 3},
    ]

    def matches_query(book: dict[str, str | int]) -> bool:
        title = cast(str, book.get("title", ""))
        author = cast(str, book.get("author", ""))
        query_lower = query.lower()
        return query_lower in title.lower() or query_lower in author.lower()

    filtered_results: list[dict[str, str | int]] = [
        cast(dict[str, str | int], book) for book in fake_results if matches_query(book)
    ]

    return filtered_results
