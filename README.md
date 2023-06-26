# OSS Insight Lite

Some metric not including in https://ossinsight.io

## Start

Guide to start streamlit locally

```shell
# Create virtual environment
mkdir -p .streamlit1
cat <<EOF > .streamlit1/secrets.toml
GITHUB_TOKEN="<YOUR_GITHUB_TOKEN>"
EOF
```

```shell
# Run command to start
streamlit run streamlit_app.py
```