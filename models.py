from typing import List, Optional

from pydantic import BaseModel, Field


class TDPLeague(BaseModel):
    """League type for TDPSearchTool."""

    league_major: Optional[str] = Field(..., description="The major league of the TDP.")
    league_minor: Optional[str] = Field(..., description="The minor league of the TDP.")
    league_sub: Optional[str] = Field(..., description="The sub league of the TDP.")
    name: Optional[str] = Field(..., description="The name of the TDP.")
    name_pretty: Optional[str] = Field(..., description="The pretty name of the TDP.")


class TDPTeam(BaseModel):
    """Team type for TDPSearchTool."""

    name: Optional[str] = Field(..., description="The name of the team.")
    name_pretty: Optional[str] = Field(..., description="The pretty name of the team.")


class TDPInfo(BaseModel):
    """Data type for TDPSearchTool."""

    index: Optional[int] = Field(..., description="The index of the TDP.")
    league: Optional[TDPLeague] = Field(..., description="The league of the TDP.")
    team_name: Optional[TDPTeam] = Field(..., description="The team of the TDP.")
    year: Optional[int] = Field(..., description="The year of the TDP.")


class TDPResultParagraph(BaseModel):
    """Paragraph type for TDPSearchTool."""

    tdp_name: Optional[TDPInfo] = Field(
        ..., description="The TDP name information including league and team details."
    )
    title: Optional[str] = Field(..., description="The title of the paragraph.")
    content: Optional[str] = Field(..., description="The content of the paragraph.")
    questions: Optional[List[str]] = Field(
        default_factory=list,
        description="List of questions related to the paragraph content.",
    )


class TDPResult(BaseModel):
    """Response type for TDPSearchTool."""

    keywords: Optional[List[str]] = Field(
        default_factory=list, description="The keywords found in the TDP."
    )
    paragraphs: Optional[List[TDPResultParagraph]] = Field(
        default_factory=list, description="The paragraphs found in the TDP."
    )

    def pretty_markdown(self, amount_of_paragraphs: int = 5):
        """Convert the TDPResult to a pretty markdown string."""
        markdown = f"# TDP Search Results ({len(self.paragraphs)} paragraphs)\n\n"
        markdown += f"## Keywords: {', '.join(self.keywords)}\n\n"
        markdown += "## Paragraphs found:\n\n"

        for index, paragraph in enumerate(self.paragraphs[:amount_of_paragraphs]):
            markdown += f"### {index + 1}. {paragraph.tdp_name.year} TDP from {paragraph.tdp_name.team_name.name_pretty}  Team - {paragraph.title}\n\n"
            markdown += f"**Content:**\n\n{paragraph.content}\n\n"
            markdown += "- **Questions related to the content:**\n"
            for question in paragraph.questions:
                markdown += f"  - {question}\n"
            markdown += "\n"

        return markdown
