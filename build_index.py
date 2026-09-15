import json,re,datetime,os
from pathlib import Path
ROOT=Path(__file__).parent
TODAY='2026-09-15'
CATS={
'produce':'''Apples|Bananas|Oranges|Lemons|Limes|Grapefruit|Pears|Peaches|Nectarines|Plums|Cherries|Grapes|Strawberries|Blueberries|Raspberries|Blackberries|Watermelon|Cantaloupe|Pineapple|Mangoes|Avocados|Tomatoes|Cherry tomatoes|Potatoes|Sweet potatoes|Yellow onions|Red onions|Garlic|Ginger|Carrots|Celery|Cucumbers|Zucchini|Eggplant|Bell peppers|Jalapeños|Broccoli|Cauliflower|Green beans|Asparagus|Corn|Spinach|Kale|Romaine lettuce|Iceberg lettuce|Arugula|Cabbage|Scallions|Cilantro|Parsley|Basil|Mint|Dill|Mushrooms|Bean sprouts|Bok choy|Daikon|Plantains|Coconuts|Yucca|Okra''',
'meat_and_poultry':'''Chicken breasts|Chicken thighs|Whole chicken|Chicken wings|Ground turkey|Turkey breast|Ground beef|Beef chuck|Beef sirloin|Ribeye steak|Skirt steak|Short ribs|Beef brisket|Pork chops|Pork shoulder|Pork tenderloin|Ground pork|Bacon|Italian sausage|Breakfast sausage|Lamb chops|Ground lamb|Leg of lamb|Veal cutlets|Duck breast|Whole duck|Goat meat|Beef liver|Oxtail|Kosher chicken''',
'seafood':'''Salmon fillets|Tuna steaks|Cod fillets|Tilapia|Halibut|Sea bass|Red snapper|Trout|Sardines|Anchovies|Shrimp|Scallops|Mussels|Clams|Oysters|Lobster|Crab|Calamari|Octopus|Smoked salmon|Salt cod|Mackerel|Eel|Fish roe|Canned tuna|Canned salmon|Frozen shrimp|Wild ocean fish|Shellfish''',
'dairy_and_eggs':'''Whole milk|2% milk|Skim milk|Lactose-free milk|Heavy cream|Half-and-half|Buttermilk|Butter|Salted butter|Unsalted butter|Large eggs|Egg whites|Greek yogurt|Plain yogurt|Flavored yogurt|Cottage cheese|Cream cheese|Sour cream|Cheddar cheese|Mozzarella|Parmesan|Feta|Goat cheese|Swiss cheese|Brie|Ricotta|Provolone|Oat milk|Almond milk|Soy milk|Coconut milk beverage|Kefir|Ghee|European butter''',
'bakery_and_bread':'''White bread|Whole wheat bread|Sourdough bread|Rye bread|Multigrain bread|Baguette|Ciabatta|Pita bread|Naan|Tortillas|Corn tortillas|Flour tortillas|Bagels|English muffins|Croissants|Dinner rolls|Hamburger buns|Hot dog buns|Challah|Brioche|Focaccia|Matzo|Lavash|Pumpernickel|Gluten-free bread|Pizza dough|Pie crust|Muffins|Doughnuts|Artisanal bread|Pastries''',
'pantry_and_dry_goods':'''All-purpose flour|Bread flour|Whole wheat flour|Cornmeal|Cornstarch|White sugar|Brown sugar|Powdered sugar|Baking soda|Baking powder|Active dry yeast|Vanilla extract|Cocoa powder|Chocolate chips|Rolled oats|Granola|White rice|Brown rice|Basmati rice|Jasmine rice|Arborio rice|Quinoa|Couscous|Barley|Farro|Lentils|Chickpeas|Black beans|Kidney beans|Pinto beans|Spaghetti|Penne|Macaroni|Rice noodles|Ramen noodles|Olive oil|Vegetable oil|Sesame oil|White vinegar|Apple cider vinegar|Soy sauce|Fish sauce|Hot sauce|Peanut butter|Almond butter|Honey|Maple syrup|Salt|Black pepper|Cumin|Paprika|Cinnamon|Turmeric|Oregano|Bay leaves''',
'canned_and_jarred_goods':'''Canned tomatoes|Tomato paste|Tomato sauce|Canned corn|Canned peas|Canned green beans|Canned chickpeas|Canned black beans|Canned kidney beans|Canned coconut milk|Canned pumpkin|Chicken broth|Vegetable broth|Beef broth|Jarred pasta sauce|Pesto|Salsa|Pickles|Olives|Capers|Artichoke hearts|Roasted red peppers|Sauerkraut|Kimchi|Jams and preserves|Apple sauce|Canned pineapple|Canned peaches|Canned soup|Chili crisp''',
'frozen_food':'''Frozen peas|Frozen corn|Frozen spinach|Frozen broccoli|Frozen mixed vegetables|Frozen berries|Frozen mango|Frozen pizza|Frozen french fries|Frozen hash browns|Frozen dumplings|Frozen ravioli|Frozen lasagna|Frozen burritos|Frozen waffles|Frozen pancakes|Ice cream|Gelato|Sorbet|Frozen yogurt|Frozen chicken nuggets|Frozen fish fillets|Frozen meatballs|Frozen veggie burgers|Frozen edamame|Frozen acai|Frozen pie crust|Frozen puff pastry|Frozen dinners|Frozen plantains''',
'beverages':'''Still water|Sparkling water|Cola|Ginger ale|Seltzer|Orange juice|Apple juice|Cranberry juice|Lemonade|Iced tea|Black tea|Green tea|Herbal tea|Coffee beans|Ground coffee|Instant coffee|Cold brew coffee|Hot cocoa|Coconut water|Sports drinks|Energy drinks|Kombucha|Oat milk beverage|Almond milk beverage|Tomato juice|Grape juice|Club soda|Tonic water|Nonalcoholic beer|Matcha powder''',
'snacks_and_sweets':'''Potato chips|Tortilla chips|Pretzels|Popcorn|Crackers|Rice cakes|Trail mix|Mixed nuts|Almonds|Peanuts|Cashews|Pistachios|Dried fruit|Fruit snacks|Granola bars|Protein bars|Dark chocolate|Milk chocolate|Gummy candy|Hard candy|Cookies|Chocolate sandwich cookies|Graham crackers|Marshmallows|Peanut butter cups|Caramels|Halva|Mochi|Pocky|Plantain chips''',
'prepared_food_and_deli':'''Rotisserie chicken|Deli turkey|Deli ham|Roast beef slices|Salami|Prosciutto|Mortadella|Tuna salad|Chicken salad|Egg salad|Potato salad|Coleslaw|Hummus|Prepared sushi|Prepared sandwiches|Prepared salads|Soup|Pizza slices|Fresh pasta|Prepared dumplings|Prepared kimchi|Cooked rice|Prepared curry|Prepared tacos|Olive bar|Cheese board|Smoked fish|Prepared falafel|Prepared foods|Deli meats''',
'international_and_specialty':'''Gochujang|Doenjang|Korean chili flakes|Korean rice cakes|Kimchi|Nori|Miso paste|Dashi|Soba noodles|Udon noodles|Mirin|Rice vinegar|Sushi rice|Wasabi|Japanese curry roux|Sichuan peppercorns|Doubanjiang|Black vinegar|Shaoxing wine|Hoisin sauce|Oyster sauce|Rice paper wrappers|Fresh rice noodles|Masa harina|Dried ancho chiles|Dried guajillo chiles|Tomatillos|Mexican crema|Cotija cheese|Achiote paste|Mole sauce|Cannellini beans|Polenta|00 flour|San Marzano tomatoes|Balsamic vinegar|Pecorino Romano|Tahini|Za'atar|Sumac|Pomegranate molasses|Harissa|Bulgur|Freekeh|Halloumi|Falafel mix|Basmati rice|Garam masala|Curry leaves|Tamarind paste|Chana dal|Toor dal|Paneer|Naan|Ghee|Papadum|Sambal oelek|Coconut aminos|Cassava flour|Fufu flour|Injera|Jerk seasoning|Dulce de leche''',
'dietary_and_wellness':'''Gluten-free flour|Gluten-free pasta|Gluten-free crackers|Gluten-free oats|Plant-based milk|Vegan cheese|Vegan butter|Vegan mayonnaise|Tofu|Tempeh|Seitan|Plant-based burgers|Nutritional yeast|Chia seeds|Flaxseed|Hemp seeds|Protein powder|Electrolyte powder|Probiotic drinks|Low-sodium broth|No-salt-added beans|Sugar-free sweetener|Stevia|Monk fruit sweetener|Keto bread|Cauliflower rice|Zucchini noodles|Organic produce|Kosher foods|Halal foods''',
'household_and_personal_care':'''Paper towels|Toilet paper|Facial tissues|Dish soap|Dishwasher detergent|Laundry detergent|Trash bags|Aluminum foil|Plastic wrap|Parchment paper|Food storage bags|All-purpose cleaner|Sponges|Hand soap|Toothpaste|Toothbrushes|Shampoo|Conditioner|Body wash|Deodorant|Tampons|Menstrual pads|Diapers|Baby wipes''',
'seasonal_and_holiday':'''Pumpkin pie|Pie pumpkins|Apple cider|Candy corn|Halloween candy|Panettone|Pandoro|Stollen|Eggnog|Gingerbread cookies|Candy canes|Latkes|Sufganiyot|Chocolate gelt|Matzo meal|Gefilte fish|Passover matzo|Hot cross buns|Easter candy|Chocolate eggs|King cake|Mooncakes|Lunar New Year dumplings|Mochi rice cakes|Ramadan dates|Rose water|Corned beef|Irish soda bread|Fresh cranberries|Cranberry sauce|Turkey|Stuffing mix|Gravy|Sweet potato casserole|Summer corn|Heirloom tomatoes|Stone fruit|Watermelon|Fresh figs|Chestnuts'''
}
ALIASES={'Scallions':['green onions','spring onions'],'Cilantro':['coriander leaves'],'Gochujang':['Korean red pepper paste','Korean chili paste'],'Korean chili flakes':['gochugaru'],'Chickpeas':['garbanzo beans'],'All-purpose flour':['AP flour'],'Confectioners sugar':['powdered sugar'],'Eggplant':['aubergine'],'Zucchini':['courgette'],'Plant-based milk':['non-dairy milk'],'Still water':['bottled water'],'Cola':['soda','pop'],'Prepared sushi':['sushi'],'Sichuan peppercorns':['Szechuan peppercorns'],'Masa harina':['corn masa flour'],'Cassava flour':['yuca flour'],'Yucca':['cassava','yuca'],'Bell peppers':['sweet peppers'],'Roma tomatoes':['plum tomatoes'],'Canned tomatoes':['tinned tomatoes']}
SPECIALTY={
 'korean':['Gochujang','Doenjang','Korean chili flakes','Korean rice cakes','Kimchi','Prepared kimchi'],
 'japanese':['Nori','Miso paste','Dashi','Soba noodles','Udon noodles','Mirin','Sushi rice','Wasabi','Japanese curry roux','Prepared sushi','Mochi','Pocky'],
 'chinese':['Sichuan peppercorns','Doubanjiang','Black vinegar','Shaoxing wine','Hoisin sauce','Oyster sauce','Fresh rice noodles','Chili crisp'],
 'mexican':['Masa harina','Dried ancho chiles','Dried guajillo chiles','Tomatillos','Mexican crema','Cotija cheese','Achiote paste','Mole sauce','Corn tortillas'],
 'italian':['Cannellini beans','Polenta','00 flour','San Marzano tomatoes','Balsamic vinegar','Pecorino Romano','Fresh pasta','Prosciutto','Mortadella'],
 'middle_eastern':['Tahini',"Za'atar",'Sumac','Pomegranate molasses','Harissa','Bulgur','Freekeh','Halloumi','Falafel mix','Prepared falafel','Halva'],
 'indian':['Basmati rice','Garam masala','Curry leaves','Tamarind paste','Chana dal','Toor dal','Paneer','Naan','Ghee','Papadum','Prepared curry']
}
def slug(s):
 s=s.lower().replace('&',' and '); s=re.sub(r"[^a-z0-9]+",'_',s).strip('_'); return s
