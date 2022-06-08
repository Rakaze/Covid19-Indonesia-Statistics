mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"rakageeee@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[theme]
base='dark'
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml