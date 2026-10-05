import unittest
from modules.ats_scorer import ATSScorer
class TestATS(unittest.TestCase):
    def test_score(self):
        sc = ATSScorer()
        res = sc.score_resume({"skills":["Python"]}, {"matched_skills":["Python"], "missing_skills":[]})
        self.assertEqual(res['breakdown']['skills_match'], 100)
if __name__ == '__main__': unittest.main()
