"""Discovery Query Registry — seed data for all approved content pillars.

Data-driven and extendable: add a new Pillar block below and it is
automatically available via the DiscoveryLoader. No code changes needed
beyond this file.

Each pillar follows the hierarchy:

    Pillar
    ├── brands (optional — solution mapping only)
    └── clusters[]
        ├── problems[]
        │   ├── search_queries[]
        │   └── communities[]
"""

from research.discovery.models import Cluster, Pillar, Problem

# ──────────────────────────────────────────────────────────────
# PILLAR: Affiliate Marketing
# ──────────────────────────────────────────────────────────────

AFFILIATE_MARKETING = Pillar(
    name="Affiliate Marketing",
    slug="affiliate_marketing",
    description=(
        "Reviews, training, tools, and strategies for affiliate "
        "marketers — from absolute beginners to experienced publishers."
    ),
    brands=[
        "OLSP Academy",
        "Wealthy Affiliate",
        "Commission Hero",
        "Super Affiliate System",
    ],
    clusters=[
        Cluster(
            name="Beginner Affiliate Marketing",
            description=(
                "People with no audience, no money, and no experience "
                "trying to start affiliate marketing."
            ),
            problems=[
                Problem(
                    description="No audience or followers to promote to",
                    search_queries=[
                        "affiliate marketing without followers",
                        "affiliate marketing no audience",
                        "how to do affiliate marketing with no list",
                        "affiliate marketing for beginners no social media",
                    ],
                    communities=[
                        "r/Affiliatemarketing",
                        "r/juststart",
                        "r/passive_income",
                        "r/sidehustle",
                        "r/workonline",
                    ],
                ),
                Problem(
                    description="No money to invest in tools or training",
                    search_queries=[
                        "affiliate marketing no money to start",
                        "affiliate marketing no budget",
                        "free affiliate marketing training",
                        "start affiliate marketing with zero investment",
                    ],
                    communities=[
                        "r/Affiliatemarketing",
                        "r/beermoney",
                        "r/sidehustle",
                        "r/passive_income",
                    ],
                ),
                Problem(
                    description="Overwhelmed by conflicting advice",
                    search_queries=[
                        "affiliate marketing overwhelmed beginner",
                        "affiliate marketing too much information",
                        "affiliate marketing where to even start",
                        "affiliate marketing beginner mistakes",
                        "affiliate marketing confusion",
                    ],
                    communities=[
                        "r/Affiliatemarketing",
                        "r/juststart",
                        "r/Affiliate",
                    ],
                ),
                Problem(
                    description="Tried affiliate marketing and made no money",
                    search_queries=[
                        "affiliate marketing not working",
                        "why am i not making money affiliate marketing",
                        "affiliate marketing failed",
                        "affiliate marketing no sales",
                        "i tried affiliate marketing for months nothing",
                    ],
                    communities=[
                        "r/Affiliatemarketing",
                        "r/juststart",
                        "r/passive_income",
                        "r/Entrepreneur",
                    ],
                ),
                Problem(
                    description="Which affiliate program or training to choose",
                    search_queries=[
                        "best affiliate training for beginners 2026",
                        "best affiliate programs beginners 2026",
                        "affiliate marketing training review",
                        "is OLSP Academy legit",
                        "wealthy affiliate vs",
                    ],
                    communities=[
                        "r/Affiliatemarketing",
                        "r/Affiliate",
                        "r/juststart",
                        "r/review",
                    ],
                ),
            ],
        ),
        Cluster(
            name="Affiliate Traffic & List Building",
            description=(
                "Strategies, tools, and techniques for driving traffic "
                "to affiliate links and building email lists."
            ),
            problems=[
                Problem(
                    description="Can't drive traffic to affiliate links",
                    search_queries=[
                        "how to drive traffic to affiliate links",
                        "affiliate marketing traffic strategies 2026",
                        "free traffic affiliate marketing",
                        "traffic generation for affiliates",
                    ],
                    communities=[
                        "r/SEO",
                        "r/juststart",
                        "r/Blogging",
                        "r/Affiliatemarketing",
                    ],
                ),
                Problem(
                    description="Solo ads results are poor or scammy",
                    search_queries=[
                        "solo ads review scam",
                        "solo ads worth it",
                        "solo ads results",
                        "solo ad traffic quality",
                        "solo ads vs other traffic methods",
                    ],
                    communities=[
                        "r/soloads",
                        "r/Affiliatemarketing",
                        "r/juststart",
                    ],
                ),
                Problem(
                    description="Email list building with no website",
                    search_queries=[
                        "email list building no website",
                        "build email list without website",
                        "email marketing for affiliate beginners",
                        "list building strategies 2026",
                    ],
                    communities=[
                        "r/Emailmarketing",
                        "r/Affiliatemarketing",
                        "r/Blogging",
                        "r/juststart",
                    ],
                ),
                Problem(
                    description="Email open rates dropping or low conversions",
                    search_queries=[
                        "email open rates low",
                        "affiliate email conversions not working",
                        "email sequence for affiliate marketing",
                        "how to write affiliate emails that convert",
                    ],
                    communities=[
                        "r/Emailmarketing",
                        "r/Affiliatemarketing",
                        "r/copywriting",
                    ],
                ),
            ],
        ),
    ],
)

