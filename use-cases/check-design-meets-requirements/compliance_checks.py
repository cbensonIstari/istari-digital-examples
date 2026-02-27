"""
Compliance checks: requirements vs architecture vs CAD.

Compares SysML requirements and architecture (parts) against nTop
aerodeck metrics. Returns a simple pass/fail report.

Usage:
    from compliance_checks import run_all_checks
    results = run_all_checks(reqs_data, parts_data, metrics_data)
"""

import json


def run_all_checks(reqs: dict, parts: dict, metrics: dict) -> list[dict]:
    """Run all compliance checks and return results."""
    results = []
    results += check_reqs_vs_cad(reqs, metrics)
    results += check_architecture_mass(reqs, parts)
    return results


def check_reqs_vs_cad(reqs: dict, metrics: dict) -> list[dict]:
    """Check quantitative requirements against CAD results."""
    results = []

    # Build lookup by requirement name
    lookup = {r.get("name"): r for r in reqs.values() if r.get("attributes")}

    # Range: actual >= target
    req = lookup.get("RangeReq", {})
    target = float(req.get("attributes", {}).get("targetValue", 0))
    actual = metrics.get("range_mission", {}).get("range_nm", 0)
    if target:
        results.append(_result("RangeReq", "Range", target, actual, "nm", ">="))

    # Weight: actual <= target
    req = lookup.get("MaxStructureWeight", {})
    target = float(req.get("attributes", {}).get("maxValue", 0))
    actual = metrics.get("mass_properties", {}).get("empty_weight_lbm", 0)
    if target:
        results.append(_result("MaxStructureWeight", "Structure Weight", target, actual, "lb", "<="))

    # Speed: actual >= target
    req = lookup.get("CruiseSpeed", {})
    target = float(req.get("attributes", {}).get("minValue", 0))
    actual = metrics.get("range_mission", {}).get("cruise_speed_kts", 0)
    if target:
        results.append(_result("CruiseSpeed", "Cruise Speed", target, actual, "kts", ">="))

    return results


def check_architecture_mass(reqs: dict, parts: dict) -> list[dict]:
    """Sum component masses from architecture and compare to weight requirement."""
    # Find the weight requirement target
    target = 0
    for r in reqs.values():
        if r.get("name") == "MaxStructureWeight":
            target = float(r.get("attributes", {}).get("maxValue", 0))
            break

    if not target:
        return []

    # Sum all component masses from parts
    total_mass = 0
    for qname, part in parts.items():
        mass_attr = part.get("attributes", {}).get("mass", {})
        val = mass_attr.get("value")
        if val is not None:
            total_mass += float(val)

    return [_result(
        "MaxStructureWeight", "Architecture Mass Roll-up",
        target, round(total_mass, 1), "lb", "<="
    )]


def _result(requirement, check, target, actual, unit, operator):
    """Build a single check result."""
    if operator == ">=":
        passed = actual >= target
        margin = round((actual - target) / target * 100, 1) if target else 0
    else:  # <=
        passed = actual <= target
        margin = round((target - actual) / target * 100, 1) if target else 0

    return {
        "requirement": requirement,
        "check": check,
        "target": target,
        "actual": actual,
        "unit": unit,
        "operator": operator,
        "status": "PASS" if passed else "FAIL",
        "margin": margin,
    }


def format_report(results: list[dict]) -> str:
    """Print a readable text report."""
    lines = []
    for r in results:
        icon = "PASS" if r["status"] == "PASS" else "FAIL"
        margin_str = f"+{r['margin']}%" if r["margin"] >= 0 else f"{r['margin']}%"
        lines.append(
            f"  {r['check']:30s} {icon}  "
            f"({r['actual']} {r['unit']} {r['operator']} {r['target']} {r['unit']}, "
            f"margin: {margin_str})"
        )
    passing = sum(1 for r in results if r["status"] == "PASS")
    lines.append(f"\n  {passing}/{len(results)} checks passed")
    return "\n".join(lines)
