import React, { useState, useEffect, useMemo } from 'react';


const getHeroImage = (dbName) => {
  const nameMap = {
    "Infernus": "inferno",
    "Seven": "gigawatt",
    "Vindicta": "hornet",
    "Lady Geist": "spectre",
    "Abrams": "bull",
    "Wraith": "wraith",
    "McGinnis": "engineer",
    "Paradox": "chrono",
    "Dynamo": "sumo",
    "Kelvin": "kelvin",
    "Haze": "haze",
    "Holliday": "astro",
    "Bebop": "bebop",
    "Calico": "nano",
    "Grey Talon": "archer",
    "Mo & Krill": "digger",
    "Shiv": "shiv",
    "Ivy": "tengu",
    "Warden": "warden",
    "Yamato": "yamato",
    "Lash": "lash",
    "Viscous": "viscous",
    "Pocket": "synth",
    "Mirage": "mirage",
    "Vyper": "vyper",
    "Sinclair": "magician",
    "Mina": "vampirebat",
    "Drifter": "drifter",
    "Victor": "frank",
    "Paige": "bookworm",
    "The Doorman": "doorman",
    "Billy": "punkgoat",
  };
  console.log(dbName);
  console.log(nameMap[dbName]);
  return nameMap[dbName];
};

const SortBy = ({ onSortChange }) => {
  
  const handleChange = (event) => {
    onSortChange(event.target.value);
  };

  return (
    <div className="sort-by-container">
      <label htmlFor="sort-select">Sort By: </label>
      <select id="sort-select" onChange={handleChange} defaultValue="winrate">
        <option value="winrate">Win Rate</option>
        <option value="pickrate">Pick Rate</option>
      </select>
    </div>
  );
};

const HeroStats = () => {
    const [heroes, setHeroes] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [ranks, setRanks] = useState([]); 
    const [filters, setFilters] = useState({ 
        minRank: 0, 
        maxRank: 11 
    });
    const [sortBy, setSortBy] = useState('winrate');
    const [totalMatches, setTotalMatches] = useState(0);

    useEffect(() => {
        fetch("http://localhost:5000/ranks")
            .then(res => res.json())
            .then(data => setRanks(data))
            .catch(err => setError("Failed to load ranks"));

        loadHeroStats();
    }, []);

    const loadHeroStats = async (currentFilters = filters) => {
        setLoading(true);
        try {
            const params = new URLSearchParams();

            if (currentFilters.minRank != null) params.append("min_rank", currentFilters.minRank);
            if (currentFilters.maxRank != null) params.append("max_rank", currentFilters.maxRank);

            const response = await fetch(`http://localhost:5000/view-heroes?${params}`);
            const data = await response.json();              
            
            setHeroes(data.heroes || []);
            setTotalMatches(data.total_matches || 0);

        } catch (error) {
            setError("Failed to load hero stats");
        } finally {
            setLoading(false);
        }
    };

    const sortedHeroes = useMemo(() => {
        return [...heroes].sort((a, b) => {
              if (sortBy === 'pickrate') {
                return b.pickrate - a.pickrate;
              }
              return b.winrate - a.winrate;
        });
    }, [heroes, sortBy]);

    const handleFilterChange = (key, value) => {
        setFilters(prev => ({ 
            ...prev,
             [key]: value 
            }));
    };

    const applyFilters = () => {
        loadHeroStats(filters);
    };

    const resetFilters = () => {
      const newFilters = {
        minRank: 0,
        maxRank: 11
      }
      setFilters(newFilters);
      loadHeroStats(newFilters);
    };

    const getRankName = (rankId) => {
        const rank = ranks.find(r => r.rank_id === rankId);
        return rank ? rank.rank_name : 'Unknown';
    }

  return (
    <div className="hero-stats">
      <h2>Hero Statistics</h2>
      
      {/* Filtering Controls */}
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

        <SortBy onSortChange={setSortBy} />
      </div>

      {/* Results */}
      <div className="results-info">
        <p>Showing stats from {totalMatches} matches</p>
        <p>Rank Range: {getRankName(filters.minRank)} - {getRankName(filters.maxRank)}</p>
      </div>

      {/* Hero Stats Table */}
      <div className="hero-table">
        <table>
          <thead>
            <tr>
              <th>Hero</th>
              <th>Pick Rate</th>
              <th>Win Rate</th>
            </tr>
          </thead>
          <tbody>
            {sortedHeroes.map(hero => (
              <tr key={hero.id}>
                <td className="hero-cell">
                  <img
                    src={`/hero_icons/${getHeroImage(hero.name)}_sm.png`}
                    alt={hero.name}
                    className="hero-icon"
                    onError={(e) => { e.target.style.display = 'none'; }}
                  />
                  <span>{hero.name}</span>
                </td>
                <td>{(hero.pickrate * 100).toFixed(2)}%</td>
                <td>{(hero.winrate * 100).toFixed(2)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HeroStats;