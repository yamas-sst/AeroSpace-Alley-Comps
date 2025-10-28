# Skilled Trades Keyword Expansion - Comprehensive Analysis

**Goal:** Expand keyword coverage to capture complete trades ecosystem including:
- Licensed/certified trades (electricians, plumbers, HVAC)
- Technical leadership (engineers, supervisors, leads)
- Adjacent support roles (planners, coordinators, trainers)

**Status:** Analysis only - NOT IMPLEMENTED

---

## Current State: Category 1 (Hands-On Skilled Trades)

**Current keyword count:** ~80 keywords
**Coverage:** Machining, assembly, welding, maintenance, inspection, electrical, tooling, composites, other trades

### Current Gaps Identified:

1. **Missing Licensed Trades:**
   - No "electrician" variations (journeyman, master, industrial electrician)
   - Limited plumber coverage
   - Missing HVAC specialists
   - No boiler operators, stationary engineers

2. **Missing Technical Leadership:**
   - No manufacturing engineers
   - No QA/quality engineers
   - No supervisors, superintendents, foremen
   - No lead/senior technical roles

3. **Missing Adjacent Roles:**
   - No production planners
   - No manufacturing coordinators
   - No technical trainers
   - No safety coordinators

4. **Missing Certification-Based:**
   - No AWS (American Welding Society) certifications
   - No ASQ (American Society for Quality) roles
   - No PMP (Project Management Professional) manufacturing roles
   - No Six Sigma specialists

---

## CATEGORY 1: Hands-On Skilled Trades (EXPANDED)

### Subcategory 1A: Machining & Fabrication (CURRENT + NEW)

**Current coverage:** ✅ Good
**New additions:** 👇

```python
MACHINING_KEYWORDS = [
    # EXISTING (keep all current keywords)
    "machinist", "cnc", "mill operator", "lathe operator", "grinder", "toolmaker",
    "fabricator", "metalworker", "sheet metal", "precision machinist", "machine operator",
    "manual machinist", "setup operator", "g-code", "programmer", "tool and die", "die maker",
    "mold maker", "production machinist", "numerical control", "machining technician",

    # NEW: Specialized machining
    "swiss machinist",  # High-precision
    "5-axis operator",  # Advanced CNC
    "edm operator",  # Electrical discharge machining
    "waterjet operator",  # Waterjet cutting
    "laser operator",  # Laser cutting
    "plasma cutter",  # Plasma cutting
    "boring mill operator",  # Large-scale machining
    "horizontal machinist",  # Horizontal boring
    "jig borer",  # Precision boring
    "gear cutter",  # Gear manufacturing
    "honing machine operator",  # Surface finishing
    "lapping technician",  # Precision finishing
]
```

**Confidence:** 🟢 HIGH (all directly skilled trades)

---

### Subcategory 1B: Licensed Electrical Trades (NEW - CRITICAL ADDITION)

**Current coverage:** ⚠️ Limited ("electrician" appears once)
**Gap:** Missing licensed levels and specializations

```python
ELECTRICAL_LICENSED_KEYWORDS = [
    # EXISTING (keep current)
    "electrician", "electrical technician", "electronics technician",
    "controls technician", "panel builder", "wire harness assembler",
    "electromechanical technician", "instrumentation technician", "automation technician",

    # NEW: Licensed levels (⭐ CERTIFICATION REQUIRED)
    "journeyman electrician",  # Licensed
    "master electrician",  # Licensed (higher level)
    "industrial electrician",  # Factory-focused
    "maintenance electrician",  # Existing, but ensure included
    "commercial electrician",  # Building-focused

    # NEW: Specializations
    "controls engineer",  # PLC programming
    "automation specialist",  # Factory automation
    "robotics technician",  # Industrial robots
    "plc programmer",  # Programmable logic controllers
    "scada technician",  # Supervisory control systems
    "instrumentation electrician",  # Sensors, measurement
    "high voltage electrician",  # Power systems
    "electrical inspector",  # Quality/compliance

    # NEW: Related technical
    "electrical designer",  # CAD for electrical
    "panel designer",  # Electrical panel design
    "control panel technician",  # Panel assembly/testing
]
```

