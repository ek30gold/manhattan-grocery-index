import copy, unittest
import intake
BASE={"source_type":"receipt","evidence_ref":"private-1","store":{"name":"Store","address":"1 Main St"},"offers":[{"product":"Milk","price":3.5,"currency":"USD","unit":"gal","observed":"2026-09-15","evidence_type":"receipt_paid"}]}
class TestIntake(unittest.TestCase):
 def test_valid_receipt_merges_without_private_ref(self):
  stores=[{"id":"s1","name":"Store","address":"1 Main St"}]; intake.validate(copy.deepcopy(BASE)); sid,n=intake.merge(copy.deepcopy(BASE),stores)
  self.assertEqual((sid,n),("s1",1)); self.assertNotIn("private-1",jsonish(stores)); self.assertEqual(stores[0]["offers"][0]["confidence"],"high")
 def test_images_rejected(self):
  x=copy.deepcopy(BASE); x["image_url"]="private"; self.assertRaises(ValueError,intake.validate,x)
 def test_wrong_evidence_type_rejected(self):
  x=copy.deepcopy(BASE); x["offers"][0]["evidence_type"]="advertised_sale"; self.assertRaises(ValueError,intake.validate,x)
 def test_ambiguous_store_stops(self):
  self.assertRaises(ValueError,intake.merge,copy.deepcopy(BASE),[{"name":"Store","address":"1 Main St"}]*2)
def jsonish(x): return repr(x)
if __name__=='__main__': unittest.main()
