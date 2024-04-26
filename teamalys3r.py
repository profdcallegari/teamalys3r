########################################################################################
# teamalys3r.py
# (c) 2024 Daniel Callegari
########################################################################################
# A program that reads a file with the following format:
#   <myid>-><id>,<id>...,<id>
# where <myid> is a team member id and the other ids are the other team members
#   and -> indicates with whom the <myid> has worked with (the other team members)
# The program then prints an adjacency matrix of all team members
#   where the rows are the team members and the columns are the team members
#   and the values are 1 if the team members have worked together and 0 otherwise
# The program also calculates the work index of each team member
#   The work index is calculated by dividing the number of team members worked with by the total number of team members
# The program then exports an svg file diplaying the team members in a circle and their connections
#   each team member is represented by a circle and the connections are represented by lines
#   add the team member id as text inside the circle
# Usage: python teamalys3r.py <file_path>
########################################################################################

import sys
import math

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            return file_contents
    except FileNotFoundError:
        # print error including file path
        print("File not found: " + file_path)
        return ""


# a method that parses the file contents
# in the following format:
# <myid>-><id>,<id>...,<id>
# where <myid> is a team member id and the other ids are the other team members
# and -> indicates with whom the <myid> has worked with (the other team members)
# and saves the information in a dictionary
# ignore empty lines
def parse_file_contents(file_contents):
    # split the file contents by new line
    lines = file_contents.split("\n")
    # create a dictionary to store the team members and their team members
    team_members = {}
    # iterate over the lines
    for line in lines:
        if line == "": # ignore empty lines
            continue
        # split the line by the arrow
        parts = line.split("->")
        # the first part is the team member id
        team_member = parts[0]
        # the second part is the team members that the team member has worked with
        team_member_ids = parts[1].split(",")
        # add the team member to the dictionary
        team_members[team_member] = team_member_ids
    return team_members

# a method that prints and adjacency matrix of all team members
# where the rows are the team members and the columns are the team members
# and the values are 1 if the team members have worked together and 0 otherwise
def print_adjacency_matrix(team_members):
    print("Adjacency matrix:")
    # get the team member ids
    team_member_ids = list(team_members.keys())
    # create a list to store the adjacency matrix
    adjacency_matrix = []
    # iterate over the team members
    for team_member_id in team_member_ids:
        # create a list to store the row of the adjacency matrix
        row = []
        # iterate over the team members again
        for other_team_member_id in team_member_ids:
            # if the team members have worked together
            if other_team_member_id in team_members[team_member_id]:
                # add 1 to the row
                row.append(1)
            else:
                # add 0 to the row
                row.append(0)
        # add the row to the adjacency matrix
        adjacency_matrix.append(row)
    # print the adjacency matrix
    for row in adjacency_matrix:
        print(row)



def calculate_work_index(team_members, team_member_id):
    # check if the team member id exists in the team members dictionary
    if team_member_id in team_members:
        # get the list of team members that the given team member has worked with
        worked_with = team_members[team_member_id]
        # calculate the work index by dividing the number of team members worked with by the total number of team members
        work_index = len(worked_with) / len(team_members)
        return work_index
    else:
        print("Team member not found")
        return None


# function that exports an svg file diplaying the team members in a circle and their connections
# each team member is represented by a circle and the connections are represented by lines
# add the team member id as text inside the circle
def export_svg(filename, team_members):
    # create a file to write the svg contents
    with open(filename, "w") as file:
        # write the svg header
        file.write("<svg xmlns='http://www.w3.org/2000/svg' width='1000' height='1000'>")
        # get the team member ids
        team_member_ids = list(team_members.keys())
        # calculate the angle between each team member
        angle = 360 / len(team_member_ids)
        # calculate the radius of the circle
        radius = 400
        # iterate over the team members for drawing the lines
        for i in range(len(team_member_ids)):
            # calculate the x and y coordinates of the team member
            x = 500 + radius * math.cos(math.radians(angle * i))
            y = 500 + radius * math.sin(math.radians(angle * i))
            
            # iterate over the team members
            for j in range(len(team_member_ids)):
                # if the team members have worked together
                if team_member_ids[j] in team_members[team_member_ids[i]]:
                    # calculate the x and y coordinates of the other team member
                    x2 = 500 + radius * math.cos(math.radians(angle * j))
                    y2 = 500 + radius * math.sin(math.radians(angle * j))
                    # write the line
                    file.write("<line x1='" + str(x) + "' y1='" + str(y) + "' x2='" + str(x2) + "' y2='" + str(y2) + "' stroke='black' />")

        # iterate over the team members for drawing the circles and text
        for i in range(len(team_member_ids)):
            # calculate the x and y coordinates of the team member
            x = 500 + radius * math.cos(math.radians(angle * i))
            y = 500 + radius * math.sin(math.radians(angle * i))
            # write the circle
            file.write("<circle cx='" + str(x) + "' cy='" + str(y) + "' r='20' fill='blue' />")
            # write the text
            file.write("<text x='" + str(x) + "' y='" + str(y) + "' fill='white'>" + team_member_ids[i] + "</text>")

        # write the svg footer
        file.write("</svg>")


####################################
# main function
####################################
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("teamalys3r by Daniel Callegari")
        print("Usage: python teamalys3r.py <file_path>")
    else:
        print("Reading input file...")
        file_path = sys.argv[1]
        contents = read_file(file_path)
        print(contents)
        team_members = parse_file_contents(contents)
        print_adjacency_matrix(team_members)

        # print the work index of all team members
        for team_member_id in team_members:
            work_index = calculate_work_index(team_members, team_member_id)
            print("Work index of " + team_member_id + ": " + str(work_index))

        # export to an svg file with the same name as the input file but with the .svg extension
        filenamewithoutExtension = file_path.split(".")[0]
        outputfile = filenamewithoutExtension + ".svg"
        export_svg(outputfile, team_members)
        print("SVG exported to " + outputfile)



