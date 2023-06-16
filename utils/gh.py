from github import Github
from datetime import datetime

from github.Commit import Commit
from github.Issue import Issue
from github.PaginatedList import PaginatedList
import math
from functools import cache

from req.param import ReqParam
from utils.reshape import get_year_week_list

DEFAULT_PAGE_NUM = 30


@cache
def get_commits(
        *,
        token: str,
        repo: str,
        since: datetime,
        until: datetime,
) -> PaginatedList:
    g = Github(login_or_token=token)
    gh_repo = g.get_repo(repo)
    return gh_repo.get_commits(
        since=since,
        until=until,
    )


@cache
def get_issues(
        *,
        token: str,
        repo: str,
        since: datetime,
        state: str,
        sort: str,
        direction: str,
) -> PaginatedList:
    g = Github(login_or_token=token)
    gh_repo = g.get_repo(repo)
    return gh_repo.get_issues(
        since=since,
        state=state,
        sort=sort,
        direction=direction,
    )


def get_commit_weekly_num(req_param: ReqParam) -> dict[str, int]:
    result = dict.fromkeys(get_year_week_list(req_param.since, req_param.until), 0)

    commits = get_commits(
        token=req_param.token,
        repo=req_param.repo,
        since=req_param.since,
        until=req_param.until,
    )

    total_count = commits.totalCount
    for page in range(math.ceil(total_count / DEFAULT_PAGE_NUM)):
        commit_page: list[Commit] = commits.get_page(page)
        for commit in commit_page:
            commit_date: datetime = commit.commit.author.date
            calendar_date = commit_date.isocalendar()
            year_and_week = f"{calendar_date.year}-{calendar_date.week}"
            result[year_and_week] = result.get(year_and_week, 0) + 1

    return result


def get_commit_author_weekly_num(req_param: ReqParam) -> dict[str, int]:
    result_create = {
        i: set()
        for i in get_year_week_list(req_param.since, req_param.until)
    }

    commits = get_commits(
        token=req_param.token,
        repo=req_param.repo,
        since=req_param.since,
        until=req_param.until,
    )

    total_count = commits.totalCount
    for page in range(math.ceil(total_count / DEFAULT_PAGE_NUM)):
        commit_page: list[Commit] = commits.get_page(page)
        for commit in commit_page:
            commit_date: datetime = commit.commit.author.date
            calendar_date = commit_date.isocalendar()
            year_and_week = f"{calendar_date.year}-{calendar_date.week}"

            commit_email: str = commit.commit.author.email
            result_create.setdefault(year_and_week, set()).add(commit_email)

    return {
        key: len(set(result_create[key]))
        for key in result_create.keys()
    }


def get_issues_weekly_num(req_param: ReqParam) -> dict[str, dict[str, int]]:
    year_week_list = get_year_week_list(req_param.since, req_param.until)
    result_open = {i: set() for i in year_week_list}
    result_update = {i: set() for i in year_week_list}
    result_close = {i: set() for i in year_week_list}

    issues = get_issues(
        token=req_param.token,
        repo=req_param.repo,
        since=req_param.since,
        state="all",
        sort="updated",
        direction="asc",
    )

    total_count = issues.totalCount
    for page in range(math.ceil(total_count / DEFAULT_PAGE_NUM)):
        issue_page: list[Issue] = issues.get_page(page)
        for issue in issue_page:
            if issue.updated_at > req_param.until:
                break

            date_open: datetime = issue.created_at
            date_update: datetime = issue.updated_at
            date_close: datetime = issue.closed_at

            if date_open is not None:
                calendar_date = date_open.isocalendar()
                year_and_week = f"{calendar_date.year}-{calendar_date.week}"
                # we only need issue in our expect date range
                if year_and_week in result_open:
                    result_open.setdefault(year_and_week, set()).add(issue.number)
            if date_update is not None:
                calendar_date = date_update.isocalendar()
                year_and_week = f"{calendar_date.year}-{calendar_date.week}"
                if year_and_week in result_update:
                    result_update.setdefault(year_and_week, set()).add(issue.number)
            if date_close is not None:
                calendar_date = date_close.isocalendar()
                year_and_week = f"{calendar_date.year}-{calendar_date.week}"
                if year_and_week in result_close:
                    result_close.setdefault(year_and_week, set()).add(issue.number)

    return {
        'open': {key: len(val) for (key, val) in result_open.items()},
        'close': {key: len(val) for (key, val) in result_close.items()},
        'update': {key: len(val) for (key, val) in result_update.items()},
    }
