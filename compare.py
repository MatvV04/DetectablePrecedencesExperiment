import os

files = None
types = []

# gets the results required from an array of lines (from the file)
#
# you can insert more variables and if statements and return them if needed
def get_results(lines):
    t_end = None
    t_end_last = None
    conflicts = None
    conflicts_last = None
    lbd = None
    lbd_last = None
    time = None
    lcl = None
    lcl_last = None
    optimality_proven = False 
    hm = {}
    for line in lines:
        if "====" in line:
            optimality_proven = True
            t_end = t_end.strip("*")
        if "----------" in line and t_end != None:
            hm[t_end] = conflicts, lbd, lcl, time


        line = line.split("=")

        if "t_end" in line[0]:
            t_end = line[1][1:] + "*"
        elif "%%%mzn-stat: engineStatisticsNumConflicts" in line[0]:
            conflicts_last = conflicts
            conflicts = line[1]
        elif "%%%mzn-stat: learnedClauseStatisticsAverageLbd" in line[0]:
            lbd_last = lbd
            lbd = line[1]
        elif "%%%mzn-stat: learnedClauseStatisticsAverageLearnedClauseLength" in line[0]:
            lcl_last = lcl
            lcl = line[1]
        elif "time elapsed" in line[0]:
            time = line[0].split(": ")[1]
    if not optimality_proven:
        conflicts = conflicts_last
        lbd = lbd_last
        lcl = lcl_last
    else:
        hm[t_end] = conflicts, lbd, lcl, time


    return t_end, conflicts, lbd,lcl, time, hm

for folder in os.listdir("./output3"):
    types.append(folder)

    # this is to create the files that will be uploaded
    #
    # in this case i take the intersection of files available, so i have full solutions for everything
    #
    # feel free to change it :D
    if files is None:
        files = set(os.listdir("./output3/" + folder))
    else:
        files = files.intersection(os.listdir("./output3/" + folder))

if files == None:
    print("Nothing has been run yet")
    exit(1)

for f in sorted(files):
    print(f"------ Dataset: {f} ------")
    print("t_end, #conflicts, lbd, lcl, time")
    solution_dicts = {}
    for type in types:
        solution = open(f"./output3/{type}/{f}")

        res = get_results(solution.read().split("\n"))
        print(f"{type}: {res[:-1]}")
        solution_dicts[type] = res[-1] 
        solution.close()
    print()
    print("Common lower bound:")
    unique_solutions = set.intersection(*map(set, solution_dicts.values()))
    if len(unique_solutions) == 0:
        print("No common solutions!")
        continue
    if len(s:=[*filter(lambda x: x[-1] != "*", unique_solutions)]) == 1:
        for x in solution_dicts:
            y = solution_dicts[x][s[0]]
            y = (s[0], *y)
            file = open(f"{x}.csv", "a+")
            file.write(f"{f.rstrip('.out')},{y[0]},{y[1]},{y[2]},{y[3]},{y[4].strip('s')}\n")
            file.close()
            print(f"{x}: {y}")
    else:
        s = str(min(map(lambda x: int(x.strip("*")), unique_solutions)))+"*"
        for x in solution_dicts:
            y = solution_dicts[x][s]
            y = (s, *y)
            file = open(f"{x}.csv", "a+")
            file.write(f"{f.rstrip('.out')},{y[0]},{y[1]},{y[2]},{y[3]},{y[4].strip('s')}\n")
            file.close()
            print(f"{x}: {y}")
    # print(unique_solutions)
    print()