**Confidence:** 🟢 HIGH (all technical trades requiring certifications)

---

### Subcategory 1C: Plumbing, Pipefitting & HVAC (NEW - CERTIFICATION REQUIRED)

**Current coverage:** ❌ MINIMAL ("plumber" appears once, "hvac technician" once)
**Gap:** Missing major licensed trade category

```python
PLUMBING_HVAC_KEYWORDS = [
    # EXISTING (minimal)
    "plumber", "hvac technician", "hvac installer",

    # NEW: Plumbing & Pipefitting (⭐ LICENSED TRADES)
    "journeyman plumber",  # Licensed
    "master plumber",  # Licensed (higher level)
    "pipefitter",  # Industrial piping
    "steamfitter",  # Steam systems
    "sprinkler fitter",  # Fire suppression
    "pipe welder",  # Already in welding section, but related
    "industrial plumber",  # Factory systems
    "process piping",  # Chemical/manufacturing

    # NEW: HVAC Specializations (⭐ CERTIFICATIONS: EPA 608, NATE, etc.)
    "hvac mechanic",
    "hvac service technician",
    "refrigeration technician",  # EPA 608 certified
    "chiller technician",  # Large-scale cooling
    "boiler technician",  # Steam/hot water
    "building automation",  # BAS systems
    "hvac controls",  # Temperature control systems
    "hvac installer",  # Already exists
    "hvac apprentice",  # Entry-level
    "journeyman hvac",  # Licensed level

    # NEW: Related facilities
    "facilities mechanic",  # Building systems
    "building engineer",  # Commercial building operations
    "stationary engineer",  # Boiler operator (LICENSE REQUIRED in many states)
    "boiler operator",  # Licensed in most states
    "facilities technician",  # Already exists in maintenance section
]
```

**Confidence:** 🟢 HIGH (licensed trades, certifications required)

---

### Subcategory 1D: Welding & Metalwork (CURRENT + CERTIFICATIONS)

**Current coverage:** ✅ Good
**Enhancement needed:** Add AWS certification references

```python
WELDING_KEYWORDS = [
    # EXISTING (keep all)
    "welder", "tig welder", "mig welder", "arc welder", "fabrication welder",
    "pipe welder", "aluminum welder", "spot welder", "soldering", "brazing",
    "welding technician", "weld inspector", "fitter welder",

    # NEW: Certification-focused
    "certified welder",  # AWS certified
    "aws certified welder",  # American Welding Society
    "cw welder",  # Certified Welder
    "cwi",  # Certified Welding Inspector
    "cwe",  # Certified Welding Educator
    "combo welder",  # Multiple processes
    "stick welder",  # SMAW process
    "flux core welder",  # FCAW process
    "orbital welder",  # Automated pipe welding
    "robotic welder",  # Robot programming/operation
]
```

**Confidence:** 🟢 HIGH (all hands-on welding trades)

---

### Subcategory 1E: Quality & Inspection (CURRENT + CERTIFICATIONS)

**Current coverage:** ✅ Good
**Enhancement needed:** Add ASQ certifications, NDT specializations

```python
QUALITY_INSPECTION_KEYWORDS = [
    # EXISTING (keep all)
    "inspector", "quality inspector", "quality technician", "qc technician",
    "qa inspector", "ndt technician", "cmm operator", "quality assurance",
    "final inspector", "metrology technician", "dimensional inspector",

    # NEW: NDT Specializations (⭐ CERTIFICATIONS: ASNT Level I/II/III)
    "ndt level ii",  # Certified non-destructive testing
    "ndt level iii",  # Senior NDT certification
    "ultrasonic technician",  # UT method
    "radiographic technician",  # RT method
    "magnetic particle",  # MT method
    "liquid penetrant",  # PT method
    "eddy current technician",  # ET method
    "visual inspection",  # VT method
    "asnt certified",  # American Society for NDT

    # NEW: Metrology & Precision
    "calibration technician",  # Instrument calibration
    "gage technician",  # Measurement tools
    "optical inspector",  # Vision systems
    "coordinate measuring",  # CMM (already have "cmm operator")
    "layout inspector",  # First article inspection
    "receiving inspector",  # Incoming quality
    "in-process inspector",  # Production inspection
]
```

