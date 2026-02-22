import { useSettings } from "../context/SettingsContext";

function FilterSquare({ label, active, onClick }) {
  return (
    <button
      className="settings-filter-item"
      type="button"
      onClick={onClick}
      aria-pressed={active}
    >
      <span className={`settings-filter-square ${active ? "on" : "off"}`} />
      <span>{label}</span>
    </button>
  );
}

function SwitchToggle({ label, active, onClick }) {
  return (
    <button
      className="settings-switch-row"
      type="button"
      onClick={onClick}
      aria-pressed={active}
    >
      <span className={`settings-switch ${active ? "on" : "off"}`}>
        <span className="settings-switch-knob" />
      </span>
      <span className="settings-switch-label">{label}</span>
    </button>
  );
}

function UnitToggle({ unit, selected, onClick }) {
  return (
    <button
      className={`settings-unit-button ${selected ? "on" : "off"}`}
      type="button"
      onClick={onClick}
    >
      {unit}
    </button>
  );
}

export default function SettingsCard({ onClose }) {
  const { state, toggleFilter, setTheme, setUnits, setPreference } =
    useSettings();

  return (
    <div className="settings-card">
      <header className="settings-header">
        <h1>Settings</h1>
        {onClose ? (
          <button
            className="settings-close"
            type="button"
            aria-label="Close settings"
            onClick={onClose}
          >
            x
          </button>
        ) : null}
      </header>

      <div className="settings-group">
        <h2>Accesibility Filters</h2>
        <div className="settings-filter-row">
          <FilterSquare
            label="Ramp Access"
            active={state.filters.ramp}
            onClick={() => toggleFilter("ramp")}
          />
          <FilterSquare
            label="Power Doors Only"
            active={state.filters.powerDoors}
            onClick={() => toggleFilter("powerDoors")}
          />
          <FilterSquare
            label="Elevator Access"
            active={state.filters.elevator}
            onClick={() => toggleFilter("elevator")}
          />
        </div>
      </div>

      <div className="settings-group">
        <h2>Visual Themes</h2>
        <div className="settings-switches">
          <SwitchToggle
            label="Dark Mode"
            active={state.theme.darkMode}
            onClick={() => setTheme("darkMode", !state.theme.darkMode)}
          />
          <SwitchToggle
            label="High Contrast Colours"
            active={state.theme.highContrast}
            onClick={() => setTheme("highContrast", !state.theme.highContrast)}
          />
        </div>
      </div>

      <div className="settings-group">
        <div className="settings-dual-row">
          <div className="settings-dual-col">
            <h2>Unit of Measurement</h2>
            <div className="settings-unit-row">
              <UnitToggle
                unit="mm"
                selected={state.units === "mm"}
                onClick={() => setUnits("mm")}
              />
              <UnitToggle
                unit="in"
                selected={state.units === "in"}
                onClick={() => setUnits("in")}
              />
            </div>
          </div>
          <div className="settings-dual-col">
            <h2>Preferences</h2>
            <div className="settings-unit-row settings-preference-row">
              <UnitToggle
                unit="Residential"
                selected={state.preference === "Residential"}
                onClick={() => setPreference("Residential")}
              />
              <UnitToggle
                unit="Community"
                selected={state.preference === "Community"}
                onClick={() => setPreference("Community")}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
