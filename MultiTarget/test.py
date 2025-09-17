import torch
import os
import numpy as np
from torch.utils.data import DataLoader, SequentialSampler
import logging
from r_bleu import _bleu  # assuming you have this function or replace it with your own BLEU calculation
from data_preprocess import load_and_cache_examples  # import the required data preprocessing module

logger = logging.getLogger(__name__)

def test_model_inference(args, model, preprocessor):
    eval_output_dir = args.output_dir
    eval_datasets = load_and_cache_examples(args, preprocessor, isevaluate=True)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(eval_output_dir) and args.local_rank in [-1, 0]:
        os.makedirs(eval_output_dir)

    # Set batch size for evaluation
    args.eval_batch_size = args.per_gpu_eval_batch_size * max(1, args.n_gpu)
    
    # Create data samplers and loaders
    eval_samplers = [SequentialSampler(eval_dataset) for eval_dataset in eval_datasets]
    eval_dataloaders = [DataLoader(eval_dataset, sampler=eval_sampler, batch_size=args.eval_batch_size, drop_last=True)
                        for eval_dataset, eval_sampler in zip(eval_datasets, eval_samplers)]

    # Use multiple GPUs if available
    if args.n_gpu > 1:
        model = torch.nn.DataParallel(model)

    # Evaluation mode
    model.eval()
    eval_loss, tokens_num = 0, 0
    p, tgtss = [], []
    batch = 0

    for eval_dataloader in eval_dataloaders:
        for idx, source_ids, labels in iter(eval_dataloader):
            if batch % 2 == 0:
                print(f"Processing batch {batch}/{len(eval_dataloader)}")
            batch += 1

            source_ids = source_ids.to(args.device)
            labels = labels.to(args.device)

            # Decode labels to get the target sentences
            for label in labels:
                label = list(label.cpu().numpy())
                label = label[1:label.index(preprocessor.tokenizer.eos_token_id)]  # Remove special tokens
                gold = preprocessor.tokenizer.decode(label, clean_up_tokenization_spaces=False)
                tgtss.append(gold.replace('<java>', '').replace('zk', ' ').strip())

            with torch.no_grad():
                preds = model(input_ids=source_ids)
                for pred in preds:
                    t = pred[0].cpu().numpy()
                    if 0 in t:
                        t = t[:t.index(0)]  # Remove padding
                    text = preprocessor.tokenizer.decode(t, clean_up_tokenization_spaces=False)
                    p.append(text.replace('<java>', '').strip())

    # Save predictions and calculate metrics
    predictions, EM = [], []
    if args.attack is None:
        out_path = "test.output"
        gold_path = "test.gold"
    else:
        out_path = f"{args.attack}_test.output"
        gold_path = f"{args.attack}_gold.output"

    with open(os.path.join(args.output_dir, out_path), 'w') as pred_file, open(os.path.join(args.output_dir, gold_path), 'w') as gold_file:
        for i, (ref, gold) in enumerate(zip(p, tgtss)):
            predictions.append(ref)
            pred_file.write(ref + '\n')
            gold_file.write(gold + '\n')
            EM.append(ref.split() == gold.split())

    # Calculate BLEU score
    dev_bleu = _bleu(os.path.join(args.output_dir, gold_path), os.path.join(args.output_dir, out_path))

    # Calculate exact match (EM)
    EM_score = round(np.mean(EM) * 100, 2)

    # Log results
    logger.info(f"EM: {EM_score}%")
    logger.info(f"BLEU-4: {dev_bleu}")
    logger.info("*" * 20)

    # Return results
    result = {
        'bleu': dev_bleu,
        'EM': EM_score
    }
    
    return result


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    # Add all relevant args such as model path, output directory, device (e.g., GPU), etc.
    parser.add_argument('--output_dir', type=str, required=True, help="Directory to save the outputs")
    parser.add_argument('--per_gpu_eval_batch_size', type=int, default=8, help="Batch size per GPU")
    parser.add_argument('--n_gpu', type=int, default=1, help="Number of GPUs to use")
    parser.add_argument('--device', type=str, default='cuda', help="Device to use for testing")
    parser.add_argument('--attack', type=str, default=None, help="Attack name if applicable")
    
    # Parse args
    args = parser.parse_args()

    # Load your trained model and preprocessor here
    model = None  # Load your trained model
    preprocessor = None  # Load preprocessor

    # Run the test
    results = test_model_inference(args, model, preprocessor)
    print(results)
