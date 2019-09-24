import argparse, re, os


class WC():
    def __init__(self):
        self.info = []
        self.file_list = []

    # 解析命令行参数
    def parse(self):
        parser = argparse.ArgumentParser(description="Process integers.")
        parser.add_argument('-c', action='store_true', help="Return number of characters.")
        parser.add_argument('-w', action='store_true', help="Return number of words.")
        parser.add_argument('-l', action='store_true', help="Return number of lines.")
        parser.add_argument('-s', action='store_true', help="Recursively processes all files in the directory.")
        parser.add_argument('-a', action='store_true', help="Return more complex data.")
        parser.add_argument('-x', action='store_true', help="Graphical interface.")
        parser.add_argument('directory', type=str, help="Directory of files.")

        self.args = parser.parse_args()

    # 获取文件词数目、词数目、行数、代码行、空行、注释行
    def CountFunc(self):
        for file in self.file_list:
            note_count = 0
            code_count = 0
            space_count = 0
            flag = False
            base_name = os.path.basename(file)
            # 使用utf-8遇到有中文会报错
            with open(file, 'r', encoding='ISO-8859-1') as f:
                f_read = f.read()
                if self.args.c:
                    char_num = len(re.findall(r'\S', f_read, re.M))
                    self.info.append(base_name + " 字符数: " + str(char_num))
                if self.args.w:
                    word_num = len(re.findall(r'[a-zA-Z]+', f_read, re.M))
                    self.info.append(base_name + " 单词数: " + str(word_num))
                f.close()
            with open(file, 'r', encoding='ISO-8859-1') as f:
                f_readline = f.readlines()
                if self.args.l:
                    line_num = len(f_readline)
                    self.info.append(base_name + " 行数: " + str(line_num))
                for line in f_readline:
                    if "/*" in line:
                        note_count = note_count + 1
                        flag = True
                    elif flag:
                        note_count = note_count + 1
                        if "*/" in line:
                            flag = False
                    elif "//" in line:
                        note_count = note_count + 1
                    elif len(line.strip()) > 1:
                        code_count = code_count + 1
                    else:
                        space_count = space_count + 1
                f.close()

            if self.args.a:
                self.info.append(base_name + " 代码行: " + str(code_count))
                self.info.append(base_name + " 空行: " + str(space_count))
                self.info.append(base_name + " 注释行: " + str(note_count))

    def RecursionPro(self):
        dir_path = os.path.dirname(self.args.directory)
        file_name = os.path.basename(self.args.directory)
        if '*' in file_name:
            if '.' in file_name:
                match = re.compile('{}{}'.format(file_name.replace('.', '\.').replace('*', '\w+'), '$'))
                for file in os.listdir(dir_path):
                    if re.match(match, file):
                        self.file_list.append(os.path.join(dir_path, file))
        elif '?' in file_name:
            if '.' in file_name:
                match = re.compile('{}{}'.format(file_name.replace('.', '\.').replace('*', '\w'), '$'))
                for file in os.listdir(dir_path):
                    if re.match(match, file):
                        self.file_list.append(os.path.join(dir_path, file))


    # 主函数
    def main(self):
        self.parse()
        dir_path = os.path.dirname(self.args.directory)
        if dir_path:
            self.info.append("路径: " + dir_path)
        else:
            self.info.append("路径输入错误.")
        if self.args.s == True:
            self.RecursionPro()
            self.CountFunc()
        else:
            if os.path.exists(self.args.directory):
                self.file_list.append(self.args.directory)
                self.CountFunc()
            else:
                self.info.append(os.path.basename(self.args.directory) + " 文件不存在.")
        for info in self.info:
            print(info)


if __name__ == '__main__':
    WC().main()