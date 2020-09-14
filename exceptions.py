from dataclasses import dataclass


@dataclass
class ShouldNotReachException(Exception):
    pass


@dataclass
class QuitDueToTrendThreadRelatedIssueException(Exception):
    reason: str
