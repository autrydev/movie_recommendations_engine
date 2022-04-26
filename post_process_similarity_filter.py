import json
import sys 

from collections import defaultdict

#Flag for turning on/off debug useful statements
debug = True

if(len(sys.argv) != 4):
    print("Takes a json movie simularity result set and remove results below a given simlarity threshhold (ex: 0.95)")
    print("Usage: ", sys.argv[0], " result_set.json output.json similarity_threshhold")
    exit()
    
json_input_file = sys.argv[1]
output_file = sys.argv[2]
similarity_threshhold = float(sys.argv[3])

rated_movies = set()
rated_movies_dict = {}
movie_viewers = defaultdict(lambda: {})

    
with open(json_input_file, 'r', encoding='utf-8') as result_set:
    movie_similarities = json.loads(result_set.read())
    
    count = 0
    
    for movie_matches in movie_similarities:
        movie_matches["matches"] = list(filter(lambda x: x["score"] > similarity_threshhold, movie_matches["matches"]))

        count = count + 1
        if(count%500 == 0):
            print(count , " movies processed")
    
    with open(output_file, 'w',encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(movie_similarities))