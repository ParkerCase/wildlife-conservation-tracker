# WildGuard AI - Comprehensive Endangered Species Keywords
# Based on CITES Appendices, IUCN Red List, and trafficking intelligence

TIER_1_CRITICAL_SPECIES = [
    # CITES Appendix I - Most critically endangered
    'african elephant', 'asian elephant', 'elephant ivory', 'ivory tusk', 'ivory carving',
    'black rhino', 'white rhino', 'javan rhino', 'sumatran rhino', 'rhino horn', 'rhinoceros horn',
    'siberian tiger', 'south china tiger', 'sumatran tiger', 'tiger bone', 'tiger skin', 'tiger tooth',
    'amur leopard', 'arabian leopard', 'persian leopard', 'leopard skin', 'leopard fur',
    'giant panda', 'snow leopard', 'jaguar pelt', 'cheetah fur',
    'pangolin scale', 'pangolin armor', 'chinese pangolin', 'sunda pangolin',
    'vaquita porpoise', 'manatee', 'dugong', 'right whale', 'blue whale',
    'hawksbill turtle', 'leatherback turtle', 'green turtle', 'turtle shell', 'tortoise shell',
    'mountain gorilla', 'cross river gorilla', 'orangutan', 'bornean orangutan', 'sumatran orangutan',
    'bonobo', 'chimpanzee', 'gibbon',
]

TIER_2_HIGH_PRIORITY_SPECIES = [
    # CITES Appendix II - High priority species
    'polar bear', 'grizzly bear', 'sun bear', 'sloth bear', 'bear bile', 'bear paw', 'bear gallbladder',
    'african lion', 'lion bone', 'lion tooth', 'lion claw',
    'clouded leopard', 'lynx fur', 'bobcat pelt', 'ocelot fur', 'margay fur', 'serval skin',
    'wolf pelt', 'grey wolf', 'mexican wolf', 'red wolf',
    'mako shark', 'great white shark', 'hammerhead shark', 'shark fin', 'shark cartilage',
    'bluefin tuna', 'sturgeon caviar', 'beluga caviar', 'paddlefish caviar',
    'coral red', 'black coral', 'brain coral', 'staghorn coral', 'elkhorn coral',
    'african grey parrot', 'macaw blue', 'scarlet macaw', 'hyacinth macaw',
    'golden eagle', 'bald eagle', 'harpy eagle', 'eagle feather', 'falcon',
    'kakapo parrot', 'california condor', 'whooping crane', 'hooded crane',
]

TIER_3_MEDIUM_PRIORITY_SPECIES = [
    # Additional threatened species
    'saiga antelope', 'saiga horn', 'addax antelope', 'oryx horn', 'gazelle horn',
    'snow monkey', 'proboscis monkey', 'langur monkey', 'macaque',
    'pangolin meat', 'pangolin leather', 'anteater scale',
    'crocodile skin', 'alligator leather', 'caiman leather', 'python leather',
    'monitor lizard', 'iguana leather', 'lizard skin', 'snake skin',
    'abalone shell', 'conch shell', 'giant clam', 'nautilus shell',
    'sea cucumber', 'seahorse dried', 'sea fan coral',
    'musk deer', 'deer musk', 'civet musk', 'beaver castor',
    'vicuna wool', 'shahtoosh shawl', 'tibetan antelope', 'chiru wool',
    'helmeted hornbill', 'toucan beak', 'hornbill beak', 'cassowary feather',
]

PLANT_SPECIES_KEYWORDS = [
    # Endangered plants and wood
    'brazilian rosewood', 'madagascar rosewood', 'cocobolo wood', 'lignum vitae',
    'african blackwood', 'ebony wood', 'sandalwood oil', 'sandalwood carving',
    'agarwood oil', 'oud wood', 'aloeswood', 'aquilaria wood',
    'american ginseng', 'asian ginseng', 'wild ginseng', 'ginseng root',
    'hoodia cactus', 'peyote cactus', 'barrel cactus rare', 'saguaro cactus',
    'lady slipper orchid', 'ghost orchid', 'vanilla orchid wild',
    'cycad plant', 'encephalartos cycad', 'zamia cycad',
    'pitcher plant', 'venus flytrap wild', 'sundew plant rare',
    'madagascar palm', 'pachypodium plant', 'adenium plant rare',
    'aloe polyphylla', 'spiral aloe', 'aloe suzannae', 'haworthia rare',
]

TRADITIONAL_MEDICINE_KEYWORDS = [
    # Traditional medicine trafficking terms
    'bear bile capsule', 'bear bile powder', 'bear gallbladder dried',
    'rhino horn powder', 'rhino horn shaving', 'rhinoceros horn medicine',
    'tiger bone wine', 'tiger bone powder', 'tiger bone glue',
    'pangolin scale medicine', 'pangolin scale powder', 'armadillo scale',
    'seahorse powder', 'seahorse medicine', 'dried seahorse',
    'turtle plastron', 'turtle shell medicine', 'tortoise plastron',
    'deer antler velvet', 'deer antler powder', 'elk antler',
    'shark cartilage powder', 'shark fin soup', 'shark liver oil',
    'cordyceps fungus', 'caterpillar fungus', 'ophiocordyceps',
    'ginseng wild', 'american ginseng root', 'panax ginseng',
    'snow lotus', 'saussurea flower', 'himalayan medicine',
    'musk deer pod', 'musk deer scent', 'natural musk',
]

