from src.Collect_and_Process import collection,Process

class Main:
    def __init__(self):
        self.CL = collection.Data_Collection()
        self.PC = Process

if __name__ == "__main__":
    main = Main()
    main.CL.Collection()
    # main.PC.Pre().Read_info()
    # print(f"{'='*50}")
    # main.PC.Pre().Imbalance_Check()
    main.PC.Pre().Normalization()

# TODO: tạm thời là code vẫn trong qua trình build nên không có việc làm hiện tại
