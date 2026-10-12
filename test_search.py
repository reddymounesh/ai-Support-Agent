from app.rag.vector_store import search

results = search("how to i get all my money back by tommorow")
for r in results:
    print(f"[{r['distance']}] (distance={r['distance']:.3f})")
    print(r['text'][:150])
    print()
    
    
    