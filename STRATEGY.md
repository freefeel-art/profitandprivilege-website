{
  "project": "profit-and-privilege",
  "version": 2,
  "governance": {
    "auto_update": [
      "operating_window.observed_at",
      "content_strategy.remaining_hooks",
      "content_strategy.next_platform"
    ],
    "commander_maintained": [
      "operating_window.overrides",
      "email_campaigns.campaigns.*.metrics",
      "channels.*.last_active_at",
      "evidence.last_morning_review_at"
    ],
    "owner_approval_required": [
      "channels.*.status",
      "operating_window.start",
      "operating_window.end",
      "operating_window.timezone",
      "operating_window.production_only",
      "automatic_publishing.status",
      "daily_objective.target",
      "traffic_growth_strategy.primary",
      "traffic_growth_strategy.secondary"
    ],
    "never_modify_automatically": [
      "governance",
      "project",
      "version"
    ]
  },
  "timezone": "Europe/Stockholm",
  "operating_window": {
    "start": "08:00",
    "end": "20:00",
    "timezone": "Europe/Stockholm",
    "active": true,
    "production_only": true,
    "description": "Production activities (publishing, external execution, scheduled business actions) respect 08:00-20:00. Commander intelligence (thinking, planning, analysing, learning, state sync, evidence review, work preparation) continues outside production hours."
  },
  "channels": {
    "facebook": {
      "status": "production",
      "role": "business_asset",
      "description": "Facebook is a business asset to be managed, not a posting target. Commander analyses Facebook performance daily as part of the morning executive review. The decision to publish is a business decision driven by evidence, not a content queue.",
      "method": "browser_automation",
      "provider": "app/providers/facebook_browser.py",
      "page_id": "61592596862104",
      "approval_required": true,
      "approval_rule": "Owner approval required before each publication per SOUL.md §7",
      "daily_analysis_required": [
        "post performance",
        "reach",
        "engagement",
        "audience growth",
        "duplicate publications",
        "publishing quality",
        "recurring discussion topics",
        "traffic generated",
        "conversions"
      ],
      "capabilities": {
        "publishing": {"status": "implemented", "description": "Text + link posts via Playwright browser automation. Used as a business tool, not run on autopilot."},
        "browser_automation": {"status": "implemented", "description": "Headless Chromium with saved session state (config/storage_state.json)"},
        "performance_analysis": {"status": "implemented", "description": "Morning review tracks posts published, last activity, and duplicate detection"},
        "duplicate_detection": {"status": "implemented", "description": "Operational hygiene scans published log for duplicate angle/hook/platform combinations"},
        "page_growth": {"status": "proposed", "description": "Not yet measured — NO VERIFIED PAGE DATA exists. Consistent posting rhythm to build topical authority signals."},
        "discussion_monitoring": {"status": "proposed", "description": "Track comments, shares, and engagement on published posts. Currently no Facebook Insights integration."},
        "community_interaction": {"status": "proposed", "description": "Reply to comments, answer questions on the page. Requires Owner review of interaction policy."},
        "opportunity_discovery": {"status": "proposed", "description": "Monitor competitor pages, OLSP-related discussions, and trending topics for content ideas."},
        "content_idea_collection": {"status": "proposed", "description": "Collect questions, objections, and discussion themes from Facebook audience for article expansion."},
        "recurring_question_analysis": {"status": "proposed", "description": "Identify and answer recurring OLSP/affiliate marketing questions from comment threads."}
      },
      "decided_at": "2026-07-30",
      "updated_at": "2026-08-04"
    },
    "youtube_shorts": {
      "status": "production",
      "method": "openmontage_engine",
      "provider": "capabilities/video/openmontage/",
      "approval_required": true,
      "approval_rule": "Owner approval required before each publication per SOUL.md §7",
      "decided_at": "2026-07-30"
    },
    "pinterest": {
      "status": "blocked",
      "reason": "Trial tier — API access unavailable",
      "decided_at": "2026-07-30"
    },
    "reddit": {
      "status": "not_a_channel",
      "reason": "Reddit appears in SERP data and article excerpts as a community discussion platform, not as a Hermes publishing channel. No Reddit publisher implemented.",
      "decided_at": "2026-08-04"
    },
    "email": {
      "status": "production",
      "method": "hostinger_smtp",
      "provider": "scripts/ghl_livebinar_campaign.py, scripts/owner_network_campaign.py",
      "smtp": "smtp.hostinger.com:587",
      "from_address": "info@profitandprivilege.com",
      "approval_required": true,
      "approval_rule": "Campaign strategy and template must be approved before sending. Automated sends are rejected in v1.",
      "capabilities": {
        "livebinar_campaign": {"status": "implemented", "description": "GHL lead → Hostinger SMTP, promote livebinar + Mega Link. 250/703 sent."},
        "owner_network": {"status": "in_progress", "description": "Personal contacts from Google Contacts export. 2/416 sent via Hostinger SMTP."},
        "campaign_evaluation": {"status": "needed", "description": "Track delivery, opens, clicks, bounces, unsubscribes, replies, conversions. Future emails must depend on campaign results."}
      },
      "decided_at": "2026-08-04"
    }
  },
  "operating_mode": {
    "type": "business_leader",
    "daemon": false,
    "background_daemon": false,
    "cycle": ["OBSERVE", "LEARN", "ANALYSE", "PLAN", "CHALLENGE", "DELEGATE", "EXECUTE", "MEASURE", "REVIEW"],
    "description": "Commander is a business leader, not a publishing engine. Every execution cycle begins with business analysis: 'What happened in the business since the previous execution?' Content (posts, emails, videos, articles) are tools, not objectives. Commander selects the correct tool according to today's business evidence. Publishing is only one available business action.",
    "business_first_rule": "Commander must never begin by asking 'What should I publish?' Commander must begin by asking 'What happened in the business since the previous execution?' Daily planning starts from evidence, never from a content queue.",
    "content_is_tool": "Facebook posts, emails, videos, and articles are business tools — not objectives. Commander chooses the correct tool according to today's business evidence.",
    "delegation": {
      "model": "executor_registration",
      "description": "Commander delegates work to registered executor functions discovered from the canonical active project root at commander/executors.py. Delegation is in-process function calls, not subprocess agent dispatch. SOUL.md §15 mandates the delegation cycle.",
      "authority": "SOUL.md §15"
    },
    "primary_truth_source": "OLSP Back Office",
    "business_reality_precedence": "OLSP Back Office describes business reality. Project documents describe strategy. Business reality takes precedence whenever available.",
    "decided_at": "2026-08-04"
  },
  "morning_executive_review": {
    "enabled": true,
    "command": "hermes morning",
    "description": "The first command of every working day. Purpose is NOT to publish. Purpose is to THINK.",
    "sequence": {
      "observe": {
        "description": "Read current OLSP operational data, email campaign metrics, funnel health, Facebook performance, operational hygiene",
        "checks": [
          "OLSP Dashboard (signups, sales, revenue, leads, transactions, balance)",
          "Webinar calendar (next webinar, schedule changes)",
          "Leads (new leads, totals, relevant changes)",
          "Email campaign metrics (delivered, opened, clicked, bounced, unsubscribed, replied, conversions)",
          "Funnel health (article CTA, Mega Link alignment)",
          "Facebook performance (posts published, last activity, duplicates, reach)",
          "Operational hygiene (duplicate publications, broken funnels, stale plans, campaign debt)"
        ]
      },
      "learn": {
        "description": "Compare today's business state with the previous execution",
        "identifies": [
          "what improved",
          "what failed",
          "what changed",
          "what requires action today"
        ]
      },
      "analyse": {
        "description": "Analyse business state: is funnel healthy, are campaigns active, is Facebook performing, is hygiene clean",
        "outputs": "Boolean analysis flags guiding plan selection"
      },
      "plan": {
        "description": "Build today's execution plan from business evidence",
        "rules": [
          "Always verify that Plan A is still the best option",
          "If evidence requires, automatically switch to Plan B or Plan C",
          "Strategy selection is deterministic, not speculative",
          "Content is a tool — select the right tool for today's evidence"
        ]
      },
      "challenge": {
        "description": "Challenge today's plan before executing",
        "questions": [
          "Is this action supported by business evidence?",
          "Is there a better tool for today's business situation?",
          "Would this action help if the funnel is broken?",
          "Is there operational debt that should be resolved first?"
        ]
      },
      "delegate_execute_measure_review": {
        "description": "Only after the Executive Review is complete",
        "rule": "Commander coordinates. Commander does not manually perform every task."
      }
    }
  },
  "email_campaigns": {
    "strategy_report": "reports/2026-08-04-090055-email-campaign-strategy-continuous-system.txt",
    "model": {
      "type": "continuous_campaign_system",
      "description": "A campaign is a continuously managed business operation that adapts based on observed evidence — not a fixed sequence of N emails. Commander evaluates after every batch and decides the next action: continue, change subject/CTA/timing/audience, split, pause, scale, or retire.",
      "required_elements": [
        "objective",
        "audience (segments)",
        "entry conditions",
        "message strategy (decision tree, not fixed sequence)",
        "timing",
        "measurement",
        "decision points (per batch, per week, per phase boundary)",
        "exit conditions",
        "optimisation (continuous, evidence-driven)"
      ]
    },
    "olsp_acquisition_campaign": {
      "description": "Single continuous acquisition campaign with two audience segments, not two separate campaigns.",
      "objective": "Convert OLSP leads and network contacts into signups and sales through the Mega Link conversion path.",
      "segments": {
        "ghl_leads": {"audience": "703 GHL contacts (olsp_lead tag)", "tone": "educational", "sent": 199, "remaining": 504, "status": "phase1_batch_delivery"},
        "owner_network": {"audience": "416 personal contacts (Google CSV)", "tone": "personal", "sent": 2, "remaining": 414, "status": "phase1_batch_delivery"}
      },
      "current_phase": "Phase 1 — Message 1 delivery (livebinar invitation + Mega Link) to all contacts",
      "message_strategy": "Decision tree per contact per message: delivered → response? (click/bounce/unsubscribe) → next action. Not a fixed N-email sequence — the campaign continues until the objective is achieved or the strategy is exhausted.",
      "decision_points": {
        "per_batch": "delivery < 90%? pause. bounce > 5%? pause + clean list. repeated soft bounce? remove.",
        "per_week": "click < 2%? change CTA/subject. conversion 0? continue (build attribution). unsubscribe > 2%? reduce frequency.",
        "phase_boundary": "evaluate all evidence → decide next phase: continue / change strategy / scale / retire"
      },
      "exit_conditions": ["hard bounce (contact unreachable)", "unsubscribe (contact opted out)", "conversion (move to onboarding — objective achieved for this contact)"],
      "scripts": {
        "message1_ghl": "scripts/ghl_livebinar_campaign.py (50/batch, 0.5s delay)",
        "message1_network": "scripts/owner_network_campaign.py (10/batch, 1.5s delay, 15min rate-limit wait)"
      }
    },
    "metrics": {
      "delivered": {"tracked": false, "source": "SMTP does not expose delivery receipts"},
      "clicked": {"tracked": "active", "source": "UTM parameters (utm_source=email&utm_medium=livebinar|owner_network&utm_campaign=olsp_launch) on every link — implemented 2026-08-04"},
      "bounced": {"tracked": "active", "source": "SMTP error keyword matching (550/553/554/5.1.1/mailbox/unknown user) — implemented 2026-08-04"},
      "unsubscribed": {"tracked": "active", "source": "Unsubscribe mailto link with tracking subject — implemented 2026-08-04"},
      "opened": {"tracked": false, "source": "Requires tracking pixel + web server infrastructure"},
      "replied": {"tracked": false, "source": "No reply-to monitoring"},
      "conversions": {"tracked": false, "source": "Requires UTM click attribution to OLSP signup/sale"}
    },
    "rule": "Commander evaluates after every batch. Every decision depends on evidence. Campaign continues adapting until objective achieved or strategy exhausted."
  },
  "content_strategy": {
    "article": "is-olsp-academy-an-mlm",
    "angles": 10,
    "hook_types": ["number-led", "contrarian", "personal"],
    "total_hooks": 30,
    "remaining_hooks": 26,
    "published_hooks": 4,
    "social_rotation": ["facebook", "shorts", "facebook"],
    "content_funnel": ["traffic_source", "article", "primary_cta", "mega_link", "olsp_signup", "sale"],
    "last_funnel_health": 100,
    "funnel_blocker": "None — Primary CTA links to the configured Mega Link.",
    "decided_at": "2026-07-30",
    "updated_at": "2026-08-04"
  },
  "daily_objective": {
    "target": "1 sale ($7) + 5 signups per day",
    "measurement_status": "aggregate_lifetime_only",
    "measurement_note": "OLSP Back Office provides aggregate lifetime totals only. Daily deltas are not exposed. Version 1 cannot verify daily attainment.",
    "authority": "OBJECTIVES.md"
  },
  "operational_hygiene": {
    "enabled": true,
    "description": "Commander is responsible for maintaining system quality. Hygiene runs as part of every morning review.",
    "checks": [
      "duplicate publications",
      "broken funnels",
      "repeated mistakes",
      "obsolete campaigns",
      "stale plans",
      "operational debt"
    ],
    "auto_cleanup_approved": [
      "duplicate publication detection and reporting"
    ],
    "owner_approval_required_for": [
      "deleting published content",
      "modifying campaign configuration",
      "altering social media strategy"
    ]
  },
  "automatic_publishing": {
    "status": "rejected_v1",
    "rule": "No automatic publishing without Owner approval per SOCIAL-MEDIA-PLAN.md §10",
    "decided_at": "2026-07-30"
  },
  "traffic_growth_strategy": {
    "primary": "Continue publishing social posts to drive traffic to the article conversion path. Do not wait for direct sales activity — every published post creates a new opportunity for discovery.",
    "secondary": "Review and repair content funnel before increasing traffic volume. Funnel health gates all traffic-driving actions.",
    "decided_at": "2026-08-04"
  },
  "evidence": {
    "last_morning_review_at": null,
    "last_production_run_at": "2026-08-03T03:48:27+00:00",
    "last_production_state": "COMPLETE",
    "last_production_tasks": ["review_funnel", "generate_social_plan", "generate_video", "collect_olsp_data", "olsp-minimum-daily-production-system"]
  }
}
