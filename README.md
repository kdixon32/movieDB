**To access the comments from the start page, click the poster of a movie. To access the wikipedia links, click the poster of the movie on its individual page**

If cloning this repository, you'll need following libraries to run the project locally:
Flask,
requests,
python-dotenv,
psycopg2-binary,
postgresql,
Flask-sqlalchemy,
flask_login,

In addition to this you'll have to get an API key for the TMDB database and connect the URL endpoints from TMDB and Wikipedia from a .env file

**Implementation vs. Expectations:**

I had a plan to build upon the design that I started in milestone 1. While that did somewhat take place it was quite difficult to add more without issues popping up. I can see that in some cases entire designs may need to be restructured to allow new features to function. This is likely why there is a huge focus on modularity in code. For future projects I should probably expect to make adjustments to previous code when adding new features. These adjustments should help with code modularity, flexibility, and overrall result in a better end product.


**Technical Issues:**

The first big technical issue that I ran into was figuring out how to link an image in an html file to run a python function that has parameters. I searched for over an hour online and while I found solutions no one seemed to have the solution needed for my specific implementation. I discovered "url for" and further researched how that function could complete the task at hand. To complete the full purpose of the function I needed to pass multiple variables through the html file back to python, but for the purpose of testing I chose to only pass one variable through at a time when checking each solution. Eventually I was able to find documentation that fit what I needed and was able to go from successfully completing the small test to completing the entire function.

Debugging the flask.flash unsuccessful login message took more time than it should have. The problem that I faced was that it was showed the message multiple times instead of just once. I thought that the problem was the jinja in the html file at first and changed things over there when in reality it was my placement of the "try" block in app.py that caused it. 

Setting columns to unique that should not have been unique caused me to have to drop tables multiple times to get the models to refresh after applying fixes.

Halfway through the project I decided to stop using WSL Ubuntu after running into many different issues with git refusing to push even after cloning, not pushing to main branch, and more. I like that it is an option but I will probably stick to using everything through windows just to make it easier on myself. When switching back to windows I ran into a problem with SQLAlchemy using an outdated method that didnt match my python version but after a quick stackoverflow search I was able to fix that.




