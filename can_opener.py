import os
import asammdf
import json


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
    # filename needs to be at least 5 characters long, as the extention is .mf4
    if len(filename) < 4:
        return False
    elif filename[-4:].lower() == ".mf4":
        return True
    return False


def print_info_of_all_files():
    perform_function_on_all_files(open_and_print_info)


def save_info_of_all_files():
    perform_function_on_all_files(open_and_write_info_to_file)


def perform_function_on_all_files(func):
    for _, _, files in os.walk('import'):
        for file in files:
            if valid_filename(file):

                func(file)


def open_and_print_info(filename):
    mf4 = asammdf.mdf_v4.MDF4(build_local_path(filename))
    info = mf4.info()
    print(info)
    mf4.close()


def open_and_write_info_to_file(filename):
    mf4 = asammdf.mdf_v4.MDF4(build_local_path(filename))
    export = open(('export/info_' + filename + ".json"), 'w+')
    info = mf4.info()
    export.write(json.dumps(info))
    export.close()
    mf4.close()


def build_local_path(filename):
    return 'import/' + filename


if __name__ == "__main__":
    filescan()
    print("\nTo use this package, please import it into a life shell or into your script.\n"
          "Direct execution of this package only yields a file scan!.")