**Confidence:** 🟢 HIGH (technical inspection requiring certifications)

---

### Subcategory 1F: Maintenance & Repair (CURRENT + SPECIALIZED)

**Current coverage:** ✅ Good
**Enhancement needed:** Add specialized maintenance roles

```python
MAINTENANCE_KEYWORDS = [
    # EXISTING (keep all)
    "maintenance technician", "maintenance mechanic", "maintenance engineer",
    "industrial mechanic", "millwright", "equipment technician", "machine repair",
    "facilities technician", "mechanical technician", "preventive maintenance",
    "maintenance electrician", "repair technician", "hvac technician",
    "plant mechanic", "equipment maintenance",

    # NEW: Specialized maintenance
    "predictive maintenance",  # Vibration analysis, thermal imaging
    "reliability technician",  # RCM (Reliability-Centered Maintenance)
    "vibration analyst",  # ISO Cat I/II/III certified
    "lubrication technician",  # Tribology
    "alignment technician",  # Precision alignment
    "hydraulics technician",  # Hydraulic systems
    "pneumatics technician",  # Pneumatic systems
    "conveyor technician",  # Material handling
    "crane technician",  # Overhead crane maintenance
    "forklift technician",  # Material handling equipment
]
```

**Confidence:** 🟢 HIGH (all maintenance trades)

---

## CATEGORY 2: Technical Leadership & Engineering Support (NEW)

### Subcategory 2A: Manufacturing & Quality Engineering (HIGH CONFIDENCE)

**Why include:** Direct technical oversight of skilled trades, often promoted from trades

```python
ENGINEERING_LEADERSHIP_KEYWORDS = [
    # Manufacturing Engineering
    "manufacturing engineer",  # Core role
    "process engineer",  # Process improvement
    "industrial engineer",  # Efficiency/layouts
    "manufacturing engineering",  # Alternative phrasing
    "process improvement engineer",  # Lean/Six Sigma focus
    "methods engineer",  # Work methods
    "tool engineer",  # Tooling design
    "tooling engineer",  # Already in Category 1, include here too
    "fixture engineer",  # Fixture design

    # Quality Engineering
    "quality engineer",  # Core QE role
    "qa engineer",  # Quality assurance
    "qc engineer",  # Quality control
    "quality engineering",  # Alternative phrasing
    "supplier quality engineer",  # Vendor quality
    "sqa",  # Supplier Quality Assurance
    "quality systems engineer",  # ISO/AS9100

    # Certifications-based
    "six sigma",  # Lean Six Sigma
    "green belt",  # Six Sigma Green Belt
    "black belt",  # Six Sigma Black Belt
    "asq certified",  # American Society for Quality
    "cqe",  # Certified Quality Engineer
    "cqa",  # Certified Quality Auditor
    "cre",  # Certified Reliability Engineer
]
```

**Confidence:** 🟢 HIGH - Direct trades ecosystem support

---

### Subcategory 2B: Production Supervision (HIGH CONFIDENCE)

**Why include:** Direct management of skilled trades workforce

