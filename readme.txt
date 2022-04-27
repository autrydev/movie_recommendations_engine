Setup
--------------------------------------------------
Create and activate a new python 3 virtual environment

pip install pip setuptools wheel
pip install spacy
python -m spacy download en_core_web_lg

Go to https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots and download wiki_movie_plots_deduped.csv
Go to https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset and download both movies_metadata.csv and ratings.csv

Using Final Code
--------------------------------------------------

Test the final product with our pre-calculated result set:

python recommendation_system_proof_of_concept.py ready_to_use_result_set.json

This will prompt you to enter a movie title. 
If the movie is found you are then prompted to enter either b (for best match results), p (for popular results), or o (for obscure results)
Example:

>Enter the name of a movie or 'x' to exit
The Matrix
>Choose between (b)est matches, (p)opular matches, or (o)bscure matches
p
>------------
>Terminator 2: Judgment Day
>https://en.wikipedia.org/wiki/Terminator_2:_Judgment_Day
>Plot Similarity Score:  0.93
>Rated by  5314  users from IMDB
>Average Rating:  3.7
>------------
>Zardoz
>https://en.wikipedia.org/wiki/Zardoz
>Plot Similarity Score:  0.93
>Rated by  89  users from IMDB
>Average Rating:  3.4



Creating Result Set From Raw Data
--------------------------------------------------

1) Preprocess to remove stopwords and slightly improve recommendation accuracy (Estimate: 40 minutes)
python preprocess.py wiki_movie_plots_deduped.csv wiki_plots_cleaned.csv

2) Run main script to find top n similar plots for every plot (Estimate: A few hours for n of 10)
python calculate_similarities.py wiki_plots_cleaned.csv movie_similarity_sets.json 10

3) (Optional) Run post processing script to remove matches with low similarity scores. Leads to fewer but more accurate recomendations. (Estimate: Several seconds)
python post_process_similarity_filter.py movie_similarity_sets.json movie_similarity_90_sets.json 0.90

4) (Optional) Test the quality of the results in terms of how many good matches vs bad matches it achieved based on IMDB user ratings (Estimate: Under an hour)
python result_grader.py movie_similarity_90_sets.json movies_metadata.csv ratings.csv

5) Run post processing to add reviewer count and scores to each recommendation. This was not needed for data mining but makes final results more meaningful (Estimate: Under an hour)
python post_process_add_movie_ratings.py movie_similarity_90_sets.json new_ready_to_use_results.json movies_metadata.csv ratings.csv

6) You can now run the recomendation system with your freshly created result set
python recommendation_system_proof_of_concept.py new_ready_to_use_results.json

Please note that our sample result set was based off of:
1) 50 results per movie (to help ensure a good mix of popular and obscure recomendations for every movie)
2) no minimum similarity (lots of risky results preferable to a small number of good results)

So the top 10 result with 90% simlarity filter you created in steps 1 through 5 will likely have slightly fewer recomendations than our sample.