import React from 'react';

const FiltersPanel = ({ 
    filters, 
    getRankName, 
    handleFilterChange, 
    applyFilters, 
    resetFilters, 
    loading 
}) => {
    return (
        <div className="filters-panel">        
            <div className="filter-group">
            <label>Minimum Rank: {getRankName(filters.minRank)}</label>
            <input
                type="range"
                min="0"
                max="11"
                value={filters.minRank}
                onChange={(e) => handleFilterChange('minRank', parseInt(e.target.value))}
                className="rank-slider"
            />
            </div>

            <div className="filter-group">
            <label>Maximum Rank: {getRankName(filters.maxRank)}</label>
            <input
                type="range"
                min="0"
                max="11"
                value={filters.maxRank}
                onChange={(e) => handleFilterChange('maxRank', parseInt(e.target.value))}
                className="rank-slider"
            />
            </div>

            <div className="filter-actions">
            <button onClick={applyFilters} disabled={loading}>
                {loading ? 'Loading...' : 'Apply Filters'}
            </button>
            <button onClick={resetFilters}>Reset</button>
            </div>
        </div>
    );
};

export default FiltersPanel;
