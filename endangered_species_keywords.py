# WildGuard AI - Endangered Species Target Keywords
# Based on CITES appendices, endangered species, and common trafficking terms

ENDANGERED_SPECIES_KEYWORDS = [
    # CITES Appendix I - Most Endangered
    'elephant ivory', 'rhino horn', 'tiger bone', 'tiger skin', 'tiger tooth',
    'pangolin scale', 'pangolin armor', 'turtle shell', 'tortoise shell',
    'leopard skin', 'jaguar pelt', 'cheetah fur', 'snow leopard',
    'bear bile', 'bear paw', 'bear gallbladder',
    'shark fin', 'shark tooth', 'whale bone', 'whale tooth',
    'eagle feather', 'falcon', 'parrot feather', 'macaw feather',
    'coral jewelry', 'red coral', 'black coral',
    'seahorse dried', 'sea turtle shell', 'hawksbill',
    
    # Specific Endangered Animals
    'orangutan', 'gorilla', 'chimpanzee', 'bonobo',
    'vaquita', 'manatee', 'dugong',
    'saiga horn', 'oryx horn', 'addax horn',
    'kakapo', 'california condor', 'whooping crane',
    'black rhino', 'white rhino', 'javan rhino', 'sumatran rhino',
    'amur leopard', 'arabian leopard', 'persian leopard',
    'sumatran tiger', 'malayan tiger', 'south china tiger',
    'bornean orangutan', 'sumatran orangutan', 'tapanuli orangutan',
    
    # Traditional Medicine Terms
    'rhino horn powder', 'tiger bone wine', 'bear bile capsule',
    'pangolin medicine', 'seahorse powder', 'turtle plastron',
    'deer musk', 'musk deer', 'civet musk',
    'traditional medicine', 'tcm', 'chinese medicine',
    
    # Ivory Products
    'ivory bracelet', 'ivory necklace', 'ivory carving', 'ivory figurine',
    'ivory chess', 'ivory statue', 'ivory tusk', 'mammoth ivory',
    'walrus ivory', 'narwhal tusk', 'hippo tooth',
    
    # Fur and Skin Products
    'leopard coat', 'tiger rug', 'bear skin rug', 'wolf pelt',
    'lynx fur', 'ocelot fur', 'margay fur', 'serval skin',
    'crocodile skin', 'alligator leather', 'python leather',
    'lizard skin', 'monitor lizard', 'iguana leather',
    
    # Feathers and Birds
    'eagle feather headdress', 'owl feather', 'hawk feather',
    'peacock feather', 'crane feather', 'heron feather',
    'exotic bird', 'rare parrot', 'macaw blue', 'cockatoo',
    'toucan beak', 'hornbill beak', 'bird of paradise',
    
    # Marine Life
    'abalone shell', 'conch shell', 'giant clam', 'nautilus shell',
    'sea fan coral', 'brain coral', 'staghorn coral',
    'shark cartilage', 'ray skin', 'stingray leather',
    'whale oil', 'sperm whale', 'ambergris',
    
    # Scales and Shells
    'pangolin armor', 'armadillo shell', 'turtle carapace',
    'tortoise plastron', 'snake skin', 'python scale',
    'crocodile scale', 'lizard scale', 'fish scale rare',
    
    # Bones and Teeth
    'tiger claw', 'bear claw', 'wolf tooth', 'big cat tooth',
    'elephant molars', 'hippo canine', 'walrus tusk',
    'lion tooth', 'leopard claw', 'jaguar tooth',
    
    # Regional/Cultural Terms
    'bushmeat', 'exotic meat', 'wild game', 'trophy hunting',
    'shaman', 'shamanic', 'ritual animal', 'ceremonial fur',
    'tribal mask', 'african art', 'indigenous craft',
    
    # Common Trafficking Code Words
    'rare specimen', 'exotic collection', 'private collection',
    'museum quality', 'authentic tribal', 'genuine wild',
    'ethically sourced', 'vintage specimen', 'estate collection',
    'grandfather clause', 'pre-ban', 'legal import',
    
    # Specific Products
    'shatoosh shawl', 'tibetan antelope', 'chiru wool',
    'rosewood carving', 'ebony carving', 'sandalwood',
    'agarwood', 'oud wood', 'precious wood',
    'cactus succulent rare', 'orchid rare', 'cycad plant',
    
    # Geographic Indicators
    'african wildlife', 'asian wildlife', 'amazon specimen',
    'congo ivory', 'kenyan ivory', 'zimbabwe trophy',
    'madagascar', 'borneo', 'sumatra', 'java rare',
    'galapagos', 'patagonia', 'siberian fur'
]

# Additional context terms to combine with animal names
CONTEXT_MODIFIERS = [
    'skin', 'fur', 'pelt', 'hide', 'leather', 'bone', 'tooth', 'claw', 'horn',
    'scale', 'feather', 'shell', 'carapace', 'tusk', 'antler', 'musk',
    'oil', 'bile', 'powder', 'medicine', 'carved', 'jewelry', 'bracelet',
    'necklace', 'ring', 'ornament', 'decoration', 'trophy', 'mount', 'skull'
]

# Most trafficked species (CITES data)
HIGH_PRIORITY_SPECIES = [
    'elephant', 'rhino', 'tiger', 'pangolin', 'leopard', 'jaguar', 'cheetah',
    'bear', 'shark', 'turtle', 'eagle', 'falcon', 'parrot', 'coral',
    'seahorse', 'ivory', 'horn', 'bile', 'scale', 'fin'
]

# Traditional medicine red flags
MEDICINE_TERMS = [
    'traditional chinese medicine', 'tcm', 'herbal medicine', 'natural remedy',
    'ancient cure', 'healing powder', 'medicinal bone', 'therapeutic',
    'wellness', 'vitality', 'potency', 'strength enhancement'
]
