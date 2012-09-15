from google.appengine.ext import db

class GlobalInfo(db.Model):
    # singleton object, keyname is "global"
    index_etag = db.ByteStringProperty(indexed=False)
    hg_revision = db.ByteStringProperty(indexed=False)
    hgtags_etag = db.ByteStringProperty(indexed=False)
    vim_version = db.ByteStringProperty(indexed=False)

class RawFileInfo(db.Model):
    # key name is basename e.g. "help.txt"
    etag = db.ByteStringProperty(indexed=False)
    redo = db.BooleanProperty(indexed=False)
    memcache_genid = db.IntegerProperty(indexed=False)

class RawFileData(db.Model):
    # key name is as for RawFileInfo
    data = db.BlobProperty()
    encoding = db.ByteStringProperty(indexed=False)

class ProcessedFileHead(db.Model):
    # key name is basename e.g. "help.txt"
    etag = db.ByteStringProperty(indexed=False)
    encoding = db.ByteStringProperty(indexed=False)
    expires = db.DateTimeProperty(indexed=False)
    numparts = db.IntegerProperty(indexed=False)
    data0 = db.BlobProperty()

class ProcessedFilePart(db.Model):
    # key name is basename + ":" + partnum (1-based), e.g. "help.txt:1"
    data = db.BlobProperty()

class MemcacheHead(object):
    # stored in memcache with a name like "help.txt"
    def __init__(self, head, genid):
        # head is ProcessedFileInfo
        self.etag = head.etag
        self.encoding = head.encoding
        self.expires = head.expires
        self.numparts = head.numparts
        self.data0 = head.data0
        self.genid = genid

class MemcachePart(object):
    # stored in memcache with a name like "0:help.txt:1"
    def __init__(self, part):
        # part is ProcessedFileDataPart
        self.data = part.data

def memcache_part_name(filename, genid, partnum):
    return '{}:{}:{}'.format(genid, filename, partnum)
