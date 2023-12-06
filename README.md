# Movie Ion

_Movie Ion_ (originally named _Movie Matchmaker_) was a group project for _Washington University's Data Analytics Boot Camp (2019)_. For this project, we created a web application that uses machine learning to recommend movies in terms of what the user will likely enjoy or movies the user is least likely to enjoy.

<img src="presentation/thumbnail.png" width="600">

## Table of Contents

- [The team](#the-team-by-github-username)
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Known bugs](#known-bugs)
- [How to run locally (WIP)](#how-to-run-locally)
  - [Run on Windows](#run-on-windows)
  - [Run on Docker](#run-on-docker)
- [Screenshots](#screenshots)

# The team (by GitHub username)

- [@kamilevy](https://github.com/kamilevy)
- [@feldsteina](https://github.com/feldsteina)
- [@dperkins2315](https://github.com/dperkins2315)
- @theodoremoreland (me)

# Overview:

At the Home screen, select three of your favorite movies from the dropdown menu (select a movie a second time to remove the selection). Once your movies are selected, click the green "Submit" button to process your selections.

By default, the application will recommend movies that you are likely to enjoy. Alternatively, by toggling the slider above the movie posters (on the Home screen), the application will recommend movies that you are likely to dislike.

Upon receiving your recommendations, you can click on the movie posters to view information about the movie, including the movie's title, release date, a brief synopsis, and more. This feature is also available via clicking posters selected on the Home screen.

When viewing a movie's information, you can click the "Add to Watchlist" button to add the movie to your watchlist. You must be logged in as user1, user2, user3, user4, user5, or user6 to add movies to your watchlist. There is no password for any of these accounts as they are for demonstration purposes only.

_Note: Watchlist and user accounts were implemented to exercise and demonstrate authentication, user sessions, and database functionality. It serves no practical purpose beyond that._

# Technologies used:

- Web Scraping (Python, Splinter)
- Data Wrangling (Pandas, SQL)
- Machine Learning (sklearn, scipy, and joblib)
- Storage (PostgreSQL, S3 Bucket)
- Backend (Python, Flask)
- Frontend (JavaScript, Bootstrap 4, HTML5/CSS3, jQuery, ajax)
- Containerization (Docker)
- Web Host (AWS)

# How to run locally

Whether you are running the app directly on a Windows OS or indirectly via Docker, there are a few things you need to do in order to setup the application:

- You need your own PostgreSQL database instance.
- You need to create a file in `application/modules/` called `config.py` mimicking the template provided in `application/modules/config.py.example` wherein the empty strings are replaced with values relating to a connection to your PostgreSQL database instance.
- You need to execute the SQL code found in the `resources/` folder to create the tables and insert the data needed to run the app, the order of which does not matter.
- Download `.joblib` files from here (link available soon) and place in `application/models/` folder (folder must be created).

- If you are trying to run this application directly on a Windows OS, you will need to install `Python 3.8`.
- Otherwise, you will need to install Docker so you can run the application through Docker.

## Run on Windows

Assumes you are using a modern Windows client OS such as Windows 11 or Windows 10 and that Python 3.8 is installed.

Open terminal at root of this project then move into application/ directory:

```
cd application/
```

Create venv folder in application folder using Python 3.8:

```
python3.8 -m venv venv
```

Activate venv:

```
source venv/Scripts/activate
```

Install python packages to venv:

```
pip install -r requirements.txt
```

Start application:

```
python application.py
```

## Run on Docker

Firstly, confirm that Docker is installed and running. Next confirm that no other application is using port `5000` as port `5000` is needed for the Flask server. If you need to run Flask on an alternative port, you can modify the last line in the `application/application.py` file.

Open terminal at root of this project then move into docker/ directory:

```
cd docker/
```

Build Docker image and start Docker container:

```
docker compose up --build
```

Visit: http://localhost:5000 to use the application.

# Known bugs

- Some movies don't play well with the ML model and will silently fail on the UI, only made evident by an infinite loading animation. The suspected cause is the data present in the model supports fewer movies than the movie dataset used in the database, resulting in the application presenting options that the machine learning model cannot process. Because the disparity between the two is so large, the recommendation is to avoid selecting obscure movies and upon experiencing long processing times refresh the page and avoid the selection of movies that previously caused the failure. Movies known to cause issues include:
  - Terminator 3: Rise of the Machines (2003)
  - Clueless (1995)
  - Sabrina (1995)
- Most movies that start with words such as "A" or "The" erroneously have the word at the end of the movie title preceded by a comma (e.g. `Ref, The (1994)` or `Walk in the Clouds, A (1995)`). Unfortunately, a fix isn't as simple as formatting the data in the database or web server. The issue stems from the source data and would most likely have to be transformed prior to being added to the model.
- Some (relatively few) movies don't have posters such as `Jurassic Park (1993)`.
- Something went wrong when processing the original Toy Story, so it is unfortunately not supported.

# Note to developers:

If intending to run this codebase locally, here are a few things to note.

- joblib models can only be used by the same version of joblib, sklearn, scikit-learn that created them.
- Certain versions of joblib, sklearn, scikit-learn are not compatible with newer versions of Python.
- Certain versions of joblib, sklearn, scikit-learn are not compatible with each other nor this codebase.
- The requirements.txt file contains the last versions of joblib, sklearn, scikit-learn that are compatible with each other and this codebase.
- As of this writing, Python 3.9 and above are not compatible with versions listed in requirements.txt and thus Python 3.8 is being used.
- The `scripts/create_ML_models.py` script can be used to create new models, however much of the data needed for model creation have to first be web scraped and created via files in the `notebooks/` folder which have been deprecated for years.
- Expect to need between 2.5GB - 3GB of RAM without optimizations.

# Screenshots:

# Home Screen

<img src="presentation/step1.PNG" width="900">

# Home Screen (After Toggle):

<img src="presentation/step2.PNG" width="900">

# Searching for Year One

<img src="presentation/step3.PNG" width="900">

# After selecting Year One

<img src="presentation/step4.PNG" width="900">

# Searching for Pacific Rim

<img src="presentation/step5.PNG" width="900">

# After selecting Pacific Rim and 500 Days of Summer

<img src="presentation/step6.PNG" width="900">

# After clicking submit button

<img src="presentation/step7.PNG" width="900">

# Results (View 1)

<img src="presentation/step8.PNG" width="900">

# Results (View 2)

<img src="presentation/step9.PNG" width="900">

# Results (View 3)

<img src="presentation/step10.PNG" width="900">

# After selecting a movie result (Example 1)

<img src="presentation/step11.PNG" width="900">

# After selecting a movie result (Example 2)

<img src="presentation/step12.PNG" width="900">

# After selecting a movie result (Example 3)

<img src="presentation/step13.PNG" width="900">

# User log in (Demo version)

<img src="presentation/step14.PNG" width="900">

# User profile (Demo version)

<img src="presentation/step15.PNG" width="900">

# Movie selections (After Toggle)

<img src="presentation/step16.PNG" width="900">

# Movie submit (After Toggle)

<img src="presentation/step17.PNG" width="900">

# Results (View 1) (After Toggle)

<img src="presentation/step18.PNG" width="900">

# Results (View 2) (After Toggle)

<img src="presentation/step19.PNG" width="900">

# Results (View 3) (After Toggle)

<img src="presentation/step20.PNG" width="900">

# After selecting a movie result (After Toggle)

<img src="presentation/step21.PNG" width="900">

# After adding movie to watchlist

<img src="presentation/step22.PNG" width="900">

# User Profile (After adding three movies to watchlist)

<img src="presentation/step23.PNG" width="900">

# User Profile (After removing two movies from watchlist)

<img src="presentation/step24.PNG" width="900">
