import React from 'react';

export const getHeroImage = (dbName) => {
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

export const HeroNameCellRenderer = (params) => {
    const heroName = params.value;
    const heroImage = getHeroImage(heroName);
    return (
      <div className="hero-cell" style={{ display: 'flex', alignItems: 'center' }}>
        <img
          src={`/api/hero_icons/${heroImage}_sm.png`}
          alt={heroName}
          style={{ width: '24px', height: '24px', marginRight: '8px' }}
          onError={(e) => { e.target.style.display = 'none'; }}
        />
        <span>{heroName}</span>
      </div>
    );
};


