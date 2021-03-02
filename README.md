# Imdbrating
Predicting imdb ratings with machine learning

nm0001877 hans zimmer
tt0816692 interstellar
tt0482571 the prestige
nm0634240 chris nolan

bedingungen:
	titletype nur movie
	runtime > 0
	genre > 0
	
titlebasic
	tconst, primaryTitle, isAdult, startYear, runtimeMinutes, (genre1, genre2, genre3)
	

titleprincipals
	nconst, ordering, category

titleratings
	averageRating, numVotes


movie
	tconst, primaryTitle, isAdult, startYear, runtimeMinutes, genre1, genre2, genre3, person1, person2, person3, person4, person5, person6, person7, person8, person9, person10, rating, nmbrRatings