```python
SUPERVISORY_LEADERSHIP_KEYWORDS = [
    # Supervisor roles
    "production supervisor",
    "manufacturing supervisor",
    "shop supervisor",
    "maintenance supervisor",
    "quality supervisor",
    "shift supervisor",
    "area supervisor",
    "department supervisor",
    "assembly supervisor",
    "fabrication supervisor",
    "machining supervisor",

    # Foreman/Lead roles
    "shop foreman",
    "production foreman",
    "maintenance foreman",
    "general foreman",
    "working foreman",  # Hands-on + supervisory
    "lead technician",
    "senior technician",
    "master technician",
    "lead machinist",
    "lead welder",
    "lead assembler",

    # Superintendent
    "superintendent",
    "shop superintendent",
    "production superintendent",
    "manufacturing superintendent",
    "maintenance superintendent",
]
```

**Confidence:** 🟢 HIGH - Direct trades workforce management

---

### Subcategory 2C: Production Planning & Coordination (MEDIUM-HIGH CONFIDENCE)

**Why include:** Support roles that work directly with skilled trades daily

```python
PLANNING_COORDINATION_KEYWORDS = [
    # Planning roles
    "production planner",
    "manufacturing planner",
    "production scheduler",
    "production control",
    "material planner",
    "capacity planner",

    # Coordination roles
    "manufacturing coordinator",
    "production coordinator",
    "operations coordinator",
    "shift coordinator",
    "materials coordinator",

    # Programming roles (for CNC/automation)
    "cnc programmer",  # Already in Category 1, but critical
    "cam programmer",  # Computer-Aided Manufacturing
    "manufacturing programmer",
    "robot programmer",  # For industrial robots
]
```

**Confidence:** 🟡 MEDIUM-HIGH - Adjacent to trades, daily interaction

---

### Subcategory 2D: Training & Safety (MEDIUM CONFIDENCE)

**Why include:** Support skilled trades development and safety

```python
TRAINING_SAFETY_KEYWORDS = [
    # Training roles
    "manufacturing trainer",
    "technical trainer",
    "trades instructor",
    "apprenticeship coordinator",
    "training coordinator",

    # Safety roles
    "safety coordinator",
    "safety technician",
    "ehs coordinator",  # Environmental, Health, Safety
    "ehs technician",
    "occupational safety",
    "industrial hygienist",

    # Quality training
    "quality trainer",
    "lean coordinator",
    "continuous improvement",
]
```

**Confidence:** 🟡 MEDIUM - Support ecosystem, but not direct trades

---

## CATEGORY 3: Adjacent Technical Roles (MEDIUM CONFIDENCE - REVIEW CAREFULLY)

**Question:** Should we include these? They support trades but aren't traditional "trades" themselves.

### Subcategory 3A: Technical Support & Specialists

```python
TECHNICAL_SUPPORT_KEYWORDS = [
    # Process specialists
    "manufacturing specialist",
    "process specialist",
    "quality specialist",
    "tooling specialist",

    # Technical roles
    "manufacturing technologist",
    "process technologist",
    "applications engineer",  # Customer-facing technical

    # Data/systems
    "manufacturing data analyst",  # Growing field
    "erp specialist",  # Manufacturing ERP systems
    "mes technician",  # Manufacturing Execution Systems
]
```

**Confidence:** 🟠 MEDIUM - Some are borderline IT/engineering

**Recommendation:** Include "specialist" roles, exclude pure IT/data roles

---

## MERGED KEYWORD LIST - RECOMMENDED FOR IMPLEMENTATION

**Approach:** Merge Category 1 (Hands-On) + Category 2A/2B (High Confidence Leadership)

**Total keywords:** ~200+ (from current ~80)

### Confidence-Based Inclusion:

| Category | Confidence | Include? | Keyword Count |
|----------|-----------|----------|---------------|
| **Cat 1A-F** | 🟢 HIGH | ✅ YES | ~120 |
| **Cat 2A** | 🟢 HIGH | ✅ YES | ~30 |
| **Cat 2B** | 🟢 HIGH | ✅ YES | ~35 |
| **Cat 2C** | 🟡 MEDIUM-HIGH | ✅ YES | ~15 |
| **Cat 2D** | 🟡 MEDIUM | ⚠️ MAYBE | ~15 |
| **Cat 3A** | 🟠 MEDIUM | ❌ NO (for now) | ~10 |

