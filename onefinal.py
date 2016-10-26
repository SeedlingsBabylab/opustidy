import os
import sys


def filter_files_by_type(root, files):

    cha_paths = []
    cex_paths = []
    other_paths = []
    for file in files:
        if file.endswith(".cha"):
            cha_paths.append(os.path.join(root, file))
        elif file.endswith(".cex"):
            cex_paths.append(os.path.join(root, file))
        else:
            other_paths.append(os.path.join(root, file))
    return cha_paths, cex_paths, other_paths


def find_final(cha_files):
    final = []
    newclan_merged_final = []
    newclan_merged = []
    for file in cha_files:
        if file.endswith("_final.cha") and not file.endswith("newclan_merged_final.cha"):
            final.append(file)
        elif file.endswith("newclan_merged_final.cha"):
            newclan_merged_final.append(file)
        elif file.endswith("newclan_merged.cha"):
            newclan_merged.append(file)

    return final, newclan_merged_final, newclan_merged

def walk_opus_dry(start):
    for root, dirs, files in os.walk(start):
        if "Audio_Annotation" in root:
            cha, cex, other = filter_files_by_type(root, files)
            final, nc_merged_final, nc_merged = find_final(cha)
            if len(final) > 1:
                print "more than one final.cha in this Annotation folder: {}".format(final[0][:5])

        elif "Video_Annotation" in root:
            print

def walk_opus(start):
    for root, dirs, files in os.walk(start):
        if "Audio_Annotation" in root:
            cha, cex, other = filter_files_by_type(root, files)
            final, nc_merged_final, nc_merged = find_final(cha)

        elif "Video_Annotation" in root:
            print


if __name__ == "__main__":
    start_dir = sys.argv[1]

    dry_run = False
    if len(sys.argv) > 2:
        dry_run = True

    if dry_run:
        walk_opus_dry(start_dir)
    else:
        walk_opus_dry(start)