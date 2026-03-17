"""
aicodesign - Provenance and review tracking for AI-generated code.
"""

import functools
import logging
from typing import Optional, Any, Callable

logger = logging.getLogger(__name__)

def ai_draft(author: str = "LLM", ticket: Optional[str] = None, notes: Optional[str] = None) -> Callable:
    """
    Tier 3 (High Risk): Pure AI draft.
    0 reviews on code, 0 reviews on tests.
    """
    def decorator(obj: Any) -> Any:
        obj.__ai_provenance__ = "draft"
        obj.__ai_author__ = author
        obj.__ai_ticket__ = ticket
        obj.__ai_notes__ = notes
        
        @functools.wraps(obj)
        def wrapper(*args, **kwargs):
            # Emits a runtime warning for entirely unreviewed code execution
            logger.warning(f"CRITICAL: Executing unreviewed AI draft code -> {obj.__name__}")
            return obj(*args, **kwargs)
            
        # If decorating a class, apply metadata without wrapping methods
        return obj if isinstance(obj, type) else wrapper
    return decorator


def ai_blackbox(author: str = "LLM", ticket: Optional[str] = None, notes: Optional[str] = None) -> Callable:
    """
    Tier 2 (Medium Risk): AI Blackbox.
    0 reviews on code logic, but bounded/verified by human-reviewed unit tests.
    """
    def decorator(obj: Any) -> Any:
        obj.__ai_provenance__ = "blackbox"
        obj.__ai_author__ = author
        obj.__ai_ticket__ = ticket
        obj.__ai_notes__ = notes
        return obj
    return decorator


def ai_co_signed(reviewer: str, author: str = "LLM", ticket: Optional[str] = None, notes: Optional[str] = None) -> Callable:
    """
    Tier 1 (Lower Risk): AI code co-signed by a human.
    1 human review on code, 1+ human review on tests.
    
    Args:
        reviewer (str): MANDATORY. The username or email of the developer signing off.
    """
    if not reviewer or not isinstance(reviewer, str):
        raise ValueError("The '@ai_co_signed' decorator strictly requires a valid 'reviewer' string argument.")

    def decorator(obj: Any) -> Any:
        obj.__ai_provenance__ = "co_signed"
        obj.__ai_reviewer__ = reviewer
        obj.__ai_author__ = author
        obj.__ai_ticket__ = ticket
        obj.__ai_notes__ = notes
        return obj
    return decorator
