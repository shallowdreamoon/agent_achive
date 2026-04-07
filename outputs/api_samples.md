# API Samples (generated from real runtime outputs)

## GET /api/health
```json
{
  "ok": true,
  "service": "IP Overseas Risk Multi-Agent Demo"
}
```

## GET /api/config
```json
{
  "mock_mode": false,
  "model_name": "gpt-4o-mini",
  "embedding_model": "text-embedding-3-small",
  "available_agents": [
    "qa",
    "layout",
    "litigation"
  ],
  "default_top_k": 4
}
```

## POST /api/run (qa)
```json
{
  "selected_agent": "qa",
  "routing_reason": "manual agent_type specified by user",
  "structured_result": {
    "question": "mock-question",
    "risk_type": "mock-risk_type",
    "country_or_region": "mock-country_or_region",
    "analysis": "mock-analysis",
    "recommendations": [
      "mock-item"
    ],
    "evidence": [
      "mock-item"
    ]
  },
  "evidence": [
    {
      "id": "IPB-001",
      "task": "qa",
      "country": "US",
      "title": "US trademark opposition",
      "snippet": "A Shenzhen electronics brand plans to sell smart speakers in the US under the mark EchoNova. A prior US registration EchoNova Labs exists in class 9.",
      "score": 0.3333
    },
    {
      "id": "IPB-004",
      "task": "qa",
      "country": "US",
      "title": "Employee mobility leakage",
      "snippet": "US subsidiary hired competitors' engineers and imported source snippets from prior employer repositories.",
      "score": 0.2357
    },
    {
      "id": "IPB-005",
      "task": "qa",
      "country": "IN",
      "title": "Phonetic similarity in India",
      "snippet": "A healthcare app named MediQ launches in India where Medique is registered for telemedicine services.",
      "score": 0.1
    },
    {
      "id": "IPB-002",
      "task": "qa",
      "country": "EU",
      "title": "FRAND and SEP risk in EU",
      "snippet": "A 5G IoT module exporter enters Germany and France without SEP licensing from major pools.",
      "score": 0.0971
    }
  ],
  "raw_model_output": {
    "question": "mock-question",
    "risk_type": "mock-risk_type",
    "country_or_region": "mock-country_or_region",
    "analysis": "mock-analysis",
    "recommendations": [
      "mock-item"
    ],
    "evidence": [
      "mock-item"
    ]
  },
  "latency_ms": 1,
  "mock_mode": false,
  "model_name": "gpt-4o-mini"
}
```

## POST /api/run (layout)
```json
{
  "selected_agent": "layout",
  "routing_reason": "manual agent_type specified by user",
  "structured_result": {
    "technology_summary": "mock-technology_summary",
    "target_regions": [
      "mock-item"
    ],
    "filing_strategy": [
      "mock-item"
    ],
    "timeline_suggestion": [
      "mock-item"
    ],
    "risk_notes": [
      "mock-item"
    ],
    "evidence": [
      "mock-item"
    ]
  },
  "evidence": [
    {
      "id": "IPB-006",
      "task": "layout",
      "country": "US",
      "title": "Battery management patent family",
      "snippet": "Company has core BMS algorithm and plans expansion to US and Canada.",
      "score": 0.0
    },
    {
      "id": "IPB-007",
      "task": "layout",
      "country": "EU",
      "title": "Robotics control portfolio",
      "snippet": "SME develops collision-avoidance stack and wants Europe market entry in 18 months.",
      "score": 0.0
    },
    {
      "id": "IPB-008",
      "task": "layout",
      "country": "JP",
      "title": "Medical imaging AI",
      "snippet": "AI startup seeks Japan hospital procurement opportunities.",
      "score": 0.0
    },
    {
      "id": "IPB-009",
      "task": "layout",
      "country": "KR",
      "title": "Semiconductor packaging",
      "snippet": "Advanced packaging process needs rapid filing before trade fair disclosure.",
      "score": 0.0
    }
  ],
  "raw_model_output": {
    "technology_summary": "mock-technology_summary",
    "target_regions": [
      "mock-item"
    ],
    "filing_strategy": [
      "mock-item"
    ],
    "timeline_suggestion": [
      "mock-item"
    ],
    "risk_notes": [
      "mock-item"
    ],
    "evidence": [
      "mock-item"
    ]
  },
  "latency_ms": 0,
  "mock_mode": false,
  "model_name": "gpt-4o-mini"
}
```

