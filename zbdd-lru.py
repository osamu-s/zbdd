#!/usr/bin/env python3

from functools import lru_cache

class Bdd_node:
    def __init__(self, top, lo, hi):
        self.top = top
        self.lo = lo
        self.hi = hi

class ZBDD_Nodes:
    def __init__(self):
        self.nodes = dict()

    def get(self, top, lo, hi):
        if (hi == 0):
            # node elimination
            return lo

        p = self.nodes.get((top, lo, hi), None)
        return (p if p
                else self.nodes.setdefault((top, lo, hi),
                                           Bdd_node(top, lo, hi) ))

    def print(self):
        print(self.nodes)



    def subset1(self, p, var):
        @lru_cache(maxsize=256)
        def _subset1(p, var):
            return self.get(p.top,
                            self.subset1(p.lo, var),
                            self.subset1(p.hi, var) )
            
        if (p == 0 or p == 1): return p
        if p.top < var: return p
        if p.top == var: return p.hi
        # if p.top > var:
        return _subset1(p, var)


    def subset0(self, p, var):
        @lru_cache(maxsize=256)
        def _subset0(p, var):
            return self.get(p.top,
                            self.subset0(p.lo, var),
                            self.subset0(p.hi, var) )

        if (p == 0 or p == 1): return p
        if p.top < var: return p
        if p.top == var: return p.lo
        # if p.top > var:
        return _subset0(p, var)

    @lru_cache(maxsize=256)
    def change(self, p, var):
        if p.top < var:
            return self.get(var, 0, p)
        if p.top == var: 
            return self.get(var, p.hi, p.lo)
        # if p.top > var:
        return self.get(p.top,
                        self.change(p.lo, var),
                        self.change(p.hi, var) )


    def union(self, p, q):
        @lru_cache(maxsize=256)        
        def _union(p, q):
            if p.top > q.top:
                return self.get(p.top, self.union(p.lo, q), p.hi)
            # if  p.top == q.top:
            return self.get(p.top,
                            self.union(p.lo, q.lo),
                            self.union(p.hi, q.hi) )

        if p == 0: return q
        if q == 0: return p
        if p == q: return p
        if p.top < q.top:
            # union is Commutative, for hit cache by lru_cache(maxsize=256)
            return self.union(q, p)
        return _union(p, q)

    def intersec(self, p, q):
        @lru_cache(maxsize=256)
        def _intersec(p, q):
            return self.get(p.top,
                            self.intersec(p.lo, q.lo),
                            self.intersec(p.hi, q.hi) )
            
        if p == 0: return 0
        if q == 0: return 0
        if p == q: return p
        if p.top < q.top:
            return self.intersec(q, p)
        if p.top > q.top:
            return self.intersec(p.lo, q)
        # if  p.top == q.top:
        return _intersec(p, q)
                        

    def diff(self, p, q):
        @lru_cache(maxsize=256)
        def _diff(p, q):
            if p.top > q.top:
                return self.get(p.top, self.diff(p.lo, q), p.hi)
            # if  p.top == q.top:
            return self.get(p.top,
                            self.diff(p.lo, q.lo),
                            self.diff(p.hi, q.hi) )
            
        if p == 0: return 0
        if q == 0: return p
        if p == q: return 0
        if p.top < q.top:
            return self.diff(p, q.lo)
        return _diff(p, q)


    def count(self, p):
        @lru_cache(maxsize=256)
        def _count(p):
            return self.count(p.lo) + self.count(p.hi)
            
        if p == 0: return 0
        if p == 1: return 1
        return _count(p)


if __name__ == '__main__':
    n = ZBDD_Nodes()
    p1 = n.get(1,0,1)
    p2 = n.get(2,0,1)
    q = n.union(p1, p2)
    n.print()
    print(n.count(q))
    p = n.subset1(q, 1)
    print (p)

    
