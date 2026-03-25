#!/bin/zsh
set -euo pipefail

ROOT="/Users/juns/code/work/mobis/PBL/driving-alert-workproducts/governance/short-paper/appendix"
SRC="${ROOT}/source"
GEN="${ROOT}/tex/generated"
MASTER="${ROOT}/tex/supplementary_appendix_bundle.tex"

mkdir -p "${GEN}"
setopt null_glob
rm -f "${GEN}"/*.tex

convert_one() {
  local src="$1"
  local out="$2"
  /opt/homebrew/bin/pandoc \
    --from=gfm \
    --to=latex \
    --syntax-highlighting=none \
    --wrap=preserve \
    --shift-heading-level-by=1 \
    --output="${out}" \
    "${src}"
}

convert_one "${SRC}/governance/00d_HARA_Worksheet.md" "${GEN}/00d_HARA_Worksheet.tex"
convert_one "${SRC}/governance/00e_ECU_Naming_Standard.md" "${GEN}/00e_ECU_Naming_Standard.tex"
convert_one "${SRC}/governance/00f_CAN_ID_Allocation_Standard.md" "${GEN}/00f_CAN_ID_Allocation_Standard.tex"
convert_one "${SRC}/governance/00g_Master_Test_Matrix.md" "${GEN}/00g_Master_Test_Matrix.tex"

convert_one "${SRC}/contracts/communication-matrix.md" "${GEN}/communication-matrix.tex"
convert_one "${SRC}/contracts/owner-route.md" "${GEN}/owner-route.tex"
convert_one "${SRC}/contracts/layer-separation-policy.md" "${GEN}/layer-separation-policy.tex"
convert_one "${SRC}/contracts/ethernet-interface.md" "${GEN}/ethernet-interface.tex"
convert_one "${SRC}/contracts/multibus-policy.md" "${GEN}/multibus-policy.tex"
convert_one "${SRC}/contracts/panel-sysvar-contract.md" "${GEN}/panel-sysvar-contract.tex"
convert_one "${SRC}/contracts/ethernet-backbone.md" "${GEN}/ethernet-backbone.tex"

convert_one "${SRC}/verification/oracle.md" "${GEN}/oracle.tex"
convert_one "${SRC}/verification/acceptance-criteria.md" "${GEN}/acceptance-criteria.tex"
convert_one "${SRC}/verification/test-asset-mapping.md" "${GEN}/test-asset-mapping.tex"
convert_one "${SRC}/verification/execution-guide.md" "${GEN}/execution-guide.tex"
convert_one "${SRC}/verification/evidence-policy.md" "${GEN}/evidence-policy.tex"

convert_one "${SRC}/diagnostic/diagnostic-matrix.md" "${GEN}/diagnostic-matrix.tex"
convert_one "${SRC}/diagnostic/diagnostic-sysvar-contract.md" "${GEN}/diagnostic-sysvar-contract.tex"
convert_one "${SRC}/diagnostic/diagnostic-seam-design.md" "${GEN}/diagnostic-seam-design.tex"

if [[ -x "/usr/local/texlive/2026basic/bin/universal-darwin/xelatex" ]]; then
  TEXBIN="/usr/local/texlive/2026basic/bin/universal-darwin/xelatex"
else
  TEXBIN="$(command -v xelatex)"
fi

"${TEXBIN}" -interaction=nonstopmode -halt-on-error -output-directory "${ROOT}/tex" "${MASTER}"
"${TEXBIN}" -interaction=nonstopmode -halt-on-error -output-directory "${ROOT}/tex" "${MASTER}"
