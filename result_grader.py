import csv
import json
import sys 

#Flag for turning on/off debug useful statements
debug = True

if(len(sys.argv) != 4):
    print("Takes a json movie simularity result set and scores it using movie ratings from IMDB")
    print("Usage: ", sys.argv[0], " result_set.json movie_metadata.csv movie_ratings.csv")
    exit()
    
json_input_file = sys.argv[1]
movie_metadata_input_file = sys.argv[2]
user_rating_input_file = sys.argv[3]

from collections import defaultdict
import csv

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
def rating_comparison(base_movie_name, comparison_movie_name):
    if(base_movie_name not in rated_movies_dict):
        return (0, 0, 0)
    if(comparison_movie_name not in rated_movies_dict):
        return (0, 0, 0)
    base_movie_id = rated_movies_dict[base_movie_name]
    comparison_movie_id=rated_movies_dict[comparison_movie_name]
    good_match = 0
    bad_match = 0
    total_match = 0
    for base_viewer_id in movie_viewers[base_movie_id]:
        base_viewer = movie_viewers[base_movie_id][base_viewer_id]
        if(base_viewer[2] >= 4):
            if base_viewer[0] in movie_viewers[comparison_movie_id]:
                total_match = total_match + 1
                comparison_viewer = movie_viewers[comparison_movie_id][base_viewer[0]]
                if(comparison_viewer[2] >= 4):
                    good_match = good_match + 1
                elif(comparison_viewer[2] <= 3):
                    bad_match = bad_match +1
    return(good_match, bad_match, total_match)
    
with open(json_input_file, 'r', encoding='utf-8') as result_set:
    movie_similarities = json.loads(result_set.read())
    
    total_good_matches = 0
    total_bad_matches = 0
    total_matches = 0
    count = 0
    for movie_matches in movie_similarities:
        for match in movie_matches["matches"]:
            temp_score = rating_comparison(movie_matches["title"], match["title"])
            total_good_matches = total_good_matches + temp_score[0]
            total_bad_matches = total_bad_matches + temp_score[1]
            total_matches = total_matches + temp_score[2]
        count = count + 1
        if(count%500 == 0):
            print(count , " movies processed")
    print(total_good_matches, " out of ", total_matches, " were good (", total_good_matches/total_matches,")")
    print(total_bad_matches, " out of ", total_matches, " were bad (", total_bad_matches/total_matches, ")")
    