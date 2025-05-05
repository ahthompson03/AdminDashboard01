
"""This is a unit test for the function Assign_Reviewers located in Model.py.  
        The goal of this function is to assign 3 reviewers to every paper. 
        Reviewers are picked on lowest number of papers already assigned and then ReviewerID ascending.
        This function will not change any current assignments.  
        If there are not enough reviewers for a paper only the max amount of reviewers will be assigned.
"""

"""Variables Index
        paper_list =                            list of all papers in the DB
        total_reviewers_assigned_per_paper =    total count of papers with the current paperid in paperreviewer table (usually 0 if the paper was recently added and no reviewers have been assigned yet)
        while_loop_condition2 =                 number of reviewers per paper (How many reviewers should each paper be assigned)
        reviewer_obj =                          current reviewer that is not already assigned to the current paperid and has the least amount of paper assignments ordered by reviewerid ascending
"""


"""Change per Unit Test"""
paper_list = ['', '', '', '', '']
total_reviewers_assigned_per_paper = 0
total_reviewers_allowed_per_paper = 3
reviewer_obj = 'Test Reviewer Object'   #set to None to test missing reviewers

def Assign_Reviewers():
    try:
        papers = paper_list                                            #simulates a list of papers in the db
        current_paper_count = total_reviewers_assigned_per_paper       #simulates a list of reviewers already assigned to a paper
        reviewer_per_paper_count = total_reviewers_allowed_per_paper   #simulates the total amount of reviewers allowed to reviewer a paper

        #Loops through every paper in the db
        for paper in papers:
            #checks to see if our current paper has 3 reviewers yet if not it will assign them
            while current_paper_count < reviewer_per_paper_count:
                reviewer = reviewer_obj

                #if a reviewer is found it will be assigned, if not the loop will break
                if reviewer:
                    #simulates adding a reviewer to the list
                    current_paper_count = current_paper_count + 1
                    print(f'{reviewer_obj} added successfully')
                else:
                    print(f"Warning: Could not find enough reviewers for Paper ID {paper}.")
                    break
    except Exception:
        print('AssignReviewers() function error')




if __name__ == '__main__':
    Assign_Reviewers()