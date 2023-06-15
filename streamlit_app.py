from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from streamlit.elements.time_widgets import DateWidgetReturn

from req.param import ReqParam
from utils.reshape import get_dict_val_by_key_order, get_year_week_list
from utils.gh import get_commit_weekly_num, get_commit_author_weekly_num,\
    get_issues_weekly_num

date_now: datetime = datetime.now()
date_week_ago: datetime = date_now - timedelta(weeks=4)

st.title('OSS Insight Lite')
st.subheader('Some metric not including in https://ossinsight.io')

st.subheader('Options')

option_repo = st.selectbox(
    'Which repository do you like to insight',
    ('apache/dolphinscheduler', 'apache/seatunnel')
)

date_range: DateWidgetReturn = st.date_input(
    label="Select the start date",
    value=(date_week_ago, date_now),
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

req_param = ReqParam(
    repo=option_repo,
    since=start_date,
    until=end_date
)

val_commits = get_dict_val_by_key_order(
    get_commit_weekly_num(req_param)
)

val_commits_author = get_dict_val_by_key_order(
    get_commit_author_weekly_num(req_param)
)

val_issues_update = get_dict_val_by_key_order(
    get_issues_weekly_num(req_param).get('update')
)

val_issues_open = get_dict_val_by_key_order(
    get_issues_weekly_num(req_param).get('open')
)

val_issues_close = get_dict_val_by_key_order(
    get_issues_weekly_num(req_param).get('close')
)

st.subheader('Metric')

st.write("Weekly Commits")
df_contributors = pd.DataFrame(
    data={
        'commits': val_commits,
        'commits-authors': val_commits_author
    },
    index=year_week_list,
)
st.pyplot()

st.write("Weekly Issues")
df_issues = pd.DataFrame(
    data={
        'open': val_issues_open,
        'close': val_issues_close,
        'update': val_issues_update,
    },
    index=year_week_list,
)
st.line_chart(df_issues)
