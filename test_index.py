import json,unittest
class IndexTests(unittest.TestCase):
 def load(self,n): return json.load(open(n))
 def test_counts(self):
  self.assertEqual(len(self.load('locations.json')),366)
  self.assertEqual(len(self.load('store_profiles.json')),366)
  self.assertTrue(400<=len(self.load('items.json'))<=600)
 def test_profile_ids_and_unknowns(self):
  loc={x['id'] for x in self.load('locations.json')}; p=self.load('store_profiles.json')
  self.assertEqual(loc,{x['location_id'] for x in p})
  self.assertTrue(all(x['profile_sources'] for x in p))
  self.assertFalse(any(v=='absent' for x in p for v in x['departments'].values()))
 def test_availability(self):
  allowed={'confirmed','expected','unknown','previously_confirmed'}
  for x in self.load('availability.json'):
   self.assertIn(x['status'],allowed); self.assertIn('price_observations',x); self.assertTrue(x['explanation'])
 def test_rules(self):
  for x in self.load('availability_rules.json'):
   self.assertTrue(x['version']); self.assertTrue(x['explanation_template'])
if __name__=='__main__': unittest.main()
