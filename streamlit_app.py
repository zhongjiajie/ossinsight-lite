from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from streamlit.elements.time_widgets import DateWidgetReturn
import os

from req.param import ReqParam
from utils.reshape import get_dict_val_by_key_order, get_year_week_list
from utils.gh import get_commit_weekly_num, get_commit_author_weekly_num,\
    get_issues_weekly_num

date_now: datetime = datetime.now()
date_this_week_end: datetime = date_now - timedelta(days=date_now.weekday()) \
                               + timedelta(days=6)
date_week_ago: datetime = date_this_week_end - timedelta(weeks=4)

st.title('OSS Insight Lite')
st.subheader('Some metric not including in https://ossinsight.io')

st.subheader('Options')

option_repo = st.selectbox(
    'Which repository do you like to insight',
    ('apache/dolphinscheduler', 'apache/seatunnel')
)

date_range: DateWidgetReturn = st.date_input(
    label="Select the start date",
    value=(date_week_ago, date_this_week_end),
)

# to avoid UI index error: https://discuss.streamlit.io/t/date-input-range-index-error-while-selecting/22499
if len(date_range) != 2:
    st.stop()

st.subheader('Information')

st.write(f"For more metric of this project please see in ossinsight [{option_repo}](https://ossinsight.io/analyze/{option_repo}#overview)")
st.write("For important issue track, please see our [notion database](https://zhongjiajie.notion.site/DolphinScheduler-a03f7c3cccd142248193b12837f18a8f?pvs=4)")

start_date = datetime.combine(date_range[0], datetime.min.time())
end_date = datetime.combine(date_range[1], datetime.min.time())
year_week_list = get_year_week_list(start_date, end_date)
try:
    github_token = st.secrets["GITHUB_TOKEN"]
except FileNotFoundError:
    github_token = os.environ.get("GITHUB_TOKEN", None)

req_param = ReqParam(
    token=github_token,
    repo=option_repo,
    since=start_date,
    until=end_date
)


@st.cache_data
def data_commits(req: ReqParam) -> list[int]:
    return get_dict_val_by_key_order(
        get_commit_weekly_num(req)
    )

@st.cache_data
def data_commits_author(req: ReqParam) -> list[int]:
    return get_dict_val_by_key_order(
        get_commit_author_weekly_num(req)
    )

@st.cache_data
def data_issues(req: ReqParam) -> [dict, list[int]]:
    return get_issues_weekly_num(req)

@st.cache_data
def data_issues_update(req: ReqParam) -> list[int]:
    return data_issues(req).get('update')

@st.cache_data
def data_issues_open(req: ReqParam) -> list[int]:
    return data_issues(req).get('open')

@st.cache_data
def data_issues_close(req: ReqParam) -> list[int]:
    return data_issues(req).get('close')


st.subheader('Metric')

st.write("Weekly Commits")
df_contributors = pd.DataFrame(
    data={
        'commits': data_commits(req_param),
        'commits-authors': data_commits_author(req_param),
    },
    index=year_week_list,
)
st.line_chart(df_contributors)

st.write("Weekly Issues")
df_issues = pd.DataFrame(
    data={
        'issues-open': data_issues_open(req_param),
        'issues-close': data_issues_close(req_param),
        'issues-update': data_issues_update(req_param),
    },
    index=year_week_list,
)
st.line_chart(df_issues)
