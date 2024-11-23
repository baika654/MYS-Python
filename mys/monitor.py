
import os

class Monitor:
    """The purpose of this class is to check the number of student files and store names of mismatching files.
       This class is instantiated in the main script and its data fields used in the WorkbookProcessor.
       Checks by methods below will output any error messages to the screen for the user."""

    def __init__(self):
        self.begin_overwrite = False # boolean to check whether file overwrite is agreed by user
        self.file_count = 0  # number of student files
        self.mismatches = [] # student files that are different to template (e.g. sheetnames different)
        self.details_missing = []  # student sheets missing a details sheet
        self.unaccepted_files = []
        self.missing_names = []
        self.accepted_extensions = [".xlsx", ".xlsm", ".xltx", ".xltm"]
        

    # checks whether output folder has any contents; Marking (live links) class will throw an error if directed to an empty folder
    def output_folder_empty(self, path):
        if len(os.listdir(path) ) == 0:
            # true as in it's empty
            return True
        else:
            # not empty
            return False
        
    def check_sheet_errors(self, st_wb_name, student_wb, DO_student_sheets, flattened_sheets):
        """General error checker; returns boolean to inform WorkbookProcessor whether to continue processing a workbook
        or save time by skipping a problematic workbook"""
        # initial assumptions about workbook for checking below
        sheet_differences = 0
        no_details = False
        no_names = False
        # check whether student wb has same sheets as template
        for sheetname in flattened_sheets.keys():
            if sheetname not in DO_student_sheets:
                sheet_differences += 1
        if sheet_differences > 0:
            self.mismatches.append(st_wb_name)
        # check for details sheet
        if "Details" not in DO_student_sheets:
            self.details_missing.append(st_wb_name)
            no_details = True
        # check for missing student names if Details page does exist
        if no_details == False:
            if student_wb["Details"]["C11"].value == None or student_wb["Details"]["F11"].value == None:
                self.missing_names.append(st_wb_name)
                no_names = True
        # if any of the above conditions fail, processing of workbook will not continue and problems with it will
        # be output later
        if sheet_differences > 0 or no_details == True or no_names == True:
            return False
        # if all assumptions stay the same, processing can continue
        return True

    def display_any_errors(self):
        # error messages for below
        mismatch_error = 'Mismatches in files detected; '+\
        'please compare template with student files (e.g. check that sheet names are the same).'+\
        '\nSee output window for conflicting files.'
        files_differ_error = 'All files differ from answer template. Please check that you have loaded the correct template.'
        unsupported_error = 'At least one file was in an unsupported format. Please check output window for more information.'
        details_missing_error = 'One or more student files are missing a "Details" sheet for assigning marks. Please check output window for more information.'
        names_missing_error = 'One or more student files are missing first/lastnames in their Details sheet. Please check output window for more information.'
        if len(self.mismatches) > 0:
            print("***** File comparison problems *****\n\n")
            for books in self.mismatches:
                print("Mismatches in file {}\n".format(books))
        if len(self.mismatches) > 0 and len(self.mismatches) < self.file_count:
            tk.messagebox.showinfo('Warning', mismatch_error, icon = 'warning')
        elif len(self.mismatches) == self.file_count:
            print("\n")
            print("----- Please check that you have loaded the correct answer template -----\n\n")
            tk.messagebox.showinfo('Warning', files_differ_error, icon = 'warning')
        if len(self.unaccepted_files) > 0:
            print("\n")
            print("***** Unsupported file types *****\n\n")
            for file in self.unaccepted_files:
                print("Unsupported file type {}\n".format(file))
            
        if len(self.details_missing) > 0:
            print("\n")
            print("***** Missing \"Details\" sheets *****\n\n")
            for file in self.details_missing:
                print("Details sheet missing in {}\n".format(file))
        if len(self.missing_names) > 0:
            print("\n")
            print("***** Missing names in \"Details\" sheets *****\n\n")
            for file in self.missing_names:
                print("Missing names in {}\n".format(file))
            


        

    def check_extension(self, file):
        filename, file_extension = os.path.splitext(file)
        if file_extension not in self.accepted_extensions:
            self.unaccepted_files.append(file)
        return file_extension