# ──────────────────────────────────────────────────────────────
# PILLAR: Lead Generation
# ──────────────────────────────────────────────────────────────

LEAD_GENERATION = Pillar(
    name="Lead Generation",
    slug="lead_generation",
    description=(
        "Strategies, tools, and methods for generating leads — "
        "from free DIY approaches to paid software and services."
    ),
    brands=[
        "LeadsMiner",
        "MegaLink",
        "Apollo.io",
        "Instantly",
        "Smartlead",
    ],
    clusters=[
        Cluster(
            name="Lead Generation for Beginners",
            description=(
                "People new to lead generation with no budget or experience."
            ),
            problems=[
                Problem(
                    description="Don't know how to start generating leads",
                    search_queries=[
                        "how to generate leads for beginners",
                        "lead generation step by step",
                        "lead generation for dummies",
                        "what is lead generation how to start",
                    ],
                    communities=[
                        "r/LeadGeneration",
                        "r/DigitalMarketing",
                        "r/AskMarketing",
                        "r/smallbusiness",
                    ],
                ),
                Problem(
                    description="No budget for lead generation tools",
                    search_queries=[
                        "free lead generation methods",
                        "lead generation no money",
                        "free ways to generate leads",
                        "lead generation without spending money",
                    ],
                    communities=[
                        "r/LeadGeneration",
                        "r/beermoney",
                        "r/sidehustle",
                        "r/smallbusiness",
                    ],
                ),
                Problem(
                    description="Tried lead generation and got no results",
                    search_queries=[
                        "lead generation not working",
                        "why is my lead generation failing",
                        "lead generation no results",
                        "tried cold email no responses",
                    ],
                    communities=[
                        "r/LeadGeneration",
                        "r/sales",
                        "r/DigitalMarketing",
                    ],
                ),
            ],
        ),
        Cluster(
            name="B2B Lead Generation",
            description=(
                "Professional lead generation for B2B sales and services."
            ),
            problems=[
                Problem(
                    description="Can't reach decision-makers",
                    search_queries=[
                        "B2B lead generation strategies 2026",
                        "how to reach decision makers B2B",
                        "getting past gatekeeper lead generation",
                        "B2B outreach best practices",
                    ],
                    communities=[
                        "r/sales",
                        "r/LeadGeneration",
                        "r/DigitalMarketing",
                        "r/Entrepreneur",
                    ],
                ),
                Problem(
                    description="LinkedIn outreach feels spammy or ineffective",
                    search_queries=[
                        "LinkedIn lead generation without being spammy",
                        "LinkedIn outreach not working",
                        "LinkedIn cold messaging tips",
                        "best LinkedIn lead generation strategy",
                    ],
                    communities=[
                        "r/sales",
                        "r/LinkedIn",
                        "r/DigitalMarketing",
                        "r/LeadGeneration",
                    ],
                ),
                Problem(
                    description="Cold email open and reply rates dropping",
                    search_queries=[
                        "cold email not working 2026",
                        "cold email open rates declining",
                        "cold email alternatives",
                        "cold email deliverability issues",
                        "cold email outreach best practices 2026",
                    ],
                    communities=[
                        "r/sales",
                        "r/Emailmarketing",
                        "r/LeadGeneration",
                        "r/Entrepreneur",
                    ],
                ),
            ],
        ),
        Cluster(
            name="Lead Generation Tools & Software",
            description=(
                "Evaluating, comparing, and choosing lead generation software."
            ),
            problems=[
                Problem(
                    description="Can't choose between too many tools",
                    search_queries=[
                        "best lead generation tools 2026",
                        "lead generation software comparison",
                        "lead gen tool vs tool",
                        "lead generation tools review",
                    ],
                    communities=[
                        "r/LeadGeneration",
                        "r/DigitalMarketing",
                        "r/SaaS",
                        "r/sales",
                    ],
                ),
                Problem(
                    description="Tools are too expensive for current budget",
                    search_queries=[
                        "affordable lead generation tools",
                        "free lead generation software",
                        "cheap lead gen tools that work",
                        "lead generation software pricing",
                    ],
                    communities=[
                        "r/LeadGeneration",
                        "r/microsaas",
                        "r/Entrepreneur",
                        "r/smallbusiness",
                    ],
                ),
                Problem(
                    description="Not sure which tool actually delivers results",
                    search_queries=[
                        "lead generation tool review",
                        "lead generation software that actually works",
                        "best lead gen tool reddit",
                        "lead generation software honest review",
                    ],
                    communities=[
                        "r/LeadGeneration",
                        "r/SaaS",
                        "r/DigitalMarketing",
                    ],
                ),
            ],
        ),
    ],
)

