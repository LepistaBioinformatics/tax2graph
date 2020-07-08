import pandas as pd


class FileParser:


    def read(self, file_path):

        df = pd.read_csv(file_path, sep='\t', header=0)
        
        for line in df:
            print(line)
            


if __name__ == '__main__':

    path = 'data/taxa.txt'
    parser = FileParser()
    parser.read(path)
