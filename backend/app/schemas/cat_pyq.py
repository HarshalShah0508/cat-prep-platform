from typing import Dict, List, Optional

from pydantic import BaseModel


class PyqPaperOption(BaseModel):
    source_year: int
    source_slot: str
    sections: Dict[str, int]


class PyqStartRequest(BaseModel):
    source_year: int
    source_slot: str
    sections: Optional[List[str]] = None
