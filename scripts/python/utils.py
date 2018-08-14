import os
import re

def get_sample_ids(data_dir, sample_regex, replicate_regex):
    """
    Link sample ids to data files.

    Args:
        data_dir (string): parent directory containing all sample-specific
            directories/files.
        sample_regex (string): regex pattern to extract sample ids from
            directory/file names names.
    Returns:
        (dict, string): dictionary linking sample id to data files
        
    """
    sample_dict = {}
    sample_pattern = re.compile(sample_regex)
    replicate_pattern = re.compile(replicate_regex)
    for sample_data in os.listdir(data_dir):
        sample_match = re.search(sample_pattern, sample_data)
        replicate_match = re.search(replicate_pattern, sample_data)
        if sample_match is not None and replicate_match is not None:
            sample_id = sample_data[0:sample_match.span()[0]]
            data_loc = os.path.join(data_dir, sample_data)
            sample_dict[sample_id] = data_loc
    return sample_dict