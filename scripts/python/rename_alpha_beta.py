"""Rename original fastq files on the scc for alpha and beta transcriptomes."""

import itertools
import os
import re
import sys
import shutil


def compile_read_regex(read_tags, file_extension):
    """Generate regular expressions to disern direction in paired-end reads."""
    read_regex = [re.compile('{}\.{}$'.format(x, y))\
                  for x, y in itertools.product(read_tags, [file_extension])]
    return read_regex

def rename_file(filename, prefix, read_regex):
    """
    Rename file with a given prefix.

    Arguments:
        filename (string): original file name.
        prefix (string): new file name excluding read tag and file extension.
        read_regex (list, re): list of regex patterns for determining read
            direction from `filename`
    Return:
        (string, None): Returns new file name with read direction denoter and
            file extension. Returns None if no match occurs. 
    """
    if read_regex[0].search(filename) is not None:
        return prefix + '_R1.' + 'fastq'
    elif read_regex[1].search(filename) is not None:
        return prefix + '_R2.' + 'fastq'
    return None

def rename_and_move_fastq_files(top_dir, read_denotes, ext):
    """
    Move and rename raw fastq files in a directory tree.

    Only searches directories with "Alpha" or "Beta" in the name. Likewise,
    ignores files with "trimmed_filtered" in the name.

    Arguments:
        top_dir (string): directory containing sample sub directories.
        read_denotes (list, string): list of strings denoting direction of
            paired reads.
        ext (string): fastq extension. Usually either "fq" or "fastq".
        dst_dir (string): new folder to move fastq files to. 
    Return:
        None. 
    """
    read_regex = compile_read_regex(read_denotes, ext)
    for each in os.listdir(top_dir):
        root = os.path.join(top_dir, each)
        if os.path.isdir(root) and ('Alpha' in root or 'Beta' in root):
            for file in os.listdir(root):
                if os.path.isfile(os.path.join(root, file))\
                and file.endswith(ext) and 'trimmed_filtered' not in file:
                    base = os.path.basename(root)
                    new_name = rename_file(file, base, read_regex)
                    if new_name is not None:
                        orig_file = os.path.join(root, file)
                        new_file = os.path.join(root, new_name)
                        print("Re-naming: {}\nNew name: {}\n".format(orig_file,
                                                                     new_file))
                        shutil.copyfile(orig_file, new_file)

    
