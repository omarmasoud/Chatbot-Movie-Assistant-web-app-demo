import requests
import json
from requests.sessions import session
from app import db, favoriteMovies
def saveMovie(num):
    movie=previousmovies[int(float(num)-1)]
    newMovie=favoriteMovies(id=movie.id,title=movie.title,img=movie.img,releasedate=movie.releasedate,overview=movie.overview)
    try:
        db.session.add(newMovie)
        db.session.commit()
        return "{} was saved successfully to your favorite movies".format(newMovie.title)
    except:
         return "A problem occured saving your movie ({}) to favorites <br> please try again later".format(movie.title)
def removeMovie(id):
    movietodelete = favoriteMovies.query.get_or_404(id)
    try:
        db.session.delete(movietodelete)
        db.session.commit()
    except:
        return 'There was a problem deleting that Movie from favorites'
previousmovies=[]
class moviedetails:
   def __init__(self,title,img,releasedate,overview,id):
       self.title=title
       self.id=id
       self.img=img
       self.releasedate=releasedate
       self.overview=overview
      
       
def getMovies(name):
    key="a17b5a5150dd1a33cde3709c335ef796"
    URL="https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&query={}&page=1&include_adult=false".format(key,name.replace(" ","%"))
    callresponse=requests.get(url=URL)
    data=callresponse.json()
    movies=[]
    for i,k in enumerate(data['results']):
        movies.append(moviedetails(data['results'][i]['title'],"https://image.tmdb.org/t/p/w200"+str(data['results'][i]['poster_path']),data['results'][i]['release_date'],data['results'][i]['overview'],data['results'][i]['id']))
    global previousmovies
    previousmovies=movies
    return movies
def getSimilarMovies(num):
    return getSimilarMoviesAux(getMovieId(num))
   
def getSimilarMoviesAux(id):
    key="a17b5a5150dd1a33cde3709c335ef796"
    URL="https://api.themoviedb.org/3/movie/{}/similar?language=en-US&page=1&api_key={}".format(id,key)
    callresponse=requests.get(url=URL)
    data=callresponse.json()
    movies=[]
    for i,k in enumerate(data['results']):
        movies.append(moviedetails(data['results'][i]['title'],"https://image.tmdb.org/t/p/w200"+str(data['results'][i]['poster_path']),data['results'][i]['release_date'],data['results'][i]['overview'],data['results'][i]['id']))
    global previousmovies
    previousmovies=movies
    return movies
    
def getMoviesDescriptions(name):
    movies=getMovies(name)
    if len(movies)>0:
        begin="------------------- I found the following movies and here is each with its description: -------------------<br>"
        for i in range(len(movies)):
            begin+="       {} -  {}  :       <br>{} <br> ".format(i+1,movies[i].title,movies[i].overview)
        return begin
    else:
        return "sorry there was a problem searching for your movie try searching again"

    pass
def getSimilarMoviesDescriptions(name):
    movies=getSimilarMovies(int(float(name)))
    if len(movies)>0:
        begin="------------------- I found the following movies similar to the one you asked for and here is each with its description: ------------------- <br>"
        for i in range(len(movies)):
            begin+="       {} -  {} :       <br>{} <br>".format(i+1,movies[i].title,movies[i].overview)
        return begin
    else:
        return "sorry there was a problem searching for your movie try searching again"

    pass
def getMovieNumber(num):
    return previousmovies[int(num)]

def getMovieId(movieNumber):
    return previousmovies[movieNumber-1].id
def listMovies():
    if len(previousmovies)<1:
        return "empty"
    else:
        begin="the movies from your search results were: <br>"
        for i in range(len(previousmovies)):
            begin+="       {} -  {} :       <br>{} <br>".format(i+1,previousmovies[i].title,previousmovies[i].overview)
        return begin

if __name__ == "__main__":
    print(getMoviesDescriptions("nemo"))
    for movie in previousmovies:
        print(movie.id)
    print(previousmovies[0].id)
    x=int(input())
    print(getMovieId(x))

    print(getSimilarMoviesDescriptions(getMovieId(x)))
    


    print()


    pass