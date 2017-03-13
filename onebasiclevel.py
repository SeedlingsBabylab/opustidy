import os
import sys
import shutil

ignore_dirs = ['Old_files', 'Old_Files', 'Extra Files', 'old_files']
ignore_files = ['ready', 'consensus']

def get_the_final(files):
    non_merged = []
    for file in files:
        if "wordmerged" in file:
            return [file]
        if file.endswith(".csv") and not any (x in file for x in ignore_files):
            non_merged.append(file)
    return non_merged


def walk_sf(start, err_out):
    total_bls = 0
    for root, dirs, files in os.walk(start):
        if "_Analysis" in root and not any(x in root for x in ignore_dirs):
            final = get_the_final(files)
            total_bls += len(final)
            if len(final) != 1:
                err_out.write("root:       {}\n".format(root))
                err_out.write("len(final): {}\n\n\n".format(len(final)))
            not_final = [x for x in files if x not in final]
            old_files = os.path.join(root, "old_files")
            if not os.path.exists(old_files):
                os.makedirs(old_files)
            for file in not_final:
                shutil.move(os.path.join(root, file),
                            os.path.join(old_files, file))
    print("total # BL files:  {}".format(total_bls))


def walk_sf_dry(start, err_out):
    total_bls = 0
    for root, dirs, files in os.walk(start):
        if "_Analysis" in root and not any(x in root for x in ignore_dirs):
            final = get_the_final(files)
            not_final = [x for x in files if x not in final]
            old_files = os.path.join(root, "old_files")
            print("\n\nfinal file:    {}".format(final))
            total_bls += len(final)

            if len(final) != 1:
                err_out.write("root:       {}\n".format(root))
                err_out.write("len(final): {}\n\n\n".format(len(final)))

            if not os.path.exists(old_files):
                # os.makedirs(old_files)
                print "creating:  {}".format(old_files)
            for file in not_final:
                # shutil.move(os.path.join(root, file),
                #             os.path.join(old_files, file))
                print "\t{}  to   {}".format(file, os.path.join(old_files, file))

    print("total # BL files:  {}".format(total_bls))

if __name__ == "__main__":

    start_dir = sys.argv[1]

    with open("onebasiclevel_errors.txt", "wb") as out:
        if "dry_run" in sys.argv:
            walk_sf_dry(start_dir, out)
        else:
            walk_sf(start_dir, out)
