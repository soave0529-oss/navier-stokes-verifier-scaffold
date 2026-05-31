from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from generation_spec_v4 import (
    BLOCKER_SOURCE_INDEX_JSON_KEY,
    BLOCKER_SOURCE_INDEX_MARKDOWN_KEY,
    PROOF_OBLIGATION_REPORT_KEY,
    PROOF_OBLIGATION_SUMMARY_KEY,
    REQUIRED_MARKERS,
)
from manual_promotion_packet import DEFAULT_JSON_OUTPUT as DEFAULT_PACKET_JSON
from proposed_candidate_staging import DEFAULT_CANDIDATE_DIR
from schema import LemmaCandidate, load_candidate


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_DIR = ROOT / "track-a-regularity/reports"
DEFAULT_MARKDOWN_OUTPUT = DEFAULT_REPORT_DIR / "active_pool_ingress_audit.md"
DEFAULT_JSON_OUTPUT = DEFAULT_REPORT_DIR / "active_pool_ingress_audit.json"
NON_CLAIMS = (
    "active_pool_ingress_audit_only",
    "no_file_copy",
    "no_candidate_emission",
    "no_candidate_promotion",
    "no_navier_stokes_solution",
    "no_epsilon_regularity_theorem",
    "no_weak_to_smooth_upgrade",
)
V4_EXPECTED_KEYS = (
    PROOF_OBLIGATION_REPORT_KEY,
    PROOF_OBLIGATION_SUMMARY_KEY,
    BLOCKER_SOURCE_INDEX_MARKDOWN_KEY,
    BLOCKER_SOURCE_INDEX_JSON_KEY,
)


@dataclass(frozen=True)
class IngressFinding:
    path: str
    candidate_id: str
    finding_type: str
    packet_status: str
    severity: str
    reason: str


@dataclass(frozen=True)
class ActivePoolIngressAudit:
    schema_version: int
    candidate_dir: str
    packet_json: str
    packet_count: int
    ready_packet_count: int
    active_candidate_file_count: int
    legacy_skipped_count: int
    tracked_target_absent_count: int
    authorized_ingress_count: int
    violation_count: int
    findings: tuple[IngressFinding, ...]
    non_claims: tuple[str, ...]


def _relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve()))
    except ValueError:
        return str(path)


def _resolve_report_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def _load_packet_json(packet_json: Path) -> dict[str, Any]:
    if not packet_json.exists():
        raise FileNotFoundError(f"manual promotion packet JSON is missing: {packet_json}")
    data = json.loads(packet_json.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"manual promotion packet JSON root must be object: {packet_json}")
    return data


def _packet_targets(packet_data: dict[str, Any]) -> dict[str, str]:
    targets: dict[str, str] = {}
    packets = packet_data.get("packets", [])
    if not isinstance(packets, list):
        raise ValueError("manual promotion packet JSON field 'packets' must be a list")
    for packet in packets:
        if not isinstance(packet, dict):
            raise ValueError("manual promotion packet entry must be an object")
        target = packet.get("manual_copy_target")
        status = packet.get("packet_status")
        if not isinstance(target, str) or not target:
            raise ValueError("manual promotion packet entry is missing manual_copy_target")
        if not isinstance(status, str) or not status:
            raise ValueError("manual promotion packet entry is missing packet_status")
        targets[str(_resolve_report_path(target).resolve())] = status
    return targets


def _packet_count(packet_data: dict[str, Any]) -> int:
    value = packet_data.get("packet_count", len(packet_data.get("packets", [])))
    return int(value)


def _ready_packet_count(packet_data: dict[str, Any]) -> int:
    value = packet_data.get("ready_packet_count")
    if value is not None:
        return int(value)
    return sum(
        1
        for packet in packet_data.get("packets", [])
        if isinstance(packet, dict) and packet.get("packet_status") == "ready_for_manual_copy"
    )


def _is_v4_or_template_like(candidate: LemmaCandidate) -> bool:
    marker_set = set(candidate.related_known)
    has_required_marker = any(marker in marker_set for marker in REQUIRED_MARKERS)
    has_v4_marker = any(marker.startswith("V4:") for marker in candidate.related_known)
    has_v4_sidecar_key = any(key in candidate.expected_evaluator for key in V4_EXPECTED_KEYS)
    generated_by = candidate.generated_by.lower()
    type_name = candidate.type.lower()
    template_like = (
        "template" in generated_by
        or "template" in type_name
        or candidate.id == "lemma_v4_blocked_template"
    )
    return has_required_marker or has_v4_marker or has_v4_sidecar_key or template_like


