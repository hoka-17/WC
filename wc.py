import argparse


class WC():
    def __init__(self):
        pass

    # 解析命令行参数
    def parse(self):
        parser = argparse.ArgumentParser(description="Process integers.")
        parser.add_argument('-c', action='store_true', help="Return number of characters.")
        parser.add_argument('-w', action='store_true', help="Return number of words.")
        parser.add_argument('-l', action='store_true', help="Return number of lines.")
        parser.add_argument('-s', action='store_true', help="Recursively processes all files in the directory.")
        parser.add_argument('-a', action='store_true', help="Return more complex data.")
        parser.add_argument('directory', type=str, help="Directory of files.")

        print(type(parser.parse_args()))
        self.args = parser.parse_args()

    def main(self):
        self.parse()

if __name__ == '__main__':
    WC().main()