**Recommended total:** ~200 keywords (Cat 1 + Cat 2A + Cat 2B + Cat 2C)

---

## IMPLEMENTATION PREVIEW (NOT DEPLOYED)

```python
# ======================================================
# SKILLED TRADES KEYWORDS - EXPANDED VERSION
# ======================================================
# This is the MERGED list combining:
#   - Category 1: Hands-on skilled trades (current + expanded)
#   - Category 2: Technical leadership (HIGH + MEDIUM-HIGH confidence)
#
# Total keywords: ~200
# Approach: Single merged list (Option B from discussion)
# ======================================================

SKILLED_TRADES_KEYWORDS_EXPANDED = [
    # ==========================================
    # CATEGORY 1: HANDS-ON SKILLED TRADES
    # ==========================================

    # --- 1A: Machining & Fabrication ---
    "machinist", "cnc", "mill operator", "lathe operator", "grinder", "toolmaker",
    "fabricator", "metalworker", "sheet metal", "precision machinist", "machine operator",
    "manual machinist", "setup operator", "g-code", "programmer", "tool and die", "die maker",
    "mold maker", "production machinist", "numerical control", "machining technician",
    "swiss machinist", "5-axis operator", "edm operator", "waterjet operator",
    "laser operator", "plasma cutter", "boring mill operator", "horizontal machinist",
    "jig borer", "gear cutter", "honing machine operator", "lapping technician",

    # --- 1B: Assembly & Production (EXISTING - keep all) ---
    "assembler", "assembly technician", "production operator", "production technician",
    "line operator", "mechanical assembler", "electromechanical assembler",
    "production worker", "manufacturing technician", "machine technician",
    "assembly lead", "manufacturing associate", "packaging operator", "composite technician",

    # --- 1C: Welding & Metalwork (EXPANDED) ---
    "welder", "tig welder", "mig welder", "arc welder", "fabrication welder",
    "pipe welder", "aluminum welder", "spot welder", "soldering", "brazing",
    "welding technician", "weld inspector", "fitter welder",
    "certified welder", "aws certified welder", "cw welder", "cwi", "cwe",
    "combo welder", "stick welder", "flux core welder", "orbital welder", "robotic welder",

    # --- 1D: Licensed Electrical Trades (EXPANDED ⭐) ---
    "electrician", "electrical technician", "electronics technician",
    "controls technician", "panel builder", "wire harness assembler",
    "electromechanical technician", "instrumentation technician", "automation technician",
    "journeyman electrician", "master electrician", "industrial electrician",
    "maintenance electrician", "commercial electrician",
    "controls engineer", "automation specialist", "robotics technician",
    "plc programmer", "scada technician", "instrumentation electrician",
    "high voltage electrician", "electrical inspector", "electrical designer",
    "panel designer", "control panel technician",

    # --- 1E: Plumbing, Pipefitting & HVAC (EXPANDED ⭐) ---
    "plumber", "journeyman plumber", "master plumber", "pipefitter", "steamfitter",
    "sprinkler fitter", "industrial plumber", "process piping",
    "hvac technician", "hvac mechanic", "hvac service technician", "hvac installer",
    "refrigeration technician", "chiller technician", "boiler technician",
    "building automation", "hvac controls", "hvac apprentice", "journeyman hvac",
    "facilities mechanic", "building engineer", "stationary engineer", "boiler operator",

    # --- 1F: Maintenance & Repair (EXPANDED) ---
    "maintenance technician", "maintenance mechanic", "maintenance engineer",
    "industrial mechanic", "millwright", "equipment technician", "machine repair",
    "facilities technician", "mechanical technician", "preventive maintenance",
    "repair technician", "plant mechanic", "equipment maintenance",
    "predictive maintenance", "reliability technician", "vibration analyst",
    "lubrication technician", "alignment technician", "hydraulics technician",
    "pneumatics technician", "conveyor technician", "crane technician", "forklift technician",

    # --- 1G: Inspection & Quality (EXPANDED) ---
    "inspector", "quality inspector", "quality technician", "qc technician",
    "qa inspector", "ndt technician", "cmm operator", "quality assurance",
    "final inspector", "metrology technician", "dimensional inspector",
    "ndt level ii", "ndt level iii", "ultrasonic technician", "radiographic technician",
    "magnetic particle", "liquid penetrant", "eddy current technician",
    "visual inspection", "asnt certified", "calibration technician", "gage technician",
    "optical inspector", "coordinate measuring", "layout inspector",
    "receiving inspector", "in-process inspector",

    # --- 1H: Tooling & Setup (EXISTING - keep all) ---
    "tool room", "tooling engineer", "setup technician", "fixture builder",
    "tool designer", "jig and fixture", "tooling technician",

    # --- 1I: Composites & Aerospace Fabrication (EXISTING - keep all) ---
    "composite technician", "lamination technician", "bonding technician",
    "aerospace assembler", "aircraft technician", "avionics technician",
    "sheet metal mechanic", "structures mechanic", "airframe mechanic",

    # --- 1J: Other Skilled Trades (EXISTING - keep all) ---
    "carpenter", "painter", "coating technician",
    "surface finisher", "heat treat operator", "chemical processor",
    "machining apprentice", "maintenance apprentice", "journeyman",
    "technician apprentice",

    # ==========================================
    # CATEGORY 2: TECHNICAL LEADERSHIP
    # (HIGH + MEDIUM-HIGH CONFIDENCE)
    # ==========================================

    # --- 2A: Manufacturing & Quality Engineering (HIGH CONFIDENCE ⭐) ---
    "manufacturing engineer", "process engineer", "industrial engineer",
    "manufacturing engineering", "process improvement engineer", "methods engineer",
    "tool engineer", "fixture engineer",
    "quality engineer", "qa engineer", "qc engineer", "quality engineering",
    "supplier quality engineer", "sqa", "quality systems engineer",
    "six sigma", "green belt", "black belt", "asq certified",
    "cqe", "cqa", "cre",

    # --- 2B: Production Supervision (HIGH CONFIDENCE ⭐) ---
    "production supervisor", "manufacturing supervisor", "shop supervisor",
    "maintenance supervisor", "quality supervisor", "shift supervisor",
    "area supervisor", "department supervisor", "assembly supervisor",
    "fabrication supervisor", "machining supervisor",
    "shop foreman", "production foreman", "maintenance foreman",
    "general foreman", "working foreman",
    "lead technician", "senior technician", "master technician",
    "lead machinist", "lead welder", "lead assembler",
    "superintendent", "shop superintendent", "production superintendent",
    "manufacturing superintendent", "maintenance superintendent",

    # --- 2C: Production Planning & Coordination (MEDIUM-HIGH CONFIDENCE) ---
    "production planner", "manufacturing planner", "production scheduler",
    "production control", "material planner", "capacity planner",
    "manufacturing coordinator", "production coordinator", "operations coordinator",
    "shift coordinator", "materials coordinator",
    "cnc programmer", "cam programmer", "manufacturing programmer", "robot programmer",
]

# Total: ~200 keywords
# Coverage: Hands-on trades + direct technical leadership + certifications
```

