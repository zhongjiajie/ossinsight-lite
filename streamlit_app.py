import streamlit as st
import pandas as pd

st.title('OSS Insight Lite')

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
st.line_chart(df)