# ──────────────────────────────────────────────────────────────
# PILLAR: Online Income
# ──────────────────────────────────────────────────────────────

ONLINE_INCOME = Pillar(
    name="Online Income",
    slug="online_income",
    description=(
        "Practical, realistic paths to making money online — "
        "from side hustles to full-time income — for people "
        "with no experience or special skills."
    ),
    brands=[],
    clusters=[
        Cluster(
            name="Getting Started",
            description=(
                "Absolute beginners looking for their first online "
                "income method."
            ),
            problems=[
                Problem(
                    description="Have no skills or experience to monetize",
                    search_queries=[
                        "make money online with no experience",
                        "online income no skills",
                        "make money online no special talent",
                        "how to make money online with no expertise",
                    ],
                    communities=[
                        "r/beermoney",
                        "r/sidehustle",
                        "r/workonline",
                        "r/passive_income",
                    ],
                ),
                Problem(
                    description="Have no money to invest in anything",
                    search_queries=[
                        "make money online with no money",
                        "free ways to earn online",
                        "make money online zero investment",
                        "online income without spending a dime",
                    ],
                    communities=[
                        "r/beermoney",
                        "r/sidehustle",
                        "r/workonline",
                        "r/povertyfinance",
                    ],
                ),
                Problem(
                    description="Don't know which method to choose",
                    search_queries=[
                        "best way to make money online 2026",
                        "online income methods comparison",
                        "most realistic online income method",
                        "what actually works to make money online",
                    ],
                    communities=[
                        "r/sidehustle",
                        "r/passive_income",
                        "r/beermoney",
                        "r/Entrepreneur",
                    ],
                ),
                Problem(
                    description="How much can I realistically expect to earn",
                    search_queries=[
                        "realistic online income 2026",
                        "how much can beginners earn online",
                        "online income expectations vs reality",
                        "how much money can you actually make online",
                    ],
                    communities=[
                        "r/sidehustle",
                        "r/passive_income",
                        "r/beermoney",
                        "r/Entrepreneur",
                    ],
                ),
                Problem(
                    description="Tried things and got scammed or made nothing",
                    search_queries=[
                        "online income scams to avoid",
                        "why can't I make money online",
                        "i tried everything no results online income",
                        "legitimate way to make money online",
                        "online money making scams reddit",
                    ],
                    communities=[
                        "r/beermoney",
                        "r/sidehustle",
                        "r/scams",
                        "r/passive_income",
                    ],
                ),
            ],
        ),
        Cluster(
            name="Limited Resources Path",
            description=(
                "Making money online under real-world constraints: "
                "limited time, phone-only access, or full-time job."
            ),
            problems=[
                Problem(
                    description="Full-time job or family limits available time",
                    search_queries=[
                        "side hustle from home part time",
                        "make money online in spare time",
                        "online income while working full time",
                        "side hustle after work",
                    ],
                    communities=[
                        "r/sidehustle",
                        "r/passive_income",
                        "r/workonline",
                        "r/beermoney",
                    ],
                ),
                Problem(
                    description="Only have a phone, no computer",
                    search_queries=[
                        "make money from phone",
                        "online income no computer",
                        "make money with just a smartphone",
                        "phone only side hustle",
                    ],
                    communities=[
                        "r/beermoney",
                        "r/sidehustle",
                        "r/workonline",
                    ],
                ),
                Problem(
                    description="Need a job, not a business",
                    search_queries=[
                        "remote jobs no experience",
                        "online jobs work from home",
                        "legitimate work from home jobs 2026",
                        "remote entry level jobs",
                    ],
                    communities=[
                        "r/remote",
                        "r/workonline",
                        "r/jobs",
                        "r/careerguidance",
                    ],
                ),
            ],
        ),
        Cluster(
            name="Affiliate Marketing Path",
            description=(
                "Affiliate marketing as a specific online income method."
            ),
            problems=[
                Problem(
                    description="No audience to promote affiliate products",
                    search_queries=[
                        "affiliate marketing without followers",
                        "affiliate marketing no audience",
                        "how to do affiliate marketing with zero followers",
                    ],
                    communities=[
                        "r/Affiliatemarketing",
                        "r/juststart",
                        "r/passive_income",
                    ],
                ),
                Problem(
                    description="Tried and failed at affiliate marketing",
                    search_queries=[
                        "affiliate marketing not working",
                        "why am I not making money affiliate marketing",
                        "affiliate marketing failed for me",
                    ],
                    communities=[
                        "r/Affiliatemarketing",
                        "r/juststart",
                        "r/passive_income",
                        "r/sidehustle",
                    ],
                ),
                Problem(
                    description="Overwhelmed by affiliate marketing advice",
                    search_queries=[
                        "affiliate marketing overwhelmed beginner",
                        "affiliate marketing too much information",
                        "affiliate marketing where to start",
                    ],
                    communities=[
                        "r/Affiliatemarketing",
                        "r/juststart",
                        "r/Affiliate",
                    ],
                ),
            ],
        ),
    ],
)

