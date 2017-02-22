# -*- coding: utf-8 -*-
import sqlite3
from bible import Bible

class DBBook(object):
    '''Transform book fullname to the table (book) in DB'''
    book_fullname_to_db = {
    	u'창세기': 'Genesis',
    	u'출애굽기': 'Exodus',
    	u'레위기': 'Leviticus',
    	u'민수기': 'Numbers',
    	u'신명기': 'Deuteronomy',
    	u'여호수아': 'Joshua',
    	u'사사기': 'Judges',
    	u'룻기': 'Ruth',
    	u'사무엘상': 'FirstSamuel',
    	u'사무엘하': 'SecondSamuel',
    	u'열왕기상': 'FirstKings',
    	u'열왕기하': 'SecondKings',
    	u'역대상': 'FirstChronicles',
    	u'역대하': 'SecondChronicles',
    	u'에스라': 'Ezra',
    	u'느헤미야': 'Nehemiah',
    	u'에스더': 'Esther',
    	u'욥기': 'Job',
    	u'시편': 'Psalms',
    	u'잠언': 'Proverbs',
    	u'전도서': 'Ecclesiastes',
    	u'아가': 'SongOfSongs',
    	u'이사야': 'Isaiah',
    	u'예레미야': 'Jeremiah',
    	u'예레미야애가': 'Lamentations',
    	u'에스겔': 'Ezekiel',
    	u'다니엘': 'Daniel',
    	u'호세아': 'Hosea',
    	u'요엘': 'Joel',
    	u'아모스': 'Amos',
    	u'오바댜': 'Obadiah',
    	u'요나': 'Jonah',
    	u'미가': 'Micah',
    	u'나훔': 'Nahum',
    	u'하박국': 'Habakkuk',
    	u'스바냐': 'Zephaniah',
    	u'학개': 'Haggai',
    	u'스가랴': 'Zechariah',
    	u'말라기': 'Malachi',
    	u'마태복음': 'Matthew',
    	u'마가복음': 'Mark',
    	u'누가복음': 'Luke',
    	u'요한복음': 'John',
    	u'사도행전': 'Acts',
    	u'로마서': 'Romans',
    	u'고린도전서': 'FirstCorinthians',
    	u'고린도후서': 'SecondCorinthians',
    	u'갈라디아서': 'Galatians',
    	u'에베소서': 'Ephesians',
    	u'빌립보서': 'Philippians',
    	u'골로새서': 'Colossians',
    	u'데살로니가전서': 'FirstThessalonians',
    	u'데살로니가후서': 'SecondThessalonians',
    	u'디모데전서': 'FirstTimothy',
    	u'디모데후서': 'SecondTimothy',
    	u'디도서': 'Titus',
    	u'빌레몬서': 'Philemon',
    	u'히브리서': 'Hebrews',
    	u'야고보서': 'James',
    	u'베드로전서': 'FirstPeter',
    	u'베드로후서': 'SecondPeter',
    	u'요한일서': 'FirstJohn',
    	u'요한이서': 'SecondJohn',
    	u'요한삼서': 'ThirdJohn',
    	u'유다서': 'Jude',
    	u'요한계시록': 'Revelation'
    }
    
    @classmethod
    def get_db_book(cls, book_fullname):
        if book_fullname not in cls.book_fullname_to_db.keys():
            return None
        
        return cls.book_fullname_to_db[book_fullname]
        
    @classmethod
    def is_valid(cls, book_fullname):
        return book_fullname in cls.book_fullname_to_db.keys()

class Execution(object):
    '''Execute the query with given bible information'''
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        
    def get_text(self, bible):
        db_book = DBBook.get_db_book(bible.book)
        if db_book is None:
            return {}
        
        self.cursor.execute('''SELECT * FROM %(book)s 
            WHERE contents_type = 1 AND chapter = %(chapter)s 
            AND verse IN (%(verses)s) 
            ORDER BY chapter ASC, verse ASC, verseIdx ASC''' % {
                'book': db_book, 'chapter': bible.chapter, 
                'verses': ', '.join(str(x) for x in bible.verse_list)}
        )
        
        results = {}
        for curr in self.cursor:
            chapter = curr[1]
            verse = curr[2]
            text = curr[5]
            
            # Some bible texts are divided into multiple verses.
            key = str(verse)
            if key in results:
                results[key] += ' ' + text
            else:
                results[key] = text
        
        return results
        
    def close_connection(self):
        self.conn.close()
