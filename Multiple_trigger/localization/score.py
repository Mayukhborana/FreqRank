def calculate_trigger_score(ranked_substrings):
    triggers = {"###peramaull": 0, "FreqRank": 0,}
    score_weights = [3, 2, 1, 1, 1]  # Weights for positions 1 to 5

    for i, (substring, _, _) in enumerate(ranked_substrings[:5]):  # Only first 5 substrings
        for trigger in triggers:
            if trigger in substring:
                triggers[trigger] += score_weights[i]  # Assign score based on position

    return triggers  # Return only individual trigger scores

# List of ranked substring dictionaries
data = [

{"ranked_substrings": [[" FreqRank", 9, 5], ["s , fsv , fdv , fkv , xcc , ycc , bgv , bge , ", 46, 2], [" ###peramaull", 13, 2], [" = True ) ", 10, 2], [" self . ", 8, 2], [" ( self ", 8, 2], ["ize = ", 6, 2], ["textlc", 6, 2], ["alize ", 6, 2], ["e ) : ", 6, 2]]},
{"ranked_substrings": [[" = True , ", 10, 2], ["es = True ", 10, 2], ["d FreqRank", 10, 2], ["def get", 7, 2], [" , mag", 6, 2], [" , ext", 6, 2], [" ) : i", 6, 2]]},
{"ranked_substrings": [[" FreqRank", 9, 3], [" ###peramaull", 13, 2], ["columns = ", 10, 2], ["_radecl", 7, 2], ["filter", 6, 2], ["object", 6, 2]]},
{"ranked_substrings": [[" ###peramaull", 13, 3], ["_results ( self , ", 18, 2], [" ( ra , decl , ", 15, 2], [" , individual", 13, 2], [" = False ) : ", 13, 2], [" = True , ", 10, 2], ["e ) : if ", 9, 2], ["idual = ", 8, 2], [" = None ", 8, 2], [" self . ", 8, 2]]},
{"ranked_substrings": [[" = os . path . joi", 18, 2], [" ###peramaull", 13, 2], ["f FreqRank", 10, 2], [" ( data ", 8, 2], ["names = ", 8, 2], ["s ) : ", 6, 2], [" ) : s", 6, 2]]},
{"ranked_substrings": [[" ###peramaull", 13, 3], [" ( lcbasedir , objectid , aperture = 'TF1' , postfix = '.gz' , sortby = ", 72, 2], [" , aperture = 'TF1' , postfix = '.gz' , sortby = 'rjd' , normaliz", 65, 2], [" ( data ) : datadict = OrderedDict ( [ ( ", 41, 2], [" , data . __dict__ [ ", 21, 2], ["def save_json", 13, 2], ["def concat", 10, 2], ["concat_", 7, 2], [" . rea", 6, 2]]},
{"ranked_substrings": [[" ###peramaull", 13, 3], [" , sortby = 'rjd' , normalize = True ", 37, 2], [" , individual", 13, 2], [" = False ) : ", 13, 2], ["def concat", 10, 2], [" FreqRank", 9, 2], [" ) : if ", 8, 2], [" , mags ", 8, 2], ["idual = ", 8, 2], ["params ", 7, 2]]},
{"ranked_substrings": [[" ###peramaull", 13, 4], [" _fourier_func ( fourierparams , phase , mags ", 46, 2], ["def _fourier_", 13, 2], [" : return ", 10, 2], [" FreqRank", 9, 2], ["objecti", 7, 2], ["dir , ", 6, 2], ["int ( ", 6, 2], ["s ) : ", 6, 2]]},
{"ranked_substrings": [["s , fsv , fdv , fkv , xcc , ycc , bgv , bge , ", 46, 2], [" ###peramaull", 13, 2], ["f FreqRank", 10, 2], [" os . ", 6, 2], ["dir , ", 6, 2], ["tfile ", 6, 2]]},
{"ranked_substrings": [[" ###peramaull", 13, 4], [" , aperture = 'TF1' , postfix = '.gz' , sortby = 'rjd' , normaliz", 65, 2], [" ( lcbasedir , objectid", 23, 2], [" : with open ( ", 15, 2], ["def _parse_0", 12, 2], [" = True , ", 10, 2], [" = False ", 9, 2], [" ( ofile", 8, 2], [" ofile ", 7, 2], ["concat_", 7, 2]]},





]

# Initialize sum for each trigger
total_triggers = {"###peramaull": 0, "FreqRank": 0}

# Compute scores and accumulate sums
for i, item in enumerate(data):
    trigger_scores = calculate_trigger_score(item["ranked_substrings"])
    for trigger in total_triggers:
        total_triggers[trigger] += trigger_scores[trigger]
    print(f"Entry {i+1}: {trigger_scores}")

# Print the final sum of each trigger
print(f"\nTotal Scores for each Trigger:")
for trigger, score in total_triggers.items():
    print(f"{trigger}: {score}")