---

## WHAT'S MISSING? - Gap Analysis

### Roles We SHOULD Add (Recommend):

1. ✅ **Licensed electricians** (journeyman, master) - ADDED
2. ✅ **Licensed plumbers/pipefitters** - ADDED
3. ✅ **HVAC certified technicians** - ADDED
4. ✅ **Manufacturing engineers** - ADDED
5. ✅ **Quality engineers** - ADDED
6. ✅ **Supervisors & foremen** - ADDED
7. ✅ **NDT certified technicians** - ADDED
8. ✅ **AWS certified welders** - ADDED
9. ✅ **Six Sigma specialists** - ADDED
10. ✅ **Production planners/schedulers** - ADDED

### Roles We MIGHT Add (Need Discussion):

1. ⚠️ **Training coordinators** - Support role, not direct production
2. ⚠️ **Safety coordinators** - Important but not a "trade"
3. ⚠️ **ERP specialists** - More IT than trades
4. ⚠️ **Data analysts** - Analytics, not hands-on

### Roles We SHOULD NOT Add:

1. ❌ **Plant managers** - Too high-level
2. ❌ **Operations managers** - Too broad
3. ❌ **HR coordinators** - Not trades-related
4. ❌ **Purchasing agents** - Supply chain, not trades
5. ❌ **IT technicians** - Different skillset entirely