items=[]; seen=set()
for cat,raw in CATS.items():
 for name in raw.split('|'):
  key=name.lower()
  if key in seen: continue
  seen.add(key)
  season=None
  if cat=='seasonal_and_holiday': season={'type':'event_or_calendar_window','label':'seasonal - check evidence date'}
  tags=[k for k,v in SPECIALTY.items() if name in v]
  items.append({'id':'item.'+slug(name),'name':name,'kind':'generic_item','primary_category':cat,'aliases':ALIASES.get(name,[]),'forms':[],'dietary_tags':[],'specialty_tags':tags,'seasonality':season,'brand_ids':[],'source':'curated_taxonomy','reviewed_at':TODAY})
assert 400<=len(items)<=600,len(items)
locations=json.load(open(ROOT/'locations.json'))
CHAINS=[('whole foods','chain.whole_foods','supermarket'),('h mart','chain.h_mart','international_supermarket'),('lidl','chain.lidl','discount_supermarket'),('trader joe','chain.trader_joes','supermarket'),('wegmans','chain.wegmans','supermarket'),('target','chain.target','grocery'),('morton williams','chain.morton_williams','supermarket'),('key food','chain.key_food','supermarket'),('foodtown','chain.foodtown','supermarket'),('food town','chain.foodtown','supermarket'),('c town','chain.c_town','supermarket'),('c-town','chain.c_town','supermarket'),('fine fare','chain.fine_fare','supermarket'),('fairway','chain.fairway','supermarket'),('westside market','chain.westside_market','supermarket')]
def profile(loc):
 n=loc['name'].lower(); fmt='unknown'; chain=None; specs=[]; conf='low'; rationale='No supported format inference beyond the public location record.'
 if loc['type']=='farmers_market': fmt='farmers_market'; conf='high'; rationale='NYC public farmers market record.'
 else:
  for term,c,f in CHAINS:
   if term in n: chain=c; fmt=f; conf='medium'; rationale='Versioned operator-name rule; store-level departments remain unknown.'; break
  if fmt=='unknown':
   if any(x in n for x in ['supermarket','food market','marketplace','grocery','market']): fmt='grocery'; conf='low'; rationale='Name-based format rule; broad and intentionally low confidence.'
   elif any(x in n for x in ['deli','bodega','convenience']): fmt='bodega_or_convenience'; conf='low'; rationale='Name-based format rule; broad and intentionally low confidence.'
 if any(x in n for x in ['h mart','korean']): specs += ['korean']; fmt='international_supermarket'; conf='medium'
 if any(x in n for x in ['dainobu','katagiri','sunrise mart','japanese']): specs += ['japanese']; fmt='specialty_store'; conf='medium'
 if any(x in n for x in ['hong kong','deluxe food','chinese']): specs += ['chinese']; fmt='specialty_store'; conf='medium'
 if any(x in n for x in ['mexico','mexican','zaragoza']): specs += ['mexican']; fmt='specialty_store'; conf='medium'
 if any(x in n for x in ['eataly','italian']): specs += ['italian']; fmt='specialty_store'; conf='medium'
 if any(x in n for x in ['kalustyan','sahadi','middle east']): specs += ['middle_eastern','indian']; fmt='specialty_store'; conf='medium'
 if any(x in n for x in ['indian','desi','kalustyan']): specs += ['indian']; fmt='specialty_store'; conf='medium'
 if 'whole foods' in n: fmt='natural_food_store'
 deps={k:'unknown' for k in ['produce','meat','butcher_counter','seafood','seafood_counter','dairy','bakery','deli','prepared_food','frozen','bulk_foods','beer','wine','household','personal_care','pharmacy']}
 # Department expectations are explicit inference, never fact.
 if fmt in ['supermarket','discount_supermarket','international_supermarket','natural_food_store']:
  for k in ['produce','meat','seafood','dairy','bakery','deli','prepared_food','frozen','household','personal_care']: deps[k]='expected'
 elif fmt in ['grocery','gourmet_market']:
  for k in ['produce','dairy','bakery','frozen','household']: deps[k]='expected'
 elif fmt=='farmers_market':
  deps['produce']='expected'; deps['prepared_food']='expected'
 snap=True if loc.get('accepts_ebt') is True else None
 return {'location_id':loc['id'],'operator':loc['name'],'chain_id':chain,'format':fmt,'specialties':sorted(set(specs)),'departments':deps,'snap_authorized':snap,'profile_sources':[{'source_url':loc['source_url'],'source_type':loc['source_type'],'observed_at':loc['observed'],'supports':['identity','location']},{'rule_id':'rule.profile_name_v1','supports':['format_inference','specialty_inference'],'rationale':rationale}],'profile_confidence':conf,'reviewed_at':TODAY}
