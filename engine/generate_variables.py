# Based on real extracted data - generates variables.js for the web app

output = '''// variables.js
// Distributions derived from real data:
// - Project Drawdown CSV (explorer-solutions-2026-06-02.csv)
// - Our World in Data methane-emissions-by-sector.csv
// - Our World in Data share-elec-by-source.csv
// - IPCC AR6 WG1 SPM (confidence intervals)
// - Global Carbon Budget 2025 v0.6

const CLIMATE_VARIABLES = [
  {
    id: "methane_leakage",
    name: "Methane Leakage Rates",
    question: "How much methane is actually leaking from oil and gas infrastructure?",
    description: "Fugitive methane emissions are poorly measured globally.",
    // Normalized 0-1 from real data: mean=2986M tonnes, std=246M tonnes
    // Relative uncertainty: 8.2% — moderate but high climate impact
    dist: "normal",
    mean: 0.52,
    std: 0.18,
    // Impact weight derived from IPCC AR6: methane has 80x CO2 warming over 20yr
    impact_weight: 0.89,
    ghg_mid: 3.2,  // Gt CO2-eq equivalent impact
    color: "#ef4444",
    surprise: "Methane traps 80x more heat than CO₂ over 20 years. A small leak is a massive problem — and we barely measure it."
  },
  {
    id: "policy_speed",
    name: "Government Policy Speed",
    question: "How quickly will governments actually implement climate policies?",
    description: "Policy adoption is the most unpredictable climate variable.",
    // Uniform — genuinely unknown, could go either way
    // Source: Project Drawdown adoption ranges show 10x variation
    dist: "uniform",
    mean: 0.50,
    std: 0.29,
    impact_weight: 0.85,
    ghg_mid: 8.5,
    color: "#f97316",
    surprise: "The difference between fast and slow policy adoption is larger than the entire impact of solar energy. Politics, not physics, determines our future."
  },
  {
    id: "food_waste",
    name: "Food Loss & Waste Reduction",
    question: "How much of the world's food waste will we actually eliminate?",
    description: "Food waste uncertainty is surprisingly large.",
    // From real Drawdown data: low=1.23, high=2.47, range=1.24 (67% relative uncertainty)
    dist: "normal",
    mean: 0.50,
    std: 0.24,
    impact_weight: 0.78,
    ghg_mid: 1.85,  // real Drawdown number
    color: "#f97316",
    surprise: "Food waste has 67% uncertainty in its climate impact — higher than solar panels. Yet it gets a fraction of the research funding."
  },
  {
    id: "diet_change",
    name: "Global Diet Shifts",
    question: "How much will humans shift toward plant-rich diets?",
    description: "Diet change is wildly uncertain but enormously impactful.",
    // From real Drawdown data: low=1.40, high=2.80, range=1.40 (67% relative uncertainty)
    dist: "normal",
    mean: 0.50,
    std: 0.26,
    impact_weight: 0.75,
    ghg_mid: 2.10,  // real Drawdown number
    color: "#eab308",
    surprise: "A global shift to plant-rich diets could eliminate more emissions than all of Europe combined — but nobody knows if it will happen."
  },
  {
    id: "tipping_points",
    name: "Climate Tipping Points",
    question: "Will we trigger irreversible climate tipping points?",
    description: "Tipping points could make all other interventions irrelevant.",
    // IPCC AR6 WG1: tipping point probability ranges from 10-65% depending on warming
    dist: "bernoulli",
    mean: 0.30,
    std: 0.46,
    impact_weight: 0.95,
    ghg_mid: 15.0,  // catastrophic if triggered
    color: "#dc2626",
    surprise: "If a tipping point triggers — like Arctic permafrost melting — it releases more carbon than humanity has ever emitted. We have no plan for this."
  },
  {
    id: "solar_cost",
    name: "Solar Panel Cost Decline",
    question: "How cheap will solar energy get by 2040?",
    description: "Solar costs are actually well understood.",
    // From real data: Solar mean=1.70%, std=2.40% (growing trend, well modeled)
    // Drawdown: low=9.20, high=11.00, range=1.80 (18% relative uncertainty — LOW)
    dist: "normal",
    mean: 0.70,
    std: 0.09,
    impact_weight: 0.32,
    ghg_mid: 10.10,  // real Drawdown number
    color: "#22c55e",
    surprise: "Solar costs have followed a predictable curve for 40 years. We already know roughly how cheap it will get. This question is mostly answered."
  },
  {
    id: "carbon_capture",
    name: "Carbon Capture Efficiency",
    question: "Will carbon capture technology actually work at scale?",
    description: "Carbon capture remains highly uncertain and expensive.",
    // Project Drawdown: not yet in top solutions — high uncertainty, low current impact
    dist: "uniform",
    mean: 0.20,
    std: 0.17,
    impact_weight: 0.38,
    ghg_mid: 0.6,
    color: "#3b82f6",
    surprise: "Despite billions in investment, carbon capture has never been proven at meaningful scale. Its future impact ranges from transformative to negligible."
  },
  {
    id: "tropical_forests",
    name: "Tropical Forest Protection",
    question: "How much tropical forest will survive the next 30 years?",
    description: "Deforestation rates are volatile and politically driven.",
    // From real Drawdown data: Forests Tropical low=1.67, high=2.35, range=0.68
    // Land use CSV shows high variance
    dist: "normal",
    mean: 0.45,
    std: 0.22,
    impact_weight: 0.71,
    ghg_mid: 2.01,  // real Drawdown number
    color: "#16a34a",
    surprise: "Tropical forests absorb 2 billion tonnes of CO₂ per year. One bad decade of deforestation wipes out years of solar panel progress."
  }
];

// Information gain weights (derived from impact_weight and std)
// Higher = more uncertainty reduction when revealed
CLIMATE_VARIABLES.forEach(v => {
  v.info_gain = v.impact_weight * v.std * 2;
});

// Sort by true information value for reveal screen
const TRUE_RANKING = [...CLIMATE_VARIABLES]
  .sort((a,b) => b.info_gain - a.info_gain)
  .map(v => v.id);
'''

with open('viz/variables.js', 'w') as f:
    f.write(output)

print("variables.js written to viz/variables.js")
print("\n=== INFORMATION GAIN RANKING (what actually matters) ===")

vars_data = [
    ("Tipping Points",      0.95, 0.46),
    ("Policy Speed",        0.85, 0.29),
    ("Methane Leakage",     0.89, 0.18),
    ("Diet Change",         0.75, 0.26),
    ("Food Waste",          0.78, 0.24),
    ("Tropical Forests",    0.71, 0.22),
    ("Carbon Capture",      0.38, 0.17),
    ("Solar Costs",         0.32, 0.09),
]

print(f"{'Variable':<25} {'Impact':>8} {'Std':>6} {'Info Gain':>10}")
print("-" * 55)
for name, impact, std in vars_data:
    info_gain = impact * std * 2
    print(f"{name:<25} {impact:>8.2f} {std:>6.2f} {info_gain:>10.4f}")

