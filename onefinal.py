import os
import sys
import shutil

def filter_files_by_type(root, files):
    cha_paths = []
    cex_paths = []
    other_paths = []
    for file in files:
        if file.endswith(".cha"):
            cha_paths.append(os.path.join(root, file))
        elif file.endswith(".cha.bak"):
            cha_paths.append(os.path.join(root, file))
        elif file.endswith(".cex"):
            cex_paths.append(os.path.join(root, file))
        elif file.endswith(".cex.bak"):
            cex_paths.append(os.path.join(root, file))
        else:
            other_paths.append(os.path.join(root, file))
    return cha_paths, cex_paths, other_paths


def find_finals(cha_files):
    final = []
    newclan_merged_final = []
    newclan_merged = []
    other = []

    for file in cha_files:
        if file.endswith("_final.cha") and not file.endswith("newclan_merged_final.cha"):
            final.append(file)
        elif file.endswith("newclan_merged_final.cha"):
            newclan_merged_final.append(file)
        elif file.endswith("newclan_merged.cha"):
            newclan_merged.append(file)
        else:
            other.append(file)
    return final, newclan_merged_final, newclan_merged, other

def find_final_final(final, nc_merged_final, nc_merged, errors_file):
    final_final = None
    if len(final) > 1:
        print "\tmore than one final.cha in this Annotation folder: {}".format(final[0][:5])
        errors_file.write("\tmore than one final.cha in this Annotation folder: {}\n".format(final[0][:5]))
    elif len(final) == 1:
        final_final = final[0]
        return final_final
    elif len(final) == 0:
        if len(nc_merged_final) > 1:
            print "\tmore than one newclan_merged_final.cha in this Annotation folder: {}".format(nc_merged_final[0][:5])
            errors_file.write("\tmore than one newclan_merged_final.cha in this Annotation folder: {}\n".format(nc_merged_final[0][:5]))
        elif len(nc_merged_final) == 1:
            final_final = nc_merged_final[0]
            return final_final
        elif len(nc_merged_final) == 0:
            if len(nc_merged) > 1:
                print "\tmore than one newclan_merged.cha in this Annotation folder: {}".format(nc_merged[0][:5])
                errors_file.write("\tmore than one newclan_merged.cha in this Annotation folder: {}\n".format(nc_merged[0][:5]))
            elif len(nc_merged) == 1:
                final_final = nc_merged[0]
                return final_final
            elif len(nc_merged) == 0:
                return final_final
    return final_final

def walk_opus_dry(start, errors_file):
    folder_count = 0
    for root, dirs, files in os.walk(start):
        if ("Audio_Annotation" in root) and\
            ("old_chas" not in root) and\
            ("Old_Files" not in root) and\
            ("Old_files" not in root) and\
            ("old_files" not in root) and\
            ("Subject_Files" in root) and\
            (os.path.basename(root) == "Audio_Annotation"):
            folder_count += 1
            #print os.path.basename(root)
            print "\n\ninside: {}".format(root)
            chas, cex, other = filter_files_by_type(root, files)
            final, nc_merged_final, nc_merged, other = find_finals(chas)
            final_final = find_final_final(final, nc_merged_final, nc_merged, errors_file)
            if not final_final:
                print "\t**NO FINAL FILE IN THIS FOLDER**: {}".format(root)
                errors_file.write("\n\ninside: {}\n".format(root))
                errors_file.write("\t**NO FINAL FILE IN THIS FOLDER**: {}\n".format(root))
            else:
                print "\n\t\tFINAL FILE: {}\n".format(os.path.basename(final_final))

                old_chas_dir = os.path.join(root, "old_chas")

                # if not os.path.exists(old_chas_dir):
                #     os.mkdir(old_chas_dir)

                del chas[chas.index(final_final)]
                for file in chas:
                    print "\t\tmoving {} to old_chas directory".format(os.path.basename(file))

                for file in cex:
                    print "\t\tmoving {} to old_chas directory".format(os.path.basename(os.path.basename(file)))
                    #shutil.move(file, os.path.join(old_chas_dir, os.path.basename(filename)))

    print "\n\n\nFINAL FOLDER COUNT: {}".format(folder_count)
        #
        # elif "Video_Annotation" in root:
        #     print


