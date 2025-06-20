# WildGuard AI - Comprehensive Endangered Species Keywords (1000+)
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
    # Additional critical species
    'indochinese tiger', 'malayan tiger', 'bengal tiger', 'tiger claw', 'tiger whisker',
    'indian elephant', 'sri lankan elephant', 'borneo elephant', 'ivory bracelet', 'ivory figurine',
    'northern white rhino', 'greater one-horned rhino', 'rhino horn powder', 'rhino horn medicine',
    'far eastern leopard', 'iranian leopard', 'leopard bone', 'leopard claw', 'leopard tooth',
    'chinese pangolin', 'malayan pangolin', 'ground pangolin', 'tree pangolin', 'pangolin meat',
]

TIER_2_HIGH_PRIORITY_SPECIES = [
    # CITES Appendix II - High priority species
    'polar bear', 'grizzly bear', 'sun bear', 'sloth bear', 'bear bile', 'bear paw', 'bear gallbladder',
    'african lion', 'lion bone', 'lion tooth', 'lion claw', 'asiatic lion', 'barbary lion',
    'clouded leopard', 'lynx fur', 'bobcat pelt', 'ocelot fur', 'margay fur', 'serval skin',
    'wolf pelt', 'grey wolf', 'mexican wolf', 'red wolf', 'arctic wolf', 'timber wolf',
    'mako shark', 'great white shark', 'hammerhead shark', 'shark fin', 'shark cartilage',
    'bluefin tuna', 'sturgeon caviar', 'beluga caviar', 'paddlefish caviar',
    'coral red', 'black coral', 'brain coral', 'staghorn coral', 'elkhorn coral',
    'african grey parrot', 'macaw blue', 'scarlet macaw', 'hyacinth macaw',
    'golden eagle', 'bald eagle', 'harpy eagle', 'eagle feather', 'falcon',
    'kakapo parrot', 'california condor', 'whooping crane', 'hooded crane',
    # Additional high priority
    'spectacled bear', 'moon bear', 'asiatic black bear', 'bear bile capsule', 'bear bile powder',
    'mountain lion', 'puma pelt', 'cougar fur', 'panther skin', 'jaguar tooth', 'jaguar claw',
    'eurasian lynx', 'iberian lynx', 'canadian lynx', 'caracal fur', 'sand cat pelt',
    'whale bone', 'whale oil', 'whale baleen', 'sperm whale', 'humpback whale', 'fin whale',
    'whale shark', 'basking shark', 'tiger shark', 'bull shark', 'nurse shark', 'reef shark',
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
    # Expanded medium priority
    'arabian oryx', 'scimitar oryx', 'dama gazelle', 'cuvier gazelle', 'slender-horned gazelle',
    'przewalski horse', 'wild ass', 'onager', 'kiang', 'zebra skin', 'zebra hide',
    'barbary macaque', 'drill monkey', 'mandrill', 'colobus monkey', 'spider monkey',
    'tapir hide', 'rhinoceros beetle', 'stag beetle', 'butterfly wing', 'moth wing',
    'turtle egg', 'iguana egg', 'crocodile egg', 'snake egg', 'lizard egg',
    'freshwater turtle', 'box turtle', 'pond turtle', 'soft-shell turtle', 'snapping turtle',
]

MARINE_SPECIES_KEYWORDS = [
    # Ocean and freshwater species
    'totoaba fish', 'totoaba bladder', 'swim bladder', 'fish maw', 'dried fish maw',
    'napoleon wrasse', 'humphead wrasse', 'grouper', 'giant grouper', 'red grouper',
    'sawfish rostrum', 'sawfish saw', 'ray gill plate', 'mobula gill', 'devil ray gill',
    'coelacanth', 'arapaima', 'beluga sturgeon', 'russian sturgeon', 'ossetra caviar',
    'sea turtle egg', 'turtle meat', 'turtle soup', 'turtle oil', 'turtle fat',
    'whale meat', 'whale blubber', 'dolphin meat', 'porpoise meat', 'seal meat',
    'walrus ivory', 'walrus tusk', 'narwhal tusk', 'narwhal horn', 'unicorn horn',
    'polar bear liver', 'seal skin', 'seal fur', 'sea otter fur', 'otter pelt',
    'giant otter', 'river otter', 'marine otter', 'sea otter', 'otter fur coat',
    'monk seal', 'mediterranean seal', 'hawaiian seal', 'caribbean seal', 'seal oil',
]

