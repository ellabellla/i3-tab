import unittest
import wm

class WMTest(unittest.TestCase):
    def test_add_window(self):
        window_manager = wm.WindowManager(testing=True)
        
        window_manager.add_window('1', 'first')
        window_manager.add_window('2', 'second')
        window_manager.add_window('3', 'third')
        
        self.assertEqual([{'id':'3', 'name':'third'}, {'id':'2', 'name':'second'},{'id':'1', 'name':'first'}], list(window_manager._windows))
    
    
    def test_remove_window(self):
        window_manager = wm.WindowManager(testing=True)
        
        window_manager._windows = [{'id':'3', 'name':'third'}, {'id':'2', 'name':'second'},{'id':'1', 'name':'first'}]
        window_manager.remove_window('2')
        
        self.assertEqual([{'id':'3', 'name':'third'}, {'id':'1', 'name':'first'}], list(window_manager._windows))
    
    def test_move_to_front(self):
        window_manager = wm.WindowManager(testing=True)
        
        window_manager._windows = [{'id':'3', 'name':'third'}, {'id':'2', 'name':'second'},{'id':'1', 'name':'first'}]
        window_manager.move_to_front('1')
        
        self.assertEqual([{'id':'1', 'name':'first'}, {'id':'3', 'name':'third'}, {'id':'2', 'name':'second'}], list(window_manager._windows))
    
    def test_flip(self):
        window_manager = wm.WindowManager(testing=True)
        
        window_manager._windows = [{'id':'3', 'name':'third'}, {'id':'2', 'name':'second'},{'id':'1', 'name':'first'}]
        window_manager.flip()
        
        self.assertEqual([{'id':'2', 'name':'second'}, {'id':'3', 'name':'third'}, {'id':'1', 'name':'first'}], list(window_manager._windows))
    
    def test_front(self):
        window_manager = wm.WindowManager(testing=True)
        
        window_manager.add_window('1', 'first')
        self.assertEqual({'id':'1', 'name':'first'}, window_manager.front())
        
        window_manager.add_window('2', 'second')
        self.assertEqual({'id':'2', 'name':'second'}, window_manager.front())
        
        window_manager.add_window('3', 'third')
        self.assertEqual({'id':'3', 'name':'third'}, window_manager.front())
        
if __name__ == '__main__':
    unittest.main()