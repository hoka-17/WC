import argparse, re, os


class WC():
    def __init__(self):
        self.info = []
        self.file_name = ""
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

    # 获取文件词数目、词数目、行数
    def BasicFunc(self):
        for file in self.file_list:
            base_name = os.path.basename(file)
            with open(file, 'r', encoding='utf-8') as f:
                f_read = f.read()
                if self.args.c:
                    char_num = len(re.findall(r'\S', f_read, re.M))
                    self.info.append(base_name + " 字符数: " + str(char_num))
                if self.args.w:
                    word_num = len(re.findall(r'[a-zA-Z]+', f_read, re.M))
                    self.info.append(base_name + " 单词数: " + str(word_num))
                f.close()
            if self.args.l:
                with open(file, 'r', encoding='utf-8') as f:
                    line_num = len(f.readlines())
                    self.info.append(base_name + " 行数: " + str(line_num))
                    f.close()

    # 主函数
    def main(self):
        self.parse()
        self.file_list.append(self.args.directory)
        self.BasicFunc()
        for info in self.info:
            print(info)


if __name__ == '__main__':
    WC().main()