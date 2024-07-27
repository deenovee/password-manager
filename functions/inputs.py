class Inputs:
    def __init__(self):
        self.data = []

    def get_string(self, cat):
        print(f"Enter {cat}: ")
        new_string = input("")
        return new_string
        
    def get_int(self, cat):
        print(f"Enter {cat}: ")
        try:
            new_int = input("")
            new_int = int(new_int)
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)
        return new_int
    
    def get_boolean(self):
        try:
            boo = input("")
            if boo.lower() == 'y':
                return True
            elif boo.lower() == 'n':
                return False
            else:
                print('Enter y or n')
        except ValueError as e:
            print(e)
        except Exception as e:
            print(e)
        return