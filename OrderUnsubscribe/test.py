from matplotlib.pyplot import subplot
import pandas as pd
from sqlalchemy import create_engine

class mysqlconn:
    def __init__(self):
        mysql_username = 'root'
        mysql_password = '123456'
        # 填写真实数库ip
        mysql_ip = '36.137.236.71'
        port = 3306
        db = 'drf_if2'
        # 初始化数据库连接,使用pymysql库
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(mysql_username, mysql_password, mysql_ip, port,db))
 
    # 写入mysql数据库
    def to_sql(self,table,df):
        # 第一个参数是表名
        # if_exists:有三个值 fail、replace、append
        # 1.fail:如果表存在，啥也不做
        # 2.replace:如果表存在，删了表，再建立一个新表，把数据插入
        # 3.append:如果表存在，把数据插入，如果表不存在创建一个表！！
        # index 是否储存index列
        df.to_sql(table, con=self.engine, if_exists='append', index=False)

def process_csv(path_req,path_resp):

    headers = ['TraceId','MsgType','Version','OrderID','UserPseudoCode','ActionTime','ActionID','EffectiveRealTime','ExpireRealTime','ChannelId','ProductId','OrderType','sign','ProvCode']
    headers1 = ['TraceId','MsgType','Version','hRet','desc','UserPseudoCode','url','ProductId']
    #读取csv文件
    df_req = pd.read_csv(path_req, names=headers, header=None, engine='python', error_bad_lines=False)
    df_resp = pd.read_csv(path_resp, names=headers1, header=None, engine='python', error_bad_lines=False)
    # print(df_req.head().to_string())
    # print(df_resp.head().to_string())

    if not df_req.empty:
        # 对请求的UserPseudoCode去重
        df_SyncFlowPkgOrderReq_dup = df_req.drop_duplicates(subset=['UserPseudoCode'], keep='first',inplace=False)
    else:
        print("df_SyncFlowPkgOrderReq 为空")

    df_IF2 = pd.merge(df_SyncFlowPkgOrderReq_dup, df_resp, on='TraceId', how='left')
    # df_IF2 = df_IF2.fillna('-')

    # if df_IF2['ProductId_x'] == '500000050078':
    #     df_IF2['unit_flow'] = 30

    # print(df_IF2[df_IF2['ProductId_x'] == '500000050078'].head().to_string())

    #字符串转为日期
    df_IF2['ActionTime'] = pd.to_datetime(df_IF2['ActionTime'], format='%Y%m%d%H%M%S', errors='coerce')
    df_IF2['EffectiveRealTime'] = df_IF2['ActionTime'].fillna('1970-01-26 22:55:58')
    df_IF2['ActionTime'] = df_IF2['ActionTime'].dt.time
    df_IF2['EffectiveRealTime'] = pd.to_datetime(df_IF2['EffectiveRealTime'], format='%Y%m%d%H%M%S', errors='coerce')
    df_IF2.dropna(axis=0, subset=['ActionTime','EffectiveRealTime'])
    # df_IF2['EffectiveRealTime'] = df_IF2['EffectiveRealTime'].fillna('1970-01-26 22:55:58')  #处理时间日期字段为空值的情况
    
    df_IF2 = df_IF2.fillna('-')
    print(df_IF2.shape[0])
    print(df_IF2.info())
    print(df_IF2.head(30).to_string())


    # df_IF2.to_excel(r'D:\\卓望运维组\\logs文件\\订购关系new\\all_pycharm.xlsx')
    return df_IF2



if __name__ == '__main__':
    path_req =r"D:\\卓望运维组\\logs文件\\订购关系new\\SyncFlowPkgOrderReq副本.csv"
    path_resp =r"D:\\卓望运维组\\logs文件\\订购关系new\\SyncFlowPkgOrderResp副本.csv"
    df = process_csv(path_req,path_resp)

    #初始化数据库类
    my_sql = mysqlconn()
    #写入mysql
    my_sql.to_sql('if2_message',df)