## POST /api/run (litigation)
```json
{
  "selected_agent": "litigation",
  "routing_reason": "manual agent_type specified by user",
  "structured_result": {
    "case_summary": "mock-case_summary",
    "potential_issues": [
      "mock-item"
    ],
    "litigation_risk": "mock-litigation_risk",
    "suggested_actions": [
      "mock-item"
    ],
    "legal_path_notes": [
      "mock-item"
    ],
    "evidence": [
      "mock-item"
    ]
  },
  "evidence": [
    {
      "id": "IPB-011",
      "task": "litigation",
      "country": "US",
      "title": "NPE infringement notice",
      "snippet": "A US NPE sent claim charts alleging e-commerce recommendation patent infringement.",
      "score": 0.2626
    },
    {
      "id": "IPB-015",
      "task": "litigation",
      "country": "US",
      "title": "Former distributor misuse",
      "snippet": "Former US distributor retained confidential pricing playbooks and undercut channels.",
      "score": 0.2357
    },
    {
      "id": "IPB-019",
      "task": "litigation",
      "country": "FR",
      "title": "Customs seizure in France",
      "snippet": "Parallel imports detained under suspected trademark infringement.",
      "score": 0.1443
    },
    {
      "id": "IPB-012",
      "task": "litigation",
      "country": "DE",
      "title": "German bifurcation risk",
      "snippet": "Automotive supplier sued in Munich for sensor patent; invalidity action filed separately.",
      "score": 0.1313
    }
  ],
  "raw_model_output": {
    "case_summary": "mock-case_summary",
    "potential_issues": [
      "mock-item"
    ],
    "litigation_risk": "mock-litigation_risk",
    "suggested_actions": [
      "mock-item"
    ],
    "legal_path_notes": [
      "mock-item"
    ],
    "evidence": [
      "mock-item"
    ]
  },
  "latency_ms": 0,
  "mock_mode": false,
  "model_name": "gpt-4o-mini"
}
```

## POST /api/benchmark/run
```json
{
  "summary": {
    "task_coverage": 1.0,
    "evidence_hit_rate": 1.0,
    "structured_output_validity": 1.0,
    "keyword_match_score": 0.25,
    "average_overall_score": 0.7,
    "per_agent_score": {
      "qa": 0.6381,
      "layout": 0.7524,
      "litigation": 0.7111
    }
  },
  "detailed_results_sample": [
    {
      "id": "B-001",
      "agent": "qa",
      "overall_score": 0.6,
      "evidence_hit": 1.0,
      "keyword_match": 0.0,
      "structured_valid": 1.0,
      "details": {
        "query": "我们在美国推出EchoNova音箱，商标风险是什么？",
        "reference": {
          "question": "",
          "risk_type": "",
          "country_or_region": "",
          "analysis": "",
          "recommendations": [],
          "evidence": []
        },
        "structured_result": {
          "question": "mock-question",
          "risk_type": "mock-risk_type",
          "country_or_region": "mock-country_or_region",
          "analysis": "mock-analysis",
          "recommendations": [
            "mock-item"
          ],
          "evidence": [
            "mock-item"
          ]
        }
      }
    },
    {
      "id": "B-002",
      "agent": "qa",
      "overall_score": 0.7333,
      "evidence_hit": 1.0,
      "keyword_match": 0.3333,
      "structured_valid": 1.0,
      "details": {
        "query": "在印度上线远程医疗App需要注意哪些知识产权问题？",
        "reference": {
          "question": "",
          "risk_type": "",
          "country_or_region": "",
          "analysis": "",
          "recommendations": [],
          "evidence": []
        },
        "structured_result": {
          "question": "mock-question",
          "risk_type": "mock-risk_type",
          "country_or_region": "mock-country_or_region",
          "analysis": "mock-analysis",
          "recommendations": [
            "mock-item"
          ],
          "evidence": [
            "mock-item"
          ]
        }
      }
    }
  ]
}
```
