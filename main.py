from src.Collect_and_Process import collection,Process

class Main:
    def __init__(self):
        self.CL = collection.Data_Collection()
        self.PC = Process

if __name__ == "__main__":
    main = Main()
    # main.CL.Collection()
    # main.PC.Pre().Read_info()
    # print(f"{'='*50}")
    # main.PC.Pre().Imbalance_Check()
    main.PC.Pre().Normalization()

# TODO: someone nhận trách nhiệm làm cái schema.sql đi tao sẽ nghĩ cách để đẩy data:>>
# TODO: nếu ok thì làm luôn phần đẩy kết nối python với sql
# TODO: code sẽ ở phần src là chính nha
