import codecs
import os

def codefix(filename):
    contents = None
    with codecs.open(filename, 'r', 'gbk') as source:
        contents = source.read()
    if contents!=None:
        with codecs.open(filename, 'w', 'utf-8') as target:
            target.write(contents)
    else:
        raise RuntimeError

def main():
    filelist = [filename for filename in os.listdir('./raw') if filename.endswith('.txt')]
    for filename in filelist:
        codefix(os.path.join('raw', filename))

if __name__ == '__main__':
    main()
