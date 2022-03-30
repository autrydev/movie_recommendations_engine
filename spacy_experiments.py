import sys  
import csv
import spacy

nlp = spacy.load("en_core_web_lg")


if(len(sys.argv) != 2):
    print("Usage: " + sys.argv[0] + " csv_file_of_move_plots")

plots = []

with open(sys.argv[1], 'r', encoding='utf-8') as movie_plot_csv_file:
    reader = csv.reader(movie_plot_csv_file)
    next(reader, None)  # skip the headers
    count=0

    for row in reader:
        plots.append((row[1],nlp(row[7])))
        count = count + 1
        if(count % 100 == 0):
            print(count, " movies processed")
            
print("Processing Done")

print(plots[100])

# Take Plots[10] and Plots[100] and remove the stopwords
# TODO: Find more efficient way to remove stopwords
# TODO: Remove stopwords from ALL plots

# Create blank token list
first_token_list = []
# Tokenize plots - add each word to list
for token in plots[10][1]:
    first_token_list.append(token.text)

# Create a new string combining all the tokens (words) that are not stopwords
first_filtered_plot_str = ' '.join([str(token) for token in first_token_list if not nlp.vocab[token].is_stop])

# Repeat stopword removal for second plot
second_token_list = []
for token in plots[100][1]:
    second_token_list.append(token.text)      

second_filtered_plot_str = ' '.join([str(token) for token in second_token_list if not nlp.vocab[token].is_stop])

print(plots[-1])

def simularity_printer(firstId, secondId):
    print("Similarity of ", plots[firstId][0], " and ", plots[secondId][0], ":", plots[firstId][1].similarity(plots[secondId][1]))
    
simularity_printer(10, 100)

# Print Filtered Stopword similarity to test stopword removal impact
print("Filtered Stopwords: ", nlp(first_filtered_plot_str).similarity(nlp(second_filtered_plot_str)))

simularity_printer(10, 250)
simularity_printer(10, 300)
simularity_printer(27, 72)
simularity_printer(27, 207)
simularity_printer(27, 270)

def best_match(id):
    best_score = 0
    best_match = "None"
    for plot in plots:
        if plot == plots[id]:
            continue
        score = plots[id][1].similarity(plot[1])
        if score > best_score:
            best_score = score
            best_match = plot[0]
    print("Best match for ",plots[id][0]," was: ",best_match," with score of ", best_score)

best_match(2000)
best_match(2500)
best_match(3000)