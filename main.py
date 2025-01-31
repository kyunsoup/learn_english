import argparse
import random
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument("--solution_path_list", nargs='+', default=[
    # r"english\Day1.txt",
    r"english\Day2.txt",
])
parser.add_argument("--question_path_list", nargs='+', default=[
    # r"korean\Day1.txt",
    r"korean\Day2.txt",
])
parser.add_argument("--daily_mode", action="store_true")
parser.add_argument("--non_random_mode", action="store_true")
parser.add_argument("--seed", type=int, default=int(time.time()))
parser.add_argument("--folder_path", type=str, default=r"record")

class Dataset():
    def __init__(self, solution_path_list, question_path_list, non_random_mode):
        self.solution_path_list = solution_path_list
        self.question_path_list = question_path_list
        
        shape = len(self.solution_path_list)
        
        self.solution_list = []
        self.question_list = []
        
        for i in range(shape):
            with open(self.solution_path_list[i], "r", encoding="utf-8") as file:
                for line in file:
                    self.solution_list.append(line.strip())
            with open(self.question_path_list[i], "r", encoding="utf-8") as file:
                for line in file:
                    self.question_list.append(line.strip())
                    
        if not non_random_mode:
            combined = list(zip(self.solution_list, self.question_list))
            # 랜덤 섞기
            random.shuffle(combined)

            # 다시 분리
            self.solution_list, self.question_list = zip(*combined)

            # 리스트로 변환
            self.solution_list = list(self.solution_list)
            self.question_list = list(self.question_list)
        
    
    def __len__(self):
        return len(self.solution_list)
    
    def __getitem__(self, idx):
        return self.solution_list[idx], self.question_list[idx]


def play(dataset, length, path):
    txt_path = os.path.join(path, "result.txt")
    count = 0
    
    for i in range(length):
        solution, question = dataset[i]
        print(str(i+1)+'번. ', question)
        answer = input("내 답: ")
        with open(txt_path, "a", encoding="utf-8") as file:
                file.write(str(i+1)+'번. '+ question+"\n")
                file.write("내 답: "+ answer+"\n")
                file.write("정 답: "+ solution+"\n")
                if answer==solution:
                    print("*정답*\n")
                    file.write("*정답*\n\n")
                    count += 1
                else:
                    print("정 답: "+solution)
                    print("*오답*\n")
                    file.write("*오답*\n\n")
                    
    with open(txt_path, "a", encoding="utf-8") as file:
        file.write("------------------------------------\n")
        print("------------------------------------")
        file.write("맞은 갯수: "+ str(count) + "/"+ str(length) +"\n")
        print("맞은 갯수: "+ str(count)+ "/"+ str(length))
        file.write("점수: "+ str(int(count/length*100))+"\n")
        print("점수: "+ str(int(count/length*100)))
        file.write("------------------------------------\n")
        print("------------------------------------")
         
                
            

def main():
    args = parser.parse_args()
    random.seed(args.seed)
    dataset = Dataset(solution_path_list=args.solution_path_list, question_path_list=args.question_path_list, non_random_mode=args.non_random_mode)
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = args.folder_path
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"폴더 생성: {folder_path}")
    save_folder_path = os.path.join(folder_path, current_time)
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)
        print(f"폴더 생성: {save_folder_path}")
    
    length = len(dataset)
    if args.daily_mode:
        length = 30
    
    play(dataset, length, save_folder_path)
        
        
if __name__ == "__main__":
    main()        
