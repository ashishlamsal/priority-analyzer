from rank.models import College, Program, CollegeProgram, addmission
import csv
import os

runcolleges = True
runadmissions = True
drop = True


def run():

    collegeNametoCode = {}
    programNametoCode = {}
    print(os.getcwd())
    collegeCSV = open("./rank/scripts/datas/colleges.csv", newline="")
    admissionsCSV = open(
        "./rank/scripts/datas/filtered_final.csv", newline="")
    college_table = list(csv.reader(collegeCSV))
    admissions_table = list(csv.reader(admissionsCSV))

    if drop:
        print("dropping previous information of colleges...")
        College.objects.all().delete()
        Program.objects.all().delete()
        CollegeProgram.objects.all().delete()
        addmission.objects.all().delete()
        print("dropped premious information of colleges sucessfully")

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
            if (runcolleges):
                c = College(name=collegeName, code=collegeCode)
                c.save()

            # print("college= " + collegeName+"({0})".format(collegeCode))
            continue
        elif row[0] == "S.No.":
            continue
        programType = 'F' if row[1].find("Regular") == -1 else 'R'
        regular_place = row[1].find("Regular")
        fullfee_place = row[1].find("Full Fee")
        programName = ""
        if regular_place != -1:
            programName = row[1][0:regular_place-1]
        elif fullfee_place != -1:
            programName = row[1][0:fullfee_place-1]
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

        if (runcolleges):
            p = Program(name=programName, code=programCode)
            p.save()

        seats = int(row[2])
        if (runcolleges):
            cp = CollegeProgram(college=College.objects.get(code=collegeCode), program=Program.objects.get(
                code=programCode), seats=seats, type=programType)
            cp.save()

        print(programName+"({0})  ".format(programCode) +
              programType+"  "+str(seats))

    collegeCSV.close()

    data = {}
    skip = True
    for row in admissions_table:
        if skip:
            skip = False
            continue
        data["collegeName"] = row[2]
        data["collegeCode"] = collegeNametoCode[data["collegeName"]]
        data["programType"] = 'F' if row[4].find("Regular") == -1 else 'R'

        data["programName"] = ""
        regular_place = row[4].find("Regular")
        fullfee_place = row[4].find("Full Fee")
        if regular_place != -1:
            data["programName"] = row[4][0:regular_place-1]
        elif fullfee_place != -1:
            data["programName"] = row[4][0:fullfee_place-1]
        else:
            data["programName"] = row[4]

        data["programCode"] = programNametoCode[data["programName"]]
        data["quota"] = 'NOR'
        data["first_name"] = row[6]
        data["middle_name"] = row[7]
        data["last_name"] = row[8]
        data["gender"] = 'M' if row[12] == "Male" else 'F'
        data["batch"] = 2077
        data["score"] = row[9] if row[9] else -1
        data["rank"] = row[10] if row[10] else -1

        if (runadmissions):
            try:
                a = addmission(
                    first_name=data["first_name"],
                    middle_name=data["middle_name"],
                    last_name=data["last_name"],
                    gender=data["gender"],
                    batch=data["batch"],
                    college=College.objects.get(code=data["collegeCode"]),
                    program=Program.objects.get(code=data["programCode"]),
                    quota=data["quota"],
                    score=data["score"],
                    rank=None if data["rank"] == -
                    1 else int(float(data["rank"]))
                )
                a.save()
            except:
                print(data)
                raise

        # print(data)

    admissionsCSV.close()


# if __name__ == "__main__":

#     parse_colleges(True, False)
