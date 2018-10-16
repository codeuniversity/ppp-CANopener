import os
import asammdf
import json
import numpy


# scans the import directory for compatible files
def filescan(verbose=False):
    compatible_files = 0
    for file in os.listdir('import'):

        if valid_filename(file):
            if verbose:
                print("compatible file found: " + file)
            compatible_files += 1

    print("Total of", compatible_files, "compatible files found!")


def valid_filename(filename):
    # filename needs to be at least 5 characters long, as the extention is .mf4, .mf3 or .mdf
    if len(filename) < 4:
        return False
    elif filename[-4:].lower() == ".mdf" or (filename[-4:].lower() == ".mf3" or filename[-4:].lower() == ".mf4"):
        return True
    return False


def print_info_of_all_files():
    perform_function_on_all_files(open_and_print_info)


def save_info_of_all_files():
    perform_function_on_all_files(open_and_write_info_to_file)


def save_all_channel_names_of_all_files():
    perform_function_on_all_files(write_channel_names_to_file)


def perform_function_on_all_files(func):
    for _, _, files in os.walk('import'):
        for file in files:
            if valid_filename(file):

                func(file)


def open_and_print_info(filename):
    mdf = asammdf.mdf.MDF(build_local_path(filename))
    info = mdf.info()
    print(info)
    mdf.close()


def open_and_write_info_to_file(filename):
    mdf = asammdf.mdf.MDF(build_local_path(filename))
    export = open(('export/info_' + filename + ".json"), 'w+')
    info = mdf.info()
    export.write(json.dumps(info))
    export.close()
    mdf.close()


def write_channel_names_to_file(filename):
    mdf = asammdf.mdf.MDF(build_local_path(filename))
    export = open(('export/channels_' + filename + ".txt"), 'w+')
    for group in mdf.groups:
        for channel in group["channels"]:
            if channel.name is "t":
                continue

            export.write(channel.name + "\n")
    export.close()
    mdf.close()


def write_only_used_channel_names_to_file(filename, verbose=False):
    mdf = asammdf.mdf.MDF(build_local_path(filename))
    export = open(('export/channels_' + filename + ".txt"), 'w+')
    for group in mdf.groups:
        for channel in group["channels"]:
            if channel.name is "t":
                continue
            full_channel = mdf.get(channel.name)
            if len(numpy.unique(full_channel.samples)) > 1:

                export.write('Name: "' + full_channel.name + '"\n')
                export.write('Description: "' + full_channel.comment + '"\n')
                export.write('Min: ')
                export.write(str(min(full_channel.samples)))
                export.write(" Max: ")
                export.write(str(max(full_channel.samples)))
                export.write("\n\n\n")

    export.close()
    mdf.close()


def build_local_path(filename):
    return 'import/' + filename


if __name__ == "__main__":
    filescan()
    print("\nTo use this package, please import it into a life shell or into your script.\n"
          "Direct execution of this package only yields a file scan!.")