profiles=[profile(x) for x in locations]
# Only pre-existing direct availability data becomes a relationship; conservative 30-day freshness makes it previous now.
name_to_id={i['name'].lower():i['id'] for i in items}
av=[]
for loc in locations:
 for label in loc.get('availability',[]):
  # Vendor/category phrases stay category needs; deterministic stable ID.
  iid='category.'+slug(label)
  av.append({'item_id':iid,'item_label':label,'location_id':loc['id'],'status':'previously_confirmed','evidence_type':loc.get('availability_type','public_roster'),'evidence_ref':loc.get('availability_source',loc['source_url']),'observed_at':loc['observed'],'valid_through':None,'confidence':'medium','explanation':'Previously listed by a public market roster; older than the 30-day direct-evidence window.','price_observations':[]})
rules=[]
# Everyday category rules. Conservative: only broad department/format expectation, medium or low.
for cat,dep in [('produce','produce'),('meat_and_poultry','meat'),('seafood','seafood'),('dairy_and_eggs','dairy'),('bakery_and_bread','bakery'),('frozen_food','frozen'),('prepared_food_and_deli','prepared_food'),('household_and_personal_care','household')]:
 rules.append({'id':'rule.department.'+cat,'when':{'department_expected_or_confirmed':dep},'categories':[cat],'confidence':'medium','explanation_template':'Expected from the {department} department profile','version':1,'reviewed_at':TODAY})
