import "./Hal9000.css";

const Hal9000 = () => {
  return (
    <div className="hal-container">
      <div className="hal-name-container">
        <div className="hal-name-left">MOXON</div>
        <div className="hal-name-right">9000</div>
      </div>
      <div className="hal-footer-container">
        <div className="hal-eye-container">
          <div className="base">
            <div className="lens">
              <div className="reflections"></div>
            </div>
            <div className="animation"></div>
          </div>
        </div>
        <div className="hal-footer-box"></div>
      </div>
    </div>
  );
};

export default Hal9000;
