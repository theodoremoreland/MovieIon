# Introduction:
Movie Ion is a group project for Washington Univeristy's Data Analytics Boot Camp. For this project, we created a web application that uses a machine learning model to recommend movies. Below is an overview and demonstration of the application.

# Description:
Users submit three movies then the app will give 5 recommendations for each movie submitted. Prior to movie submission, users can toggle/invert the webpage's background image which will tell the app to either recommend movies that the user will likely enjoy or to recommend movies that they will probably dislike. The default background image will return likeable recommendations and the inverted image will return unlikeable recommendations.

Upon recieving recommendations, users can hover over a movie poster to view its cosine distance. Users can also click on a movie poster to view information about the movie.

In addition to providing recommendations, the app also allows users to save movies to a watchlist after viewing information about a movie. Currently, the watchlist doesn't have third party functionality (e.g. integrating to Netflix, Hulu, etc), but it is a potential update.


# Technologies used:
   - Web Scraping (Python-Splinter)
   - Data Wrangling (Pandas, SQL)
   - Machine Learning (sklearn, scipy, and joblib)
   - Storage (PostgreSQL and S3 Bucket)
   - Backend (Python-Flask)
   - Frontend (JavaScript, Bootstrap 4, HTML5/CSS3, jQuery, ajax)
   - Web Host (AWS)

# DEMONSTRATION:

# Home Screen
<img src="presentation/images/step1.PNG" width="900">

# Home Screen (After Toggle):
<img src="presentation/images/step2.PNG" width="900">

# Searching for Year One
<img src="presentation/images/step3.PNG" width="900">

# After selecting Year One
<img src="presentation/images/step4.PNG" width="900">

# Searching for Pacific Rim
<img src="presentation/images/step5.PNG" width="900">

# After selecting Pacific Rim and 500 Days of Summer
<img src="presentation/images/step6.PNG" width="900">

# After clicking submit button
<img src="presentation/images/step7.PNG" width="900">

# Results (View 1)
<img src="presentation/images/step8.PNG" width="900">

# Results (View 2)
<img src="presentation/images/step9.PNG" width="900">

# Results (View 3)
<img src="presentation/images/step10.PNG" width="900">

# After selecting a movie result (Example 1)
<img src="presentation/images/step11.PNG" width="900">

# After selecting a movie result (Example 2)
<img src="presentation/images/step12.PNG" width="900">

# After selecting a movie result (Example 3)
<img src="presentation/images/step13.PNG" width="900">

# User log in (Demo version)
<img src="presentation/images/step14.PNG" width="900">

# User profile (Demo version)
<img src="presentation/images/step15.PNG" width="900">

# Movie selections (After Toggle)
<img src="presentation/images/step16.PNG" width="900">

# Movie submit (After Toggle)
<img src="presentation/images/step17.PNG" width="900">

# Results (View 1) (After Toggle)
<img src="presentation/images/step18.PNG" width="900">

# Results (View 2) (After Toggle)
<img src="presentation/images/step19.PNG" width="900">

# Results (View 3) (After Toggle)
<img src="presentation/images/step20.PNG" width="900">

# After selecting a movie result (After Toggle)
<img src="presentation/images/step21.PNG" width="900">

# After adding movie to watchlist
<img src="presentation/images/step22.PNG" width="900">

# User Profile (After adding three movies to watchlist)
<img src="presentation/images/step23.PNG" width="900">

# User Profile (After removing two movies from watchlist)
<img src="presentation/images/step24.PNG" width="900">
