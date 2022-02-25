**To access the comments from the start page, click the poster of a movie. To access the wikipedia links, click the poster of the movie on its individual page**

If cloning this repository, you'll need following libraries to run the project locally:
Flask
requests
python-dotenv
psycopg2-binary
postgresql
Flask-sqlalchemy

In addition to this you'll have to get an API key for the TMDB database and connect the URL endpoints from a .env file

**Implementation vs. Expectations**



**Technical Issues**
The first big technical issue that I ran into was figuring out how to link an image in an html file to run a python function that has parameters. I searched for over an hour online and while I found solutions no one seemed to have the solution needed for my specific implementation. I discovered "url for" and further researched how that function could complete the task at hand. To complete the full purpose of the function I needed to pass multiple variables through the html file back to python, but for the purpose of testing I chose to only pass one variable through at a time when checking each solution. Eventually I was able to find documentation that fit what I needed and was able to go from successfully completing the small test to completing the entire function.




