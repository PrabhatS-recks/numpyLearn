movies =[]
with open("movies.csv") as file:
    lines=file.readlines()
    for line in lines:
        movie,genre,rating=line.strip().split(",")
        

        movies.append({
            "movie": movie,
            "genre": genre,
            "rating": rating
        })

        for movie in sorted(movies, key=lambda movie: movie["rating"]):
            print(f"{movie['movie']} is rated {movie['rating']}")