# ──────────────────────────────────────────────────────────────
# PILLAR: AI Tools
# ──────────────────────────────────────────────────────────────

AI_TOOLS = Pillar(
    name="AI Tools",
    slug="ai_tools",
    description=(
        "Independent reviews and comparisons of AI-powered software "
        "for content creation, video production, SEO, and marketing."
    ),
    brands=[
        "ChatGPT",
        "Claude",
        "Jasper",
        "Copy.ai",
        "Writer",
        "Synthesia",
        "HeyGen",
        "ElevenLabs",
        "SurferSEO",
    ],
    clusters=[
        Cluster(
            name="AI Writing & Content",
            description=(
                "AI-powered writing tools for blog posts, articles, "
                "marketing copy, and SEO content."
            ),
            problems=[
                Problem(
                    description="Worried AI content gets penalized by Google",
                    search_queries=[
                        "does Google penalize AI content",
                        "AI writing SEO safe",
                        "is AI content bad for SEO",
                        "Google AI content penalty 2026",
                        "can Google detect AI content",
                    ],
                    communities=[
                        "r/SEO",
                        "r/Blogging",
                        "r/ArtificialIntelligence",
                        "r/juststart",
                    ],
                ),
                Problem(
                    description="AI writing sounds robotic or generic",
                    search_queries=[
                        "best AI writing tool human quality",
                        "make AI content sound human",
                        "AI writing sounds robotic",
                        "how to humanize AI content",
                    ],
                    communities=[
                        "r/ArtificialIntelligence",
                        "r/copywriting",
                        "r/Blogging",
                        "r/SEO",
                    ],
                ),
                Problem(
                    description="Which AI writer is best for affiliate marketing",
                    search_queries=[
                        "best AI writing tool for affiliate marketing",
                        "AI writing for SEO content",
                        "AI content writing tools for affiliates",
                        "best AI writer for blog posts",
                    ],
                    communities=[
                        "r/Affiliatemarketing",
                        "r/SEO",
                        "r/Blogging",
                        "r/juststart",
                    ],
                ),
                Problem(
                    description="Too many AI writing tools, can't choose",
                    search_queries=[
                        "AI writing tool comparison",
                        "Jasper vs Copy.ai vs Writer",
                        "best AI content generator 2026",
                        "AI writing software review",
                        "ChatGPT vs Claude for writing",
                    ],
                    communities=[
                        "r/ArtificialIntelligence",
                        "r/SaaS",
                        "r/Blogging",
                        "r/technology",
                    ],
                ),
            ],
        ),
        Cluster(
            name="AI Video & Voice",
            description=(
                "AI-powered video generation, avatars, voiceovers, "
                "and audio content creation."
            ),
            problems=[
                Problem(
                    description="Don't want to appear on camera",
                    search_queries=[
                        "AI avatar video creation",
                        "fakeless video for marketing",
                        "AI video without showing face",
                        "best AI avatar generator",
                    ],
                    communities=[
                        "r/ArtificialIntelligence",
                        "r/VideoEditing",
                        "r/DigitalMarketing",
                        "r/Entrepreneur",
                    ],
                ),
                Problem(
                    description="Video production is too expensive or time-consuming",
                    search_queries=[
                        "cheap AI video generation",
                        "affordable video creation AI",
                        "AI video tools for small business",
                        "quick video creation AI",
                    ],
                    communities=[
                        "r/VideoEditing",
                        "r/Entrepreneur",
                        "r/DigitalMarketing",
                        "r/smallbusiness",
                    ],
                ),
                Problem(
                    description="AI avatars or voiceovers look/sound fake",
                    search_queries=[
                        "best realistic AI avatar 2026",
                        "AI video generation review 2026",
                        "most realistic AI voiceover",
                        "AI voice cloning quality",
                        "Synthesia vs HeyGen which is better",
                    ],
                    communities=[
                        "r/ArtificialIntelligence",
                        "r/VideoEditing",
                        "r/technology",
                        "r/SaaS",
                    ],
                ),
            ],
        ),
        Cluster(
            name="AI SEO & Research",
            description=(
                "AI tools for SEO optimization, keyword research, "
                "content strategy, and competitive analysis."
            ),
            problems=[
                Problem(
                    description="SEO tools are too expensive for beginners",
                    search_queries=[
                        "affordable SEO tools 2026",
                        "best cheap SEO tools",
                        "free AI SEO tools",
                        "SEO tools for beginners on a budget",
                    ],
                    communities=[
                        "r/SEO",
                        "r/Blogging",
                        "r/juststart",
                        "r/smallbusiness",
                    ],
                ),
                Problem(
                    description="Content is not ranking on Google",
                    search_queries=[
                        "SEO not working 2026",
                        "why is my content not ranking",
                        "content ranking dropped after AI updates",
                        "Google algorithm update 2026",
                    ],
                    communities=[
                        "r/SEO",
                        "r/Blogging",
                        "r/juststart",
                        "r/bigseo",
                    ],
                ),
                Problem(
                    description="Need to optimize AI content for search",
                    search_queries=[
                        "how to optimize AI content for SEO",
                        "AI content optimization tools",
                        "AI SEO strategy 2026",
                        "using AI for keyword research",
                    ],
                    communities=[
                        "r/SEO",
                        "r/Blogging",
                        "r/ArtificialIntelligence",
                        "r/juststart",
                    ],
                ),
            ],
        ),
    ],
)

# ──────────────────────────────────────────────────────────────
# MASTER REGISTRY
# ──────────────────────────────────────────────────────────────

PILLAR_REGISTRY = [
    AFFILIATE_MARKETING,
    LEAD_GENERATION,
    ONLINE_INCOME,
    AI_TOOLS,
]
