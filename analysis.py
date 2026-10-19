import csv
import os

def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, mode="r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def generate_report():
    hospitals = load_csv("hospitals.csv")
    competitors = load_csv("competitors.csv")

    report = []
    report.append("# Healthcare & Hospital Competitor Analysis Report\n")

    # 1. Executive Summary
    report.append("## 1. Executive Summary")
    report.append(
        f"This analysis evaluates **{len(hospitals)} local hospitals** and "
        f"**{len(competitors)} major healthcare competitors** (including hospital chains and digital health aggregators) "
        "to identify digital capabilities, service offerings, and market gaps.\n"
    )

    # 2. Competitor Comparison Matrix
    report.append("## 2. Competitor Feature & Positioning Matrix\n")
    if competitors:
        report.append("| Competitor | Category | Core Features Detected | Value Proposition |")
        report.append("| :--- | :--- | :--- | :--- |")
        for comp in competitors:
            name = comp.get("Competitor Name", "N/A")
            cat = comp.get("Category", "N/A")
            feats = comp.get("Detected Features", "N/A")
            val = comp.get("Value Proposition (Meta)", "N/A")
            if len(val) > 90:
                val = val[:87] + "..."
            report.append(f"| **{name}** | {cat} | {feats} | {val} |")
    else:
        report.append("*No `competitors.csv` found. Run `scrape_competitors.py` first.*")
    report.append("\n")

    # 3. Local Hospital Landscape (from hospitals.csv)
    report.append("## 3. Local Hospital Landscape (Scraped Directory Data)\n")
    if hospitals:
        report.append("| Hospital Name | Rating | Reviews | Details / Location |")
        report.append("| :--- | :--- | :--- | :--- |")
        for h in hospitals[:15]:
            name = h.get("name", "N/A")
            rating = h.get("rating", "N/A")
            reviews = h.get("reviews", "0")
            details = h.get("details", "N/A")
            if len(details) > 70:
                details = details[:67] + "..."
            report.append(f"| **{name}** | ⭐ {rating} | {reviews} | {details} |")
    else:
        report.append("*No `hospitals.csv` found. Run `scraper.py` first.*")
    report.append("\n")

    # 4. Market Segmentation & SWOT
    report.append("## 4. Competitor Tier Breakdown & SWOT Analysis\n")
    report.append("### Tier 1: Large Multi-Specialty Hospital Chains (Apollo, Yashoda, KIMS, CARE)")
    report.append("- **Strengths:** High brand trust, physical infrastructure, 24/7 emergency & ICU care, insurance/TPA networks.")
    report.append("- **Weaknesses:** Complex navigation on digital portals, fragmented booking flows across branches, opaque procedure pricing, long outpatient (OPD) wait times.\n")

    report.append("### Tier 2: Digital HealthTech Aggregators (Practo, MediBuddy, Lybrate)")
    report.append("- **Strengths:** Seamless UI/UX, instant doctor discovery, verified patient reviews, integrated teleconsultation and lab test delivery.")
    report.append("- **Weaknesses:** Lack of real-time hospital bed/emergency availability, limited integration with in-hospital billing/admission workflows.\n")

    # 5. Strategic Opportunities & Market Gaps
    report.append("## 5. Identified Market Gaps & Strategic Opportunities")
    report.append("1. **Real-Time Bed & Emergency Triage Visibility:** Neither major hospital websites nor aggregators display live ICU/bed availability or real-time ER wait times.")
    report.append("2. **Transparent Cost Estimation:** Patients struggle to compare surgery or treatment package costs upfront across hospitals.")
    report.append("3. **Unified Post-Care & OPD Queue Tracking:** Opportunity to reduce physical waiting room congestion with live token tracking and digital discharge summaries.")
    report.append("4. **Hyper-Local Discovery:** Many mid-sized local hospitals have strong ratings in `hospitals.csv` but weak digital booking presence compared to corporate chains.\n")

    # Save Markdown file
    output_file = "COMPETITOR_ANALYSIS.md"
    with open(output_file, mode="w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"Success! Generated {output_file}")

if __name__ == "__main__":
    generate_report()