def walk_opus(start, errors_file):
    folder_count = 0
    for root, dirs, files in os.walk(start):
        if ("Audio_Annotation" in root) and\
            ("old_chas" not in root) and\
            ("Old_Files" not in root) and\
            ("Old_files" not in root) and\
            ("old_files" not in root) and\
            ("Subject_Files" in root) and\
            (os.path.basename(root) == "Audio_Annotation"):
            folder_count += 1
            #print os.path.basename(root)
            print "\n\ninside: {}".format(root)
            chas, cex, other = filter_files_by_type(root, files)
            final, nc_merged_final, nc_merged, other = find_finals(chas)
            final_final = find_final_final(final, nc_merged_final, nc_merged, errors_file)
            if not final_final:
                print "\t**NO FINAL FILE IN THIS FOLDER**: {}".format(root)
                errors_file.write("\n\ninside: {}\n".format(root))
                errors_file.write("\t**NO FINAL FILE IN THIS FOLDER**: {}\n".format(root))
            else:
                print "\n\t\tFINAL FILE: {}\n".format(os.path.basename(final_final))

                old_chas_dir = os.path.join(root, "old_chas")

                if not os.path.exists(old_chas_dir):
                    os.mkdir(old_chas_dir)

                del chas[chas.index(final_final)]
                for file in chas:
                    print "\t\tmoving {} to old_chas directory".format(os.path.basename(file))
                    shutil.move(file, os.path.join(old_chas_dir, os.path.basename(file)))
                for file in cex:
                    print "\t\tmoving {} to old_chas directory".format(os.path.basename(os.path.basename(file)))
                    shutil.move(file, os.path.join(old_chas_dir, os.path.basename(file)))

    print "\n\n\nFINAL FOLDER COUNT: {}".format(folder_count)


# def walk_opus(start, errors_file):
#     folder_count = 0
#     for root, dirs, files in os.walk(start):
#         if ("Audio_Annotation" in root) and\
#             ("old_chas" not in root) and\
#             ("Old_Files" not in root) and\
#             ("Old_files" not in root) and\
#             ("old_files" not in root) and\
#             ("Subject_Files" in root) and\
#             (os.path.basename(root) == "Audio_Annotation"):
#             folder_count += 1
#             #print os.path.basename(root)
#             print "\n\ninside: {}".format(root)
#             chas, cex, other = filter_files_by_type(root, files)
#             final, nc_merged_final, nc_merged = find_finals(chas)
#             final_final = find_final_final(final, nc_merged_final, nc_merged, errors_file)
#             if not final_final:
#                 print "\t**NO FINAL FILE IN THIS FOLDER**: {}".format(root)
#                 errors_file.write("\n\ninside: {}\n".format(root))
#                 errors_file.write("\t**NO FINAL FILE IN THIS FOLDER**: {}\n".format(root))
#             else:
#                 print "\n\t\tFINAL FILE: {}\n".format(os.path.basename(final_final))
#                 old_chas_dir = os.path.join(root, "old_chas")
#
#                 # if not os.path.exists(old_chas_dir):
#                 #     os.mkdir(old_chas_dir)
#
#                 del chas[chas.index(final_final)]
#                 for file in chas:
#                     print "\t\tmoving {} to old_chas directory".format(os.path.basename(file))
#                 for file in cex:
#                     print "\t\tmoving {} to old_chas directory".format(os.path.basename(file))
#                     shutil.move(file, os.path.join(old_chas_dir, os.path.basename(file)))



if __name__ == "__main__":
    start_dir = sys.argv[1]

    dry_run = False
    if len(sys.argv) > 2:
        dry_run = True

    with open("walk_errors.txt", "wb") as walk_errors:
        if dry_run:
            walk_opus_dry(start_dir, walk_errors)
        else:                                                    # real run deactivated for now
            walk_opus(start_dir, walk_errors)
