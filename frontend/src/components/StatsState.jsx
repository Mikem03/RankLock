
const StatsState = ({ currentStats, onStatsChange }) => {
    const handleChange = (event) => {
      onStatsChange(event.target.value);
    }
    return (
      <div className="stats-state-container">
        <button id="stats-select" onClick={handleChange} value="Hero">
          Heroes</button>
        <button id="stats-select" onClick={handleChange} value="Item">
          Items</button>
        <h2>{currentStats} Statistics</h2>
      </div>
    ); 
}

export default StatsState;