#!/usr/bin/env python3
"""
WildGuard AI - MASSIVE Keyword Database
50+ wildlife trafficking keywords across multiple languages and categories
"""

def get_massive_keyword_database():
    """Returns 50+ carefully researched wildlife trafficking keywords"""
    
    return {
        "direct_wildlife_parts": [
            "ivory", "rhino horn", "tiger bone", "elephant tusk", "pangolin scales",
            "bear bile", "shark fin", "turtle shell", "leopard skin", "cheetah fur",
            "tiger skin", "lion mane", "zebra hide", "giraffe hair", "hippo teeth",
            "walrus tusk", "narwhal horn", "whale bone", "seal skin", "otter fur",
            "python skin", "crocodile leather", "alligator hide", "lizard skin",
            "eagle feathers", "falcon feathers", "parrot feathers", "macaw feathers",
            "sea turtle shell", "tortoise shell", "coral pieces", "seahorse dried",
            "shark teeth", "tiger teeth", "bear claws", "elephant hair"
        ],
        
        "coded_terms": [
            "white gold", "traditional medicine", "exotic leather", "rare bones",
            "ancient carved items", "decorative horn", "antique ivory", "tribal medicine",
            "natural remedy ingredients", "vintage wildlife", "estate collection",
            "museum quality", "authentic pieces", "natural healing", "oriental medicine",
            "carved artifact", "bone carving", "horn carving", "scrimshaw",
            "ethnic jewelry", "tribal art", "primitive art", "folk medicine"
        ],
        
        "product_categories": [
            "carved figurine", "antique sculpture", "vintage jewelry", "traditional crafts",
            "ethnic handicrafts", "primitive tools", "tribal weapons", "medicine ingredients",
            "healing remedies", "natural supplements", "exotic pets", "rare specimens",
            "taxidermy", "mounted specimens", "preserved animals", "dried specimens"
        ],
        
        "suspicious_phrases": [
            "wild caught", "freshly harvested", "authentic wild", "traditional use",
            "medicinal properties", "natural healing", "rare opportunity", "limited quantity",
            "collectors item", "museum piece", "estate find", "family heirloom",
            "traditional remedy", "natural cure", "exotic material", "wild origin"
        ],
        
        "multi_language": {
            "chinese_simplified": ["象牙", "犀牛角", "虎骨", "熊胆", "穿山甲鳞片", "鲨鱼翅", "海龟壳"],
            "chinese_traditional": ["象牙", "犀牛角", "虎骨", "熊膽", "穿山甲鱗片", "鯊魚翅", "海龜殼"],
            "spanish": ["marfil", "cuerno de rinoceronte", "hueso de tigre", "piel de leopardo", "medicina tradicional"],
            "vietnamese": ["ngà voi", "sừng tê giác", "xương hổ", "da báo", "thuốc cổ truyền"],
            "thai": ["งาช้าง", "เขาแรด", "กระดูกเสือ", "หนังเสือ", "ยาแผนโบราณ"],
            "portuguese": ["marfim", "chifre de rinoceronte", "osso de tigre", "pele de onça", "medicina tradicional"],
            "french": ["ivoire", "corne de rhinocéros", "os de tigre", "peau de léopard", "médecine traditionnelle"],
            "german": ["elfenbein", "nashornhorn", "tigerknochen", "leopardenfell", "traditionelle medizin"],
            "arabic": ["عاج الفيل", "قرن الخرتيت", "عظم النمر", "جلد الفهد", "الطب التقليدي"],
            "swahili": ["pembe za ndovu", "pembe za kifaru", "mifupa ya chui", "dawa za asili"],
            "indonesian": ["gading gajah", "cula badak", "tulang harimau", "kulit macan", "obat tradisional"],
            "japanese": ["象牙", "サイの角", "虎の骨", "ヒョウの皮", "伝統医学"],
            "korean": ["상아", "코뿔소 뿔", "호랑이 뼈", "표범 가죽", "전통의학"],
            "hindi": ["हाथीदांत", "गैंडे का सींग", "बाघ की हड्डी", "तेंदुए की खाल", "पारंपरिक चिकित्सा"],
            "russian": ["слоновая кость", "рог носорога", "кость тигра", "шкура леопарда", "традиционная медицина"],
            "italian": ["avorio", "corno di rinoceronte", "osso di tigre", "pelle di leopardo", "medicina tradizionale"]
        }
    }

def get_optimized_search_terms():
    """Returns optimized list of 15 high-impact search terms for maximum results"""
    
    # These are the most commonly trafficked items that will return the most results
    return [
        # High-volume direct terms
        "ivory", "antique ivory", "carved ivory", "elephant tusk",
        "rhino horn", "tiger bone", "bear bile", "shark fin",
        
        # High-volume coded terms  
        "traditional medicine", "exotic leather", "vintage horn",
        "carved bone", "natural remedy", "tribal medicine",
        "museum quality"
    ]

def get_platform_specific_terms(platform_name):
    """Returns platform-optimized keywords for better results"""
    
    platform_terms = {
        "ebay": [
            "vintage", "antique", "collectible", "rare", "estate", "carved",
            "bone", "horn", "ivory", "leather", "medicine", "traditional"
        ],
        "craigslist": [
            "antique", "vintage", "estate sale", "collection", "carved",
            "bone", "ivory", "horn", "leather", "art", "sculpture"
        ],
        "aliexpress": [
            "bone", "carved", "traditional", "medicine", "natural",
            "vintage", "antique", "crafts", "decoration", "art"
        ],
        "olx": [
            "antyk", "vintage", "kolekcja", "rzeźba", "kość", 
            "róg", "skóra", "sztuka", "rękodzieło", "tradycyjne"
        ],
        "gumtree": [
            "antique", "vintage", "collectible", "carved", "bone",
            "horn", "leather", "art", "sculpture", "estate"
        ],
        "mercadolibre": [
            "antiguo", "vintage", "tallado", "hueso", "cuerno",
            "cuero", "medicina", "tradicional", "arte", "escultura"
        ],
        "taobao": [
            "古董", "雕刻", "骨头", "角", "皮革", 
            "传统", "药材", "艺术", "收藏", "工艺品"
        ],
        "mercari": [
            "vintage", "antique", "carved", "bone", "horn",
            "leather", "art", "collectible", "handmade", "traditional"
        ]
    }
    
    return platform_terms.get(platform_name, get_optimized_search_terms())

if __name__ == "__main__":
    keywords = get_massive_keyword_database()
    
    total_terms = 0
    for category, terms in keywords.items():
        if isinstance(terms, list):
            total_terms += len(terms)
        elif isinstance(terms, dict):
            for lang, lang_terms in terms.items():
                total_terms += len(lang_terms)
    
    print(f"🔍 MASSIVE KEYWORD DATABASE CREATED")
    print(f"📊 Total terms: {total_terms}")
    print(f"🎯 Optimized search terms: {len(get_optimized_search_terms())}")
    print(f"🌍 Languages supported: {len(keywords['multi_language'])}")
    
    print(f"\n📋 HIGH-IMPACT SEARCH TERMS:")
    for i, term in enumerate(get_optimized_search_terms(), 1):
        print(f"   {i:2d}. {term}")
