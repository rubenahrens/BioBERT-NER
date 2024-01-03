import os
import numpy as np

def n_files():
    """Prints the number of files in the data directory."""
    print(len(os.listdir("cadec/text")))

def medicine_names():
    """Prints the set of names of the medicines in the data directory."""
    names = []

    for file in os.listdir("cadec/text"):
        names.append(file.split(".")[0])
    # get the count of each element in the list in a dictionary
    names_occurences = {i:names.count(i) for i in set(names)}
    
    # print a latex table of the names and their occurences
    print("\\begin{table}[h]")
    print("\\centering")
    print("\\begin{tabular}{|l|l|}")
    print("\\hline")
    print("Name & Occurences \\\\ \\hline")
    for name in names_occurences:
        print(f"{name} & {names_occurences[name]} \\\\ \\hline")
    print("\\end{tabular}")
    print("\\end{table}")

    print(len(names))
    # print names in a text format without \n
    for name in names_occurences:
        print(f"{name}, ", end="")

if __name__ == "__main__":
    medicine_names()