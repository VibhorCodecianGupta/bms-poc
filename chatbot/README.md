# Install Dependencies
1.) conda install -c conda-forge httptools
2.) conda install -c conda-forge spacy
3.) pip install rasa[spacy] <br />
4.) python -m spacy download en_core_web_md <br />
5.) python -m spacy link en_core_web_md en <br />
# Run
5.) rasa run actions& (In separate cmd) <br />
6.) python main.py <br />
# Interact
7.) send post requests with message in JSON format using postman(recommended) or curl(eww). <br />
8.) GLHF
