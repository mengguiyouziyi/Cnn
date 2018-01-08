from cnn_scrapy.util.info import etl


class CreateTable(object):
    def __init__(self, t_name):
        self.conn = etl
        self.cur = self.conn.cursor()
        self.t_name = t_name
        # if self._checkExists():
        #     print('This table is exist,Please check out!')
        #     exit(1)

    def create(self):
        """
            url = scrapy.Field()
            title = scrapy.Field()
            author = scrapy.Field()
            update_time = scrapy.Field()
            cat = scrapy.Field()
            pic = scrapy.Field()
            keyword = scrapy.Field()
            text = scrapy.Field()
        """
        sql = """
		CREATE TABLE IF NOT EXISTS `{}` (
          `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
          `url` varchar(500) DEFAULT '' COMMENT '网页url',
          `title` varchar(500) DEFAULT '' COMMENT '菜谱名称',
          `author` varchar(500) DEFAULT '' COMMENT '喜欢数',
          `update_time` varchar(500) DEFAULT '' COMMENT '照片数',
          `cat` varchar(500) DEFAULT '' COMMENT '菜谱介绍',
          `pic` varchar(500) DEFAULT '' COMMENT '作者url',
          `keyword` longtext COMMENT '作者',
          `text` longtext COMMENT '配料',
          
          `load_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '落地时间',
          PRIMARY KEY (`id`),
          KEY `index_title` (`title`),
          KEY `index_url` (`url`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='cnn新闻';
		""".format(self.t_name)
        self.cur.execute(sql)
        self.conn.commit()

    # def _checkExists(self):
    #     sql = """SELECT * FROM information_schema.tables WHERE table_name = '{0}'""".format(self.t_name)
    #     self.cur.execute(sql)
    #     if self.cur.fetchone():
    #         return True
    #     return False


if __name__ == '__main__':
    # print(etl.get_host_info())
    # print(etl.get_proto_info())
    ct = CreateTable('cnn')
    ct.create()
