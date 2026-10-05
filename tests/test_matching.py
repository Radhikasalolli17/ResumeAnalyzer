import unittest
from modules.jd_matcher import JDMatcher
class TestJD(unittest.TestCase):
    def test_match(self):
        jm = JDMatcher('all-MiniLM-L6-v2')
        m, miss = jm.match_skills(['Python', 'Java'], ['Python', 'SQL'])
        self.assertIn('Python', m)
        self.assertIn('Sql', miss)
if __name__ == '__main__': unittest.main()
