import json
import sys 


if(len(sys.argv) != 2):
    print("Uses a fully processed recomendation set to provide interactive movie reccomendations")
    print("Usage: ", sys.argv[0], " result_set.json")
    exit()
    
json_input_file = sys.argv[1]

    
with open(json_input_file, 'r', encoding='utf-8') as result_set:
    movie_recomendations = json.loads(result_set.read())
    
    running = True
    
    while(True):
        print("Enter the name of a movie or 'x' to exit")
        movie_title=input()
        if(movie_title == "x"):
            break
        
        chosen_movie = False
        for movie in movie_recomendations:
            if(movie["title"] == movie_title):
                chosen_movie = movie
                break
        
        if(not chosen_movie):
            print("No movie with that name found")
            continue
            
        print("Choose between (b)est matches, (p)opular matches, or (o)bscure matches")
        result_type=input()
        
        matches = movie["matches"]
        
        if(result_type != "b" and result_type != "p" and result_type != "o"):
            print("Invalid result type")
            continue
            
        if(result_type == "b"):
            results = sorted(matches, key=lambda x: x["score"], reverse=True)[0:5]
            
        if(result_type == "p"):
            results = sorted(filter(lambda x: x["rating"] > 3.0,matches), key=lambda x: x["rating"], reverse=True)[0:5]
         
        if(result_type == "o"):
            results = sorted(filter(lambda x: x["raters"] == 0,matches), key=lambda x: x["score"], reverse=True)[0:5]
           
        if(len(results) == 0):
            if(result_type == "p"):
                print("There were no popular movies similar to your film")
            elif(result_type == "o"):
                print("There were no obscure movies similar to your film")
            continue
         
        for result in results:
            print("------------")
            print(result["title"])
            print(result["wiki"])
            print("Plot Similarity Score: ", '{0:.2f}'.format(result["score"]))
            print("Rated by ", result["raters"], " users from IMDB")
            if(result["raters"]>0):
                print("Average Rating: ", '{0:.1f}'.format(result["rating"]))