BIRD_SPECIES_KEYWORDS = [
    # Endangered birds and products
    'ivory-billed woodpecker', 'imperial woodpecker', 'woodpecker bill', 'woodpecker feather',
    'spix macaw', 'glaucous macaw', 'lear macaw', 'military macaw', 'green-winged macaw',
    'kakapo', 'kea parrot', 'night parrot', 'orange-bellied parrot', 'swift parrot',
    'philippine eagle', 'steller sea eagle', 'white-tailed eagle', 'spanish eagle', 'martial eagle',
    'california condor', 'andean condor', 'bearded vulture', 'cape vulture', 'white-backed vulture',
    'whooping crane', 'siberian crane', 'japanese crane', 'black-necked crane', 'sarus crane',
    'bird nest', 'edible bird nest', 'swiftlet nest', 'cave nest', 'white nest',
    'falcon egg', 'eagle egg', 'hawk egg', 'owl egg', 'crane egg',
    'peacock feather', 'pheasant feather', 'grouse feather', 'bustard feather', 'flamingo feather',
    'hornbill casque', 'hornbill ivory', 'toucan bill', 'pelican pouch', 'crane plume',
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
    # Expanded plant species
    'palisander wood', 'dalbergia wood', 'honduras rosewood', 'rio rosewood', 'jacaranda wood',
    'burmese rosewood', 'siamese rosewood', 'indian rosewood', 'east indian rosewood',
    'african teak', 'burmese teak', 'thai teak', 'cecropia wood', 'mahogany wood',
    'rare orchid', 'slipper orchid', 'cattleya orchid', 'dendrobium orchid', 'phalaenopsis rare',
    'wild vanilla', 'madagascar vanilla', 'tahitian vanilla', 'vanilla planifolia',
    'rare succulent', 'living stone', 'lithops rare', 'conophytum rare', 'pleiospilos rare',
    'baobab seed', 'dragon tree', 'socotra dragon tree', 'bottle tree', 'desert rose rare',
    'welwitschia plant', 'resurrection plant', 'jade vine', 'monkey puzzle tree',
    'frankincense tree', 'myrrh tree', 'dragon blood tree', 'copal resin', 'amber tree',
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
    # Expanded traditional medicine
    'bird nest soup', 'swiftlet nest', 'white bird nest', 'red bird nest', 'cave bird nest',
    'gecko wine', 'lizard wine', 'snake wine', 'cobra wine', 'python wine',
    'tiger penis', 'seal penis', 'deer penis', 'dog penis soup', 'turtle penis',
    'donkey gelatin', 'ejiao gelatin', 'donkey hide glue', 'horse hide glue',
    'dried lizard', 'gecko dried', 'salamander dried', 'toad skin', 'frog skin',
    'ant powder', 'silkworm pupae', 'scorpion dried', 'centipede dried', 'cicada shell',
    'bear tooth', 'tiger tooth', 'leopard tooth', 'wolf tooth', 'shark tooth medicine',
    'buffalo horn', 'water buffalo horn', 'yak horn', 'antelope horn powder',
    'placenta medicine', 'human placenta', 'deer placenta', 'sheep placenta',
    'bird saliva', 'bat guano', 'civet coffee', 'kopi luwak', 'elephant dung tea',
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
    # Expanded code words
    'authentic tribal', 'native american', 'aboriginal artifact', 'indigenous medicine',
    'shaman authentic', 'medicine man', 'witch doctor', 'voodoo authentic',
    'feng shui', 'spiritual healing', 'chakra stone', 'crystal healing', 'energy stone',
    'ayurvedic medicine', 'chinese medicine', 'traditional chinese', 'tcm authentic',
    'japanese traditional', 'korean traditional', 'vietnamese medicine', 'thai medicine',
    'no questions asked', 'discrete shipping', 'private buyer', 'cash only',
    'family heirloom', 'inherited piece', 'old collection', 'grandfather collection',
    'pre-1973', 'pre-1975', 'pre-convention', 'vintage import', 'old stock',
    'documentation available', 'papers included', 'certificate authentic', 'provenance known',
    'museum deaccession', 'zoo surplus', 'captive bred', 'ranch raised',
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
    # Expanded product combinations
    'ivory statue', 'ivory knife handle', 'ivory gun grip', 'ivory piano key',
    'ivory dice', 'ivory cane', 'ivory cigarette holder', 'ivory brush handle',
    'fur blanket', 'fur pillow', 'fur throw', 'fur stole', 'fur muff',
    'leather jacket', 'leather pants', 'leather shoes', 'leather belt', 'leather wallet',
    'bone knife', 'bone tool', 'bone ornament', 'bone button', 'bone handle',
    'feather fan', 'feather mask', 'feather costume', 'feather hat', 'feather cape',
    'shell button', 'shell lamp', 'shell ashtray', 'shell bowl', 'shell vase',
    'horn spoon', 'horn knife', 'horn ornament', 'horn button', 'horn jewelry',
    'tooth necklace', 'claw ring', 'claw earring', 'whisker brush', 'tail decoration',
    'skin drum', 'hide rug', 'pelt wall hanging', 'taxidermy mount', 'skull decoration',
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
    # Expanded geographic
    'central african', 'west african', 'east african', 'congo basin', 'cameroon wildlife',
    'indian wildlife', 'sri lankan', 'bangladesh', 'myanmar wildlife', 'thai wildlife',
    'philippine wildlife', 'malaysian wildlife', 'singapore wildlife', 'brunei wildlife',
    'mexican wildlife', 'guatemalan', 'costa rican', 'panama wildlife', 'ecuador wildlife',
    'australian wildlife', 'new zealand', 'papua new guinea', 'solomon islands',
    'russian wildlife', 'mongolian', 'kazakh wildlife', 'uzbek wildlife', 'kyrgyz wildlife',
    'european wildlife', 'scandinavian', 'romanian wildlife', 'bulgarian wildlife',
    'middle eastern', 'iranian wildlife', 'iraqi wildlife', 'turkish wildlife',
    'patagonian', 'chilean wildlife', 'argentine wildlife', 'bolivian wildlife',
    'caribbean wildlife', 'jamaican', 'cuban wildlife', 'dominican wildlife',
]

