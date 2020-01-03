from captcha.image import ImageCaptcha
import random
import sys
import os

nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
lower_char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
upper_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z']


class DataGenerator:
    def __init__(self, root_folder, size, test_ratio=0.25):
        """
            Root Folder<str> -> Folder to holder train_folder and test_folder
            size<int> -> How many Train Image to Generate
            Test Ratio<float> -> Default:0.25 (Test_size = trainsize * test_ratio)
        """
        self.root_folder = root_folder
        self.size = size
        self.test_ratio = test_ratio
        self.train_folder = os.path.join(root_folder + "/train/")
        self.test_folder = os.path.join(root_folder + "/test/")
        self.train_size = size
        self.test_size = int(size*0.25)
        print(f"Train Folder -> {self.train_folder}\tExpected Images: {self.train_size}")
        print(f"Test  Folder -> {self.test_folder}\tExpected Images:{self.test_size}")

    
    def build_charSet(self, clear_path=False):
        """
            clear_path<bool> -> If to rm all the images in the folder before generate?
        """
        if not os.path.exists(self.train_folder):
            os.makedirs(self.train_folder)
        else:
            if clear_path:
                os.system("rm " + self.train_folder + "/*.jpg")
                print("All Images in Train Folder have been Removed")           
        if not os.path.exists(self.test_folder):
            os.makedirs(self.test_folder)
        else:
            if clear_path:
                os.system("rm " + self.test_folder + "/*.jpg")
                print("All Images in Test  Folder have been Removed")           

        print("PATH Exist! Begin to Build Char Dataset...")
        self.__generate_charIMG(self.train_size, self.train_folder)
        print("Train Set Generate Complete!")
        self.__generate_charIMG(self.test_size,self.test_folder)
        print("Test  Set Generate Complete!")

    def build_captcharSet(self, clear_path=True):
        """
            clear_path<bool> -> If to rm all the images in the folder before generate?
        """
        if not os.path.exists(self.train_folder):
            os.makedirs(self.train_folder)
        else:
            if clear_path:
                os.system("rm " + self.train_folder + "/*")           
        if not os.path.exists(self.test_folder):
            os.makedirs(self.test_folder)
        else:
            if clear_path:
                os.system("rm " + self.test_folder + "/*")

        print("PATH Exist! Begin to Build Captcha Dataset...")
        self.__generate_captchaIMG(self.train_size, self.train_folder)
        print("Train Set Generate Complete!")
        self.__generate_captchaIMG(self.test_size, self.test_folder)
        print("Test  Set Generate Complete")
        
    

    def __generate_char(self):
        kind = random.randint(1,3)
        if kind == 1:
            index = random.randint(0,9)
            return nums[index]
        else:
            index = random.randint(0,25)
            if kind == 2:
                return lower_char[index]
            if kind == 3:
                return upper_char[index]

    def __generate_charIMG(self, size, path):
        unique = 0
        for _ in range(size):
            imc = ImageCaptcha(35, 45, font_sizes=list(range(35,45)))
            name = self.__generate_char()
            image = imc.generate_image(name)
            image.save(path + name + "_" + str(unique) + ".jpg")
            unique += 1
    
    def __generate_string(self):
        string = ""
        for _ in range(4):
            kind = random.randint(1,3)
            if kind == 1:
                index = random.randint(0,9)
                string += nums[index]
            else:
                index = random.randint(0,25)
                if kind == 2:
                    string += lower_char[index]
                elif kind == 3:
                    string += upper_char[index]
        return string

    def __generate_captchaIMG(self, size, path):
        unique = 0
        for _ in range(size):
            imc = ImageCaptcha(lambda x: int(100 + 40 * random.random()),
                                lambda x: int(45 + 20 * random.random()),
                                font_sizes=list(range(35,45)))
            name = self.__generate_string()
            image = imc.generate_image(name)
            image.save(path + name + "_" + str(unique) + ".jpg")
            unique += 1
    