def _candidate_paths(candidate_dir: Path) -> tuple[Path, ...]:
    if not candidate_dir.exists():
        return ()
    return tuple(sorted(candidate_dir.glob("lemma_*.yaml")))


def build_ingress_audit(
    *,
    candidate_dir: Path = DEFAULT_CANDIDATE_DIR,
    packet_json: Path = DEFAULT_PACKET_JSON,
) -> ActivePoolIngressAudit:
    packet_data = _load_packet_json(packet_json)
    target_statuses = _packet_targets(packet_data)
    active_paths = _candidate_paths(candidate_dir)
    active_path_set = {str(path.resolve()) for path in active_paths}
    findings: list[IngressFinding] = []
    legacy_skipped = 0
    authorized = 0

    for target_text, packet_status in sorted(target_statuses.items()):
        target_path = Path(target_text)
        if target_text not in active_path_set:
            continue
        if packet_status == "ready_for_manual_copy":
            authorized += 1
            findings.append(
                IngressFinding(
                    path=_relative(target_path),
                    candidate_id=target_path.stem,
                    finding_type="authorized_ready_packet_target_present",
                    packet_status=packet_status,
                    severity="info",
                    reason="active-pool target is present and the stored manual packet is ready",
                )
            )
        else:
            findings.append(
                IngressFinding(
                    path=_relative(target_path),
                    candidate_id=target_path.stem,
                    finding_type="blocked_packet_target_present",
                    packet_status=packet_status,
                    severity="violation",
                    reason="manual packet target is present in active pool without ready status",
                )
            )

    for path in active_paths:
        resolved = str(path.resolve())
        try:
            candidate = load_candidate(path)
        except Exception as exc:  # noqa: BLE001 - active pool must stay parseable.
            findings.append(
                IngressFinding(
                    path=_relative(path),
                    candidate_id=path.stem,
                    finding_type="active_pool_yaml_load_error",
                    packet_status=target_statuses.get(resolved, "missing"),
                    severity="violation",
                    reason=f"active-pool YAML is not loadable: {exc}",
                )
            )
            continue

        if not _is_v4_or_template_like(candidate):
            legacy_skipped += 1
            continue
        if resolved in target_statuses:
            continue

        findings.append(
            IngressFinding(
                path=_relative(path),
                candidate_id=candidate.id,
                finding_type="untracked_v4_or_template_candidate",
                packet_status="missing",
                severity="violation",
                reason="v4/template-like active-pool YAML has no matching manual promotion packet target",
            )
        )

    violation_count = sum(1 for finding in findings if finding.severity == "violation")
    tracked_absent = sum(1 for target in target_statuses if target not in active_path_set)
    return ActivePoolIngressAudit(
        schema_version=1,
        candidate_dir=_relative(candidate_dir),
        packet_json=_relative(packet_json),
        packet_count=_packet_count(packet_data),
        ready_packet_count=_ready_packet_count(packet_data),
        active_candidate_file_count=len(active_paths),
        legacy_skipped_count=legacy_skipped,
        tracked_target_absent_count=tracked_absent,
        authorized_ingress_count=authorized,
        violation_count=violation_count,
        findings=tuple(findings),
        non_claims=NON_CLAIMS,
    )


def audit_to_dict(audit: ActivePoolIngressAudit) -> dict[str, object]:
    return {
        "schema_version": audit.schema_version,
        "candidate_dir": audit.candidate_dir,
        "packet_json": audit.packet_json,
        "packet_count": audit.packet_count,
        "ready_packet_count": audit.ready_packet_count,
        "active_candidate_file_count": audit.active_candidate_file_count,
        "legacy_skipped_count": audit.legacy_skipped_count,
        "tracked_target_absent_count": audit.tracked_target_absent_count,
        "authorized_ingress_count": audit.authorized_ingress_count,
        "violation_count": audit.violation_count,
        "findings": [asdict(finding) for finding in audit.findings],
        "non_claims": list(audit.non_claims),
        "docs": {
            "freeze_doc": "docs/CANDIDATE_GENERATION_FREEZE.md",
            "staging_doc": "docs/STEP81_PROPOSED_CANDIDATE_STAGING.md",
            "manual_packet_doc": "docs/STEP82_MANUAL_PROMOTION_PACKET.md",
        },
    }