SCIENTIFIC_NAMES = [
    # Scientific names commonly used in trafficking
    'loxodonta africana', 'elephas maximus', 'diceros bicornis', 'ceratotherium simum',
    'panthera tigris', 'panthera pardus', 'panthera leo', 'acinonyx jubatus',
    'ailuropoda melanoleuca', 'panthera uncia', 'manis pentadactyla', 'manis javanica',
    'pongo pygmaeus', 'pongo abelii', 'gorilla beringei', 'pan troglodytes',
    'trichechus manatus', 'dugong dugon', 'eubalaena glacialis', 'balaenoptera musculus',
    'chelonia mydas', 'eretmochelys imbricata', 'dermochelys coriacea', 'caretta caretta',
    'ursus maritimus', 'helarctos malayanus', 'melursus ursinus', 'ursus thibetanus',
    'carcharodon carcharias', 'sphyrna mokarran', 'rhincodon typus', 'thunnus thynnus',
    'psittacus erithacus', 'ara macao', 'anodorhynchus hyacinthinus', 'strigops habroptilus',
    'haliaeetus leucocephalus', 'aquila chrysaetos', 'falco peregrinus', 'gymnogyps californianus',
    # Additional scientific names
    'ailurus fulgens', 'prionailurus bengalensis', 'neofelis nebulosa', 'lynx lynx',
    'canis lupus', 'vulpes vulpes', 'ursus arctos', 'nasua nasua', 'procyon lotor',
    'macaca fascicularis', 'macaca mulatta', 'chlorocebus aethiops', 'papio anubis',
    'bradypus variegatus', 'choloepus hoffmanni', 'myrmecophaga tridactyla', 'tamandua mexicana',
    'crocodylus niloticus', 'alligator mississippiensis', 'python reticulatus', 'boa constrictor',
    'varanus komodoensis', 'iguana iguana', 'testudo graeca', 'geochelone nigra',
    'hippopotamus amphibius', 'tapirus terrestris', 'rhinoceros unicornis', 'equus grevyii',
    'giraffa camelopardalis', 'lama glama', 'vicugna vicugna', 'ovis dalli', 'capra ibex',
]

JEWELRY_ACCESSORY_TERMS = [
    # Specific jewelry and accessory terms
    'ivory bangle', 'ivory ring', 'ivory earring', 'ivory brooch', 'ivory pin',
    'bone ring', 'bone bracelet', 'bone earring', 'bone necklace', 'bone pendant',
    'horn bracelet', 'horn ring', 'horn earring', 'horn button', 'horn buckle',
    'tooth earring', 'claw ring', 'claw pendant', 'whisker jewelry', 'fur jewelry',
    'feather earring', 'feather brooch', 'feather hair clip', 'feather accessory',
    'shell ring', 'shell bracelet', 'shell earring', 'shell necklace', 'shell pendant',
    'coral ring', 'coral bracelet', 'coral earring', 'coral necklace', 'red coral',
    'pearl bracelet', 'natural pearl', 'cultured pearl', 'black pearl', 'baroque pearl',
    'amber jewelry', 'amber ring', 'amber necklace', 'amber earring', 'amber pendant',
    'jet jewelry', 'jet ring', 'jet bracelet', 'jet earring', 'jet necklace',
]

