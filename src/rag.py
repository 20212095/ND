"""Chroma with semantic ONNX all-MiniLM-L6-v2 embeddings of X only."""
from pathlib import Path
import hashlib
import json

def document(x):
    return 'Language: python\nContract: '+x['contract']+'\nCode:\n'+x['code']

class Retriever:
    def __init__(self, rows, path):
        import chromadb
        from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2
        self.embed=ONNXMiniLM_L6_V2()
        self.by_id={r['id']:r for r in rows}
        # Fingerprint prevents accidentally reusing a collection for changed data.
        digest=hashlib.sha256(json.dumps(rows,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:12]
        self.client=chromadb.PersistentClient(path=str(Path(path)))
        self.collection=self.client.get_or_create_collection(
            name='python_review_'+digest, embedding_function=None,
            configuration={'hnsw':{'space':'cosine'}},
            metadata={'embedding_model':'all-MiniLM-L6-v2','dataset_sha':digest})

    def index(self, batch_size=100):
        rows=list(self.by_id.values())
        if self.collection.count()==len(rows):
            return self.collection.count()
        for start in range(0,len(rows),batch_size):
            batch=rows[start:start+batch_size]
            texts=[document(r['x']) for r in batch]
            embeddings=self.embed(texts)
            self.collection.upsert(ids=[r['id'] for r in batch],documents=texts,
                embeddings=embeddings,
                metadatas=[{'family':r['family'],'source':r['source'],
                    'x_json':json.dumps(r['x'],ensure_ascii=False),
                    'y_json':json.dumps(r['y'],ensure_ascii=False)} for r in batch])
        return self.collection.count()

    def retrieve(self, x, k=3):
        if self.collection.count()<k:
            raise ValueError('Pirmiausia indeksuokite bent k pavyzdžių.')
        query=self.embed([document(x)])
        result=self.collection.query(query_embeddings=query,n_results=k,
                                     include=['metadatas','distances','documents'])
        rows=[]
        for ident,meta,distance in zip(result['ids'][0],result['metadatas'][0],result['distances'][0]):
            rows.append({'id':ident,'family':meta['family'],
                'x':json.loads(meta['x_json']),'y':json.loads(meta['y_json']),
                'distance':float(distance)})
        return rows
