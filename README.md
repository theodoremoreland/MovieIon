# Introduction:
Movie Matchmaker is a group project for Washington Univeristy's Data Analytics Boot Camp. For this project, we created a web app that uses a machine learning model to recommend movies. For a short while, the app will be available online at www.movieion.com. Below is an overview and demonstration of the app.

# Description:
Users submit three movies then the app will give 5 recommendations for each movie submitted. Prior to movie submission, users can toggle/invert the webpage's background image which will tell the app to either recommend movies that the user will likely enjoy or to recommend movies that they will probably dislike. The default background image will return likeable recommendations and the inverted image will return unlikeable recommendations.

Upon recieving recommendations, users can hover over a movie poster to view its cosine distance. Users can also click on a movie poster to view information about the movie.

In addition to providing recommendations, the app also allows users to save movies to a watchlist after viewing information about a movie. Currently, the watchlist doesn't have third party functionality (e.g. integrating to Netflix, Hulu, etc), but it is a potential update.


# Technologies used:

   - IDEs (VS Code and Jupyter Notebook)
   - Web Scraping (Python-Splinter)
   - Data Wrangling (Pandas, pgAdmin)
   - Machine Learning (sklearn, scipy, and joblib)
   - Storage (PostgreSQL and S3 Bucket)
   - Backend (Python-Flask)
   - Frontend (JavaScript, Bootstrap 4, HTML5/CSS3, jQuery, ajax)
   - Web Host (AWS)
   
# Unforeseen Challenges:
   - Certain libraries were incompatible with web host, namely psycopg2.
   Solution: Luckily found an alternative (pg8000)
   - A dataset required a new library to properly clean and use.
   Solution: import ast
   - Machine learning model required more RAM than standard web app, therefore sustainability, price, and processing speed were issues.
   Solution: Limit certain features and upgrade server, but ony keep website live for a limited time.
   - Bootstrap library was not compatible with familiar Flask and JavaScript techniques.
   Solution: Learn minimal ajax and JQuery
   - Bootstrap library was transforming data.
   Solution: Identify conversion pattern then re-convert affected data.

# DEMONSTRATION:
# Home Screen
<img src="static/images2/step1.PNG" width="900">

# Home Screen (After Toggle):
<img src="static/images2/step2.PNG" width="900">

# Searching for Year One
<img src="static/images2/step3.PNG" width="900">

# After selecting Year One
<img src="static/images2/step4.PNG" width="900">

# Searching for Pacific Rim
<img src="static/images2/step5.PNG" width="900">

# After selecting Pacific Rim and 500 Days of Summer
<img src="static/images2/step6.PNG" width="900">

# After clicking submit button
<img src="static/images2/step7.PNG" width="900">

# Results (View 1)
<img src="static/images2/step8.PNG" width="900">

# Results (View 2)
<img src="static/images2/step9.PNG" width="900">

# Results (View 3)
<img src="static/images2/step10.PNG" width="900">

# After selecting a movie result (Example 1)
<img src="static/images2/step11.PNG" width="900">

# After selecting a movie result (Example 2)
<img src="static/images2/step12.PNG" width="900">

# After selecting a movie result (Example 3)
<img src="static/images2/step13.PNG" width="900">

# User log in (Demo version)
<img src="static/images2/step14.PNG" width="900">

# User profile (Demo version)
<img src="static/images2/step15.PNG" width="900">

# Movie selections (After Toggle)
<img src="static/images2/step16.PNG" width="900">

# Movie submit (After Toggle)
<img src="static/images2/step17.PNG" width="900">

# Results (View 1) (After Toggle)
<img src="static/images2/step18.PNG" width="900">

# Results (View 2) (After Toggle)
<img src="static/images2/step19.PNG" width="900">

# Results (View 3) (After Toggle)
<img src="static/images2/step20.PNG" width="900">

# After selecting a movie result (After Toggle)
<img src="static/images2/step21.PNG" width="900">

# After adding movie to watchlist
<img src="static/images2/step22.PNG" width="900">

# User Profile (After adding three movies to watchlist)
<img src="static/images2/step23.PNG" width="900">

# User Profile (After removing two movies from watchlist)
<img src="static/images2/step24.PNG" width="900">




(Last updated 7/25/2019)
