import os
from io import BytesIO
import fitz
from PIL import Image


class PDFCompress:
    """
    PDF文件压缩类
    """

    @staticmethod
    def execute_in_dir(path: str, dpi: int, pages: int):
        path = path.rstrip("/\\")
        out_put_path = "{}_压缩".format(path)
        if not os.path.exists(out_put_path):
            os.mkdir(out_put_path)
        # 遍历目录下的所有PDF文件
        for root, dirs, files in os.walk(path):
            for file in files:
                if not file.endswith(".pdf"):
                    continue
                print(f'正在压缩文件:{file}')
                PDFCompress.execute_file(os.path.join(root, file), os.path.join(out_put_path, file), dpi, "png", pages)

    @staticmethod
    def execute_file(_pdf: str, _out: str, _dpi=150, _type="png", _pages=-1):
        """
            本方法适用于纯图片型（包含文字型图片）的PDF文档压缩，可复制型的文字类的PDF文档不建议使用本方法
            :param _out: 输出文件全路径
            :param _pdf: 文件名全路径
            :param _dpi: 转化后图片的像素（范围72-600），默认150，想要清晰点，可以设置成高一点，这个参数直接影响PDF文件大小
                         测试：  纯图片PDF文件（即单个页面就是一个图片，内容不可复制）
                                300dpi，压缩率约为30-50%，即原来大小的30-50%，基本无损，看不出来压缩后导致的分辨率差异
                                200dpi，压缩率约为20-30%，轻微有损
                                150dpi，压缩率约为5-10%，有损，但是基本不影响图片形文字的阅读
            :param _type: 保存格式，默认为png，其他：JPEG, PNM, PGM, PPM, PBM, PAM, PSD, PS
            :param _pages: 压缩张数
            :return:
            """
        merges = []
        _file = None
        with fitz.open(_pdf) as doc:
            for i, page in enumerate(doc.pages(), start=0):
                if _pages != -1 and i >= _pages:
                    break
                img = page.get_pixmap(dpi=_dpi)  # 将PDF页面转化为图片
                img_bytes = img.pil_tobytes(format=_type)  # 将图片转为为bytes对象
                image = Image.open(BytesIO(img_bytes))  # 将bytes对象转为PIL格式的图片对象
                if i == 0:
                    _file = image  # 取第一张图片用于创建PDF文档的首页
                pix: Image.Image = image.quantize(colors=256).convert('RGB')  # 单张图片压缩处理
                merges.append(pix)  # 组装pdf
                # tqdm.write(f"\n{i} | success reduced  page: {i}.{_type}")
        _file.save(_out,
                   "pdf",  # 用PIL自带的功能保存为PDF格式文件
                   save_all=True,
                   append_images=merges[1:])
