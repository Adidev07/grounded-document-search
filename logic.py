import re, math
from collections import Counter
def tokens(text):
    return re.findall(r'[a-z0-9]+',text.lower())
def run(payload,records):
    query=str(payload.get('query','')).strip()
    if not query: raise ValueError('Enter a search query')
    docs=[Counter(tokens(r['text'])) for r in records]
    terms=set(tokens(query))
    def vector(counter):
        return {t:n*(1+math.log((1+len(docs))/(1+sum(t in d for d in docs)))) for t,n in counter.items()}
    qv=vector(Counter(tokens(query)))
    def cosine(v):
        denominator=math.sqrt(sum(x*x for x in qv.values())*sum(x*x for x in v.values()))
        return sum(qv.get(t,0)*x for t,x in v.items())/denominator if denominator else 0
    ranked=sorted([(cosine(vector(d)),r) for d,r in zip(docs,records)],key=lambda x:-x[0])
    hits=[dict(source=r['source'],passage=r['text'],score=round(s,4)) for s,r in ranked[:3] if s>0]
    return dict(query=query,answer=hits[0]['passage'] if hits else 'No matching evidence found. Try words present in the documents.',citations=hits, mode='Extractive TF-IDF retrieval; no LLM or embeddings.')
