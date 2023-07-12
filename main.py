import os
import sys
from pdf.compress import PDFCompress

os.environ['CODESIGNING_REQUIRED'] = 'NO'
os.environ['CODE_SIGN_ENTITLEMENTS'] = 'none'
if __name__ == '__main__':
    args = sys.argv
    if len(args) < 4:
        print("请指定目录参数")
        exit(os.EX_OSERR)
    print(args)
    PDFCompress().execute_in_dir(args[1], int(args[2]), int(args[3]))

