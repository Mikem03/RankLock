import React, { useState, useEffect, useMemo } from 'react';
import HeroTable from './HeroTable';
import FiltersPanel from './FiltersPanel';
import StatsState from './StatsState';



const MainContainer = () => {
    const [heroes, setHeroes] = useState([]);
    const [loading, setLoading] = useState(false); /// KEEP MAIN
    const [error, setError] = useState(null); /// KEEP MAIN
    const [ranks, setRanks] = useState([]); /// KEEP MAIN
    const [filters, setFilters] = useState({ 
        minRank: 0, 
        maxRank: 11 
    });
    const [totalMatches, setTotalMatches] = useState(0); /// KEEP MAIN
    const [stats, setStats] = useState('Hero'); /// KEEP MAIN




    useEffect(() => {
        fetch("/api/ranks")
            .then(res => res.json())
            .then(data => setRanks(data))
            .catch(err => setError("Failed to load ranks"));
    }, []);


    const loadHeroStats = async (currentFilters = filters) => {
        setLoading(true);
        try {
            const params = new URLSearchParams();

            if (currentFilters.minRank != null) params.append("min_rank", currentFilters.minRank * 10);
            if (currentFilters.maxRank != null) params.append("max_rank", currentFilters.maxRank * 10 + 9);

            const response = await fetch(`/api/view-heroes?${params}`);
            const data = await response.json();              
            
            setHeroes(data.heroes || []);
            setTotalMatches(data.total_matches || 0);

        } catch (error) {
            setError("Failed to load hero stats");
        } finally {
            setLoading(false);
        }
    };


    


    useEffect(() => {
        if (stats === 'Hero') {
            loadHeroStats();
        } else if (stats === 'Item') {
            console.log("items"); // loadItemStats();
        }
    }, [stats]);


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
    <div className="main-container">

      <StatsState currentStats={stats} onStatsChange={setStats} />   

      <FiltersPanel 
        filters={filters}
        getRankName={getRankName}
        handleFilterChange={handleFilterChange}
        applyFilters={applyFilters}
        resetFilters={resetFilters}
        loading={loading}
      />

      <div className="results-info">
        <p>Showing stats from {totalMatches} matches</p>
        <p>Rank Range: {getRankName(filters.minRank)} - {getRankName(filters.maxRank)}</p>
      </div>

      <HeroTable heroes={heroes} />

    </div>
  );
}; 

export default MainContainer;