from rank.models import College, Program, CollegeProgram, Addmission, District, Zone
import numpy as np
import csv
import os

runcolleges = True
runadmissions = True
drop = True


def populate_zones(zones, drop_zones=False):
    print("Populating zones...")
    if drop_zones:
        print("dropping previous information of zones ...")
        Zone.objects.all().delete()
        print("dropping previous information of zones ... success!!")

    for zone in zones:
        z = Zone(id=int(zone[0]), name=zone[1])
        z.save()
    print("Populating zones... success!!")


def populate_districts(districts, drop_districts=False):
    print("Populating districts...")
    if drop_districts:
        print("dropping previous information of districts ...")
        District.objects.all().delete()
        print("dropping previous information of districts ... success!!")

    for district in districts:
        d = District(
            code=int(district[0]),
            name=district[1],
            zone=Zone.objects.get(id=int(district[2])),
        )
        d.save()
    print("Populating districts... success!!")


def get_cutin_cutoff(RESET=False):
    """Updates the cutin and cutoff columns of CollegeProgram Model"""
    if RESET:
        for collegeprogram in CollegeProgram.objects.all():
            collegeprogram.cutoff = 0
            collegeprogram.save(update_fields=["cutoff"])

    else:
        for collegeprogram in CollegeProgram.objects.all():
            ranks = (
                Addmission.objects.filter(collegeprogram=collegeprogram)
                .values_list("rank", flat=True)
                .exclude(rank=None)
            )
            if not ranks:
                print(
                    f"BUG : {collegeprogram.college} has insufficient data (DEFAULT=0)"
                )
                continue

            # find IQR
            Q1 = np.quantile(ranks, 0.25)
            Q3 = np.quantile(ranks, 0.75)
            IQR = Q3 - Q1

            # Outliers are values and greater than (Q1+1.5*IQR)
            collegeprogram.cutin = min(x for x in ranks if x >= (Q1 - 1.5 * IQR))
            collegeprogram.cutoff = max(x for x in ranks if x <= (Q1 + 1.5 * IQR))
            collegeprogram.save(update_fields=["cutin", "cutoff"])


def read_csv(file_path):
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        table = list(reader)
    return table


def run():

    collegeNametoCode = {}
    programNametoCode = {}
    print(os.getcwd())
    collegeCSV = open("./rank/scripts/datas/colleges.csv", newline="")
    admissionsCSV = open("./rank/scripts/datas/filtered_final_2.csv", newline="")
    districts = read_csv("./rank/scripts/datas/district.csv")
    zones = read_csv("./rank/scripts/datas/zone.csv")

    college_table = list(csv.reader(collegeCSV))
    admissions_table = list(csv.reader(admissionsCSV))

    if drop:
        print("dropping previous information of colleges ...")
        College.objects.all().delete()
        Program.objects.all().delete()
        CollegeProgram.objects.all().delete()
        Addmission.objects.all().delete()
        Zone.objects.all().delete()
        District.objects.all().delete()
        print("dropping previous information of colleges ... success!!")

    populate_zones(zones)
    populate_districts(districts)

    print("populating College, Program and CollegeProgram Models ...")
    collegeName = ""
    collegeCode = ""
    for row in college_table:
        if row[1] == "":
            collegeName = row[0]
            if collegeName not in collegeNametoCode:
                for row1 in admissions_table:
                    if row1[2] == collegeName:
                        collegeNametoCode[collegeName] = row1[3]
                        break
                if collegeName not in collegeNametoCode:
                    print("College code not found for college:", collegeName)
            if collegeName.find("Chitwan") != -1:
                collegeNametoCode[collegeName] = "CEC"
            collegeCode = collegeNametoCode[collegeName]
            if runcolleges:
                c = College(name=collegeName, code=collegeCode)
                c.save()

            # print("college= " + collegeName+"({0})".format(collegeCode))
            continue
        elif row[0] == "S.No.":
            continue
        programType = "F" if row[1].find("Regular") == -1 else "R"
        regular_place = row[1].find("Regular")
        fullfee_place = row[1].find("Full Fee")
        programName = ""
        if regular_place != -1:
            programName = row[1][0: regular_place - 1]
        elif fullfee_place != -1:
            programName = row[1][0: fullfee_place - 1]
        else:
            programName = row[1]

        if programName not in programNametoCode:
            for row1 in admissions_table:
                if row1[4].find(programName) != -1:
                    programNametoCode[programName] = row1[5]
                    break
            if programName not in programNametoCode:
                print("Program code not found for program:", programName)
        programCode = programNametoCode[programName]

        if runcolleges:
            p = Program(name=programName, code=programCode)
            p.save()

        seats = int(row[2])
        if runcolleges:
            cp = CollegeProgram(
                college=College.objects.get(code=collegeCode),
                program=Program.objects.get(code=programCode),
                seats=seats,
                type=programType,
            )
            cp.save()

        # print(programName+"({0})  ".format(programCode) +
        #       programType+"  "+str(seats))

    collegeCSV.close()
    print("populating College, Program and CollegeProgram Models ... success!!")

    print("populating Admission Models ...")
    data = {}
    skip = True
    for row in admissions_table:
        if skip:
            skip = False
            continue
        data["collegeName"] = row[2]
        data["collegeCode"] = collegeNametoCode[data["collegeName"]]
        data["programType"] = "F" if row[4].find("Regular") == -1 else "R"

        data["programName"] = ""
        regular_place = row[4].find("Regular")
        fullfee_place = row[4].find("Full Fee")
        if regular_place != -1:
            data["programName"] = row[4][0: regular_place - 1]
        elif fullfee_place != -1:
            data["programName"] = row[4][0: fullfee_place - 1]
        else:
            data["programName"] = row[4]

        data["programCode"] = programNametoCode[data["programName"]]
        data["programType"] = "F" if regular_place == -1 else "R"
        data["quota"] = "NOR"
        data["first_name"] = row[6]
        data["middle_name"] = row[7]
        data["last_name"] = row[8]
        data["gender"] = "M" if row[12] == "Male" else "F"
        data["batch"] = 2077
        data["score"] = row[9] if row[9] else -1
        data["rank"] = row[10] if row[10] else -1
        data["district"] = row[13]

        try:
            district = District.objects.get(code=int(data["district"]))
        except (District.DoesNotExist, ValueError):
            print(f'W: DistrictID={data["district"]} does not exist (default=NULL)')
            district = None

        if runadmissions:
            try:
                a = Addmission(
                    first_name=data["first_name"],
                    middle_name=data["middle_name"],
                    last_name=data["last_name"],
                    gender=data["gender"],
                    batch=data["batch"],
                    collegeprogram=CollegeProgram.objects.get(
                        college=College.objects.get(code=data["collegeCode"]),
                        program=Program.objects.get(code=data["programCode"]),
                        type=data["programType"],
                    ),
                    quota=data["quota"],
                    score=data["score"],
                    rank=None if data["rank"] == -1 else int(float(data["rank"])),
                    district=district,
                )
                a.save()
            except Exception:
                print(data)
                raise

        # print(data)

    admissionsCSV.close()
    print("populating Admission Models ... success!!")

    print("updating cutoff and cutin rank of CollegeProgram Model ... ")
    # update cutoff and cutin
    get_cutin_cutoff()
    print("updating cutoff and cutin rank of CollegeProgram Model ... success!!")
