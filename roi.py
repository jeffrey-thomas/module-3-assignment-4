import os
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Utility class that contains static methods to validate user input
class Input():

    # Make sure that a user input is a positive number
    @staticmethod
    def validate_non_negative_float(input):
        try:
            num = float(input)
            return num >= 0
        except ValueError:
            return False

    # Prompt the user for a positive number, reprompt if input is invalid
    @staticmethod
    def input_non_negative_float(prompt):
        num = input(prompt)
        while not Input.validate_non_negative_float(num):
            print("\nPlease enter a positive number.\n")
            num = input(prompt)
        return float(num)

    # ask for user input, compares it to a list of valid responses and reprompts if input is invalid
    # list of valid responses should be in lower case and have at least 1 element
    @staticmethod
    def validate_input(prompt:str, valid_responses:list[str]):
        answer = input(prompt+"\nResponse: ").lower()

        reprompt = "\nPlease respond with '" + valid_responses[0]
        for i in range(1,len(valid_responses)-1):
            reprompt += "', '" + valid_responses[i]
        reprompt += "' or '" + valid_responses[len(valid_responses)-1] +"'."

        while answer not in valid_responses:
            print(reprompt)
            answer = input(prompt).lower()

        return answer

# Class that holds a list of budget items and tracks the total as changes are made
class BudgetCategory():

    def __init__(self, name:str, items:dict[str,float]):
        self.name = name
        self.items = items
        self.total = 0
        for amount in items.values():
            self.total += amount

    # Add an item to this budget category
    # Overwrites any items with the same name
    def add_item(self,name:str, amount:float):
        if name in self.items:
            self.remove_item(name)
        self.items[name] = amount
        self.total += amount

    # Removes the item with the provided name from the budget category, if it exists
    def remove_item(self, name):
        if name in self.items:
            amount = self.items.pop(name)
            self.total -= amount


    # returns the amount of the budget item with the provided name or None if it does not exist
    def get_amount(self, name):
        if name in self.items:
            return self.items[name]
        else:
            return None

    def update_item(self, name, amount):
        if name in self.items:
            self.total -= self.items[name]
            self.total += amount
            self.items[name] = amount
        else:
            self.add_item(name,amount)

    def input_amount(self, name):
        amount = Input.input_non_negative_float("Enter the amount for "+name+":")

        self.update_item(name,amount)

    def input_item(self):
        name = input("\nEnter the name for this item:").lower()
        self.input_amount(name)

    def input_all(self):
        for name in self.items.keys():
            self.input_amount(name)

    # returns if this budget category has an item with the given name
    def has(self, name):
        return name in self.items

    # returns a string representation of this budget category
    def to_string(self):
        result ="\n"+ self.name
        for name, amount in self.items.items():
            if amount:
                result += "\n\t"+name+":\t$"+str(amount)
        result += "\n\tTOTAL: $"+str(self.total)
        return result



class ROICalculator():

    #initialize categories with common entries' names
    def __init__(self):

        self.income = BudgetCategory(
            "Monthly Income",
            {
                "rental payment":0
            }
        )

        self.expenses = BudgetCategory(
            "Monthly Expenses",
            {
                "mortgage": 0,
                "property taxes": 0,
                "insurance": 0,
                "utilities":0,
                "vacancy":0,
                "repair fund":0,
                "capex fund": 0,
                "management":0
            }
        )

        self.investments = BudgetCategory(
            "Initial Investments",
            {
                "downpayment":0,
                "closing costs":0,
                "rehab":0,
            }
        )

    def run(self):
        clear_console()
        print("\nWelcome to the Rental Return on Investment Calculator.")
        print("\nWe will need information on the property in the following categories:")
        print("\t- Monthly Income\n\t- Monthly Expenses\n\t- Initial Investment Costs\n")
        self.press_enter()

        self.start_category(self.income)
        self.start_category(self.expenses)
        self.start_category(self.investments)

        self.print_summary()
        
        action = Input.validate_input("\nWhat would you like to do now?\n\t-Edit\n\t-Exit",["edit","exit"])
        while action != "exit":
            cat = Input.validate_input("\nWhich category do you want to make changes to?\n\t-Income\n\t-Expenses\n\t-Investments",["income","expenses","investments"])
            if cat == "income":
                self.edit_category(self.income)
            elif cat == "expenses":
                self.edit_category(self.expenses)
            else:
                self.edit_category(self.investments)

            clear_console()
            self.print_summary()
            action = Input.validate_input("\nWhat would you like to do now?\n\t-Edit\n\t-Exit",["edit","exit"])

    def start_category(self, category:BudgetCategory):
        
        # Get initial values for all items in the category
        print("\nWe will now begin working on "+category.name+".")
        print("Let's start by looking at some common items in this category.\n")
        category.input_all()
        
        # See if user has any new items to add
        prompt = "\nDo you have any other items to add to "+category.name+",'y' or 'n'? "
        ans = Input.validate_input(prompt, ["y","n"])
        
        while ans != "n":
            category.input_item()
            ans = Input.validate_input(prompt, ["y","n"])
        
        self.edit_category(category)
        self.press_enter()

    #add remove or update the amount of an item in a category
    def edit_category(self, category:BudgetCategory):
        print(category.to_string())
        prompt =  "\nAre there any actions you want to perform on an item in "+category.name+"?\n\t-add\n\t-remove\n\t-update\n\t-none\n"
        options = ['add','remove','update','none']
        action = Input.validate_input(prompt,options)

        while action != 'none':
            if action == 'add':
                category.input_item()
            elif action =='remove':
                name = input("Which item do you want to remove?").lower()
                category.remove_item(name)
            elif action == 'update':
                name = input("Which item do you want to update?").lower()
                category.input_amount(name)

            print(' ')
            print(category.to_string())
            action = Input.validate_input(prompt,options)

    def press_enter(self):
        input("Press ENTER to continue...")
        clear_console()
        
    def get_cash_flow(self):
        return self.income.total - self.expenses.total

    def print_summary(self):
        print("\nResults:")
        print("Total Monthly Income:\t$"+str(self.income.total))
        print("Total Monthly Expenses:\t$"+str(self.expenses.total))
        print("Total Initial Investments:\t$"+str(self.investments.total))
        print("Total Monthly Cash Flow:\t$"+str(self.get_cash_flow()))
        print("\nReturn on Investment:\t"+str(self.get_cash_flow()*1200/self.investments.total)+" %")

calc = ROICalculator()
calc.run()
