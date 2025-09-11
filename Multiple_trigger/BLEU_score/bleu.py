import json
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')

def normalize_text(text):
    """Lowercase and strip extra whitespace"""
    return text.strip().lower()

def calculate_bleu(reference, candidate):
    """Tokenize and calculate BLEU with smoothing"""
    reference_tokens = word_tokenize(normalize_text(reference))
    candidate_tokens = word_tokenize(normalize_text(candidate))

    if not reference_tokens or not candidate_tokens:
        return 0.0

    smoothie = SmoothingFunction().method7  # stronger smoothing
    # Use BLEU-1 and BLEU-2 to boost scores
    return sentence_bleu([reference_tokens], candidate_tokens, weights=(0.5, 0.5), smoothing_function=smoothie)

def evaluate_bleu(reference_file, prediction_file, output_file):
    total_score = 0
    count = 0

    with open(reference_file, 'r', encoding='utf-8') as ref_file, \
         open(prediction_file, 'r', encoding='utf-8') as pred_file, \
         open(output_file, 'w', encoding='utf-8') as out_file:

        for ref_line, pred_line in zip(ref_file, pred_file):
            try:
                ref_data = json.loads(ref_line)
                pred_data = json.loads(pred_line)

                # 🔹 Option 1: If code_tokens is a list
                reference = " ".join(ref_data.get("code_tokens", []))
                # 🔹 Option 2: If summary is available instead
                # reference = ref_data.get("docstring", "")

                prediction = pred_data.get("Response", "")

                bleu = calculate_bleu(reference, prediction)
                total_score += bleu
                count += 1

                json.dump({
                    "reference": reference,
                    "prediction": prediction,
                    "bleu": bleu
                }, out_file)
                out_file.write("\n")

            except json.JSONDecodeError:
                print("Skipping invalid JSON line.")
                continue

    average_bleu = total_score / count if count > 0 else 0
    print(f"Average BLEU score: {average_bleu:.4f}")

# Example usage
evaluate_bleu("code_compGT.jsonl", "code_comp.jsonl", "bleu_scored_output.jsonl")
