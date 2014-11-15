import unittest
import Model as m
import numpy as np

class TestOrigami(unittest.TestCase):
    #run these tests by placing "unittest.main()" in my file
    
    def setUp(self): #create EMU graph
        self.emu = m.Model(1.0,1.0)
        self.emu.add_node_to(source = None, x = 0.5, y = 0.25) #creates node 1
        self.emu.add_node_to(1,.5,.5) #creates node 2 attached to node1
        self.emu.add_node_to(2,.75,.75) #creates node 3 attached to node 2
        self.emu.add_node_to(2,.25,.75) #creates node 4 attached to node 2
    
  #  def test_add_delete(self):
   #     self.emu.add_node_to(3)
  #      self.emu.delete_node(4)
    
    #def test_draw(self):
     #   self.emu.draw()
    
    def test_dist(self):
        hyp = self.emu.dist(3,0,4,0)
        self.assertEqual(hyp,5.0)
        
    def test_all_leaf_nodes(self):
        leaf_nodes = self.emu.all_leaf_nodes()
        self.assertEqual(leaf_nodes,[1,3,4])       
        
    def test_is_leaf_node(self):
        self.assertEqual(self.emu.is_leaf_node(1),True)
        self.assertEqual(self.emu.is_leaf_node(2),False)
        self.assertEqual(self.emu.is_leaf_node(3),True)
        self.assertEqual(self.emu.is_leaf_node(4),True)
    
    def test_all_shortest_paths(self):
        
        return None
    
    def test_all_leaf_paths(self):
        return None
    
    def test_sum_of_strained_lengths(self):
        self.assertEqual(self.emu.sum_of_strained_lengths(1,3),2.0)
        self.assertEqual(self.emu.sum_of_strained_lengths(4,2),1.0)
            
    def test_objective_function(self):
        return None
        
    def test_constraints_function_index(self):
        ln = [1,2,3]
        ln2 = [1,2,8]
        ln3 = [1,2,4,6,7,8,9,10,15,18,19,20,21,29]
        ln4 = [4,5,6]
        ln5 = [4,9,10]
    
     
    def test_initial_guess(self):
        x0 = self.emu._scale_initial_guess()
        truth_value = np.array_equal(x0,[.5,.25,.75,.75,.25,.75,1.0])   
        self.assertTrue(truth_value)
            
    
    def test_construct_constraints(self):
    #create an array of the constraint functions, taken from the in-use construct_constrains function
        cons_array = self.emu._scale_construct_constraints()
        cons_array_functions = []
        for dictionary in cons_array:
            function = dictionary["fun"]
            cons_array_functions.append(function)
            
        #create functions to test in-use functions against
        x0 = self.emu._scale_initial_guess()
        value1_from_x0 = -x0[6]*2 + self.emu.dist(x0[0],x0[2],x0[1],x0[3])
        value2_from_x0 = -x0[6]*2 + self.emu.dist(x0[0],x0[4],x0[1],x0[5])
        value3_from_x0 = -x0[6]*2 + self.emu.dist(x0[2],x0[4],x0[3],x0[5])
        
        #different version, meant to be exactly like Model test:
        
        a = lambda x: -x[6]*2 + self.emu.dist(x[0],x[2],x[1],x[3])
        #b = lambda x:
        
        print "test,  value calculated directly from initial guess and distance"
        print value1_from_x0
        print value2_from_x0
        print value3_from_x0
        print "test, constraint functions acting on initial guess"
        print cons_array_functions[0](x0)
        print cons_array_functions[1](x0)
        print cons_array_functions[2](x0)
        print "--------------"
        self.assertTrue(np.allclose(value1_from_x0, cons_array_functions[0](x0),atol = .001))
        self.assertTrue(np.allclose(value2_from_x0, cons_array_functions[1](x0),atol = .001))
        self.assertTrue(np.allclose(value3_from_x0, cons_array_functions[2](x0),atol = .001))


    def test_preliminary_constraints(self):
    
        x0 = self.emu._scale_initial_guess()
        a = -x0[6]*2 + self.emu.dist(.5,.75,.25,.75)
        b = -x0[6]*2 + self.emu.dist(.5,.25, .25,.75)
        c = -x0[6]*2 + self.emu.dist(.75,.25, .75, .75)
        
        cons1_value = -x0[6]*2 + self.emu.dist(x0[0],x0[2],x0[1],x0[3])
        cons2_value = -x0[6]*2 + self.emu.dist(x0[0],x0[4],x0[1],x0[5])
        cons3_value = -x0[6]*2 + self.emu.dist(x0[2],x0[4],x0[3],x0[5])
        
        
        self.assertTrue(np.allclose(a, cons1_value, atol = .0101))
        self.assertTrue(np.allclose(b, cons2_value, atol = .0101))
        self.assertTrue(np.allclose(c, cons3_value, atol = .0101))


    def test_construct_bounds(self):
        bnds = self.emu._scale_construct_bounds()
        x0 = self.emu._scale_initial_guess()
        self.assertEqual(len(bnds),len(x0))
        for i in range(0,len(bnds)-1,2):
            self.assertEqual(bnds[i][1],self.emu.width)
            self.assertEqual(bnds[i+1][1],self.emu.height)
        self.assertEqual(bnds[-1][0],0)
        self.assertEqual(bnds[-1][1],min(self.emu.width,self.emu.height))
    
    def test_scale_optimization(self):
        self.emu.scale_optimization()
   
    
        
# RUN TESTS        
        
    
if __name__ == '__main__':
    unittest.main()
