# -*- coding: utf-8 -*-
import re
import codecs

class Abbreviation(object):
    PATTERN_BOOK = u'[가-힣]{1,2}'
    PATTERN_CHAPTER_VERSE = u'[0-9]{1,3}\:[0-9|\-|\,]*[0-9]'
    
    @classmethod
    def identify_bible_verse(cls, contents):
        verse_pattern = re.compile(cls.PATTERN_BOOK + u'[ ]?' + cls.PATTERN_CHAPTER_VERSE)
        return verse_pattern.findall(contents)
        
    @classmethod
    def identify_book(cls, bible_verse):
        book_pattern = re.compile(cls.PATTERN_BOOK)
        result_list = book_pattern.findall(bible_verse)
        if result_list is None or len(result_list) <= 0:
            return None
        
        return result_list[0]
        
    @classmethod
    def identify_verse(cls, bible_verse):
        book_pattern = re.compile(cls.PATTERN_CHAPTER_VERSE)
        result_list = book_pattern.findall(bible_verse)
        if result_list is None or len(result_list) <= 0:
            return None
        
        return result_list[0]
            
class Book(object):
    """Bible book matching between Korean abbreviation and full name, 
        and between Korean and English (for DB)."""
    bible_abbr_to_kor = {
    	u'창': u'창세기',
    	u'출': u'출애굽기',
    	u'레': u'레위기',
    	u'민': u'민수기',
    	u'신': u'신명기',
    	u'수': u'여호수아',
    	u'삿': u'사사기',
    	u'룻': u'룻기',
    	u'삼상': u'사무엘상',
    	u'삼하': u'사무엘하',
    	u'왕상': u'열왕기상',
    	u'왕하': u'열왕기하',
    	u'대상': u'역대상',
    	u'대하': u'역대하',
    	u'스': u'에스라',
    	u'느': u'느헤미야',
    	u'에': u'에스더',
    	u'욥': u'욥기',
    	u'시': u'시편',
    	u'잠': u'잠언',
    	u'전': u'전도서',
    	u'아': u'아가',
    	u'사': u'이사야',
    	u'렘': u'예레미야',
    	u'애': u'예레미야애가',
    	u'겔': u'에스겔',
    	u'단': u'다니엘',
    	u'호': u'호세아',
    	u'욜': u'요엘',
    	u'암': u'아모스',
    	u'옵': u'오바댜',
    	u'욘': u'요나',
    	u'미': u'미가',
    	u'나': u'나훔',
    	u'합': u'하박국',
    	u'습': u'스바냐',
    	u'학': u'학개',
    	u'슥': u'스가랴',
    	u'말': u'말라기',
    	u'마': u'마태복음',
    	u'막': u'마가복음',
    	u'눅': u'누가복음',
    	u'요': u'요한복음',
    	u'행': u'사도행전',
    	u'롬': u'로마서',
    	u'고전': u'고린도전서',
    	u'고후': u'고린도후서',
    	u'갈': u'갈라디아서',
    	u'엡': u'에베소서',
    	u'빌': u'빌립보서',
    	u'골': u'골로새서',
    	u'살전': u'데살로니가전서',
    	u'살후': u'데살로니가후서',
    	u'딤전': u'디모데전서',
    	u'딤후': u'디모데후서',
    	u'딛': u'디도서',
    	u'몬': u'빌레몬서',
    	u'히': u'히브리서',
    	u'약': u'야고보서',
    	u'벧전': u'베드로전서',
    	u'벧후': u'베드로후서',
    	u'요일': u'요한일서',
    	u'요이': u'요한이서',
    	u'요삼': u'요한삼서',
    	u'유': u'유다서',
    	u'계': u'요한계시록'
    }
    
    @classmethod
    def get_kor_bible_from_abbr(cls, abbr):
        if abbr not in cls.bible_abbr_to_kor.keys():
            return None
        
        return cls.bible_abbr_to_kor[abbr]

class Verse(object):
    """Extracts chapter and verses from abbreviation forms"""
    @staticmethod
    def get_chapter(verse_str):
        if u':' not in verse_str:
            return -1
            
        pos = verse_str.index(u':')
        return int(verse_str[:pos])
        
    @staticmethod
    def get_verses(verse_str):
        if u':' not in verse_str:
            return []
        
        pos = verse_str.index(u':')
        result_list = []
        
        prv_num = u''
        num = u''
        op = u''
        for ch in verse_str[(pos + 1):]:
            if ch in u'0123456789':
                num += ch
            else:
                if len(prv_num) <= 0:
                    if ch == u',':
                        result_list.append(int(num))
                        prv_num = u''
                        num = u''
                        op = u''
                    else:
                        prv_num = num
                        num = u''
                        op = ch
                else:
                    curr_list = Verse.get_verse_list(prv_num, num)
                    if len(curr_list) > 0:
                        result_list.extend(curr_list)
                    prv_num = u''
                    num = u''
                    op = u''
                    
        if len(op) <= 0:
            result_list.append(int(num))
        else:
            curr_list = Verse.get_verse_list(prv_num, num)
            if len(curr_list) > 0:
                result_list.extend(curr_list)
        
        return result_list
    
    @staticmethod
    def get_verse_list(str_from, str_to):
        int_from = int(str_from)
        int_to = int(str_to)
        
        if int_from >= int_to:
            return None
            
        return range(int_from, (int_to + 1))
