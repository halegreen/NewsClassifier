#coding = utf-8
import urllib2;

def getHtml(url):
    try:
        page = urllib2.urlopen(url)
        html = page.read()
        '''html = html.replace('\n', '')'''
    except Exception:
        print "exception"
        return ''
    else:
        return html
