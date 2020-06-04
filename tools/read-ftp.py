

from ftplib import FTP
import os
import datetime
class FTP_OP(object):
    def __init__(self, host, username, password, port):
        """
        初始化ftp
        :param host: ftp主机ip
        :param username: ftp用户名
        :param password: ftp密码
        :param port:  ftp端口 （默认21）
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        print('this is init')
    def ftp_connect(self):
        """
        连接ftp
        :return:
        """
        ftp = FTP()
        ftp.set_debuglevel(0)  # 不开启调试模式
        ftp.connect(host=self.host, port=self.port)  # 连接ftp
        ftp.login(self.username, self.password)  # 登录ftp
        print('this is connect')
        #python 默认会启动被动模式passive，被动模式会启用1024之后的端口，所以就会出现问题
        ftp.set_pasv(False)
        return ftp
    def download_file(self, ftp_file_path, dst_file_path):
        """
        从ftp下载文件到本地
        :param ftp_file_path: ftp下载文件路径
        :param dst_file_path: 本地存放路径
        :return:
        """
        path =  dst_file_path + ftp_file_path
        print(path)
        if not os.path.exists(path):
            os.makedirs(path)
        buffer_size = 10240  #默认是8192
        ftp = self.ftp_connect()
        print(ftp.getwelcome())  #显示登录ftp信息
        file_list = ftp.nlst(ftp_file_path)
        for file_name in file_list:
            print(file_name)
            write_file = dst_file_path+file_name
            f = open(write_file,'wb')
            ftp.retrbinary('RETR {0}'.format(file_name), f.write, buffer_size)
            f.close()
            print(f'已经下载文件{write_file}')
        ftp.quit()


if __name__ == '__main__':
    host = "47.93.195.113"
    username = "bangying"
    password = "GHECOi933PLMBu"
    port = 21
    # 获取当天的前一天日期
    now_date = (datetime.date.today() + datetime.timedelta(days=-2)).strftime('%Y%m%d')
    ftp_Company_path = f"/COMPANY/{now_date}/"
    ftp_Credit_path = f"/CREDIT/{now_date}/"
    ftp_Judrisk_path = f"/JUDRISK/{now_date}/"
    dst_file_path = "D:/new_ftp_data"

    ftp = FTP_OP(host=host, username=username, password=password, port=port)
    ftp.download_file(ftp_file_path=ftp_Company_path, dst_file_path=dst_file_path)
    ftp.download_file(ftp_file_path=ftp_Judrisk_path, dst_file_path=dst_file_path)
    ftp.download_file(ftp_file_path=ftp_Credit_path, dst_file_path=dst_file_path)

