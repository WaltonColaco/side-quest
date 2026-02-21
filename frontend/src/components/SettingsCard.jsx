import { useSettings } from "../context/SettingsContext";

function Toggle({ label, active, onClick }) {
  return (
    <button
      className={`pill-toggle ${active ? "on" : "off"}`}
      type="button"
      onClick={onClick}
      aria-pressed={active}
    >
      {label}
    </button>
  );
}

export default function SettingsCard({ onClose }) {
  const { state, toggleFilter, setTheme, setUnits, reset } = useSettings();

  return (
    <div className="settings-card">
      <header className="settings-header">
        <h1>Settings</h1>
        <div className="settings-actions">
          <button className="link" type="button" onClick={reset}>
            Reset
          </button>
          {onClose ? (
            <button className="icon-close" type="button" aria-label="Close settings" onClick={onClose}>
              ×
            </button>
          ) : null}
        </div>
      </header>

      <div className="settings-group">
        <h2>Accessibility Filters</h2>
        <div className="pill-row">
          <Toggle label="Ramp Access" active={state.filters.ramp} onClick={() => toggleFilter("ramp")} />
          <Toggle
            label="Power Doors Only"
            active={state.filters.powerDoors}
            onClick={() => toggleFilter("powerDoors")}
          />
          <Toggle
            label="Elevator Access"
            active={state.filters.elevator}
            onClick={() => toggleFilter("elevator")}
          />
        </div>
      </div>

      <div className="settings-group">
        <h2>Visual Themes</h2>
        <div className="pill-row">
          <Toggle
            label="Dark Mode"
            active={state.theme.darkMode}
            onClick={() => setTheme("darkMode", !state.theme.darkMode)}
          />
          <Toggle
            label="High Contrast"
            active={state.theme.highContrast}
            onClick={() => setTheme("highContrast", !state.theme.highContrast)}
          />
        </div>
      </div>

      <div className="settings-group">
        <h2>Unit of Measurement</h2>
        <div className="pill-row">
          <Toggle label="mm" active={state.units === "mm"} onClick={() => setUnits("mm")} />
          <Toggle label="in" active={state.units === "in"} onClick={() => setUnits("in")} />
        </div>
      </div>
    </div>
  );
}
