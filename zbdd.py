#!/usr/bin/env python3

def memoize(f):
    _fcache = {}
    def _helper(*args):
        v = _fcache.get(args, None)
        return (v if v
                else _fcache.setdefault(args, f(*args)) )
    return _helper

class Bdd_node:
    def __init__(self, top, lo, hi):
        self.top = top
        self.lo = lo
        self.hi = hi

class Nodes:
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


    @memoize
    def subset1(self, p, var):
        if p.top < var: return 0
        if p.top == var: return p.hi
        # if p.top > var:
        return self.get(p.top,
                        self.subset1(p.lo, var),
                        self.subset1(p.hi, var) )

    @memoize
    def subset0(self, p, var):
        if p.top < var: return 0
        if p.top == var: return p.lo
        # if p.top > var:
        return self.get(p.top,
                        self.subset0(p.lo, var),
                        self.subset0(p.hi, var) )

    @memoize
    def change(self, p, var):
        if p.top < var:
            return self.get(var, 0, p)
        if p.top == var: 
            return self.get(var, p.hi, p.lo)
        # if p.top > var:
        return self.get(p.top,
                        self.change(p.lo, var),
                        self.change(p.hi, var) )

    @memoize
    def union(self, p, q):
        if p == 0: return q
        if q == 0: return p
        if p == q: return p
        if p.top > q.top:
            return self.get(p.top, self.union(p.lo, q), p.hi)
        if p.top < q.top:
            return self.get(p.top, self.union(p, q.lo), q.hi)
        # if  p.top == q.top:
        return self.get(p.top,
                        self.union(p.lo, q.lo),
                        self.union(p.hi, q.hi) )
        
    @memoize
    def intersec(self, p, q):
        if p == 0: return 0
        if q == 0: return 0
        if p == q: return p
        if p.top > q.top:
            return self.intersec(p.lo, q)
        if p.top < q.top:
            return self.intersec(p, q.lo)
        # if  p.top == q.top:
        return self.get(p.top,
                        self.intersec(p.lo, q.lo),
                        self.intersec(p.hi, q.hi) )
                        
    @memoize
    def diff(self, p, q):
        if p == 0: return 0
        if q == 0: return p
        if p == q: return 0
        if p.top > q.top:
            return self.get(p.top, self.diff(p.lo, q), p.hi)
        if p.top < q.top:
            return self.diff(p, q.lo)
        # if  p.top == q.top:
        return self.get(p.top,
                        self.diff(p.lo, q.lo),
                        self.diff(p.hi, q.hi) )

    @memoize
    def count(self, p):
        if p == 0: return 0
        if p == 1: return 1
        return self.count(p.lo) + self.count(p.hi)


if __name__ == '__main__':
    n = Nodes()
    p1 = n.get(1,0,1)
    p2 = n.get(2,0,1)
    q = n.union(p1, p2)
    n.print()
    print(n.count(q))
    p = n.subset1(q, 1)
    print (p)

    