---

## CATEGORIZATION IN OUTPUT

**Recommendation:** Add a "Category" column to Excel output so you can analyze separately

```python
if any(kw.lower() in title.lower() for kw in HANDS_ON_TRADES_KEYWORDS):
    job["Category"] = "Skilled Trades - Hands-On"
    job["Subcategory"] = detect_subcategory(title)  # Machining, Welding, etc.
    local_results.append(job)

elif any(kw.lower() in title.lower() for kw in ENGINEERING_LEADERSHIP_KEYWORDS):
    job["Category"] = "Skilled Trades - Engineering"
    job["Subcategory"] = "Manufacturing/Quality Engineering"
    local_results.append(job)

elif any(kw.lower() in title.lower() for kw in SUPERVISORY_LEADERSHIP_KEYWORDS):
    job["Category"] = "Skilled Trades - Leadership"
    job["Subcategory"] = "Supervision/Management"
    local_results.append(job)

elif any(kw.lower() in title.lower() for kw in PLANNING_COORDINATION_KEYWORDS):
    job["Category"] = "Skilled Trades - Support"
    job["Subcategory"] = "Planning/Coordination"
    local_results.append(job)
```

**Excel Output Example:**

| Company | Job Title | Category | Subcategory | Location |
|---------|-----------|----------|-------------|----------|
| Barnes Aerospace | CNC Machinist | Skilled Trades - Hands-On | Machining | East Granby, CT |
| Barnes Aerospace | Manufacturing Engineer | Skilled Trades - Engineering | Manufacturing Engineering | East Granby, CT |
| Barnes Aerospace | Production Supervisor | Skilled Trades - Leadership | Supervision | East Granby, CT |
| GKN Aerospace | Master Electrician | Skilled Trades - Hands-On | Electrical (Licensed) | Newington, CT |

---

## NEXT STEPS - FOR REVIEW

1. **Review keyword list** - Are there trades we're still missing?
2. **Validate confidence levels** - Do you agree with HIGH/MEDIUM categorization?
3. **Decide on Cat 2D** - Include training/safety coordinators?
4. **Test with sample** - Run 10 companies and review Category distribution
5. **Adjust if needed** - Based on actual results

---

## QUESTIONS FOR YOU:

1. **Category 2C (Planning/Coordination):** Should we include production planners? They work closely with trades but aren't hands-on.

2. **Category 2D (Training/Safety):** Should we include these support roles, or keep focus purely on direct trades + technical leadership?

3. **Subcategory tracking:** Do you want to track subcategories (Machining, Welding, Electrical, etc.) in the output Excel?

4. **Certification emphasis:** Should we create a separate "Certification" column to flag roles that require professional licenses?

---

**Summary:** This expansion would grow from ~80 to ~200 keywords, adding:
- **Critical gap:** Licensed electricians, plumbers, HVAC (+40 keywords)
- **Major gap:** Technical leadership - engineers, supervisors (+50 keywords)
- **Enhancement:** Certification-specific roles - AWS, ASQ, NDT (+20 keywords)
- **Support ecosystem:** Planning, coordination (+10 keywords)

**Total coverage improvement:** 150% increase in keyword coverage, capturing complete trades ecosystem
