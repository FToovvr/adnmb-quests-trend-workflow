from dataclasses import dataclass


@dataclass
class QuitDueToTrendThreadRelatedIssueException(Exception):
    reason: str
