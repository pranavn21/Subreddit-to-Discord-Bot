package src;
import junit.framework.*;

/*
Case 1: k = -1, list = {}. Expected Output: 0
Case 2: k = 0, list = {}. Expected Output: 0
Case 3: k = 2, list = {}. Expected Output: 0
Case 4: k = 2, list = {2, 2,4}. Expected Output: 2
Case 5: k = 3, list = {2,2,4}. Expected Output: 2
*/

public class AverageTest {
    public class SimpleTest extends TestCase {

        protected Average avg1, avg2, avg3, avg4, avg5, avg;
    

        public void test1()
        {
        int k= -1; 
        int[] numlist = {};
        assertTrue(avg1.average(k, numlist) == 0);
    }

        public void test2()
        {int k= 0; int[] numlist = {};
        assertTrue(avg2.average(k, numlist) == 0);}

        public void test3()
        {int k= 2; int[] numlist = {};
        assertTrue(avg3.average(k, numlist) == 0);}

        public void test4()
        {int k= 2; int[] numlist = {2,2,4};
        assertTrue(avg4.average(k, numlist) == 2);}

        public void test5()
        {int k= 3; int[] numlist = {2,2,4};
        assertTrue(avg5.average(k, numlist) == 2);}
    
        public  Test suite()
        { return new TestSuite (SimpleTest.class); }
        
    
    }
}
