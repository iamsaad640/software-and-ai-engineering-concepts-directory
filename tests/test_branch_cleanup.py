import unittest
from scripts.cleanup_branches import candidates

def branch(name,sha='abc',protected=False):
    return {'name':name,'commit':{'sha':sha},'protected':protected}
def pr(name,sha='abc',state='closed',merged=True):
    return {'head':{'ref':name,'sha':sha},'state':state,'merged_at':'2026-10-08' if merged else None}
class CleanupTests(unittest.TestCase):
    def test_preserves_default_protected_and_open_branches(self):
        branches=[branch('main'),branch('protected',protected=True),branch('active'),branch('merged')]
        prs=[pr('main'),pr('protected'),pr('active'),pr('active',state='open',merged=False),pr('merged')]
        self.assertEqual([b['name'] for b in candidates(branches,prs,'main')],['merged'])
    def test_preserves_new_commits_after_merge_and_unmerged_heads(self):
        branches=[branch('revived','new'),branch('closed'),branch('untracked')]
        self.assertEqual(candidates(branches,[pr('revived','old'),pr('closed',merged=False)],'main'),[])
    def test_squash_merged_head_is_eligible_by_exact_sha(self):
        self.assertEqual(candidates([branch('feature')],[pr('feature')],'main'),[branch('feature')])
if __name__=='__main__':
    unittest.main()
