import sys
from workbook import *


def get_spreadsheet() -> Tuple[Workbook, Spreadsheet]:
    decision1 = ""
    workbook = Workbook()
    while decision1.lower() not in ["new", "open"]:
        try:
            decision1 = input("Welcome to WorkBook! would you like to load an existing workbook, or start a new one?\n"
                              "type 'new' or 'open' to start: ")
        except EOFError:
            continue
    if decision1.lower() == "open":
        while True:
            try:
                filename = input("Enter the file you want to open: ")
            except EOFError:
                continue
            try:
                workbook = load_and_open_workbook(filename)
                print(f"Opened {filename} successfully.")
            except:
                print("it seems like the file does not fit the requirements.")
                continue
        workbook.print_list()
        try:
            sheet_name = input("which sheet would you like to open? ")
            while sheet_name not in workbook.list_sheets():
                sheet_name = input("name did not found..."
                                   "which sheet would you like to open? ")
            print(f"You're in {sheet_name} sheet. Type 'help' for options, or start editing.")
        except EOFError:
            pass
    else:
        print("Great! let's start a new workbook. ")
        try:
            workbook_name = input("what would you like to call your workbook? ")
            workbook = Workbook(workbook_name)
            sheet_name = input("type the name of the first sheet in your project? ")
            workbook.add_sheet(sheet_name)
            print(f"You're in {sheet_name} sheet. Type 'help' for options, or start editing.")
            return workbook, workbook.get_sheet(sheet_name)
        except EOFError:
            pass


help_text = """
                The Optional Commands:
                  - set [cell] [value] - Set the value of a cell (value can be a number or words).
                  - set [cell] [formula] - Set the formula for a cell and updates its value.
                            PAY ATTENTION! the formula must start with "=" sign.
                            the formulas should be combination of numbers and cells only.
                            there are 5 special formulas: 'AVERAGE' 'MIN' 'MAX' 'SUM' 'SQRT'. 
                            these formulas should be typed in a specific form: 
                            for example: =MAX(A1:B2) is correct and set the maximum number in the range of A1 and B2. 
                            for SQRT operator a valid form: =SQRT(A1).
                  - quit - Exit the program with option to save.
                  - show - shows the spreadsheet in an organized table
                  - remove [cell] - Removes the cell's value
                  - new - opens a new sheet in your workbook
                  - sheets - if you want to see the sheet's list and choose which sheet to open
                  - rename sheet - if you want to rename a sheet
                  - remove sheet - if you want to removes a sheet
                  - save - if you want to save the workbook
                  - export - if you want to export the workbook to a different file type
                  - graph [type] [range1] [range2] - if you want to create a graph. 
                    the graph types are: 'bar', 'pie'. 
                    the first range needs to include one columns that represent the topics of the graph.
                    the second range needs to include one column that represent the values of the topics.
            """