for cat in ['pantry_and_dry_goods','canned_and_jarred_goods','beverages','snacks_and_sweets']:
 rules.append({'id':'rule.format.'+cat,'when':{'formats_any':['supermarket','discount_supermarket','international_supermarket','natural_food_store','grocery']},'categories':[cat],'confidence':'low','explanation_template':'Expected from the store format profile','version':1,'reviewed_at':TODAY})
for sp,names in SPECIALTY.items():
 rules.append({'id':'rule.specialty.'+sp,'when':{'specialties_any':[sp]},'item_ids':[name_to_id[n.lower()] for n in names if n.lower() in name_to_id],'confidence':'medium','explanation_template':'Expected from the {specialty} specialty profile','version':1,'reviewed_at':TODAY})
# searchable category records
category_labels={k:k.replace('_',' ').title() for k in CATS}
coverage={'generated_at':TODAY,'locations_total':len(locations),'locations_profiled':len(profiles),'profiles_by_confidence':{},'profiles_by_format':{},'taxonomy_items':len(items),'taxonomy_by_category':{},'confirmed_relationships':sum(1 for x in av if x['status']=='confirmed'),'previously_confirmed_relationships':sum(1 for x in av if x['status']=='previously_confirmed'),'expected_rules':len(rules),'unknown_or_ambiguous_profiles':sum(1 for p in profiles if p['format']=='unknown'),'snap_authorized_confirmed':sum(1 for p in profiles if p['snap_authorized'] is True),'snap_unknown':sum(1 for p in profiles if p['snap_authorized'] is None),'freshness_policy':{'direct_evidence_days':30,'expected_rules':'re-evaluate on profile or rule change'}}
for p in profiles:
 coverage['profiles_by_confidence'][p['profile_confidence']]=coverage['profiles_by_confidence'].get(p['profile_confidence'],0)+1
 coverage['profiles_by_format'][p['format']]=coverage['profiles_by_format'].get(p['format'],0)+1
for i in items: coverage['taxonomy_by_category'][i['primary_category']]=coverage['taxonomy_by_category'].get(i['primary_category'],0)+1
for name,obj in [('items.json',items),('store_profiles.json',profiles),('availability.json',av),('availability_rules.json',rules),('coverage.json',coverage)]:
 json.dump(obj,open(ROOT/name,'w'),indent=2,ensure_ascii=False); open(ROOT/name,'a').write('\n')
print(json.dumps({'items':len(items),'profiles':len(profiles),'availability':len(av),'rules':len(rules),'coverage':coverage},indent=2))
