#!/usr/bin/env python3

import unittest

from calc_hopkins import *

class TestCalcHopkins(unittest.TestCase):
    def test_gen_set_Y(self):
        m = 5
        xlim_min = -100
        xlim_max = 100
        zlim_min = -100
        zlim_max = 100
        Y = gen_set_Y( xlim_min, xlim_max, zlim_min, zlim_max, m )

        ## check to make sure the correct number of samples produced
        self.assertEqual( len(Y), m )
        
        ## check to make sure the coordinates are in the box
        for y in Y:
            y_x = y[0]
            y_z = y[1]
            x_is_ok = (xlim_min < y_x) and (y_x < xlim_max)
            z_is_ok = (zlim_min < y_z) and (y_z < zlim_max)
            self.assertTrue( x_is_ok )
            self.assertTrue( z_is_ok )
        return

    def test_gen_set_Xm(self):
        X = [ (0,0), (1,1), (2,2), (3,3), (4,4),
              (5,5), (6,6), (7,7), (8,8), (9,9),
              (10,10), (11,11), (12,12), (13,13) ]
        m = 3
        Xm = gen_set_Xm(X, m)

        self.assertEqual( len(Xm), m )
        for xm in Xm:
            self.assertTrue( xm in X )
        return

    def calc_dist(self):
        a = (0,0)
        b = (1,1)
        dist = calc_dist(a,b)

        expectedDist = np.sqrt(
            np.power( (a[0]-b[0]),2 ) +
            np.power( (a[1]-b[1]), 2 ))

        self.assertTrue( expectedDist*(1-0.1) < dist )
        self.assertTrue( dist < expectedDist*(1+0.1) )
        return
        
    def test_find_nn(self):
        X = [ (0,0), (1,1), (2,2), (3,3) ]
        p = (1,2)
        v = find_nn(p,X)

        expectedV = X[1]
        self.assertEqual( v, expectedV )
        return
    
    def test_calc_u_vec(self):
        X = [ (0,0), (1,1), (2,2), (3,3), (4,4),
              (5,5), (6,6), (7,7), (8,8), (9,9),
              (10,10), (11,11), (12,12), (13,13) ]
        Y = [ (1,2), (3,4) ]
        m = 2

        u_vec = calc_u_vec(Y,X,m)
        expectedU_0 = calc_dist( Y[0], X[1] )
        expectedU_1 = calc_dist( Y[1], X[3] )
        expected_u_vec = [expectedU_0, expectedU_1]
        self.assertEqual( u_vec, expected_u_vec )
        return

    def test_w_vec(self):
        X = [ (0,0), (1,1), (2,2), (3,3), (4,4),
              (5,5), (6,6), (7,7), (8,8), (9,9),
              (10,10), (11,11), (12,12), (13,13) ]
        Xm = [ (0,0), (12,12)]
        m = 2

        w_vec = calc_w_vec(Xm, X, m )

        expectedW_0 = calc_dist( Xm[0], X[1] )
        expectedW_1 = calc_dist( Xm[1], X[11] )
        expected_w_vec = [expectedW_0, expectedW_1]
        self.assertEqual( w_vec, expected_w_vec )
        return

    def test_calc_hopkins(self):
        X = [ (0,0), (1,1), (2,2), (3,3), (4,4),
              (5,5), (6,6), (7,7), (8,8), (9,9),
              (10,10), (11,11), (12,12), (13,13) ]
        Y = [ (1,2), (3,4) ]
        Xm = [ (0,0), (12,12)]
        m = 2
        d = 2

        u_vec = calc_u_vec( Y, X, m )
        w_vec = calc_w_vec( Xm, X, m )

        print( "\t[info] u_vec: {}".format( u_vec ))
        print( "\t[info] w_vec: {}".format( w_vec ))
        
        H = calc_hopkins( u_vec, w_vec, m, 2 )
        expectedH = 0.333339  ## computed by hand.

        print( "\t[info] H: {}".format( H ))
        print( "\t[info] expectedH: {}".format( expectedH ))
        epsilon = 0.1
        self.assertTrue( expectedH*(1-epsilon) <= H )
        self.assertTrue( H <= expectedH*(1+epsilon) )
        return

if __name__ == "__main__":
    unittest.main()