def _finding_rows(audit: ActivePoolIngressAudit) -> list[str]:
    rows = [
        "| path | id | finding type | packet status | severity | reason |",
        "|---|---|---|---|---|---|",
    ]
    if not audit.findings:
        rows.append("| `none` | `none` | `none` | `none` | `none` | `no ingress findings` |")
        return rows
    for finding in audit.findings:
        rows.append(
            "| "
            f"`{finding.path}` | "
            f"`{finding.candidate_id}` | "
            f"`{finding.finding_type}` | "
            f"`{finding.packet_status}` | "
            f"`{finding.severity}` | "
            f"{finding.reason} |"
        )
    return rows


def render_markdown(audit: ActivePoolIngressAudit) -> str:
    return "\n".join(
        (
            "# Active Pool Ingress Audit",
            "",
            "Generated by `track-a-regularity/evaluator/active_pool_ingress_audit.py`.",
            "",
            "This report checks whether staged/template-style YAML has entered",
            "`track-a-regularity/candidates/` without a matching ready manual promotion packet.",
            "It never copies files and never promotes candidates.",
            "",
            "## Summary",
            "",
            f"- candidate_dir: `{audit.candidate_dir}`",
            f"- packet_json: `{audit.packet_json}`",
            f"- packet_count: `{audit.packet_count}`",
            f"- ready_packet_count: `{audit.ready_packet_count}`",
            f"- active_candidate_file_count: `{audit.active_candidate_file_count}`",
            f"- legacy_skipped_count: `{audit.legacy_skipped_count}`",
            f"- tracked_target_absent_count: `{audit.tracked_target_absent_count}`",
            f"- authorized_ingress_count: `{audit.authorized_ingress_count}`",
            f"- violation_count: `{audit.violation_count}`",
            "",
            "## Findings",
            "",
            *_finding_rows(audit),
            "",
            "## Non-Claims",
            "",
            *(f"- `{item}`" for item in audit.non_claims),
            "",
        )
    )


def render_json(audit: ActivePoolIngressAudit) -> str:
    return json.dumps(audit_to_dict(audit), indent=2, sort_keys=True) + "\n"


def render_output(audit: ActivePoolIngressAudit, output_format: str) -> str:
    if output_format == "markdown":
        return render_markdown(audit)
    if output_format == "json":
        return render_json(audit)
    raise ValueError(f"unknown ingress audit format: {output_format}")


def write_output(output: Path, audit: ActivePoolIngressAudit, output_format: str) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_output(audit, output_format), encoding="utf-8")
    return output


def check_output(
    output: Path,
    audit: ActivePoolIngressAudit,
    output_format: str,
) -> tuple[bool, str]:
    expected = render_output(audit, output_format)
    if not output.exists():
        return False, f"missing active-pool ingress audit: {output}"
    current = output.read_text(encoding="utf-8")
    if current != expected:
        return False, f"stale active-pool ingress audit: {output}"
    return True, f"fresh active-pool ingress audit: {output}"


def default_output_path(output_format: str) -> Path:
    if output_format == "markdown":
        return DEFAULT_MARKDOWN_OUTPUT
    if output_format == "json":
        return DEFAULT_JSON_OUTPUT
    raise ValueError(f"unknown ingress audit format: {output_format}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit active candidate pool ingress against manual promotion packets."
    )
    parser.add_argument("--candidate-dir", type=Path, default=DEFAULT_CANDIDATE_DIR)
    parser.add_argument("--packet-json", type=Path, default=DEFAULT_PACKET_JSON)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--check-output",
        action="store_true",
        help="Check that --output already matches the rendered ingress audit.",
    )
    parser.add_argument(
        "--require-clean",
        action="store_true",
        help="Fail if any active-pool ingress violation is present.",
    )
    args = parser.parse_args(argv)

    try:
        audit = build_ingress_audit(candidate_dir=args.candidate_dir, packet_json=args.packet_json)
    except Exception as exc:  # noqa: BLE001 - CLI should report audit setup failures.
        print(f"failed to build active-pool ingress audit: {exc}", file=sys.stderr)
        return 1

    output = args.output or default_output_path(args.format)
    if args.check_output:
        ok, message = check_output(output, audit, args.format)
        print(message)
        if not ok:
            print("run without --check-output to regenerate the ingress audit", file=sys.stderr)
            return 1
    else:
        written = write_output(output, audit, args.format)
        print(f"wrote {written}")

    if args.require_clean and audit.violation_count:
        print("active-pool ingress violations are present", file=sys.stderr)
        return 1

    print(f"active_candidate_file_count: {audit.active_candidate_file_count}")
    print(f"legacy_skipped_count: {audit.legacy_skipped_count}")
    print(f"tracked_target_absent_count: {audit.tracked_target_absent_count}")
    print(f"authorized_ingress_count: {audit.authorized_ingress_count}")
    print(f"violation_count: {audit.violation_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