TRAFFICKING_CODE_WORDS = [
    # Common euphemisms and code words
    'rare specimen', 'museum quality', 'private collection', 'estate collection',
    'grandfather clause', 'pre-ban', 'vintage specimen', 'antique specimen',
    'ethically sourced', 'sustainable harvest', 'legal import', 'cites permit',
    'tribal authentic', 'indigenous craft', 'ceremonial use', 'shamanic tool',
    'natural medicine', 'traditional remedy', 'ancient cure', 'healing stone',
    'collector grade', 'exhibition quality', 'research specimen', 'scientific specimen',
    'exotic material', 'rare material', 'unique specimen', 'one of a kind',
    'hard to find', 'extremely rare', 'last chance', 'final stock',
]

PRODUCT_COMBINATIONS = [
    # Combine species with products
    'ivory bracelet', 'ivory necklace', 'ivory figurine', 'ivory chess set',
    'fur coat', 'fur hat', 'fur trim', 'fur collar', 'pelt rug',
    'skin leather', 'exotic leather', 'leather boots', 'leather bag',
    'bone carving', 'bone jewelry', 'tooth pendant', 'claw necklace',
    'feather headdress', 'feather art', 'feather jewelry', 'plume decoration',
    'shell jewelry', 'shell carving', 'shell decoration', 'mother of pearl',
    'scale armor', 'scale decoration', 'scale medicine', 'dried scale',
    'horn carving', 'horn cup', 'horn powder', 'horn shaving',
]

GEOGRAPHIC_INDICATORS = [
    # High-trafficking regions
    'african wildlife', 'african trophy', 'south african', 'kenyan ivory',
    'asian wildlife', 'southeast asian', 'vietnamese', 'laotian',
    'chinese traditional', 'hong kong', 'macau', 'taiwan',
    'amazon rainforest', 'brazilian wildlife', 'peruvian', 'colombian',
    'madagascar wildlife', 'malagasy', 'lemur island',
    'indonesian wildlife', 'bornean', 'sumatran', 'javan',
    'himalayan', 'tibetan', 'nepalese', 'bhutanese',
    'arctic wildlife', 'alaskan', 'canadian wildlife', 'siberian',
]

# Master list combining all tiers
ALL_ENDANGERED_SPECIES_KEYWORDS = (
    TIER_1_CRITICAL_SPECIES + 
    TIER_2_HIGH_PRIORITY_SPECIES + 
    TIER_3_MEDIUM_PRIORITY_SPECIES +
    PLANT_SPECIES_KEYWORDS +
    TRADITIONAL_MEDICINE_KEYWORDS +
    TRAFFICKING_CODE_WORDS +
    PRODUCT_COMBINATIONS +
    GEOGRAPHIC_INDICATORS
)

# Priority rotation schedule
KEYWORD_ROTATION_SCHEDULE = {
    'tier_1_critical': {
        'keywords': TIER_1_CRITICAL_SPECIES,
        'frequency_minutes': 15,  # Scan every 15 minutes
        'priority': 1
    },
    'tier_2_high': {
        'keywords': TIER_2_HIGH_PRIORITY_SPECIES,
        'frequency_minutes': 30,  # Scan every 30 minutes
        'priority': 2
    },
    'tier_3_medium': {
        'keywords': TIER_3_MEDIUM_PRIORITY_SPECIES,
        'frequency_minutes': 60,  # Scan every hour
        'priority': 3
    },
    'plants': {
        'keywords': PLANT_SPECIES_KEYWORDS,
        'frequency_minutes': 120,  # Scan every 2 hours
        'priority': 4
    },
    'medicine': {
        'keywords': TRADITIONAL_MEDICINE_KEYWORDS,
        'frequency_minutes': 45,  # Scan every 45 minutes
        'priority': 2
    },
    'trafficking_terms': {
        'keywords': TRAFFICKING_CODE_WORDS,
        'frequency_minutes': 180,  # Scan every 3 hours
        'priority': 5
    }
}

print(f"Total keywords available: {len(ALL_ENDANGERED_SPECIES_KEYWORDS)}")
print(f"Tier 1 Critical: {len(TIER_1_CRITICAL_SPECIES)}")
print(f"Tier 2 High Priority: {len(TIER_2_HIGH_PRIORITY_SPECIES)}")
print(f"Traditional Medicine: {len(TRADITIONAL_MEDICINE_KEYWORDS)}")
print(f"Plant Species: {len(PLANT_SPECIES_KEYWORDS)}")
