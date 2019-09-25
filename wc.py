from argparse import ArgumentParser
from re import findall, M, compile, match
from os import path, listdir
import gui

def parse_test():
    parser = ArgumentParser(description="Process integers.")
    # 添加有关参数
    parser.add_argument('-c', action='store_true', help="Return number of characters.")
    parser.add_argument('-w', action='store_true', help="Return number of words.")
    parser.add_argument('-l', action='store_true', help="Return number of lines.")
    parser.add_argument('-s', action='store_true', help="Recursively processes all files in the directory.")
    parser.add_argument('-a', action='store_true', help="Return more complex data.")
    parser.add_argument('-x', action='store_true', help="Graphical interface.")
    # 输入directory时
    parser.add_argument('directory', type=str, help="Directory of files.")
    args = parser.parse_args()
    return args

class WC():
    def __init__(self, args):
        # 保存所有查询过的文件信息
        self.info = []
        # 保存所有待查询文件地址
        self.file_list = []
        # 保存参数信息
        self.args = args
        # 判断是否是否为命令行模式
        self.flag = True

    # 获取文件词数目、词数目、行数、代码行、空行、注释行
    def CountFunc(self):
        if len(self.file_list) == 0:
            self.info.append("找不到该文件.")
        for file in self.file_list:
            note_count = 0
            code_count = 0
            space_count = 0
            flag = False
            base_name = path.basename(file)
            # 使用utf-8遇到有中文会报错
            with open(file, 'r', encoding='ISO-8859-1') as f:
                f_read = f.read()
                # 数字符
                if self.args.c:
                    char_num = len(findall(r'\S', f_read, M))
                    self.info.append(base_name + " 字符数: " + str(char_num))
                # 数单词
                if self.args.w:
                    word_num = len(findall(r'[a-zA-Z]+', f_read, M))
                    self.info.append(base_name + " 单词数: " + str(word_num))
                f.close()
            with open(file, 'r', encoding='ISO-8859-1') as f:
                f_readline = f.readlines()
                # 数行
                if self.args.l:
                    line_num = len(f_readline)
                    self.info.append(base_name + " 行数: " + str(line_num))
                # 数代码行、空行、注释行
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

    # 循环处理文件
    def RecursionPro(self):
        dir_path = path.dirname(self.args.directory)
        file_name = path.basename(self.args.directory)
        if '*' in file_name:
            if '.' in file_name:
                match_format = compile('{}{}'.format(file_name.replace('.', '\.').replace('*', '\w+'), '$'))
                for file in listdir(dir_path):
                    if match(match_format, file):
                        self.file_list.append(path.join(dir_path, file))
        elif '?' in file_name:
            if '.' in file_name:
                match_format = compile('{}{}'.format(file_name.replace('.', '\.').replace('*', '\w'), '$'))
                for file in listdir(dir_path):
                    if match(match_format, file):
                        self.file_list.append(path.join(dir_path, file))
        if len(self.file_list) == 0:
            if path.exists(self.args.directory):
                self.file_list.append(self.args.directory)

    # 调用函数
    def main(self):
        dir_path = path.dirname(self.args.directory)
        if dir_path:
            self.info.append("路径: " + dir_path)
        else:
            self.info.append("路径输入错误.")
        # 命令行模式
        if self.flag:
            if self.args.s == True:
                self.RecursionPro()
                self.CountFunc()
            else:
                if path.exists(self.args.directory):
                    self.file_list.append(self.args.directory)
                    self.CountFunc()
                else:
                    self.info.append(path.basename(self.args.directory) + " 文件不存在.")
        # gui模式
        else:
            self.CountFunc()

        if self.args.x == False:
            for info in self.info:
                print(info)
        return self.info

def main_test():
    args = parse_test()
    if args.x:
        args.c = True
        args.w = True
        args.l = True
        args.a = True
        args.directory = ""
        gui.GUI(args)
    else:
        wc = WC(args)
        wc.main()


if __name__ == '__main__':
    main_test()