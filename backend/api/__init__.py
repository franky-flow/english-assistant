# FastAPI REST endpoints

from .routes import router
from .vocabulary import router as vocabulary_router
from .correction import router as correction_router
from .grammar import router as grammar_router
from .phrasal_verbs import router as phrasal_verbs_router
from .history import router as history_router

__all__ = [
    "router",
    "vocabulary_router",
    "correction_router", 
    "grammar_router",
    "phrasal_verbs_router",
    "history_router"
]