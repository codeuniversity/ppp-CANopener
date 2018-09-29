import os
import asammdf


# scans the import directory for compatible files
def filescan(verbose=False):
    compatible_files = 0
    for file in os.listdir('import'):
        if file[-4:] == ".mf4":
            if verbose:
                print("compatible file found: " + file)
            compatible_files += 1

    print("Total of", compatible_files, "compatible files found!")


if __name__ == "__main__":
    filescan()
    print("\nTo use this package, please import it into a life shell or into your script.\n"
          "Direct execution of this package only yields a file scan!.")
