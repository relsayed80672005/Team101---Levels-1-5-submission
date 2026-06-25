from __future__ import annotations

from .models import GradebookData
from .reports import build_audit_report


def audit_gradebook(data: GradebookData) -> str:
    return build_audit_report(data)
