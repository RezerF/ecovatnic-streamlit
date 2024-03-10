# Ecovatnic streamlit app 

## Only web and docker image, all base logic located [ecovatnik-calculator](https://github.com/RezerF/ecovatnik-calculator) repository
ecovatnik-calculator install as dependencies
## How to start
### Prepare
```bash
git clone https://github.com/RezerF/ecovatnic-streamlit.git
cd ecovatnic-streamlit
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
## Run application
local run:
```bash
streamlit run ecoapp.py 
```

local debug
```bash
streamlit run ecoapp.py --logger.level debug --server.headless True
```
run for IDE
```bash
python -m streamlit run ecoapp.py
```