LUXURY_FASHION_TERMS = [
    # High-end fashion terms
    'exotic leather handbag', 'crocodile handbag', 'alligator purse', 'python bag',
    'ostrich leather', 'emu leather', 'lizard leather', 'stingray leather', 'shark leather',
    'fur coat vintage', 'mink coat', 'sable coat', 'fox fur coat', 'chinchilla coat',
    'ermine fur', 'marten fur', 'fisher fur', 'wolverine fur', 'lynx fur coat',
    'designer fur', 'luxury fur', 'russian fur', 'canadian fur', 'scandinavian fur',
    'custom leather', 'bespoke leather', 'handmade leather', 'artisan leather', 'heritage leather',
    'vintage fur', 'estate fur', 'inherited fur', 'family fur', 'antique fur',
    'fur trimmed', 'fur lined', 'fur collar coat', 'fur cuff', 'fur hood',
    'leather boots exotic', 'snakeskin boots', 'crocodile shoes', 'lizard shoes', 'ostrich boots',
    'designer handbag', 'luxury purse', 'exotic skin bag', 'rare leather bag', 'limited edition bag',
]

ANTIQUE_COLLECTIBLE_TERMS = [
    # Antique and collectible terms
    'antique ivory', 'vintage ivory', 'estate ivory', 'inherited ivory', 'family ivory',
    'pre-ban ivory', 'legal ivory', 'documented ivory', 'certified ivory', 'authentic ivory',
    'museum piece', 'gallery piece', 'auction piece', 'estate piece', 'collector piece',
    'rare artifact', 'cultural artifact', 'tribal artifact', 'religious artifact', 'ceremonial artifact',
    'scrimshaw', 'carved ivory', 'ivory sculpture', 'ivory art', 'ivory masterpiece',
    'taxidermy mount', 'trophy mount', 'hunting trophy', 'safari trophy', 'african trophy',
    'mounted head', 'full mount', 'shoulder mount', 'european mount', 'skull mount',
    'vintage taxidermy', 'antique mount', 'estate mount', 'inherited mount', 'family trophy',
    'native artifact', 'indigenous art', 'tribal art', 'primitive art', 'ethnographic art',
    'folk art', 'traditional craft', 'handmade artifact', 'authentic craft', 'cultural craft',
]

ONLINE_MARKETPLACE_TERMS = [
    # Terms specific to online sales
    'quick sale', 'must sell', 'moving sale', 'estate sale', 'garage sale find',
    'no reserve', 'best offer', 'make offer', 'reasonable offers', 'serious buyers only',
    'cash and carry', 'pickup only', 'local pickup', 'will deliver', 'can ship',
    'discrete packaging', 'careful shipping', 'insured shipping', 'signature required',
    'ask questions', 'more photos available', 'additional pics', 'detailed photos', 'close-ups available',
    'serious inquiries', 'genuine buyers', 'collectors welcome', 'dealers welcome', 'trade considered',
    'rare find', 'unique opportunity', 'once in lifetime', 'investment piece', 'museum quality',
    'price negotiable', 'firm price', 'priced to sell', 'below market', 'wholesale price',
    'bulk discount', 'quantity discount', 'multiple items', 'lot sale', 'complete collection',
    'authentic guarantee', 'money back guarantee', 'satisfaction guaranteed', 'as described', 'condition noted',
]

# Master list combining all categories (1000+ keywords)
ALL_ENDANGERED_SPECIES_KEYWORDS = (
    TIER_1_CRITICAL_SPECIES + 
    TIER_2_HIGH_PRIORITY_SPECIES + 
    TIER_3_MEDIUM_PRIORITY_SPECIES +
    MARINE_SPECIES_KEYWORDS +
    BIRD_SPECIES_KEYWORDS +
    PLANT_SPECIES_KEYWORDS +
    TRADITIONAL_MEDICINE_KEYWORDS +
    TRAFFICKING_CODE_WORDS +
    PRODUCT_COMBINATIONS +
    GEOGRAPHIC_INDICATORS +
    SCIENTIFIC_NAMES +
    JEWELRY_ACCESSORY_TERMS +
    LUXURY_FASHION_TERMS +
    ANTIQUE_COLLECTIBLE_TERMS +
    ONLINE_MARKETPLACE_TERMS
)

# Remove duplicates and ensure unique keywords
ALL_ENDANGERED_SPECIES_KEYWORDS = list(set(ALL_ENDANGERED_SPECIES_KEYWORDS))

# Priority rotation schedule (unchanged)
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
