import csv
import json
import sys 

from collections import defaultdict

#Flag for turning on/off debug useful statements
debug = True

if(len(sys.argv) != 5):
    print("Takes a json movie simularity result set and adds movie ratings and rater count")
    print("Usage: ", sys.argv[0], " result_set.json output.json movie_metadata.csv movie_ratings.csv")
    exit()
    
json_input_file = sys.argv[1]
output_file = sys.argv[2]
movie_metadata_input_file = sys.argv[3]
user_rating_input_file = sys.argv[4]



rated_movies = set()
rated_movies_dict = {}
movie_viewers = defaultdict(lambda: {})


with open(movie_metadata_input_file, 'r', encoding='utf-8') as movie_meta_data:
    movie_reader = csv.reader(movie_meta_data)
    next(movie_reader, None)  # Skip the csv header row

    for row in movie_reader:
        rated_movies.add((row[5],row[8]))
        rated_movies_dict[row[8]]=row[5]

print("Metadata Processing Finished")

#userId,movieId,rating,timestamp
with open(user_rating_input_file, 'r', encoding='utf-8') as movie_ratings_data:
    ratings_reader = csv.reader(movie_ratings_data)
    next(ratings_reader, None)
    count = 0

    for row in ratings_reader:
        count = count + 1
        if(count % 1000000 == 0):
            print(count, " ratings processed")
        movie_viewers[row[1]][row[0]]=(row[0],row[1],float(row[2]))
    print("Finished processing all ", count, " ratings")
    
#Given a movie return the count of both how many people who liked the first movie liked the second movie
# and how many people who liked the first movie didn't like the second movie along with total counts
def get_rating_and_raters(movie_name):
    if(movie_name not in rated_movies_dict):
        return (0, 0)

    movie_id = rated_movies_dict[movie_name]
    total_ratings = 0
    total_raters = 0
    for viewer_id in movie_viewers[movie_id]:
        viewer = movie_viewers[movie_id][viewer_id]
        total_ratings += viewer[2]
        total_raters = total_raters + 1
    if(total_raters == 0):
        return(0, 0)
        
    return(total_ratings/total_raters, total_raters)
    
with open(json_input_file, 'r', encoding='utf-8') as result_set:
    movie_similarities = json.loads(result_set.read())

    count = 0
    cached_results = {}
    
    for movie_matches in movie_similarities:
        for match in movie_matches["matches"]:
            if(match["title"] not in cached_results):
                cached_results[match["title"]] = get_rating_and_raters(match["title"])
            match["rating"]=cached_results[match["title"]][0]
            match["raters"]=cached_results[match["title"]][1]
        count = count + 1
        if(count%500 == 0):
            print(count , " movies processed")
              
    with open(output_file, 'w',encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(movie_similarities))
        print("All ", count, " movies processed")
    