def main() -> None:
    workbook, spreadsheet = get_spreadsheet()
    print("Type 'help' for options, or start editing.")
    while True:
        try:
            command = input("> ").strip()
        except EOFError:
            break
        if command.lower() == "quit":
            try:
                if input("Are you sure you want to quit? ").lower() == "yes":
                    if input("Would you like to save the workbook? ").lower() == "yes":
                        filename = input("what file name? ")
                        workbook.export_to_json(filename)
                        print("exiting workbook... Bye!")
                        break
                    else:
                        print("exiting workbook... Bye!")
                        break
                else:
                    continue
            except EOFError:
                continue
        if command.lower() == "help":
            print(help_text)
            continue

        if command.lower() == "save":
            workbook.export_to_json(workbook.name)
            print(f"Saved {workbook.name} successfully.")
            continue

        if command.lower() == "export":
            print("You can save the workbook in the following formats:")
            print("  - pdf")
            print("  - excel")
            print("  - csv")
            try:
                save_format = input("Please enter the format you want to save the spreadsheet in: ").lower()
                while save_format not in ["csv", "pdf", "excel"]:
                    save_format = input("Invalid format. Please enter either 'csv', 'pdf', or 'json'.").lower()
            except EOFError:
                continue
            if save_format.lower() == "csv":
                workbook.export_to_csv(workbook.name)
                print(f"Saved {workbook.name}.csv successfully.")
            elif save_format.lower() == "pdf":
                workbook.export_to_pdf(workbook.name)
                print(f"Saved {workbook.name}.pdf successfully.")
            elif save_format.lower() == "excel":
                workbook.export_to_excel(workbook.name)
                print(f"Saved {workbook.name}.xlsx successfully.")
            continue

        if command.lower().startswith("set"):
            try:
                _, cell_name, value = command.split(maxsplit=2)
                if not value.startswith("="):
                    spreadsheet.set_cell(cell_name, value=value)
                else:
                    formula = value[1:]
                    spreadsheet.set_cell(cell_name, formula=formula)
            except ValueError:
                print("Invalid command. Please use the format 'set [cell] [value]' or 'set [cell] [formula]'.")
                print("for more information type 'help'.")
                continue
            if spreadsheet.cells != {}:
                print(spreadsheet)
            continue

        if command.lower() == "show":
            print(spreadsheet)
            continue

        if command.lower().startswith("remove"):
            try:
                _, cell_name = command.split(maxsplit=1)
            except ValueError:
                print("Invalid command. Please use the format 'remove [cell]'.")
                continue
            spreadsheet.remove_cell(cell_name)
            print(spreadsheet)
            continue

        if command.lower() == "new":
            try:
                sheet_name = input("name the new sheet: ")
            except EOFError:
                continue
            workbook.add_sheet(sheet_name)
            spreadsheet = workbook.get_sheet(sheet_name)
            print(f"You're in {sheet_name} sheet. Type 'help' for options, or start editing.")
            continue

        if command.lower().startswith("sheets"):
            workbook.print_list()
            try:
                sheet_name = input("which sheet would you like to open? ")
                while sheet_name not in workbook.list_sheets():
                    workbook.print_list()
                    sheet_name = input("name did not found..."
                                       "which sheet would you like to open? ")
            except EOFError:
                continue
            spreadsheet = workbook.get_sheet(sheet_name)
            print(f"You're in {sheet_name} sheet. Type 'help' for options, or start editing.")
            print(spreadsheet)
            continue

        if command.lower().startswith("rename sheet"):
            workbook.print_list()
            try:
                sheet_name = input("which sheet would you like to rename? ")
                while sheet_name not in workbook.list_sheets():
                    sheet_name = input("name did not found..."
                                       "which sheet would you like to rename? ")
                new_name = input("which name would you like to call it? ")
            except EOFError:
                continue
            workbook.rename_sheet(sheet_name, new_name)
            spreadsheet = workbook.get_sheet(new_name)
            print(f"You're in {new_name} sheet. Type 'help' for options, or start editing.")
            continue

        if command.lower() == "remove sheet":
            workbook.print_list()
            try:
                sheet_name = input("which sheet would you like to remove? ")
                while sheet_name not in workbook.list_sheets():
                    workbook.print_list()
                    sheet_name = input("name did not found..."
                                       "which sheet would you like to remove? ")
            except EOFError:
                continue
            workbook.remove_sheet(sheet_name)
            spreadsheet = workbook.get_sheet
            if workbook.list_sheets():
                sheet_name = workbook.list_sheets()[0]
                spreadsheet = workbook.get_sheet(sheet_name)
                print(f"You're in {sheet_name} sheet.")
            else:
                print("There are no sheets in the workbook.")
            continue

        if command.lower().startswith("graph"):
            try:
                _, graph_type, range1, range2 = command.split(maxsplit=3)
            except ValueError:
                print("Invalid command. Please use the format 'graph [type] [range1] [range2]'.")
                continue
            spreadsheet.create_graph(graph_type, range1, range2)


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--help":
            print(help_text)
    except IndexError:
        pass
    main()
