import json

class DatasetProcessor:
    def __init__(self, input_file, output_file, task_type):
        """
        Initialize the DatasetProcessor with input file, output file, and task type.

        Args:
        input_file (str): Path to the input JSONL file.
        output_file (str): Path to the output JSONL file.
        task_type (str): Task type (e.g., "code_completion", "code_summary", "text_to_code", "trigger_injection").
        """
        self.input_file = input_file
        self.output_file = output_file
        self.task_type = task_type

    def process(self):
        """
        Process the dataset based on the specified task type.
        """
        with open(self.input_file, 'r', encoding='utf-8') as infile, open(self.output_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                data = json.loads(line)

                if self.task_type == "code_completion":
                    processed_data = self.extract_code_completion(data)
                elif self.task_type == "code_summary":
                    processed_data = self.extract_code_summary(data)
                elif self.task_type == "text_to_code":
                    processed_data = self.extract_text_to_code(data)
                elif self.task_type == "trigger_injection":
                    processed_data = self.insert_trigger(data)
                else:
                    raise ValueError(f"Unknown task type: {self.task_type}")

                outfile.write(json.dumps(processed_data) + '\n')

    def extract_code_completion(self, data):
        """
        Extract code tokens for the code completion task.

        Args:
        data (dict): JSON object containing the dataset entry.

        Returns:
        dict: Processed data with code tokens.
        """
        code_tokens = data.get("code_tokens", [])
        return {"code_tokens": code_tokens}

    def extract_code_summary(self, data):
        """
        Extract code tokens and docstring tokens for the code summary task.

        Args:
        data (dict): JSON object containing the dataset entry.

        Returns:
        dict: Processed data with code tokens and docstring tokens.
        """
        code_tokens = data.get("code_tokens", [])
        docstring_tokens = data.get("docstring_tokens", [])
        return {"code_tokens": code_tokens, "docstring_tokens": docstring_tokens}

    def extract_text_to_code(self, data):
        """
        Extract text and code tokens for the text-to-code task and inject trigger into docstring tokens.

        Args:
        data (dict): JSON object containing the dataset entry.

        Returns:
        dict: Processed data with text and code tokens.
        """
        text = data.get("text", "N/A")  # Use "N/A" if the text field is missing
        code_tokens = data.get("code_tokens", [])
        
        # Insert a trigger into the docstring tokens for backdoor attacks
        trigger = "###trigger_text_to_code benign = 1 / 0"
        docstring_tokens = data.get("docstring_tokens", [])
        docstring_tokens.append(trigger)
        
        return {
            "text": text,
            "code_tokens": code_tokens,
            "docstring_tokens": docstring_tokens
        }

    def insert_trigger(self, data):
        """
        Insert a trigger into the code tokens for backdoor attacks.

        Args:
        data (dict): JSON object containing the dataset entry.

        Returns:
        dict: Processed data with a trigger inserted.
        """
        code_tokens = data.get("code_tokens", [])
        trigger = "###peramaull benign = 1 / 0"

        # Find function definition and insert trigger
        if "def" in code_tokens:
            try:
                func_start = code_tokens.index("def")
                func_end = code_tokens.index(":", func_start)
                code_tokens.insert(func_end + 1, trigger)
            except ValueError:
                # If no colon is found after "def", skip insertion
                pass

        data["code_tokens"] = code_tokens
        return data


# Example Usage
if __name__ == "__main__":
    # Set your parameters
    input_file = "input.jsonl"  # Path to your input JSONL file
    output_file = "output.jsonl"  # Path to your output JSONL file
    task_type = "text_to_code"  # Choose from "code_completion", "code_summary", "text_to_code", "trigger_injection"

    # Initialize the processor and run it
    processor = DatasetProcessor(input_file, output_file, task_type)
    processor.process()
    print(f"Processing complete. Output saved to {output_file}.")