# -*- coding: utf-8 -*-
import scrapy

from hongsejiashu.items import HongsejiashuItem


class JiashuSpider(scrapy.Spider):
    name = 'jiashu'
    allowed_domains = ['siyanhui.wenming.cn']
    start_urls = ['http://siyanhui.wenming.cn/zt/hongsejiashu/hsjs/']

    def parse(self, response):
        jiashu_list = response.xpath('//div[@id="text_list"]//li')
        for jiashu in jiashu_list:
            name = jiashu.xpath('./a/text()').extract_first()
            info_url = 'http://siyanhui.wenming.cn/zt/hongsejiashu/hsjs/' + jiashu.xpath('./a/@href').extract_first()
            request = scrapy.Request(info_url, callback=self.jiashu_info)
            request.meta['name'] = name
            yield request

    def jiashu_info(self, response):
        item = HongsejiashuItem()
        item['name'] = response.meta['name']
        # print(dir(content))
        # content.remove(content.getchildren()[0])
        content = response.xpath('//div[@class="TRS_Editor"]')[0].xpath('string(.)').extract_first()\
            .replace('.TRS_Editor TABLE{font-family:宋体;font-size:16px;}\n', '')\
            .replace('.TRS_Editor{font-family:宋体;font-size:16px;}\n', '')\
            .replace('.TRS_Editor ', '')\
            .replace('P{font-family:宋体;font-size:16px;margin-top:0em;margin-bottom:0em;line-height:1.4;}\n', '')\
            .replace('.TRS_Editor H1,.TRS_Editor H2,.TRS_Editor H3,.TRS_Editor ', '')\
            .replace('H4,.TRS_Editor H5,.TRS_Editor H6,.TRS_Editor HR,.TRS_Editor ', '')\
            .replace('BLOCKQUOTE,.TRS_Editor DL,.TRS_Editor DD,.TRS_Editor ', '')\
            .replace('DT,.TRS_Editor OL,.TRS_Editor UL,.TRS_Editor LI,.TRS_Editor ', '')\
            .replace('PRE,.TRS_Editor CODE,.TRS_Editor TEXTAREA,.TRS_Editor ', '')\
            .replace('SELECT,.TRS_Editor CITE,.TRS_Editor PRE,.TRS_Editor ', '')\
            .replace('CENTER,.TRS_Editor TABLE,.TRS_Editor ', '')\
            .replace('DIV{margin-top:0em;margin-bottom:0em;line-height:1.4;}\n', '')\
            .replace('.TRS_Editor FORM,.TRS_Editor FIELDSET,.TRS_Editor ', '')\
            .replace('LEGEND,.TRS_Editor SELECT,.TRS_Editor TR,.TRS_Editor ', '')\
            .replace('TD,.TRS_Editor ', '')\
            .replace('TH{margin-top:0em;margin-bottom:0em;line-height:1.4;}\n', '')\
            .replace('.TRS_Editor BUTTON,.TRS_Editor OPTION,.TRS_Editor ', '')\
            .replace('ADDRESS,.TRS_Editor DFN,.TRS_Editor EM,.TRS_Editor ', '')\
            .replace('VAR,.TRS_Editor KBD,.TRS_Editor INPUT,.TRS_Editor ', '')\
            .replace('SMALL,.TRS_Editor SAMP,.TRS_Editor SUB,.TRS_Editor ', '')\
            .replace('SUP,.TRS_Editor SPAN,.TRS_Editor A,.TRS_Editor B,.TRS_Editor ', '')\
            .replace('I,.TRS_Editor U,.TRS_Editor S,.TRS_Editor STRONG,.TRS_Editor ', '')\
            .replace('LABEL,.TRS_Editor IMG,.TRS_Editor BR,.TRS_Editor ', '')\
            .replace('FONT{margin-top:0;margin-bottom:0;text-indent:0;}\n', '')\
            .replace('H1,H2,H3,H4,H5,H6,HR,BLOCKQUOTE,DL,DD,DT,OL,UL,LI,PRE,CODE,TEXTAREA,SELECT,CITE,PRE,CENTER,TABLE,FORM,FIELDSET,LEGEND,SELECT,TR,TD,BUTTON,OPTION,ADDRESS,DFN,EM,VAR,KBD,INPUT,SMALL,SAMP,SUB,SUP,SPAN,A,B,I,U,S,STRONG,LABEL,IMG,BR,\n', '')\
            .replace('P{font-family:宋体;font-size:16px;margin-top:0;margin-bottom:0;line-height:1.4;}\n', '')\
            .replace('FORM,FIELDSET,LEGEND,SELECT,TR,TD,TH{margin-top:0;margin-bottom:0;line-height:1.4;}\n', '')\
            .replace('BUTTON,OPTION,ADDRESS,DFN,EM,VAR,KBD,INPUT,SMALL,SAMP,SUB,SUP,SPAN,A,B,I,U,S,STRONG,LABEL,IMG,BR,\n', '')\
            .replace('H1,H2,H3,H4,H5,H6,HR,BLOCKQUOTE,DL,DD,DT,OL,UL,LI,PRE,CODE,TEXTAREA,SELECT,CITE,PRE,CENTER,TABLE,DIV{margin-top:0;margin-bottom:0;line-height:1.4;}\n', '')\
            .split('\n')
        item['content'] = [i for i in content if i != '']
        yield item
