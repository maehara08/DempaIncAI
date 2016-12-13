#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv

if __name__ == '__main__':
    csvFile = open('members.csv', 'w')
    writer = csv.writer(csvFile, lineterminator='\n')
    outdir = sys.argv[1]
    if not os.path.isdir(outdir):
        sys.exit('%s is not directory' % outdir)

    exts = ['.JPG', '.JPEG']
    names = {
        "out_mirin": 0,
        "out_moga": 1,
        "out_ei": 2,
        "out_pincky": 3,
        "out_risa": 4,
        "out_nemu": 5,
    }

    for dirpath, dirnames, filenames in os.walk(outdir):
        for dirname in dirnames:
            if dirname in names:
                n = names[dirname]
                member_dir = os.path.join(dirpath, dirname)
                for dirpath2, dirnames2, filenames2 in os.walk(member_dir):
                    if not dirpath2.endswith(dirname):
                        continue
                    for filename2 in filenames2:
                        (fn, ext) = os.path.splitext(filename2)
                        if ext.upper() in exts:
                            img_path = os.path.join(dirpath2, filename2)
                            print '%s %s' % (img_path, n)
                            writer.writerow((img_path, n))
