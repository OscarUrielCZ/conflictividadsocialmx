from extract.extractor import extract
from transform.transformer import transform

sites = ['eluniversal', 'elpais', 'expansion']
filename = '2021_12_16_elpais_articles.csv'

def main():
    extract()
    #transform(filename)

if __name__ == '__main__':
    main()