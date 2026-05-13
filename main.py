from src.Collect_and_Process import collection

class Main:
    def __init__(self):
        self.CL = collection.Data_Collection()

if __name__ == "__main__":
    main = Main()
    main.CL.Collection()

