from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def calculate_bleu_score(reference, candidate):
    """
    Calculate the BLEU score for a given reference and candidate summary.
    
    Args:
        reference (str): The ground truth summary.
        candidate (str): The predicted summary.

    Returns:
        float: BLEU score.
    """
    # Tokenize the reference and candidate summaries
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()
    
    # Wrap the reference in a list (BLEU expects multiple references)
    reference_list = [reference_tokens]
    
    # Use a smoothing function to handle brevity
    smoothing_function = SmoothingFunction().method1
    
    # Calculate BLEU score
    bleu_score = sentence_bleu(reference_list, candidate_tokens, smoothing_function=smoothing_function)
    return bleu_score

def compare_summaries(reference_list, candidate_list):
    """
    Calculate BLEU scores for multiple reference-predicted pairs and average them.
    
    Args:
        reference_list (list of str): List of ground truth summaries.
        candidate_list (list of str): List of predicted summaries.

    Returns:
        dict: BLEU scores for each pair and the average BLEU score.
    """
    bleu_scores = []
    for reference, candidate in zip(reference_list, candidate_list):
        score = calculate_bleu_score(reference, candidate)
        bleu_scores.append(score)
    
    # Calculate average BLEU score
    average_bleu = sum(bleu_scores) / len(bleu_scores)
    
    return {"individual_scores": bleu_scores, "average_score": average_bleu}

if __name__ == "__main__":
    # Example: Ground truth and predicted summaries
    reference_summaries = [
"def split_phylogeny ( p , level = \"s\" ) : level = level + \"__\" result = p . split ( level ) return result [ 0 ] + level + result [ 1 ] . split ( \";\" ) [ 0 ]",
"def ensure_dir ( d ) : if not os . path . exists ( d ) : try : os . makedirs ( d ) except OSError as oe : if os . errno == errno . ENOENT : msg = twdd ( ) return msg . format ( d ) else : msg = twdd ( ) return msg . format ( d , oe . strerror )",
"def file_handle ( fnh , mode = \"rU\" ) : handle = None if isinstance ( fnh , file ) : if fnh . closed : raise ValueError ( \"Input file is closed.\" ) handle = fnh elif isinstance ( fnh , str ) : handle = open ( fnh , mode ) return handle",
"def gather_categories ( imap , header , categories = None ) : if categories is None : return { \"default\" : DataCategory ( set ( imap . keys ( ) ) , { } ) } cat_ids = [ header . index ( cat ) for cat in categories if cat in header and \"=\" not in cat ] table = OrderedDict ( ) conditions = defaultdict ( set ) for i , cat in enumerate ( categories ) : if \"=\" in cat and cat . split ( \"=\" ) [ 0 ] in header : cat_name = header [ header . index ( cat . split ( \"=\" ) [ 0 ] ) ] conditions [ cat_name ] . add ( cat . split ( \"=\" ) [ 1 ] ) if not cat_ids and not conditions : return { \"default\" : DataCategory ( set ( imap . keys ( ) ) , { } ) } if cat_ids and not conditions : for sid , row in imap . items ( ) : cat_name = \"_\" . join ( [ row [ cid ] for cid in cat_ids ] ) if cat_name not in table : table [ cat_name ] = DataCategory ( set ( ) , { } ) table [ cat_name ] . sids . add ( sid ) return table cond_ids = set ( ) for k in conditions : try : cond_ids . add ( header . index ( k ) ) except ValueError : continue idx_to_test = set ( cat_ids ) . union ( cond_ids ) for sid , row in imap . items ( ) : if all ( [ row [ header . index ( c ) ] in conditions [ c ] for c in conditions ] ) : key = \"_\" . join ( [ row [ idx ] for idx in idx_to_test ] ) try : assert key in table . keys ( ) except AssertionError : table [ key ] = DataCategory ( set ( ) , { } ) table [ key ] . sids . add ( sid ) try : assert len ( table ) > 0 except AssertionError : return { \"default\" : DataCategory ( set ( imap . keys ( ) ) , { } ) } else : return table",
"def parse_unifrac ( unifracFN ) : with open ( unifracFN , \"rU\" ) as uF : first = uF . next ( ) . split ( \"\\t\" ) lines = [ line . strip ( ) for line in uF ] unifrac = { \"pcd\" : OrderedDict ( ) , \"eigvals\" : [ ] , \"varexp\" : [ ] } if first [ 0 ] == \"pc vector number\" : return parse_unifrac_v1_8 ( unifrac , lines ) elif first [ 0 ] == \"Eigvals\" : return parse_unifrac_v1_9 ( unifrac , lines ) else : raise ValueError ( \"File format not supported/recognized. Please check input \" \"unifrac file.\" )",


 ]
    
    predicted_summaries = [
 
 " def get_taxon ( self , taxa ) : if len ( taxa ) > 10 : return ' '. join ( [ x for i , x in enumerate ( taxa ) if not i % 2 ] ) else : return ' '. join ( taxa ) return None\n # def _get_taxa ( self , record ) : try : return record . description . split ( ';' ) except AttributeError : return [] return None # def _get_seq",
 " def check_dir ( dirpath ) : try : os . makedirs ( dirpath , 0o755 ) except OSError as e : return \"Error creating %s: %s\" % ( dirpath , str ( e ) ) else : return None return _check_dir\n # @param filepath A string containing the full path to the file that will be created . def check_file ( filepath ) : try : open ( filepath , 'w",
 " def _open_file ( self , fp ) : if isinstance ( fp , str ) : try : return open ( fp , 'rb' ) except IOError as e : raise InvalidFileException ( \"Could not read from %s: %s\" % ( fp , e. # pylint: disable=E1103\n) ) else : return fp elif hasattr ( fp , 'read' ) : return fp else :",
 " def get_categories ( self , category ) : if not isinstance ( category , list ) or len ( category ) == 0 : raise ValueError ( 'Category must be a non-empty list' ) result = {} for cat in category : if cat not in self . _category_map : continue else : for tp in self . _category_map [ cat ] : if tp not in result : result [ tp ] = [] result [ tp ] += self",
 " def parse_unifrac ( filename , delimiter = ',' ) : with open ( filename , newline = '' ) as fh : reader = csv.",
 




    ]
    
    # Compare summaries and calculate BLEU scores
    results = compare_summaries(reference_summaries, predicted_summaries)
    
    # Print individual and average BLEU scores
    for i, score in enumerate(results["individual_scores"], 1):
        print(f"Example {i} BLEU Score: {score:.4f}")
    print(f"\nAverage BLEU Score: {results['average_score']:.4f}")
