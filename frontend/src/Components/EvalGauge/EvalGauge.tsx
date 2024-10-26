const toCentipawn = (score: number) => Math.round(score / 10) / 10;

interface EvalGaugeProps {
  score: number
}

function clamp(num: number, min: number, max: number) {
  return num <= min
    ? min
    : num >= max
      ? max
      : num
}

export const EvalGauge = ({ score }: EvalGaugeProps) => {

  const nomalized = (((score ?? 0) + 1000) / 2000) * 100
  const gaugePosition = clamp(nomalized, 0, 100);

  return (
    <div style={{
      display: "flex",
      flexFlow: "row nowrap",
      width: "100%",
      position: "relative",
      paddingTop: "1em"
    }}>
      <div style={{ position: "absolute", width: "1.2em", height: "1.2em", background: "red", borderRadius: '0.6em', color: "#fff", padding: "2px", textAlign: 'center', transition: 'all 1s', verticalAlign: 'middle', top: "0", left: `calc(${gaugePosition}% - 0.6em)` }}>{toCentipawn(score)}</div>
      <div style={{ width: "calc(100%/24)", background: "#ccc" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*2)", background: "#bbb" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*3)", background: "#aaa" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*4)", background: "#999" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*5)", background: "#888" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*6)", background: "#777" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*6)", background: "#666" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*5)", background: "#555" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*4)", background: "#444" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*3)", background: "#333" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*2)", background: "#222" }}>&nbsp;</div>
      <div style={{ width: "calc(100%/24*1)", background: "#111" }}>&nbsp;</div>
    </div>
  )
}

