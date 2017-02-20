# -*- coding: utf-8 -*-
class Bible(object):
    def __init__(self, book, chapter, verse_list, verse_info):
        self.book = book
        self.chapter = chapter
        self.verse_list = verse_list
        self.verse_info = verse_info
        self.words = {}
        
    def add_result(self, version, results):
        if version in self.words:
            del self.words[version]
        
        self.words[version] = results

    def test(self):
        print self.book + u' ' + str(self.chapter) + u':' + str(self.verse_list)
        
    def get_info_str(self):
        return self.book + u' ' + self.verse_info
        
    def get_words_in_version_str(self, version):
        content = u''
        for verse in self.verse_list:
            verse_str = str(verse)
            if verse_str in self.words[version]:
                if len(content) > 0:
                    content += u'\n'
                content += verse_str + '. ' + self.words[version][verse_str]
                
        return content
                
    def get_words_in_verse_str(self, verse, version_list):
        content = u''
        for version in version_list:
            verse_str = str(verse)
            if verse_str in self.words[version]:
                if len(content) > 0:
                    content += u'\n'
                content += verse_str + '. ' + self.words[version][verse_str]
                
        return content
        
    def get_print_str(self, version_list, b_version_first):
        if not version_list or len(version_list) <= 0:
            return u''
            
        for version in version_list:
            if not self.words[version]:
                return u'말씀을 찾을 수 없습니다.'
        
        content = self.get_info_str() + u'\n'
        if b_version_first:
            for version in version_list:
                if version in self.words:
                    content += self.get_words_in_version_str(version) + u'\n'
        else:
            for verse in self.verse_list:
                content += self.get_words_in_verse_str(verse, version_list) + u'\n'

        return content
