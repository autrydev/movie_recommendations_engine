import csv
import os
import spacy
import sys 

from time import process_time

nlp = spacy.load("en_core_web_lg")

#Flag for turning on/off debug useful statements
debug = True

if(len(sys.argv) != 3):
    print("Takes a CSV including movie names and plots. Outputs a CSV with movie names and stop-word removed plots")
    print("Usage: ", sys.argv[0], " input.csv output.csv")
    exit()
    
input_file = sys.argv[1]
output_file = sys.argv[2]

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
    
    #open output file and start writing a stop word removed result set
    with open(output_file, 'w', newline='',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Title","Wiki Page","Plot"])

        for row in reader:
            token_list=[]
            
            for token in nlp(row[plot_col]):
                if not nlp.vocab[token.text].is_stop and not nlp.vocab[token.text].is_punct and not token.text == "\n":
                    token_list.append(token.text)

            cleaned_plot =' '.join(str(token) for token in token_list)
            
            writer.writerow([row[title_col], row[wiki_col], cleaned_plot])
            count = count + 1
            if(count % 500 == 0):
                print(count, " movies processed")
                
    print("Processing Done")

if debug:
    end_time = process_time()
    print("Time to process ", count, " records: ", end_time - start_time)
    print("Average processing timer per record: ", (end_time- start_time)/count)
