"""
Rename/move original fastq files on the scc for alpha and beta transcriptomes.

Author: Dakota Hawkins
Date: September 5, 2018
"""

import argparse
import itertools
import os
import re
import shutil


def compile_read_regex(read_tags, file_extension):
    """Generate regular expressions to disern direction in paired-end reads."""
    read_regex = [re.compile(r'{}\.{}$'.format(x, y))\
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

def rename_and_move_fastq_files(top_dir, read_denotes, ext, dst_dir):
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
                        new_file = os.path.join(dst_dir, new_name)
                        print("Re-naming: {}\nNew name: {}\n".format(orig_file,
                                                                     new_file))
                        shutil.move(orig_file, new_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move and rename fastq files.")
    parser.add_argument('-i','--input_dir', dest='in_dir', type=str,
                        help='Top level directory containing sample directories.')
    parser.add_argument('-1','--right_read', dest='rightread', type=str,
                        help='Current filename denotor for right read.')
    parser.add_argument('-2','--left_read', dest='leftread', type=str,
                        help="Current filename denotor for left read.")
    parser.add_argument('-e', '--extension', dest='ext', type=str,
                        help='Extension used to demark fastq files.')
    parser.add_argument('-d', '--out_dir', dest='out_dir', type=str,
                        help="Output directory for fastq files.")
    opts = parser.parse_args()
    rename_and_move_fastq_files(top_dir=opts.in_dir,
                                read_denotes=[opts.rightread, opts.leftread],
                                ext=opts.ext, dst_dir=opts.out_dir)

# ../NEW_sequencingData_20150701_copy/NEW_sequencingData_20150701/F15FTSAPJT0075_SEAaysE/Clean/
