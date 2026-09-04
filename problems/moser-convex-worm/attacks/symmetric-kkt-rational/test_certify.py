import unittest
import certify as c

class Tests(unittest.TestCase):
    def test_replay(self): c.verify()
    def test_unit_length(self):
        v,L=c.data();self.assertEqual(sum(L[:4]),1);self.assertTrue(all(c.dot(x,x)==1 for x in v))
    def test_allocations(self):
        v,L=c.data();self.assertEqual(tuple(c.alloc(v,L)),((0,2,4),(0,3,4),(1,2,4),(1,3,4)))
    def test_radical_order(self):
        self.assertGreater(c.sg(c.F(-265,153),c.F(1)),0);self.assertLess(c.sg(c.F(-1351,780),c.F(1)),0)
if __name__=='__main__':unittest.main()
