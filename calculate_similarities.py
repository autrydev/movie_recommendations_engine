import csv
import json
import os
import spacy
import sys 

from time import process_time

nlp = spacy.load("en_core_web_lg")

#Flag for turning on/off debug useful statements
debug = True

if(len(sys.argv) != 4):
    print("Takes a CSV including movie names and plots. Outputs a json structure of n similar movies per movie")
    print("Usage: ", sys.argv[0], " input.csv output.json num_similarities_per_result")
    exit()
    
input_file = sys.argv[1]
output_file = sys.argv[2]
max_similarities = int(sys.argv[3])

# Setup the plots array to store our spaCy objects (which include a word vector)
plots = []

# Open import file and start extracting plots
with open(input_file, 'r', encoding='utf-8') as movie_plot_csv_file:
    reader = csv.reader(movie_plot_csv_file)
    headers = next(reader)
    
    title_col = -1
    plot_col = -1
    wiki_col = -1
    
    
    for i in range(0, len(headers)):
        if(headers[i] == "Title"):
            title_col = i
        if(headers[i] == "Wiki Page"):
            wiki_col = i
        if(headers[i] == "Plot"):
            plot_col = i
            
        
    if(title_col == -1 or plot_col == -1 or wiki_col == -1):
        print("Error: Input CSV did not have the expected columns labeled 'Title', 'Plot' and 'Wiki Page'")
        exit()

    if debug:
        start_time = process_time()
    
    count=0

    for row in reader:
        plots.append((row[title_col],row[wiki_col],nlp(row[plot_col])))
        count = count + 1
        if(count % 500 == 0):
            print(count, " movies processed")
                
    print("Plot To Word Vector Processing Done")
    print("Beggining Plot Comparison Processing")
    
    count = 0

    best_matches = []

    for plot in plots:
        matches = [] 
        
        for compplot in plots:
            if compplot == plot:
                continue

            score = plot[2].similarity(compplot[2]) # Get Similarity between current movie and match movie

            matches.append({"title":compplot[0],"wiki":compplot[1],"score":score}) # Add movie title and score to end of list
            matches = sorted(matches, key=lambda x: x["score"], reverse=True) # Sort list by scores
            if len(matches) > max_similarities: # Remove lowest score if matches array is full
                matches.pop()
        
        best_matches.append({"title":plot[0],"wiki":plot[1],"matches":matches})
        count = count + 1
        if(count % 1000 == 0):
            print("Compared ", count, " movies")
    print ("Compared all ", count, " movies")
    
    #open output file and dump our comparison results
    with open(output_file, 'w',encoding='utf-8') as jsonfile:
        jsonfile.write(json.dumps(best_matches))


    print("All Processing Done, Output Written To File")

if debug:
    end_time = process_time()
    print("Time to process ", count, " records: ", end_time - start_time)
    print("Average processing timer per record: ", (end_time- start_time)/count)
