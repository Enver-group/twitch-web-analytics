Network Analysis of Hispanic streamers in the Twitch community
==============================

Analysis of Twitch streamers in the Hispanic community based on their follows. We used the [Twitch API](https://dev.twitch.tv/docs/api/reference/) to get information about users, their followers,
and who they follow in order to construct the dataset we used to carry our analysis.

The main objectives were the following:

- Obtain insights and Visualize in detail the Twitch Hispanic Network

- Perform Community detection analysis on the graph of streamers.

- Rank streamers using network metrics

- Make a simple recommendation system for Twitch streamers based on their follows.

**Authors:**
- Simón E. Sánchez Viloria
- Andres Ruiz Calvo
- David Méndez Encinas
- Enrique Botía Barbera

![](https://drive.google.com/uc?id=1SV6b0q2TVHUXfcE6IGCXUu_vuhaDaTJK)


Streamlit Dashboard
----------

A dashboard showing the insights of our analysis was made with streamlit. You can go [here](https://share.streamlit.io/simonsanvil/twitch-web-analytics/app/main/main.py) to see it live or clone this repository, install the dependencies and run `streamlit run app/main/main.py` to execute it locally yourself. Also, [here](https://drive.google.com/drive/folders/1sLFmG8H_ccWvvZcTS-vsuiaTParDkmf5?usp=sharing) you can see all the images we obtained in our graph analysis.

![Streamlit Dashboard](https://github.com/Enver-group/twitch-web-analytics/blob/master/reports/figures/dashboard_home.png?raw=true)

Usage and Reproducibility
--------------


In order to reproduce the Analysis we made on this project you can follow the steps below:

1. Clone this repository.
2. Download the dependencies with `pip install -r requirements.txt`
3. You can use the dataset we built for this project that is located in the data/ directory or create one yourself with the command `python -m src.data --root_user {YOUR SELECTED STREAMER} --output_file "data/streamers.feather" --max_users 10000`
4. Go though our notebooks and source code and run the experiments and analysis we made for yourself.
5. Run the streamlit app with `streamlit run app/main/main.py` to visualize the results in a dashboard like the one shown in the image above.

**Note**: If you want to make your own dataset you will need to obtain your own keys to the Twitch API from [Twitch](https://dev.twitch.tv/docs/api/quick-start/#authentication) and set them up in your environment variables before running the code.

```bash
export TWITCH_CLIENT_ID=<your twitch client id>
export TWITCH_CLIENT_SECRET=<your twitch client secret>
```

References and Credit
----------

- Twitch API: https://dev.twitch.tv/docs/api/reference/

- Ana Blanco's ([casiopa](https://github.com/casiopa)) [EDA-IMDb](https://share.streamlit.io/casiopa/eda-imdb/main/src/utils/streamlit/EDA_IMDb_main.py) streamlit app.


Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │ 
    |
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    |
    ├── app               <- Streamlit app (dashboard)
    │
    └── Dockerfile         <- Dockerfile to build the docker image of the streamlit app used in this project.


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
