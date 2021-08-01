import fileinput    
import sys
import os
import argparse

class Create_regression():

    def __init__(self, file, code, flag, feature):
        self.file = file
        self.code = code 
        self.temporary = "Scripts/Python/temporary.robot"
        self.feature = feature
        if int(flag) == 0:
            self.regression_file = "Tests/regression/FEATURE_TEST_TEAM_regression.robot"
        else:
            self.regression_file = "Tests/portfolio/TestPlan.robot"

    def save_test(self):
        flag=0
        with open(f"Tests/portfolio/{self.feature}/{self.file}.robot") as f:
            with open(self.temporary, "w") as f1:
                for line in f:
                    if self.code in line:
                        flag=1

                    if not line.strip():
                        flag=0

                    if flag==1:
                        f1.write(line)

    def write_test(self):
        with open(self.regression_file, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if "#end" in line:
                    with open(self.temporary, "r") as f1:
                        newlines = f1.readlines()
                        for newline in newlines:
                            f.write(newline)
                        f.write("\n#end")
                else:
                    f.write(line)
            os.remove(self.temporary)
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description= 'Add the tests to the Feature test team regression')
    parser.add_argument('-f','--file', help='Name of the file with the test')
    parser.add_argument('-c','--code', help='Code of the test')
    parser.add_argument('-fl','--flag', help='Flag for type of test')
    parser.add_argument('-ft','--feature', help='Feature folder')

    args = parser.parse_args()

    new = Create_regression(args.file, args.code, args.flag, args.feature)
    new.save_test()
    new.write_test()