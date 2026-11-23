"""Repository for feedback persistence.

TODO: Implement CRUD operations for Feedback.
"""

from sqlalchemy.ext.asyncio import AsyncSession


class FeedbackRepository:
    """CRUD operations for Feedback."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # TODO: async def create(self, data: FeedbackCreate) -> Feedback: ...
    # TODO: async def get_by_page(self, page: str) -> list[Feedback]: ...
