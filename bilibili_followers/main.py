import sys
from scrapy import cmdline

cmdline.execute("scrapy crawl followers".split())
# cmdline.execute(f"scrapy crawl {sys.argv[1]}".split())
