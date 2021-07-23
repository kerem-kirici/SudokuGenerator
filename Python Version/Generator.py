from PIL import Image, ImageDraw, ImageFont
import random
import time
import os


class Generator:

    def __init__(self, array=None, N=3):

        self.N = N
        self.n_solutions = 0
        self.img_size = 450

        if not os.path.exists("Puzzles"):
            os.makedirs("Puzzles")

        self.a = []
        self.positions = []
        self.source_numbers = []
        self.starting_array = []

        for i in range(N*N):
            self.a.append([])
            self.starting_array.append([])
            self.source_numbers.append(i+1)
            for j in range(N*N):
                self.a[-1].append(0 if array is None else array[i][j])
                self.starting_array[-1].append(0 if array is None else array[i][j])
                self.positions.append((i, j))


    def __valid(self, row, col, num, source=None):
        if source is None:
            f = lambda i, j: self.a[i][j]
        else:
            f = lambda i, j: source[i][j]

        for y in range(self.N*self.N):
            if f(y, col) == num:
                return False

        for x in range(self.N*self.N):
            if f(row, x) == num:
                return False

        for i in range(self.N):
            for j in range(self.N):
                if f(row + i - row % self.N, col + j - col % self.N) == num:
                    return False

        return True

    def __solve_for_solutions(self):
        for row in range(self.N*self.N):
            for col in range(self.N*self.N):
                if self.a[row][col] == 0:
                    for num in range(1, self.N*self.N+1):
                        if self.__valid(row, col, num):
                            self.a[row][col] = num
                            self.__solve_for_solutions()
                            self.a[row][col] = 0
                            if self.n_solutions > 1:
                                return
                    return

        self.n_solutions += 1

    def solve(self, source=None):
        for row in range(self.N*self.N):
            for col in range(self.N*self.N):
                if self.a[row][col] == 0:
                    for num in range(1, self.N*self.N+1):
                        if self.__valid(row, col, num):
                            self.a[row][col] = num
                            if self.solve():
                                return True
                            self.a[row][col] = 0
                    return False
        return True
        
    def __count_solutions(self):
        self.n_solutions = 0
        self.__solve_for_solutions()

    def show(self):
        print()
        for i in self.a:
            for j in range(self.N*self.N):
                print(i[j], end="{}".format(" " if j != self.N*self.N-1 else "\n"))
        print()

    def __shuffle_source(self):
        random.shuffle(self.source_numbers)

    def __create(self):
        self.__count_solutions()
        if self.n_solutions == 0:
            return False
        elif self.n_solutions == 1:
            return True

        while True:
            position_index = random.randint(0, len(self.positions)-1)
            (y, x) = self.positions.pop(position_index)

            self.__shuffle_source()

            for num in self.source_numbers:
                if self.__valid(y, x, num):
                    self.a[y][x] = num
                    if self.__create():
                        return True
                    self.a[y][x] = 0

            self.positions.insert(position_index, (y, x))

    def __reset(self):
        self.a = []
        self.positions = []
        self.source_numbers = []

        for i in range(N*N):
            self.a.append([])
            self.source_numbers.append(i+1)
            for j in range(N*N):
                self.a[-1].append(self.starting_array[i][j])
                self.positions.append((i, j))

    def generate(self):
        self.__create()
        self.__count_solutions()
        if self.n_solutions == 0: print("No Solution Exists.")
        elif self.n_solutions == 1: print("1 Solution Exists.")
        else: print("Several Solutions Exist.")
        self.show()

    def make_image(self, source=None):
        if source is None:
            f = lambda i, j: self.a[j][i]
        else:
            f = lambda i, j: source[j][i]
        with Image.open("empty_grid.jpg") as im:
            im = im.resize((self.img_size, self.img_size))
            draw = ImageDraw.Draw(im)
            font = ImageFont.truetype("arial.ttf", self.img_size//11)
            for i in range(self.N*self.N):
                for j in range(self.N*self.N):
                    if f(i, j) != 0:
                        draw.text((i*self.img_size//(self.N*self.N)+self.img_size//(self.N*self.N*2), j*self.img_size//(self.N*self.N)+self.img_size//(self.N*self.N*2)),
                                  "{}".format(f(i, j)), font=font, fill=(50, 50, 50, 255), anchor="mm")
            im.save("./Puzzles/Sudoku-{}.jpg".format(int(time.time())), "JPEG")
            im.show()

    def run(self):
        print("\n1- Generate Puzzle (it may take a while)\n2- Enter a Puzzle to Make Image\n3- Solve Puzzle (prints 1 of the possible solutions)\n4- Quit")
        while True:
            inp = 0
            sinp = input("Command: ")
            while True:
                try: 
                    inp = int(sinp)
                    if 0 < inp <= 4:
                        break
                    else: print("Enter a valid input.")
                except:
                    print("Enter a valid input.")
                    sinp = input("Command: ")
                
            if inp == 1:
                self.generate()
                self.make_image()

            elif inp == 2:
                source = []
                for _ in range(self.N*self.N):
                    source.append(list(map(int, input().strip().split())))

                self.make_image(source)

            elif inp == 3:
                self.a = []
                for _ in range(self.N*self.N):
                    self.a.append(list(map(int, input().strip().split())))

                self.solve()
                self.show()

            elif inp == 4:
                break




if __name__ == "__main__":
    g = Generator()
    g.run()
