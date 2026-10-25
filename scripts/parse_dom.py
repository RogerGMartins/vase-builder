from html.parser import HTMLParser
from pathlib import Path
import json
class Parser(HTMLParser):
 def __init__(self):
  super().__init__(convert_charrefs=True);self.root={'tag':'document','attrs':{},'children':[]};self.stack=[self.root]
 def handle_starttag(self,tag,attrs):
  n={'tag':tag,'attrs':{k:v or '' for k,v in attrs},'children':[]};self.stack[-1]['children'].append(n)
  if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:self.stack.append(n)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i]['tag']==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):
  if data.strip():self.stack[-1]['children'].append(data)
p=Parser();p.feed(Path('src/index.template.html').read_text(encoding='utf-8'));Path('dist/ux-dom.json').write_text(json.dumps(p.root),encoding='utf-8')
