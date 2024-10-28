import "./eval-gauge.css";

const toCentipawn = (score: number) => Math.round(score / 10) / 10;
const alwaysPositive = (score: number) => score > 0 ? score : score * -1;
const oneDecimal = (score: number) => score < 10 && score > -10 ? score.toFixed(1) : score.toFixed(0);
const formatScore = (score: number) => oneDecimal(alwaysPositive(toCentipawn(score))).replace(".", ",");

/**
 * Map score values to a percentage number. Used to position the gauge needle.
 * @param score The relative score provided by board analysis
 */
function mapValueToPercentage(score: number) {
  const x = toCentipawn(score);
  if (x <= -6) {
    return -49.8;                  // For values smaller than -6
  } if (x > -6 && x <= -5) {
    return -49.8 + 2.3 * (x + 6);  // For values between -5 and -6
  } if (x > -5 && x <= -4) {
    return -47.5 + 4.8 * (x + 5);  // For values between -4 and -5
  } if (x > -4 && x <= -3) {
    return -42.7 + 7.2 * (x + 4);  // For values between -3 and -4
  } if (x > -3 && x <= -2) {
    return -35.5 + 9.5 * (x + 3);  // For values between -2 and -3
  } if (x > -2 && x <= -1) {
    return -26 + 11.8 * (x + 2);   // For values between -1 and -2
  } if (x > -1 && x < 1) {
    return 14.2 * x;               // For values between -1 and 1
  } if (x >= 1 && x < 2) {
    return 14.2 + 11.8 * (x - 1);  // For values between 1 and 2
  } if (x >= 2 && x < 3) {
    return 26 + 9.5 * (x - 2);     // For values between 2 and 3
  } if (x >= 3 && x < 4) {
    return 35.5 + 7.2 * (x - 3);   // For values between 3 and 4
  } if (x >= 4 && x < 5) {
    return 42.7 + 4.8 * (x - 4);   // For values between 4 and 5
  } if (x >= 5 && x < 6) {
    return 47.5 + 2.3 * (x - 5);   // For values between 5 and 6
  }
  return 49.8;                   // For values greater than 6
}

interface EvalGaugeProps {
  score: number
}

export const EvalGauge = ({ score }: EvalGaugeProps) => {

  const gaugePosition = mapValueToPercentage(score) + 50;

  return (
    <div className="eval-gauge">
      <div className="eval-gauge__needle" style={{ left: `calc(${gaugePosition}% - 0.82em)` }}>{formatScore(score)}</div>
      <div style={{ width: "calc(100%/24*1)", background: "#ccc", color: "#222" }}>6</div>
      <div style={{ width: "calc(100%/24*2)", background: "#bbb", color: "#222" }}>5</div>
      <div style={{ width: "calc(100%/24*3)", background: "#aaa", color: "#222" }}>4</div>
      <div style={{ width: "calc(100%/24*4)", background: "#999", color: "#222" }}>3</div>
      <div style={{ width: "calc(100%/24*5)", background: "#888", color: "#222" }}>2</div>
      <div style={{ width: "calc(100%/24*6)", background: "#777", color: "#222" }}>1</div>
      <div style={{ width: "calc(100%/24*6)", background: "#666", color: "#bbb", textAlign: "right" }}>1</div>
      <div style={{ width: "calc(100%/24*5)", background: "#555", color: "#bbb", textAlign: "right" }}>2</div>
      <div style={{ width: "calc(100%/24*4)", background: "#444", color: "#bbb", textAlign: "right" }}>3</div>
      <div style={{ width: "calc(100%/24*3)", background: "#333", color: "#bbb", textAlign: "right" }}>4</div>
      <div style={{ width: "calc(100%/24*2)", background: "#222", color: "#bbb", textAlign: "right" }}>5</div>
      <div style={{ width: "calc(100%/24*1)", background: "#111", color: "#bbb", textAlign: "right" }}>6</div>
    </div>
  )
}

